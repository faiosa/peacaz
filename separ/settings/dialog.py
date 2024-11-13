from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget

from separ.settings.dictionary import ControllerSettings, SettingsComposer


class TotalSettings(SettingsComposer):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame, json_settings)
        #self.layout = QVBoxLayout(self)
        #self.setLayout(self.layout)
        self.global_labels = {
            "theme": "Тема інтерфейсу",
            "language": "Мова інтерфейсу"
        }
        self.global_policies = {
            "theme": ["Світла", "Темна"],
            "language": ["Українська", "English"]
        }
        self.global_settings_view = self.get_dictionary_settings(QFrame(self), self.global_labels, self.global_policies)
        self.controllers_settings = {}
        for num, c_settings in self.settings["controller_values"].items():
            self.controllers_settings[num] = ControllerSettings(self, c_settings)
        self.pack_layout()

    def pack_layout(self):
        self.layout.addWidget(self.global_settings_view.frame)
        self.controller_tabs = QTabWidget(self)
        for c_setting in self.controllers_settings.values():
            self.controller_tabs.addTab(c_setting, c_setting.settings["name"])
        self.layout.addWidget(self.controller_tabs)

    #def paintEvent(self, event):
        #print("painting TotalSettings...")
