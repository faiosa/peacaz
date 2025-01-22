from tkinter import Button, Frame
from utils.settings import load_settings
from utils import pyboard


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
        self.controller_values = controller_values
        self.current_controller = None
        self.buttons = []
        self.pins = [17, 27, 22]
        self.controller_states = {}  # Store button states for each controller
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
        self.update_button_states()

    def create_widgets(self):
        button_texts = ["1", "2", "3", "4"]
        button_x_positions = [100, 300, 500, 700]

        for i in range(4):  # Always create 4 buttons
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
        if self.current_controller is None:
            return

        controller_name = self.current_controller["name"]
        is_full_controller = self.current_controller.get("full_controller", False)

        if controller_name not in self.controller_states:
            self.controller_states[controller_name] = [False] * 4

        current_state = self.controller_states[controller_name]

        if is_full_controller:
            current_state[index] = not current_state[index]  # Toggle the state
        else:
            # For non-full controllers, only one button can be active
            current_state = [False] * 4
            current_state[index] = True

        self.controller_states[controller_name] = current_state
        self.update_button_visuals()

        if is_full_controller:
            self.send_gpio_command(index, current_state[index])
        else:
            self.send_pico_command(index)

    def send_gpio_command(self, index, state):
        pin = self._get_pins_list()[index]
        pyb = self._connect_device(
            self.current_controller.get("switchboard_serial_port")
        )
        command = [
            "import machine",
            f"pin = machine.Pin({pin}, machine.Pin.OUT); pin.{'high' if state else 'low'}()",
        ]
        for cmd in command:
            result = self.exec_command(pyb, cmd)
        print(f"Command result: {result}")
        if pyb:
            pyb.close()

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
        if pyb:
            pyb.close()

    def update_button_visuals(self):
        if self.current_controller is None:
            return

        controller_name = self.current_controller["name"]
        current_state = self.controller_states.get(controller_name, [False] * 4)

        for i, button in enumerate(self.buttons):
            if current_state[i]:
                button.config(bg="#ADD8E6")  # Light blue for active buttons
            else:
                button.config(bg="#FFFFFF")  # White for inactive buttons

            # Hide buttons 3 and 4 for full controllers
            if self.current_controller.get("full_controller", False) and i >= 3:
                button.place_forget()
            else:
                button.place(x=[100, 300, 500, 700][i], y=20, width=50, height=50)

    def update_button_states(self):
        self.update_button_visuals()

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
