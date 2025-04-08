from pearax.channel import socket_client_channel
from pearax.client import PearaxClient

from separ.pearax_util import SerialMonitor
from separ.qt5_control_view import ControllerView
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
            radxa_serial_port = self.settings.get("radxa_serial_port")
            #connection_provider = lambda: SerialConnection(func.serial_connect(radxa_serial_port, PEARAX_BAUD_RATE))
            connection_provider = lambda: socket_client_channel('192.168.0.104', 3799)
            #connection_provider = lambda: repeat_call(lambda: socket_client_channel('192.168.0.104', 3799), 8, 0.05)
            self.radxa = Pearax(connection_provider, [STEPPER_MOTOR_INDEX, PINNER_CLIENT_INDEX, HEART_BEAT_INDEX])
            self.radxa.start(f"Controller_{self.name}_radxa_{time.time()}")
            self.serial_monitor = SerialMonitor(self.radxa, [self])
        self.rollers = [ self.create_roller(json) for json in json_settings.get("rollers") ]

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

    def show(self, parent_frame):
        if self.view is None:
            self.view = ControllerView(self, parent_frame)
        else:
            raise Exception("Controller show should appear only once")

    def create_roller(self, json):
        is_vertical = json.get("type") == "vertical"
        if json.get("engine") == "stepper":
            return StepperRoller(
                self,
                rotation_speed=json.get("rotation_speed"),
                steps=json.get("steps"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                is_vertical = is_vertical
            )
        elif is_vertical:
            return VerticalRoller(
                self,
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=json.get("serial_port")
            )
        else:
            return HorizontalRoller(
                self,
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=json.get("serial_port")
            )

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

class SwitchBoard:
    def __init__(self, pearax: Pearax, switchboard_serial_port: str, pins, is_full_control):
        self.pins = [int(sp) for sp in pins]
        self.states = []
        self.app_index = 16
        self.switchboard_pearax = None

        if switchboard_serial_port is None:
            if pearax is None:
                func.func_logger.fatal("Controller missing pearax for swithcboard configured with 'radxa'")
            else:
                self.serial_client = PearaxClient(pearax.mail_agent(self.app_index))
        else:
            self.switchboard_pearax = Pearax(lambda: func.serial_connect(switchboard_serial_port, PEARAX_BAUD_RATE), [self.app_index])
            self.switchboard_pearax.start("SwitchBoardPearax")
            self.serial_client = PearaxClient(self.switchboard_pearax.mail_agent(self.app_index))
        self.is_full_control = is_full_control
        self.ints_to_bytes = func.ints_to_bytes_lambda(PINNER_INT_BYTE_SIZE, PINNER_INT_BYTE_ORDER)
        self._initial_command()


    def _compose_command(self, *args):
        return self.ints_to_bytes(*args)

    def _exec_command(self, command):
        self.serial_client.write(command)

    def _initial_command(self):
        args = [0] * len(self.pins) * 2
        args[0::2] = self.pins
        command = self._compose_command(*args)
        self._exec_command(command)


class FullControlSwitchBoard(SwitchBoard):
    def __init__(self, pearax, switchboard_serial_port, pins):
        super().__init__(pearax, switchboard_serial_port, pins,True)
        self.states = [False] * len(pins)

    def send_command(self, index):
        self.states[index] = not self.states[index]
        self.__send_gpio_command(index, self.states[index])

    def __send_gpio_command(self, index, state):
        command = self._compose_command(self.pins[index], 1 if state else 0)
        self._exec_command(command)

class SimplySwitchBoard(SwitchBoard):
    def __init__(self, pearax, switchboard_serial_port, pins):
        super().__init__(pearax, switchboard_serial_port, pins,False)
        self.states = [False] * 4

    def send_command(self, index):
        for i in range(0, len(self.states)):
            self.states[i] = True if i == index else False
        self.__send_pico_command(index)

    def __send_pico_command(self, index):
        first_pin, second_pin = self.pins
        command = self._compose_command(first_pin, index % 2, second_pin, index // 2)
        self._exec_command(command)