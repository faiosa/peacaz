from typing import List

from PyQt5.QtCore import QTimer
from pearax.channel import udp_client_socket, tcp_client_socket, SerialConnection
from pearax.func import IntByteConverter
from pearax.mail import MailClient

from separ.pearax_util import SerialMonitor
from separ.qt5_control_view import ControllerView, SwitchBoardView
from separ.roller import HorizontalRoller, VerticalRoller, StepperRoller
from pearax import func, STEPPER_MOTOR_INDEX, PINNER_CLIENT_INDEX, PEARAX_BAUD_RATE, PINNER_INT_BYTE_SIZE, \
    PINNER_INT_BYTE_ORDER, HEART_BEAT_INDEX
from pearax.core import Pearax
import time

class Manager:
    def __init__(self, json_settings):
        self.controller_values = json_settings.get("controller_values")
        self.controllers = [
            Controller(self.controller_values.get(key))
            for key in self.controller_values
        ]

    def is_moving(self):
        for controller in self.controllers:
            if controller.is_moving():
                return True
        return False

    def close(self):
        for controller in self.controllers:
            controller.close()

class Controller:
    def __init__(self, json_settings):
        self.name = json_settings.get("name")
        self.view = None
        self.lambda_queue = []
        self.settings = json_settings
        self.radxa: Pearax = None
        self.serial_monitor = None
        if self.settings.get("use_radxa"):
            protocol = self.settings.get("pearax_protocol")
            if protocol == "uart":
                radxa_serial_port = self.settings.get("radxa_serial_port")
                connection_provider = lambda: SerialConnection(func.serial_connect(radxa_serial_port, PEARAX_BAUD_RATE))
            elif protocol == "tcp":
                host = str(self.settings.get("radxa_ip_host"))
                port = int(self.settings.get("radxa_ip_port"))
                connection_provider = lambda: tcp_client_socket(host, port)
            elif protocol == "udp":
                host = str(self.settings.get("radxa_ip_host"))
                port = int(self.settings.get("radxa_ip_port"))
                connection_provider = lambda: udp_client_socket(host, port)
            else:
                raise Exception(f"Unknown protocol '{protocol}'")
            self.radxa = Pearax(connection_provider)
            self.serial_monitor = SerialMonitor(self.radxa.provide_agent(HEART_BEAT_INDEX), [self])

        self.rollers = [ self.__create_roller(roller_index, json) for roller_index, json in enumerate(json_settings.get("rollers")) ]

        switchboard_settings = self.settings.get("switchboard")
        switchboard_serial_port = switchboard_settings.get("serial_port")

        if switchboard_serial_port is None:
            assert self.radxa is not None
            assert switchboard_settings.get("use_radxa") is True

        switchboard_pins = [
            pin.strip()
            for pin in switchboard_settings.get("pins", "28, 29").split(
                ","
            )
        ]
        self.switchboard = FullControlSwitchBoard(self.radxa, switchboard_serial_port, switchboard_pins) if switchboard_settings.get("full_control") else SimplySwitchBoard(self.radxa, switchboard_serial_port, switchboard_pins)
        if not self.radxa is None:
            self.radxa.start(f"Controller_{self.name}_radxa_{time.time()}")

    def on_view_ready(self):
        #for roller in self.rollers:
        if not self.radxa is None:
            self.on_serial_disconnect()
            self.serial_monitor.start_monitor()

    def on_serial_disconnect(self):
        self.view.restore_button.setEnabled(False)
        self.view.stop_button.setEnabled(False)
        for roller in self.rollers:
            roller.state_update(False, False)

    def on_serial_connect(self):
        self.view.restore_button.setEnabled(True)
        self.view.stop_button.setEnabled(True)
        for roller in self.rollers:
            roller.state_update(True, True)
            roller.on_motor_connect()

    def show(self, parent_frame):
        if self.view is None:
            self.view = ControllerView(self, parent_frame)
        else:
            raise Exception("Controller show should appear only once")

    def __create_roller(self, roller_index, json):
        is_vertical = json.get("type") == "vertical"
        if json.get("engine") == "stepper":
            return StepperRoller(self, roller_index)
        elif is_vertical:
            return VerticalRoller(self, roller_index)
        else:
            return HorizontalRoller(self, roller_index)

    def is_moving(self):
        for roller in self.rollers:
            if roller.is_moving():
                return True
        return False

    def roller_start(self, roller):
        self.view.restore_button.setEnabled(False)
        for rl in self.rollers:
            if not rl == roller:
                rl.view.disable_buttons()

    def roller_finish(self, roller):
        for rl in self.rollers:
            if not rl == roller:
                rl.view.enable_buttons()
        self.view.restore_button.setEnabled(True)
        self.__check_lambdas()

    def stop_ptz(self):
        for roller in self.rollers:
            if roller.is_moving():
                roller.stop_ptz()

    def __check_lambdas(self):
        if len(self.lambda_queue) > 0:
            my_lambda = self.lambda_queue.pop(0)
            my_lambda()

    def tune_angles(self):
        angles = [json.get("current_angle") for json in self.settings.get("rollers")]
        for i in range(0, len(angles)):
            if angles[i] is None:#Stepper motor has no current_angle attribute
                continue
            if self.rollers[i].is_moving():
                self.rollers[i].stop_ptz()
            my_lambda = (lambda index, angle: lambda: self.rollers[index].turn_ptz_move(angle))(i, angles[i])
            self.lambda_queue.append(my_lambda)
        self.__check_lambdas()

    def close(self):
        if self.radxa:
            self.serial_monitor.stop_monitor()
            self.radxa.stop()
        if self.switchboard:
            if self.switchboard.switchboard_pearax:
                self.switchboard.switchboard_pearax.stop()

