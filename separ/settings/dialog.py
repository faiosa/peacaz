import json
import os

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QGroupBox, QHBoxLayout, QGridLayout, QPushButton

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
        self.controllers_settings = {}
        for num, c_settings in self.settings["controller_values"].items():
            self.controllers_settings[num] = ControllerSettings(self, c_settings)


        top_frame = QFrame(self)
        top_layout = QGridLayout(top_frame)
        top_frame.setLayout(top_layout)
        self.layout.addWidget(top_frame)

        top_layout.addWidget(self.global_settings_view.frame, 0, 0, 5, 1)

        save_button = QPushButton("Зберегти зміни", self)
        save_button.clicked.connect(lambda: self.__write_settings_to_file(SEPAR_SETTINGS_FILE))
        top_layout.addWidget(save_button, 1, 2)

        self.controller_tabs = QTabWidget(self)
        for c_setting in self.controllers_settings.values():
            self.controller_tabs.addTab(c_setting, c_setting.settings["name"])
        self.layout.addWidget(self.controller_tabs)

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
            for cs in self.controllers_settings.values():
                settings["controller_values"][str(num)] = cs.get_settings()
                num += 1
        return settings

    def save_settings(self):
        self.settings = self.get_settings()

