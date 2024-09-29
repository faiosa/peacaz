from tkinter import Button, Frame
from utils.settings import load_settings
import pyboard


class Switchboard(Frame):
    def __init__(self, master, controller_values):
        super().__init__(
            master,
            width=800,
            height=80,
            bg="#FFFFFF",
            relief="sunken",
        )
        self.master = master
        self.settings = load_settings()
        # self.device = self.settings["switchboard_settings"]["serial_port"]
        self.controller_values = controller_values
        # self.device = self.controller_values["switchboard_serial_port"]
        self.current_controller = None
        self.buttons = []
        self.pins = [17, 27, 22]
        self.last_pressed_button = None
        self.create_widgets()

    def _get_pins_list(self):
        return [
            pin.strip()
            for pin in self.current_controller.get("switchboard_pins", "28, 29").split(
                ","
            )
        ]

    def update_controller(self, controller_name):
        self.current_controller = next(
            (
                c
                for c in self.controller_values.values()
                if c["name"] == controller_name
            ),
            None,
        )
        if self.current_controller.get("full_controller", False):
            self.create_widgets(3)
        self.update_button_states()

    def create_widgets(self, number_of_buttons=4):
        if self.current_controller and self.current_controller.get(
            "full_controller", False
        ):
            number_of_buttons = 3
        button_texts = ["1", "2", "3", "4"]
        button_x_positions = [100, 300, 500, 700]

        for i in range(number_of_buttons):
            button = Button(
                self,
                text=button_texts[i],
                bg="#FFFFFF",
                fg="#000000",
                border=1,
                command=lambda idx=i: self.send_command(idx),
            )
            button.place(x=button_x_positions[i], y=20, width=50, height=50)
            self.buttons.append(button)

    def _connect_device(self, device):
        try:
            return pyboard.Pyboard(device)
        except Exception as e:
            print(f"Failed to connect to the device: {e}")

    def send_command(self, index):
        if self.current_controller and self.current_controller.get(
            "full_controller", False
        ):
            self.send_gpio_command(index)
        else:
            self.send_pico_command(index)

    def send_gpio_command(self, index):
        button = self.buttons[index]
        pin = self._get_pins_list()[index]
        pyb = self._connect_device(
            self.current_controller.get("switchboard_serial_port")
        )
        if button.cget("bg") == "#ADD8E6":  # If button is already pressed
            button.config(bg="#FFFFFF")  # Unpress the button
            command = (
                [
                    "import machine",
                    f"pin = machine.Pin({pin}, machine.Pin.OUT); pin.low()",
                ],
            )
            for cmd in command:
                result = self.exec_command(pyb, cmd)
        else:
            button.config(bg="#ADD8E6")  # Press the button
            command = (
                [
                    "import machine",
                    f"pin = machine.Pin({pin}, machine.Pin.OUT); pin.high()",
                ],
            )
            for cmd in command:
                result = self.exec_command(pyb, cmd)

        print(f"Command result: {result}")

    def send_pico_command(self, index):
        pins = self._get_pins_list()
        first_pin, second_pin = pins
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
        pyb = self._connect_device(
            self.current_controller.get("switchboard_serial_port")
        )
        for cmd in commands[index]:
            result = self.exec_command(pyb, cmd)
            print(f"Command '{cmd}' output:", result)
        self.update_button_highlight(self.buttons[index])
        # finally:
        #     if "pyb" in locals():
        #         pyb.close()

    def update_button_highlight(self, button):
        if self.last_pressed_button:
            self.last_pressed_button.config(bg="#FFFFFF")
        button.config(bg="#ADD8E6")  # Light blue color
        self.last_pressed_button = button

    def update_button_states(self):
        for button in self.buttons:
            button.config(state="normal")
            button.config(bg="#FFFFFF")  # Reset color
        if self.last_pressed_button:
            self.last_pressed_button.config(bg="#FFFFFF")
        self.last_pressed_button = None

    def exec_command(self, pyboard, command):
        try:
            pyboard.enter_raw_repl()
            pyboard.exec_(command)
            output = pyboard.exec_(command).decode("utf-8")
            pyboard.exit_raw_repl()
            return output
        except Exception as e:
            print(f"Error executing command '{command}': {e}")
            return None
