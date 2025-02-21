import json
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QStyle, \
    QMessageBox

from separ.settings.dictionary import SettingsComposer, DictionarySettings, ComboPolicy, PinsPolicy, StrPolicy, BoolPolicy, DoublePolicy, IntPolicy
from utils.settings import SEPAR_SETTINGS_FILE


class TotalSettings(SettingsComposer):
    def __init__(self, parent_frame, main_view):
        super().__init__(parent_frame, main_view.settings)
        self.main_view = main_view
        self.tweak = self.main_view.tweak
        self.global_policies = [
            ComboPolicy("theme", 0, "Тема інтерфейсу", ["Світла", "Темна"]),
            ComboPolicy("language", 1, "Мова інтерфейсу", ["Українська", "English"])
        ]


        top_frame = QFrame(self)
        top_layout = QGridLayout(top_frame)
        top_frame.setLayout(top_layout)
        self.layout.addWidget(top_frame)

        gs_frame = QFrame()
        gs_layout = QVBoxLayout(gs_frame)
        gs_frame.setLayout(gs_layout)
        top_layout.addWidget(gs_frame, 0, 0, 5, 1)
        self.global_settings_view = DictionarySettings("global settings", gs_layout, self.settings["global_settings"], self.global_policies)
        self.global_settings_view.showView()
        #top_layout.addWidget(self.global_settings_view.outFrame, 0, 0, 5, 1)

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
        #if not 'name' in controller.settings:
        #    controller.settings['name'] = f"Контролер {index + 1}"
        #    controller.controller_settings_view.input_fields["name"].widget.setText(controller.settings['name'])
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

