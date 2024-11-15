import copy
import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QDir, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, qApp, QAction, \
    QDialog, QLabel

from separ.control import Manager
from separ.qt5_control_view import ManagerView
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


class MainRollerView(QMainWindow):
    def __init__(self, settings,  *args):
        super().__init__(*args)

        self.settings = settings
        window = QWidget(self)
        self.setCentralWidget(window)

        main_layout = QHBoxLayout(window)
        window.setLayout(main_layout)

        self.left_column = QWidget(window)
        self.left_layout = QVBoxLayout(self.left_column)
        self.left_column.setLayout(self.left_layout)
        self.left_top_frame = QWidget(self.left_column)
        self.left_layout.addWidget(self.left_top_frame)

        main_layout.addWidget(self.left_column)

        right_column = QWidget(window)
        main_layout.addWidget(right_column)

        settings_button = QPushButton(window)
        settings_button.setIcon(QIcon("assets/settings.png"))
        settings_button.clicked.connect(lambda: self.open_settings_window())
        settings_button.setFixedWidth(25)
        main_layout.addWidget(settings_button, stretch=0, alignment=QtCore.Qt.AlignTop)

        self.roller_manager = None
        self.roller_manager_view = None

        self._set_ui()


    def _set_ui(self):
        self.roller_manager = Manager(self.settings)
        self.roller_manager_view = ManagerView(self.roller_manager, self.left_top_frame)

    def open_settings_window(self):
        dlg = QDialog()
        dlg.setWindowTitle("Налаштування")
        settings = load_settings_from_file(SEPAR_SETTINGS_FILE)
        settings_view = TotalSettings(dlg, settings)
        dlg_layout = QVBoxLayout(dlg)
        dlg.setLayout(dlg_layout)
        dlg_layout.addWidget(settings_view)

        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

class WithUrhView(MainRollerView):
    def __init__(self, settings, *args):
        super().__init__(settings, *args)
        self.urh_controller = MainController()
        self.left_layout.addWidget(self.urh_controller)
        self.setMenuBar(self.urh_controller.ui.menubar)

