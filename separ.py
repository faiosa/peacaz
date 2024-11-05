from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
import sys

from separ.MainView import MainView
from utils.position_window import position_window_at_centre
from utils.path import resource_path
from utils.palette import getPalette
from config import ui
from utils.settings import *
from separ.control import Manager
from separ.qt5_control_view import ManagerView



def main():
    app = QApplication(sys.argv)
    #main_window = QWidget()
    main_window = MainView()

    main_window.setWindowTitle("PTZ Controller")


    window = QWidget(main_window)
    main_window.setCentralWidget(window)
    #main_window.addW

    #settings_button = QPushButton("aloha", window)
    #settings_button.setIcon(QIcon("assets/settings.png"))
    #settings_button.clicked.connect(lambda : print("aloha Kyiv"))

    main_window.setGeometry(*position_window_at_centre(app, window_width=825, window_height=730))

    main_window.setPalette(getPalette())


    json_settings = load_settings_from_file(SEPAR_SETTINGS_FILE)
    manager = Manager(json_settings)
    ManagerView(manager, window)

    app.setWindowIcon(QIcon("assets/icon.png"))
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
