from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
import sys

from separ.MainView import MainRollerView, WithUrhView
from utils.position_window import position_window
from utils.path import resource_path
from utils.palette import getPalette
from config import ui
from utils.settings import *
from separ.control import Manager
from separ.qt5_control_view import ManagerView



def main():
    app = QApplication(sys.argv)

    json_settings = load_settings_from_file(SEPAR_SETTINGS_FILE)
    main_window = WithUrhView(json_settings) if json_settings["global_settings"]["urh"] else MainRollerView(json_settings)

    main_window.setWindowTitle("PTZ Controller")

    main_window.setGeometry(*position_window(app, window_width=825, window_height=730))

    main_window.setPalette(getPalette())




    app.setWindowIcon(QIcon("assets/icon.png"))
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
