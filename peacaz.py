from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
import sys

from separ.MainView import MainRollerView
from utils.position_window import position_window
from utils.path import resource_path
from utils.palette import getPalette
from config import ui
from utils.settings import *
from separ.control import Manager



def main():
    app = QApplication(sys.argv)
    main_window = MainRollerView()

    main_window.setWindowTitle("PTZ Controller")

    main_window.setGeometry(*position_window(app, window_width=825, window_height=730))

    main_window.setPalette(getPalette())




    app.setWindowIcon(QIcon("assets/icon.png"))
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
