import pyboard

from tkinter import Button, Frame

from utils.settings import load_settings


RF1 = [
    "import machine",
    "pin = machine.Pin(28, machine.Pin.OUT); pin.low()",  # Replace 2 with the appropriate pin number for your board
    "pin = machine.Pin(29, machine.Pin.OUT); pin.low()",  # Replace 2 with the appropriate pin number for your board
]

RF2 = [
    "import machine",
    "pin = machine.Pin(28, machine.Pin.OUT); pin.high()",  # Replace 2 with the appropriate pin number for your board
    "pin = machine.Pin(29, machine.Pin.OUT); pin.low()",  # Replace 2 with the appropriate pin number for your board
]

RF3 = [
    "import machine",
    "pin = machine.Pin(28, machine.Pin.OUT); pin.low()",  # Replace 2 with the appropriate pin number for your board
    "pin = machine.Pin(29, machine.Pin.OUT); pin.high()",  # Replace 2 with the appropriate pin number for your board
]

RF4 = [
    "import machine",
    "pin = machine.Pin(28, machine.Pin.OUT); pin.high()",  # Replace 2 with the appropriate pin number for your board
    "pin = machine.Pin(29, machine.Pin.OUT); pin.high()",  # Replace 2 with the appropriate pin number for your board
]


class Switchboard(Frame):
    def __init__(self, master):
        super().__init__(
            master,
            width=800,
            height=80,
            bg="#FFFFFF",
            relief="sunken",
        )
        self.master = master
        self.settings = load_settings()
        self.device = self.settings["switchboard_settings"]["serial_port"]
        self.create_widgets()

    # Function to connect to the device
    def connect_device(self, device):
        return pyboard.Pyboard(device)

    # Function to execute a command on the device
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

    def create_widgets(self):
        self.button1 = Button(
            self,
            text="1",
            bg="#FFFFFF",
            fg="#000000",
            border=0,
            command=lambda: self.send_pico_command(RF1),
        )
        self.button1.place(x=100, y=20, width=50, height=50)

        self.button2 = Button(
            self, text="2", border=0, command=lambda: self.send_pico_command(RF2)
        )
        self.button2.place(x=300, y=20, width=50, height=50)

        self.button3 = Button(
            self, text="3", border=0, command=lambda: self.send_pico_command(RF3)
        )
        self.button3.place(x=500, y=20, width=50, height=50)

        self.button4 = Button(
            self, text="4", border=0, command=lambda: self.send_pico_command(RF4)
        )
        self.button4.place(x=700, y=20, width=50, height=50)

    def send_pico_command(self, command):
        try:
            pyb = self.connect_device(self.device)

            for cmd in command:
                result = self.exec_command(pyb, cmd)
                print(f"Command '{cmd}' output:", result)

        except Exception as e:
            print(f"Failed to connect to the device: {e}")
        finally:
            if "pyb" in locals():
                pyb.close()
