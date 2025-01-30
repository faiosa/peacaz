import json
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QStyle, \
    QMessageBox

from separ.settings.dictionary import ControllerSettings, SettingsComposer, DictionarySettings
from utils.settings import SEPAR_SETTINGS_FILE


class TotalSettings(SettingsComposer):
    def __init__(self, parent_frame, main_view):
        super().__init__(parent_frame, main_view.settings)
        self.main_view = main_view
        self.tweak = self.main_view.tweak
        self.global_labels = {
            "theme": "Тема інтерфейсу",
            "language": "Мова інтерфейсу",
            #"urh": "Enable Radio Hacker"
        }
        self.global_policies = {
            "theme": ["Світла", "Темна"],
            "language": ["Українська", "English"],
            #"urh": "bool"
        }
        self.global_settings_view = DictionarySettings(QGroupBox("global settings"), self.global_labels, self.settings["global_settings"], self.global_policies)


        top_frame = QFrame(self)
        top_layout = QGridLayout(top_frame)
        top_frame.setLayout(top_layout)
        self.layout.addWidget(top_frame)

        top_layout.addWidget(self.global_settings_view.frame, 0, 0, 5, 1)

        save_button = QPushButton("Зберегти зміни", self)
        save_button.clicked.connect(lambda: self.__write_settings_to_file(SEPAR_SETTINGS_FILE))
        top_layout.addWidget(save_button, 1, 2)

        #add_controller_button = QPushButton("Додати контролер", self)
        #add_controller_button.clicked.connect(lambda: self.__add_settings_controller({}))
        #top_layout.addWidget(add_controller_button, 3, 2)

        self.controller_tabs = QTabWidget(self)
        self.right_side = self.controller_tabs.tabBar().RightSide

        self.controllers_settings = []
        for c_settings in self.settings["controller_values"].values():
            self.__add_settings_controller(c_settings)

        self.layout.addWidget(self.controller_tabs)

    def __add_settings_controller(self, settings):
        index = len(self.controllers_settings)
        controller = ControllerSettings(self, settings)
        if not 'name' in controller.settings:
            controller.settings['name'] = f"Контролер {index + 1}"
            controller.controller_settings_view.input_fields["name"].widget.setText(controller.settings['name'])
        self.controllers_settings.append(controller)
        self.controller_tabs.addTab(controller, controller.settings["name"])
        #del_button = QPushButton()
        #del_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_BrowserStop")))
        #del_button.clicked.connect((lambda cs=controller: lambda: self.__delete_controller(cs))())
        #self.controller_tabs.tabBar().setTabButton(index, self.right_side, del_button)
    '''
    def __delete_controller(self, c_settings):
        for index in range(len(self.controllers_settings)):
            if c_settings == self.controllers_settings[index]:
                self.controllers_settings.pop(index)
                self.controller_tabs.removeTab(index)
                return
    '''
    def __update_current_angles(self):
        for controller in self.main_view.roller_manager.controllers:
            for c_key, controller_settings in self.settings["controller_values"].items():
                if controller.name == controller_settings["name"]:
                    for roller in controller.rollers:
                        for r_index, roller_settings in enumerate(controller_settings["rollers"]):
                            if roller_settings["type"] == "vertical" and roller.is_vertical:
                                self.settings["controller_values"][c_key]["rollers"][r_index]["current_angle"] = roller.current_angle
                            elif roller_settings["type"] == "horizontal" and not roller.is_vertical:
                                self.settings["controller_values"][c_key]["rollers"][r_index]["current_angle"] = roller.current_angle



    def __write_settings_to_file(self, file_name):
        if self.main_view.roller_manager.is_moving():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не можна зберегти")
            msg.setInformativeText("Деякі з антен все ще в русі! Для успішного сберігання дочекайтесь повної зупинки поворотних двигунів.")
            msg.setWindowTitle("Помилка зберігання")
            msg.exec_()
        else:
            self.save_settings()
            self.__update_current_angles()
            self.tweak.write_settings(self.settings)
            self.main_view.reload_settings()
            self.main_view.reload_print()

    def get_settings(self):
        settings = {}
        settings["global_settings"] = self.global_settings_view.get_settings()
        if len(self.controllers_settings) > 0:
            settings["controller_values"] = {}
            num = 1
            for cs in self.controllers_settings:
                settings["controller_values"][str(num)] = cs.get_settings()
                num += 1
        return settings

    def save_settings(self):
        for index in range(len(self.controllers_settings)):
            self.controllers_settings[index].save_settings()
            self.controller_tabs.setTabText(index, self.controllers_settings[index].settings['name'])
        self.settings = self.get_settings()

