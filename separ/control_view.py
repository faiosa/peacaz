#from tkinter import Frame, Button, PhotoImage
from PyQt5.QtWidgets import QVBoxLayout

from separ.roller_view import RollerViewHorizontal, RollerViewVertical
from config import ui
#from tkinter import ttk, LEFT, RIGHT
from utils.path import resource_path
from windows.settings import SettingsWindow

class ManagerView:
    def __init__(self, manager, frame):
        self.manager = manager
        self.frame = frame

        layout = QVBoxLayout()
        self.controllers_views = []
        for controller in self.manager.controllers:
            tab = Frame(self.tab_control)
            self.tab_control.add(tab, text=controller.name)
            controller_view = ControllerView(controller, tab)
            self.controllers_views.append(controller_view)
        self.tab_control.pack(expand=1, fill="both", side=LEFT)
        #self.tab_control.grid(column=0, row=0, padx=5, pady=5)

        self.settings_image = PhotoImage(file=resource_path("assets/settings.png"))
        self.settings_button = Button(
            self.frame,
            image=self.settings_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_settings_window,
            relief="flat",
        )
        #self.settings_button.grid(column=1, row=0, padx=5, pady=5)
        self.settings_button.pack(expand=0, anchor="ne", side=RIGHT)

    def open_settings_window(self):
        # Open the settings window
        SettingsWindow(self.frame, self.manager.controller_values, self.manager)

class ControllerView:
    def __init__(self, controller, frame):
        self.controller = controller
        self.frame = frame
        self.roller_views = []
        self.lambda_queue = []
        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller_frame = Frame(frame, bg=ui.BG_COLOR, highlightbackground="black", highlightthickness=2)
            roller_frame.grid(column=indx, row=1, padx=5, pady=5)
            roller_view = RollerViewVertical(roller, roller_frame, self, indx) if roller.is_vertical else RollerViewHorizontal(roller, roller_frame, self, indx)
            self.roller_views.append(roller_view)

        self.restore_defaults_button = Button(
            self.frame,
            borderwidth=1,
            highlightthickness=0,
            command=self.__tune_angles,
            text="Відновити початкові значення",
            bg=ui.BG_COLOR,
        )
        self.restore_defaults_button.grid(column=0, row=2, padx=40, pady=10)

        switchboard_frame = Frame(frame, bg=ui.BG_COLOR, highlightbackground="black", highlightthickness=2)
        switchboard_frame.grid(column=1, row=2, columnspan=2, padx=10, pady=10, sticky="nw")

        self.switchboard_view = SwitchBoardView(controller.switchboard, switchboard_frame)

    def roller_start(self, roller_index):
        for i in range(0, len(self.roller_views)):
            if i != roller_index:
                self.roller_views[i].disable_all_buttons()

    def roller_finish(self, roller_index):
        for i in range(0, len(self.roller_views)):
            if i != roller_index:
                self.roller_views[i].enable_all_buttons()
        self.__check_lambdas()

    def __check_lambdas(self):
        if len(self.lambda_queue) > 0:
            my_lambda = self.lambda_queue.pop(0)
            my_lambda()

    def __tune_angles(self):
        angles = [json.get("current_angle") for json in self.controller.settings.get("rollers")]
        for i in range(0, min(len(self.roller_views), len(angles))):
            if self.roller_views[i].moving_id:
                self.roller_views[i].stop_ptz()
            my_lambda = lambda: self.roller_views[len(self.roller_views) - len(angles)].roll_desired_angle(angles.pop(0))
            self.lambda_queue.append(my_lambda)
        self.__check_lambdas()

class SwitchBoardView:
    def __init__(self, switchboard, frame):
        self.switchboard = switchboard
        self.frame = frame
        self.buttons = []
        switch_buttons_len = len(switchboard.pins) if self.switchboard.is_full_control else 4
        for i in range(switch_buttons_len):  # Always create 4 buttons
            button = Button(
                self.frame,
                text=f"{i + 1}",
                bg="#FFFFFF",
                fg="#000000",
                border=1,
                width=5,
                height=3,
                command=lambda idx=i: self.send_command(idx),
            )
            button.grid(column=i, row=0, padx=15, pady=15)
            self.buttons.append(button)

    def send_command(self, idx):
        self.switchboard.send_command(idx)
        self.update_button_visuals()

    def update_button_visuals(self):
        for i, button in enumerate(self.buttons):
            if self.switchboard.states[i]:
                button.config(bg="#ADD8E6")  # Light blue for active buttons
            else:
                button.config(bg="#FFFFFF")  # White for inactive buttons