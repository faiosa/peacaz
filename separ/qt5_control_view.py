from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QFrame, QSplitter, QScrollArea, QScrollBar, \
    QStyle
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5 import Qt, QtCore

from utils.path import resource_path
from windows.settings import SettingsWindow
from separ.qt5_roller_view import RollerViewVertical, RollerViewHorizontal



class ControllerView:
    def __init__(self, controller, parent_frame):
        self.frame = QFrame(parent_frame)
        self.frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.frame.setLineWidth(4)
        self.frame.setMaximumWidth(480)

        self.controller = controller
        rollers_layout = QGridLayout()
        self.frame.setLayout(rollers_layout)
        controller_label = QLabel(self.frame)
        controller_label.setText(self.controller.name)
        header_font = QFont("Arial",14)
        header_font.setBold(True)
        controller_label.setFont(header_font)
        rollers_layout.addWidget(controller_label, 0, 0, 1, 2)


        self.restore_button = QPushButton(self.frame)
        self.restore_button.setIcon(self.restore_button.style().standardIcon(getattr(QStyle, "SP_BrowserReload")))
        self.restore_button.clicked.connect(self.controller.tune_angles)
        rollers_layout.addWidget(self.restore_button, 8, 5)

        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller.show(self.frame)

        self.stop_button = QPushButton(self.frame)
        self.stop_button.setIcon(QIcon("assets/stop.png"))
        self.stop_button.clicked.connect(self.controller.stop_ptz)
        rollers_layout.addWidget(self.stop_button, 8, 4)


        switchboard_frame = QFrame(self.frame)
        switchboard_layout = QHBoxLayout()
        switchboard_frame.setLayout(switchboard_layout)
        self.switchboard_view = SwitchBoardView(controller.switchboard, switchboard_frame, switchboard_layout)
        rollers_layout.addWidget(switchboard_frame, 8, 0, 1, 3)

class SwitchBoardView:
    def __init__(self, switchboard, frame, layout):
        self.switchboard = switchboard
        self.frame = frame

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
                button.setStyleSheet("background-color : #ADD8E6")  # Light blue for active buttons
            else:
                button.setStyleSheet("background-color : #DDDDDD")  # White for inactive buttons