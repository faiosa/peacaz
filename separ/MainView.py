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
from urh import settings
from urh.controller.CompareFrameController import CompareFrameController
from urh.controller.MainController import MainController
from urh.controller.SignalTabController import SignalTabController
from urh.models.FileFilterProxyModel import FileFilterProxyModel
from urh.plugins.PluginManager import PluginManager
from urh.signalprocessing.ProtocolAnalyzer import ProtocolAnalyzer
from urh.signalprocessing.Signal import Signal
from urh.util import FileOperator
from urh.util.Errors import Errors
from urh.util.ProjectManager import ProjectManager
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
        if True:#self.settings["global_settings"]["urh"]:
            self.urh_controller = MainController(self.blue_print)
            #self.urh_controller = MainController(None)
            #self.blue_print.set_urh(self.urh_controller)
            self.setMenuBar(self.urh_controller.ui.menubar)

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

