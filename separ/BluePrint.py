from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QFrame, QSplitter, QScrollArea, QGridLayout

from separ.qt5_control_view import ControllerView


class BluePrint:
    def __init__(self, window):
        self.window = window

        self.main_layout = QHBoxLayout(window)
        window.setLayout(self.main_layout)

        self.__set_left_frame()


        right_column = QWidget(window)
        self.main_layout.addWidget(right_column)
        self.open_index = -1

        self.buttons = [None, None, None]
        self.repl_frames = [None, None, None]


    def __set_left_frame(self):
        self.left_column = QWidget(self.window)
        self.left_layout = QVBoxLayout(self.left_column)
        self.left_column.setLayout(self.left_layout)
        self.main_layout.addWidget(self.left_column)
        #self.__set_rollers_slots()

    def __unset_left_frame(self):
        self.main_layout.removeWidget(self.left_column)
        self.left_column.deleteLater()
        self.left_column = None
        self.left_layout = None

    def set_urh(self, urh_controller):
        self.left_layout.addWidget(urh_controller)

    def reload_roller_slots(self):
        self.__unset_rollers_slots()
        #self.__set_rollers_slots()

    def __unset_rollers_slots(self):
        self.left_layout.removeWidget(self.rollers_frame)
        self.rollers_frame.deleteLater()
        self.rollers_frame = None

    def __set_rollers_slots(self):
        self.rollers_frame = QWidget(self.left_column)
        #self.left_layout.addWidget(self.rollers_frame)
        self.left_layout.insertWidget(0, self.rollers_frame)

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
        if (not hasattr(self, "rollers_frame")) or self.rollers_frame == None:
            self.__set_rollers_slots()
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

class GridBluePrint(BluePrint):
    def __init__(self, window):
        super().__init__(window)


    def set_urh(self, urh_controller):
        pass

    def __set_rollers_slots(self):
        self.rollers_frame = QWidget(self.left_column)
        self.left_layout.insertWidget(0, self.rollers_frame)

        self.roller_layout = QGridLayout(self.rollers_frame)
        self.rollers_frame.setLayout(self.roller_layout)


    def add_roller(self, controller, index):
        if (not hasattr(self, "rollers_frame")) or self.rollers_frame == None:
            self.__set_rollers_slots()
        frame = QFrame(self.rollers_frame)
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        frame.setLineWidth(4)
        frame.setMaximumWidth(480)
        controller_view = ControllerView(controller, frame)

        self.roller_layout.addWidget(frame, index, 0, alignment=QtCore.Qt.AlignLeft)

        return controller_view

    def add_open_signal_button(self, button, index):
        self.buttons[index] = button
        self.roller_layout.addWidget(button, index, 1, alignment=QtCore.Qt.AlignCenter)

    def del_open_signal_button(self, index):
        self.roller_layout.removeWidget(self.buttons[index])
        self.buttons[index].deleteLater()
        self.buttons[index] = None

    def open_signal_frame(self, sig_frame, index):
        sig_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        sig_frame.setLineWidth(4)
        sig_frame.setMaximumWidth(500)
        self.roller_layout.addWidget(sig_frame, index, 1)

    def open_signal_replay_frame(self, repl_frame, index):
        repl_frame.setMaximumWidth(500)
        self.roller_layout.addWidget(repl_frame, index, 2)
        self.repl_frames[index] = repl_frame

    def del_signal_replay_frame(self, index):
        self.roller_layout.removeWidget(self.repl_frames[index])
        self.repl_frames[index].deleteLater()
        self.repl_frames[index] = None