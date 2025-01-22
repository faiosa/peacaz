import copy
import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QDir, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, qApp, QAction, \
    QDialog, QLabel

from separ.BluePrint import BluePrint, GridBluePrint
from separ.control import Manager
from separ.settings.dialog import TotalSettings

from utils.settings import load_settings_from_file, SEPAR_SETTINGS_FILE

#class PTZRolerView(QMainWindow):


class MainRollerView(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)


        window = QWidget(self)
        self.setCentralWidget(window)

        #self.blue_print = BluePrint(window)
        self.blue_print = GridBluePrint(window)
        settings_button = QPushButton(window)
        settings_button.setIcon(QIcon("assets/settings.png"))
        settings_button.clicked.connect(lambda: self.open_settings_window())
        settings_button.setFixedWidth(25)
        #main_layout.addWidget(settings_button, stretch=0, alignment=QtCore.Qt.AlignTop)
        self.blue_print.add_settings_button(settings_button)

        self.roller_manager = None
        self.roller_manager_view = None

        self.reload_settings(SEPAR_SETTINGS_FILE)
        for index in range(len(self.roller_manager.controllers)):
            self.blue_print.add_roller(self.roller_manager.controllers[index], index)

        self.urh_controller = None
        self.open_index = -1
        for i in range(3):
            self.setup_open_button(i)

    def setup_open_button(self, ind):
        open_button = self.__get_open_button(ind)
        self.blue_print.add_open_signal_button(open_button, ind)

    def __get_open_button(self, index):
        open_button = QPushButton()
        open_button.setIcon(QtGui.QIcon.fromTheme("document-open"))
        open_button.clicked.connect((lambda i = index: lambda: self.open_signal_file(i))())
        open_button.setFixedWidth(25)
        return open_button

    def open_signal_frame(self, sig_frame):
        self.blue_print.del_open_signal_button(self.open_index)
        self.blue_print.open_signal_frame(sig_frame, self.open_index)

    def open_signal_file(self, index):
        self.open_index = index
        self.urh_controller.on_open_file_action_triggered()
        self.open_index = -1

    def reload_settings(self, file):
        self.settings = load_settings_from_file(file)
        self.roller_manager = Manager(self.settings)

    def reload_print(self):
        self.blue_print.reload_roller_slots()
        for index in range(len(self.roller_manager.controllers)):
            self.blue_print.add_roller(self.roller_manager.controllers[index], index)


    def open_settings_window(self):
        dlg = QDialog()
        dlg.setWindowTitle("Налаштування")
        dlg.setFixedWidth(750)
        settings_view = TotalSettings(dlg, self)
        dlg_layout = QVBoxLayout(dlg)
        dlg.setLayout(dlg_layout)
        dlg_layout.addWidget(settings_view)

        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