class ControllerSettings(SettingsComposer):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame, json_settings)
        self.switchboard_policies = [
            PinsPolicy("pins", 0, "Піни комутатора:"),
            StrPolicy("serial_port", 1, "Серійний порт комутатора:"),
            BoolPolicy("full_control", 2, "Повний контроль")
        ]

        use_radxa_policy = BoolPolicy("use_radxa", 1, "Використовує спільний порт (radxa)")
        radxa_port_policy = StrPolicy("radxa_serial_port", 2, "Спільний серійний порт (radxa)")

        use_radxa_policy.addSubPolicy(radxa_port_policy, True)
        self.controller_policies = [
            StrPolicy("name", 0, "Назва контроллера"),
            use_radxa_policy,
            radxa_port_policy
        ]

        self.controller_settings_view = DictionarySettings("general", self.layout, self.settings, self.controller_policies)
        self.switchboard_settings_view = DictionarySettings("switchboard", self.layout, self.settings["switchboard"], self.switchboard_policies)
        self.controller_settings_view.showView()
        self.switchboard_settings_view.showView()

        self.vroller_settings_view = None
        self.hroller_settings_view = None

        self.vroller_add_button = None
        self.hroller_add_button = None

        if "rollers" in self.settings:
            for roller in self.settings["rollers"]:
                if roller["type"] == "vertical":
                    vertical_roller_frame = QFrame(self)
                    self.vertical_roller_layout = QVBoxLayout(vertical_roller_frame)
                    vertical_roller_frame.setLayout(self.vertical_roller_layout)
                    self.layout.addWidget(vertical_roller_frame)
                    self.vroller_settings_view = self.__create_roller(roller, self.vertical_roller_layout)
                    self.vroller_settings_view.showView()
                elif roller["type"] == "horizontal":
                    horizontal_roller_frame = QFrame(self)
                    self.horizontal_roller_layout = QVBoxLayout(horizontal_roller_frame)
                    horizontal_roller_frame.setLayout(self.horizontal_roller_layout)
                    self.layout.addWidget(horizontal_roller_frame)
                    self.hroller_settings_view = self.__create_roller(roller, self.horizontal_roller_layout)
                    self.hroller_settings_view.showView()

        '''
        else:
            self.vroller_add_button = QPushButton()
            self.vroller_add_button.setText("Додати вертикальний ролер")
            self.vroller_add_button.clicked.connect(lambda: self._new_roller("vertical"))
            self.vertical_roller_layout.addWidget(self.vroller_add_button)
        '''

        #self.controller_settings_view.destroyView()
        self.normalizeSubPolicies()
        '''
        else:
            self.hroller_add_button = QPushButton()
            self.hroller_add_button.setText("Додати горизонтальний ролер")
            self.hroller_add_button.clicked.connect(lambda: self._new_roller("horizontal"))
            self.horizontal_roller_layout.addWidget(self.hroller_add_button)
        '''

    def normalizeSubPolicies(self):
        self.controller_settings_view.normalizeSubPolicies()
        self.switchboard_settings_view.normalizeSubPolicies()
        if self.vroller_settings_view:
            self.vroller_settings_view.normalizeSubPolicies()
        if self.hroller_settings_view:
            self.hroller_settings_view.normalizeSubPolicies()
    '''
    def _new_roller(self, roller_type):
        roller_settings = {
            "type": roller_type,
            "rotation_speed": 0.0,
            "min_angle": 0.0,
            "max_angle": 0.0,
            "current_angle": 0.0
        }
        if roller_type == "vertical":
            self.vroller_settings_view = self.__create_roller(roller_settings)
            self.vertical_roller_layout.removeWidget(self.vroller_add_button)
            self.vroller_add_button.deleteLater()
            self.vertical_roller_layout.addWidget(self.vroller_settings_view.frame)
            self.vroller_add_button = None
        else:
            self.hroller_settings_view = self.__create_roller(roller_settings)
            self.horizontal_roller_layout.removeWidget(self.hroller_add_button)
            self.hroller_add_button.deleteLater()
            self.horizontal_roller_layout.addWidget(self.hroller_settings_view.frame)
            self.hroller_add_button = None
    '''

    def __create_roller(self, roller_settings, roller_layout):
        '''
        labels = self.stepper_roller_labels if roller_settings["engine"] == "stepper" else self.line_roller_labels
        policies = self.stepper_roller_policies if roller_settings["engine"] == "stepper" else self.line_roller_policies
        settings_view = DictionarySettings(QGroupBox(f"{roller_settings['type']} roller"), labels, roller_settings, policies)
        '''
        roller_policies = [
            ComboPolicy("type", 0, "тип ролера", ["vertical", "horizontal"], False),
            ComboPolicy("engine", 1, "тип двигуна", ["stepper", "line"]),
            DoublePolicy("min_angle", 2, "Мін кут"),
            DoublePolicy("max_angle", 3, "Макс кут"),
            DoublePolicy("current_angle", 4, "Поточний кут"),
            StrPolicy("serial_port", 5, "Серійний порт"),
            DoublePolicy("rotation_speed", 6, "Швидкість повертання (градус/с)"),
            IntPolicy("steps", 7, "кроків в повному оберті")
        ]

        settings_view = DictionarySettings(f"{roller_settings['type']} roller", roller_layout, roller_settings, roller_policies)
        #del_button = QPushButton("Видалити", self)
        #del_button.clicked.connect(lambda: self.__remove_roller(settings_view))
        #settings_view.add_bottom_widget(del_button)
        return settings_view

    '''
    def __remove_roller(self, roller_view):
        target_layout = self.vertical_roller_layout if roller_view.settings['type'] == "vertical" else self.horizontal_roller_layout
        target_layout.removeWidget(roller_view.frame)
        roller_view.frame.deleteLater()
        if roller_view.settings['type'] == "vertical":
            self.vroller_add_button = QPushButton()
            self.vroller_add_button.setText("Додати вертикальний ролер")
            self.vroller_add_button.clicked.connect(lambda: self._new_roller("vertical"))
            target_layout.addWidget(self.vroller_add_button)
            self.vroller_settings_view = None
        else:
            self.hroller_add_button = QPushButton()
            self.hroller_add_button.setText("Додати горизонтальний ролер")
            self.hroller_add_button.clicked.connect(lambda: self._new_roller("horizontal"))
            target_layout.addWidget(self.hroller_add_button)
            self.hroller_settings_view = None
    '''
    def get_settings(self):
        settings = {}
        settings.update(self.controller_settings_view.get_settings())
        settings["switchboard"] = {}
        settings["switchboard"].update(self.switchboard_settings_view.get_settings())
        if self.hroller_settings_view or self.vroller_settings_view:
            settings["rollers"] = list()
            if self.hroller_settings_view:
                settings["rollers"].append(self.hroller_settings_view.get_settings())
            if self.vroller_settings_view:
                settings["rollers"].append(self.vroller_settings_view.get_settings())
        return settings

    def save_settings(self):
        self.settings = self.get_settings()
