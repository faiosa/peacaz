from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow


class MainView(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 30))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")

        self.actionOpen = QtWidgets.QAction(self)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setText("Open")

        self.menuFile.addAction(self.actionOpen)
        self.menubar.addMenu(self.menuFile)
        self.setMenuBar(self.menubar)
        print("MenuBar SET")