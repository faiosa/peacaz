from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QFrame, QSplitter, QScrollArea

from separ.qt5_control_view import ControllerView


class BluePrint:
    def __init__(self, window):
        self.window = window

        self.main_layout = QHBoxLayout(window)
        window.setLayout(self.main_layout)

        self.left_column = QWidget(window)
        self.left_layout = QVBoxLayout(self.left_column)
        self.left_column.setLayout(self.left_layout)

        self.main_layout.addWidget(self.left_column)

        right_column = QWidget(window)
        self.main_layout.addWidget(right_column)

        self.__set_rollers_slots()


    def set_urh(self, urh_controller):
        self.left_layout.addWidget(urh_controller)


    def __set_rollers_slots(self):

        self.rollers_frame = QWidget(self.left_column)
        self.left_layout.addWidget(self.rollers_frame)

        layout = QHBoxLayout(self.rollers_frame)
        self.roller_splitter = QSplitter(self.rollers_frame)

        self.roller_splitter.setStyleSheet(
            "QSplitter::handle:horizontal {\n"
            "margin: 4px 0px;\n"
            "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
            "stop:0 rgba(255, 255, 255, 0), \n"
            "stop:0.5 rgba(100, 100, 100, 100), \n"
            "stop:1 rgba(255, 255, 255, 0));\n"
            "image: url(:/icons/icons/splitter_handle_vertical.svg);\n"
            "}"
        )

        self.roller_splitter.setHandleWidth(6)
        self.roller_splitter.setObjectName("splitter")
        self.roller_splitter.setSizes([250, 250, 250])
        layout.addWidget(self.roller_splitter)

        self.rollers_frame.setLayout(layout)

    def add_roller(self, controller, index):
        tab = QFrame(self.rollers_frame)
        tab.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        tab.setLineWidth(4)
        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(300)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(tab)
        scroll_area.setVerticalScrollBarPolicy(1)
        self.roller_splitter.addWidget(scroll_area)
        controller_view = ControllerView(controller, tab)

        widget = self.roller_splitter.widget(index)
        policy = widget.sizePolicy()
        policy.setHorizontalStretch(1)
        widget.setSizePolicy(policy)

        return controller_view


    def add_settings_button(self, settings_button):
        self.main_layout.addWidget(settings_button, stretch=0, alignment=QtCore.Qt.AlignTop)