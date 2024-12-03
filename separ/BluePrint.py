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

    def set_urh(self, urh_controller):
        self.left_layout.addWidget(urh_controller)

    def set_up_rollers(self, roller_manager):
        left_top_frame = QWidget(self.left_column)
        self.left_layout.addWidget(left_top_frame)
        self.__set_up_rollers(roller_manager, left_top_frame)

    def __set_up_rollers(self, roller_manager, frame):
        layout = QHBoxLayout(frame)
        splitter = QSplitter(frame)

        splitter.setStyleSheet(
            "QSplitter::handle:horizontal {\n"
            "margin: 4px 0px;\n"
            "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
            "stop:0 rgba(255, 255, 255, 0), \n"
            "stop:0.5 rgba(100, 100, 100, 100), \n"
            "stop:1 rgba(255, 255, 255, 0));\n"
            "image: url(:/icons/icons/splitter_handle_vertical.svg);\n"
            "}"
        )

        splitter.setHandleWidth(6)
        splitter.setObjectName("splitter")
        controllers_views = []
        for controller in roller_manager.controllers:
            tab = QFrame(frame)
            tab.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
            tab.setLineWidth(4)
            scroll_area = QScrollArea()
            scroll_area.setFixedHeight(300)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(tab)
            scroll_area.setVerticalScrollBarPolicy(1)
            splitter.addWidget(scroll_area)
            controller_view = ControllerView(controller, tab)
            controllers_views.append(controller_view)
        splitter.setSizes([250, 250, 250])
        layout.addWidget(splitter)

        widget = splitter.widget(0)
        policy = widget.sizePolicy()
        policy.setHorizontalStretch(1)
        widget.setSizePolicy(policy)
        frame.setLayout(layout)


    def add_settings_button(self, settings_button):
        self.main_layout.addWidget(settings_button, stretch=0, alignment=QtCore.Qt.AlignTop)