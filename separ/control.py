from separ.roller import HorizontalRoller, VerticalRoller
import pyboard

class Manager:
    def __init__(self, json_settings):
        self.controller_values = json_settings.get("controller_values")
        self.controllers = [
            Controller(self.controller_values.get(key))
            for key in self.controller_values
        ]

class Controller:
    def __init__(self, json_settings):
        self.name = json_settings.get("name")
        self.settings = json_settings
        self.rollers = [
            VerticalRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=json_settings.get("serial_port")
            ) if json.get("type") == "vertical" else HorizontalRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=json_settings.get("serial_port")
            )
            for json in json_settings.get("rollers")
        ]
        switchboard_pins = [
            pin.strip()
            for pin in self.settings.get("switchboard_pins", "28, 29").split(
                ","
            )
        ]
        switchboard_serial_port = self.settings.get("switchboard_serial_port")
        self.switchboard = FullControlSwitchBoard(switchboard_pins, switchboard_serial_port) if self.settings.get("full_controller") else SimplySwitchBoard(switchboard_pins, switchboard_serial_port)

class SwitchBoard:
    def __init__(self, pins, switchboard_serial_port, is_full_control):
        self.pins = pins
        self.states = []
        self.switchboard_serial_port = switchboard_serial_port
        self.is_full_control = is_full_control

    def _connect_device(self):
        try:
            return pyboard.Pyboard(self.switchboard_serial_port)
        except Exception as e:
            print(f"Failed to connect to the device: {e}")

    def _exec_command(self, pyboard, command):
        try:
            pyboard.enter_raw_repl()
            pyboard.exec_(command)
            output = pyboard.exec_(command).decode("utf-8")
            pyboard.exit_raw_repl()
            return output
        except Exception as e:
            print(f"Error executing command '{command}': {e}")
            return None


class FullControlSwitchBoard(SwitchBoard):
    def __init__(self, pins, switchboard_serial_port):
        super().__init__(pins, switchboard_serial_port, True)
        self.states = [False] * len(pins)

    def send_command(self, index):
        self.states[index] = not self.states[index]
        self.__send_gpio_command(index, self.states[index])

    def __send_gpio_command(self, index, state):
        pin = self.pins[index]
        pyb = self._connect_device()
        command = [
            "import machine",
            f"pin = machine.Pin({pin}, machine.Pin.OUT); pin.{'high' if state else 'low'}()",
        ]
        for cmd in command:
            result = self._exec_command(pyb, cmd)
            print(f"Command result: {result}")
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
        commands = [
            [
                "import machine",
                f"pin = machine.Pin({first_pin}, machine.Pin.OUT); pin.low()",
                f"pin = machine.Pin({second_pin}, machine.Pin.OUT); pin.low()",
            ],
            [
                "import machine",
                f"pin = machine.Pin({first_pin}, machine.Pin.OUT); pin.high()",
                f"pin = machine.Pin({second_pin}, machine.Pin.OUT); pin.low()",
            ],
            [
                "import machine",
                f"pin = machine.Pin({first_pin}, machine.Pin.OUT); pin.low()",
                f"pin = machine.Pin({second_pin}, machine.Pin.OUT); pin.high()",
            ],
            [
                "import machine",
                f"pin = machine.Pin({first_pin}, machine.Pin.OUT); pin.high()",
                f"pin = machine.Pin({second_pin}, machine.Pin.OUT); pin.high()",
            ],
        ]
        pyb = self._connect_device()
        for cmd in commands[index]:
            result = self._exec_command(pyb, cmd)
            print(f"Command '{cmd}' output:", result)
        if pyb:
            pyb.close()