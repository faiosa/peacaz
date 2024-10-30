from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QFrame
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5 import Qt, QtCore

from utils.path import resource_path
from windows.settings import SettingsWindow
from separ.qt5_roller_view import RollerViewVertical, RollerViewHorizontal

class ManagerView:
    def __init__(self, manager, frame):
        self.manager = manager
        self.frame = frame

        layout = QHBoxLayout()

        controllers_frame = QWidget()
        layout.addWidget(controllers_frame)
        controllers_layout = QVBoxLayout()
        self.controllers_views = []
        for controller in self.manager.controllers:
            tab = QFrame(frame)
            tab.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
            tab.setLineWidth(4)
            controllers_layout.addWidget(tab)
            controller_view = ControllerView(controller, tab)
            self.controllers_views.append(controller_view)
        controllers_frame.setLayout(controllers_layout)

        settings_button = QPushButton(self.frame)
        settings_button.setIcon(QIcon("assets/settings.png"))
        settings_button.clicked.connect(lambda: self.open_settings_window())
        settings_button.setFixedWidth(25)
        layout.addWidget(settings_button, stretch=0, alignment=QtCore.Qt.AlignTop)

        self.frame.setLayout(layout)

    def open_settings_window(self):
        print("Opening the settings \n")
        # Open the settings window
        #SettingsWindow(self.frame, self.manager.controller_values, self.manager)


class ControllerView:
    def __init__(self, controller, frame):
        self.controller = controller
        self.frame = frame
        self.roller_views = []
        self.lambda_queue = []
        rollers_layout = QGridLayout()
        frame.setLayout(rollers_layout)
        controller_label = QLabel(self.frame)
        controller_label.setText(self.controller.name)
        header_font = QFont("Arial",14)
        header_font.setBold(True)
        controller_label.setFont(header_font)
        rollers_layout.addWidget(controller_label, 0, 0, 1, 2)

        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller_view = RollerViewVertical(roller, frame, rollers_layout, self, indx) if roller.is_vertical else RollerViewHorizontal(roller, frame, rollers_layout, self, indx)
            self.roller_views.append(roller_view)

        self.stop_button = QPushButton(self.frame)
        self.stop_button.setIcon(QIcon("assets/stop.png"))
        self.stop_button.clicked.connect(lambda: self.stop_ptz())
        rollers_layout.addWidget(self.stop_button, 4, 6)

        self.restore_button = QPushButton(self.frame)
        self.restore_button.setText("Відновити початкові значення")
        self.restore_button.clicked.connect(self.__tune_angles)
        rollers_layout.addWidget(self.restore_button, 8, 4, 1, 4)

        switchboard_frame = QFrame(self.frame)
        switchboard_layout = QHBoxLayout()
        switchboard_frame.setLayout(switchboard_layout)
        self.switchboard_view = SwitchBoardView(controller.switchboard, switchboard_frame, switchboard_layout)
        rollers_layout.addWidget(switchboard_frame, 8, 0, 1, 3)

    def stop_ptz(self):
        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            if roller.is_moving_increase or roller.is_moving_decrease:
                self.roller_views[indx].stop_ptz()

    def roller_start(self, roller_index):
        self.restore_button.setEnabled(False)
        for i in range(0, len(self.roller_views)):
            if i != roller_index:
                self.roller_views[i].disable_buttons()

    def roller_finish(self, roller_index):
        for i in range(0, len(self.roller_views)):
            if i != roller_index:
                self.roller_views[i].enable_buttons()
        self.restore_button.setEnabled(True)
        self.__check_lambdas()

    def __check_lambdas(self):
        if len(self.lambda_queue) > 0:
            my_lambda = self.lambda_queue.pop(0)
            my_lambda()

    def __tune_angles(self):
        angles = [json.get("current_angle") for json in self.controller.settings.get("rollers")]
        for i in range(0, min(len(self.roller_views), len(angles))):
            if self.roller_views[i].is_roller_moving():
                self.roller_views[i].stop_ptz()
            my_lambda = lambda: self.roller_views[len(self.roller_views) - len(angles)].roll_desired_angle(angles.pop(0))
            self.lambda_queue.append(my_lambda)
        self.__check_lambdas()

class SwitchBoardView:
    def __init__(self, switchboard, frame, layout):
        self.switchboard = switchboard
        self.frame = frame

        self.active_palette = QPalette()
        self.active_palette.setColor(QPalette.Active, QPalette.Button, QColor("#ADD8E6"))#QColor("#ADD8E6")
        self.active_palette.setColor(QPalette.Inactive, QPalette.Button, QColor("#ADD8E6"))
        self.inactive_palette = QPalette()
        self.inactive_palette.setColor(QPalette.Active, QPalette.Button, QColor("#FFFFFF"))#QColor("#FFFFFF"))
        self.inactive_palette.setColor(QPalette.Inactive, QPalette.Button, QColor("#FFFFFF"))  # QColor("#FFFFFF"))

        self.buttons = []
        switch_buttons_len = len(switchboard.pins) if self.switchboard.is_full_control else 4
        for ind in range(switch_buttons_len):
            button = QPushButton(self.frame)
            button.setText(f"{ind + 1}")
            button.clicked.connect((lambda index=ind: lambda: self.send_command(index))())
            layout.addWidget(button)
            self.buttons.append(button)
        self.update_button_visuals()

    def send_command(self, idx):
        self.switchboard.send_command(idx)
        self.update_button_visuals()

    def update_button_visuals(self):
        for i, button in enumerate(self.buttons):
            if self.switchboard.states[i]:
                button.setPalette(self.active_palette)  # Light blue for active buttons
            else:
                button.setPalette(self.inactive_palette)  # White for inactive buttons