from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QFrame
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5 import Qt, QtCore

from utils.path import resource_path
from windows.settings import SettingsWindow
from separ.qt5_roller_view import RollerViewVertical, RollerViewHorizontal

class ManagerView:
    def __init__(self, manager, frame):
        print("init manager")
        self.manager = manager
        self.frame = frame

        layout = QHBoxLayout()

        controllers_frame = QWidget()
        layout.addWidget(controllers_frame)
        controllers_layout = QVBoxLayout()
        self.controllers_views = []
        for controller in self.manager.controllers:
            #tab = QWidget()
            tab = QFrame(frame)
            tab.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
            tab.setLineWidth(4)
            controllers_layout.addWidget(tab)
            controller_view = ControllerView(controller, tab)
            self.controllers_views.append(controller_view)
        #self.tab_control.pack(expand=1, fill="both", side=LEFT)
        controllers_frame.setLayout(controllers_layout)

        settings_button = QPushButton(self.frame)
        settings_button.setIcon(QIcon("assets/settings.png"))
        settings_button.clicked.connect(lambda: self.open_settings_window())
        settings_button.setFixedWidth(25)
        layout.addWidget(settings_button, stretch=0, alignment=QtCore.Qt.AlignTop)

        self.frame.setLayout(layout)

    #@pyqtSlot()
    def open_settings_window(self):
        print("Openning the settings \n")
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
        controller_label.setFont(QFont("Arial",14))
        rollers_layout.addWidget(controller_label, 0, 0, 1, 6)

        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller_view = RollerViewVertical(roller, frame, rollers_layout, self, indx) if roller.is_vertical else RollerViewHorizontal(roller, frame, rollers_layout, self, indx)
            self.roller_views.append(roller_view)
        '''
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
        '''
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