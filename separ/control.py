from pearax.client import PearaxClient
from separ.roller import HorizontalRoller, VerticalRoller, StepperRoller
from pearax import func
from pearax.core import ManagePeer
import threading


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

class Controller:
    def __init__(self, json_settings):
        self.name = json_settings.get("name")
        self.settings = json_settings
        self.radxa = None
        if self.settings.get("use_radxa"):
            radxa_serial_port = self.settings.get("radxa_serial_port")
            self.radxa = ManagePeer(lambda: func.serial_connect(radxa_serial_port, 115200), 3, [42, 16])
            self.radxa.start()
        self.rollers = [ self.create_roller(json, json_settings.get("serial_port")) for json in json_settings.get("rollers") ]

        switchboard_settings = self.settings.get("switchboard")
        switchboard_serial_port = switchboard_settings.get("serial_port")
        switchboard_pins = [
            pin.strip()
            for pin in switchboard_settings.get("pins", "28, 29").split(
                ","
            )
        ]
        self.switchboard = FullControlSwitchBoard(self.radxa, switchboard_serial_port, switchboard_pins) if switchboard_settings.get("full_control") else SimplySwitchBoard(self.radxa, switchboard_serial_port, switchboard_pins)

    def create_roller(self, json, serial_port):
        is_vertical = json.get("type") == "vertical"
        if json.get("engine") == "stepper":
            return StepperRoller(
                self.radxa,
                steps=json.get("steps"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                is_vertical = is_vertical
            )
        elif is_vertical:
            return VerticalRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=serial_port
            )
        else:
            return HorizontalRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=serial_port
            )

    def is_moving(self):
        for roller in self.rollers:
            if roller.is_moving():
                return True
        return False

BYTE_SIZE = 3
BYTE_ORDER = 'big'

class SwitchBoard:
    def __init__(self, pearax: Pearax, switchboard_serial_port: str, pins, is_full_control):
        self.pins = [int(sp) for sp in pins]
        self.states = []
        self.app_index = 16
        self.switchboard_pearax = None
        if switchboard_serial_port == "radxa":
            if pearax is None:
                func_logger.fatal("Controller missing pearax fro swithcboard configured with 'radxa'")
        else:
            self.switchboard_pearax = ManagePeer(lambda: self.__connect_device(switchboard_serial_port), 3, [self.app_index])
            self.switchboard_pearax.start()
        self.serial_client = PearaxClient(self.app_index, pearax)
        self.is_full_control = is_full_control
        self.ints_to_bytes = func.ints_to_bytes_lambda(BYTE_SIZE, BYTE_ORDER)


    def _compose_command(self, *args):
        return self.ints_to_bytes(*args)

    def __connect_device(self, serial_port):
        return func.serial_connect(serial_port, 115200)

    def _exec_command(self, command):
        self.serial_client.write(command)


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