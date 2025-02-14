from separ.roller import HorizontalRoller, VerticalRoller, StepperRoller
from utils.comutator import BYTE_SIZE, toByteArray
from pearax.func import serial_connect
from pearax.core import Pearax
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
            self.radxa = Pearax(lambda: serial_connect(radxa_serial_port, 115200), 3, [42])
            rthread = threading.Thread(target=self.radxa.run, daemon=True, name="PearaxConnector")
            rthread.start()
        self.rollers = [ self.create_roller(json, json_settings.get("serial_port")) for json in json_settings.get("rollers") ]
        switchboard_pins = [
            pin.strip()
            for pin in self.settings.get("switchboard_pins", "28, 29").split(
                ","
            )
        ]
        switchboard_serial_port = self.settings.get("switchboard_serial_port")
        self.switchboard = FullControlSwitchBoard(switchboard_pins, switchboard_serial_port) if self.settings.get("full_controller") else SimplySwitchBoard(switchboard_pins, switchboard_serial_port)

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

class SwitchBoard:
    def __init__(self, pins, switchboard_serial_port, is_full_control):
        self.pins = [int(sp) for sp in pins]
        self.states = []
        self.switchboard_serial_port = switchboard_serial_port
        self.is_full_control = is_full_control
        self.app_index = 42

    def _compose_command(self, *args):
        return toByteArray(self.app_index, len(args) * BYTE_SIZE, *args)

    def _connect_device(self):
        try:
            return serial.Serial(port=self.switchboard_serial_port, baudrate=115200)
        except Exception as e:
            print(f"Failed to connect to the device: {e}")

    def _exec_command(self, pyboard, command):
        try:
            pyboard.write(command)
        except Exception as e:
            print(f"Error executing command '{command}': {e}")


class FullControlSwitchBoard(SwitchBoard):
    def __init__(self, pins, switchboard_serial_port):
        super().__init__(pins, switchboard_serial_port, True)
        self.states = [False] * len(pins)

    def send_command(self, index):
        self.states[index] = not self.states[index]
        self.__send_gpio_command(index, self.states[index])

    def __send_gpio_command(self, index, state):
        command = self._compose_command(self.pins[index], 1 if state else 0)
        pyb = self._connect_device()
        self._exec_command(pyb, command)
        if pyb:
            pyb.close()

class SimplySwitchBoard(SwitchBoard):
    def __init__(self, pins, switchboard_serial_port):
        super().__init__(pins, switchboard_serial_port, False)
        self.states = [False] * 4

    def send_command(self, index):
        for i in range(0, len(self.states)):
            self.states[i] = True if i == index else False
        self.__send_pico_command(index)

    def __send_pico_command(self, index):
        first_pin, second_pin = self.pins
        command = self._compose_command(first_pin, index % 2, second_pin, index // 2)
        pyb = self._connect_device()
        self._exec_command(pyb, command)
        if pyb:
            pyb.close()