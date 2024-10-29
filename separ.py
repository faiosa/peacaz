from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
import sys

from utils.position_window import position_window_at_centre
from utils.path import resource_path
from utils.palette import getPalette
from config import ui
from utils.settings import *
from separ.control import Manager
from separ.qt5_control_view import ManagerView



def main():
    app = QApplication(sys.argv)
    window = QWidget()

    window.setWindowTitle("PTZ Controller")

    #settings_button = QPushButton("aloha", window)
    #settings_button.setIcon(QIcon("assets/settings.png"))
    #settings_button.clicked.connect(lambda : print("aloha Kyiv"))

    window.setGeometry(*position_window_at_centre(app, window_width=825, window_height=730))

    window.setPalette(getPalette())


    json_settings = load_settings_from_file(SEPAR_SETTINGS_FILE)
    manager = Manager(json_settings)
    ManagerView(manager, window)

    app.setWindowIcon(QIcon("assets/icon.png"))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