class SwitchBoard(IntByteConverter):
    def __init__(self, pearax: Pearax, switchboard_serial_port: str, pins, is_full_control):
        super().__init__(PINNER_INT_BYTE_SIZE, PINNER_INT_BYTE_ORDER)
        self.pins = [int(sp) for sp in pins]
        self.states = []
        self.app_index = PINNER_CLIENT_INDEX
        self.switchboard_pearax = None
        self.view = None

        if switchboard_serial_port is None:
            if pearax is None:
                func.func_logger.fatal("Controller missing pearax for swithcboard configured with 'radxa'")
            else:
                self.serial_client = MailClient(pearax.provide_agent(self.app_index))
        else:
            self.switchboard_pearax = Pearax(lambda: func.serial_connect(switchboard_serial_port, PEARAX_BAUD_RATE))
            self.serial_client = MailClient(self.switchboard_pearax.provide_agent(self.app_index))
            self.switchboard_pearax.start("SwitchBoardPearax")
        self.is_full_control = is_full_control

    def _switch_for_index(self, index) -> List[int]:
        pass

    def _update_states(self, nstates: List[int]):
        pass

    def _ensure_exec_command(self, cmd, retry = 8):
        resp = self.serial_client.receive()
        if resp:
            self._update_states(self.ints_from_bytes(resp))
            retry = 0
        if retry > 0:
            self.serial_client.send(cmd)
            QTimer.singleShot(
                32,
                lambda: self._ensure_exec_command(cmd, retry - 1)
            )
        else:
            self.view.update_button_visuals()

    def pin(self, index):
        command = self._switch_for_index(index)
        bts = self.ints_to_bytes(*command)
        self._ensure_exec_command(bts)

    def show(self, switch_board_frame):
        self.view = SwitchBoardView(self, switch_board_frame)
        self.__initial_command()

    def __initial_command(self):
        args = [2] * len(self.pins) * 2
        args[0::2] = self.pins
        command = self.ints_to_bytes(*args)
        self._ensure_exec_command(command)


class FullControlSwitchBoard(SwitchBoard):
    def __init__(self, pearax, switchboard_serial_port, pins):
        super().__init__(pearax, switchboard_serial_port, pins,True)
        self.states = [False] * len(pins)

    def _switch_for_index(self, index) -> List[int]:
        return [self.pins[index], 0 if self.states[index] else 1]


    def _update_states(self, nstates: List[int]):
        for i in range(len(nstates)//2):
            pin = nstates[i * 2]
            status = nstates[i * 2 + 1]
            if status > 1:
                func.func_logger.warning(f"Error response status for pin {pin}")
                continue
            for idx in range(len(self.pins)):
                if self.pins[idx] == pin:
                    self.states[idx] = status == 1

class SimplySwitchBoard(SwitchBoard):
    def __init__(self, pearax, switchboard_serial_port, pins):
        super().__init__(pearax, switchboard_serial_port, pins,False)
        assert len(pins) == 2
        self.states = [False] * 4

    def _switch_for_index(self, index) -> List[int]:
        return [self.pins[0], index // 2, self.pins[1], index % 2]

    def _update_states(self, nstates: List[int]):
        active = 0
        for i in range(len(self.pins)):
            pin = nstates[i * 2]
            state = nstates[i * 2 + 1]
            if state > 1:
                func.func_logger.warning(f"Error response status for pin {pin}")
                return
            if pin == self.pins[0]:
                active += state * 2
            elif pin == self.pins[1]:
                active += state
        for i in range(len(self.states)):
            self.states[i] = True if i == active else False