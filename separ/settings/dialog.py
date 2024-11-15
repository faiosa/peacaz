import json
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QStyle

from separ.settings.dictionary import ControllerSettings, SettingsComposer, DictionarySettings
from utils.settings import SEPAR_SETTINGS_FILE


class TotalSettings(SettingsComposer):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame, json_settings)
        self.global_labels = {
            "theme": "Тема інтерфейсу",
            "language": "Мова інтерфейсу",
            "urh": "Enabble Radio Hacker"
        }
        self.global_policies = {
            "theme": ["Світла", "Темна"],
            "language": ["Українська", "English"],
            "urh": "bool"
        }
        self.global_settings_view = DictionarySettings(QGroupBox("global settings"), self.global_labels, self.settings["global_settings"], self.global_policies)
        self.controllers_settings = []
        for num, c_settings in self.settings["controller_values"].items():
            self.controllers_settings.append(ControllerSettings(self, c_settings))


        top_frame = QFrame(self)
        top_layout = QGridLayout(top_frame)
        top_frame.setLayout(top_layout)
        self.layout.addWidget(top_frame)

        top_layout.addWidget(self.global_settings_view.frame, 0, 0, 5, 1)

        save_button = QPushButton("Зберегти зміни", self)
        save_button.clicked.connect(lambda: self.__write_settings_to_file(SEPAR_SETTINGS_FILE))
        top_layout.addWidget(save_button, 1, 2)

        self.controller_tabs = QTabWidget(self)
        right_side = self.controller_tabs.tabBar().RightSide
        index = 0
        for c_setting in self.controllers_settings:
            #print(f"type of c_settings is {type(c_setting)}")
            self.controller_tabs.addTab(c_setting, c_setting.settings["name"])
            del_button = QPushButton()
            del_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_BrowserStop")))
            del_button.clicked.connect((lambda cs=c_setting: lambda: self.__delete_controller(cs))())
            self.controller_tabs.tabBar().setTabButton(index, right_side, del_button)
            index += 1

        self.layout.addWidget(self.controller_tabs)

    def __delete_controller(self, c_settings):
        #print(f"deleting controller {c_settings.settings['name']}, len={len(self.controllers_settings)}")
        for index in range(len(self.controllers_settings)):
            if c_settings == self.controllers_settings[index]:
                self.controllers_settings.pop(index)
                self.controller_tabs.removeTab(index)
                return

    def __write_settings_to_file(self, file_name):
        self.save_settings()
        with open(os.path.abspath(file_name), "w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4, ensure_ascii=False)


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
        self.settings = self.get_settings()
