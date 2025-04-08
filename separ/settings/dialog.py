import json
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QGroupBox, QHBoxLayout, QGridLayout, QPushButton, QStyle, \
    QMessageBox

from separ.settings.dictionary import SettingsComposer, DictionarySettings, ComboPolicy, PinsPolicy, StrPolicy, BoolPolicy, DoublePolicy, IntPolicy
from separ.settings.specific import SetCurrentAnglePolicy
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

        save_button = QPushButton("Зберегти зміни", self)
        save_button.clicked.connect(lambda: self.__write_settings_to_file())
        top_layout.addWidget(save_button, 1, 2)

        #add_controller_button = QPushButton("Додати контролер", self)
        #add_controller_button.clicked.connect(lambda: self.__add_settings_controller({}))
        #top_layout.addWidget(add_controller_button, 3, 2)

        self.controller_tabs = QTabWidget(self)
        self.right_side = self.controller_tabs.tabBar().RightSide

        self.controllers_settings = []
        for controller in self.main_view.roller_manager.controllers:
            self.__add_settings_controller(controller)

        self.layout.addWidget(self.controller_tabs)

    def __add_settings_controller(self, controller):
        index = len(self.controllers_settings)
        controller_set = ControllerSettings(self, controller)
        self.controllers_settings.append(controller_set)
        self.controller_tabs.addTab(controller_set, controller_set.settings["name"])
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


    def __write_settings_to_file(self):
        if self.main_view.roller_manager.is_moving():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не можна зберегти")
            msg.setInformativeText("Деякі з антен все ще в русі! Для успішного сберігання дочекайтесь повної зупинки поворотних двигунів.")
            msg.setWindowTitle("Помилка зберігання")
            msg.exec_()
        else:
            self.save_settings()
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
    def __init__(self, parent_frame, controller):
        super().__init__(parent_frame, controller.settings)
        self.controller = controller

        switchboard_use_radxa_policy = BoolPolicy("use_radxa", 2, "Використовує спільний порт (radxa)")
        switchboard_serial_port = StrPolicy("serial_port", 3, "Серійний порт комутатора:")
        self.switchboard_policies = [
            PinsPolicy("pins", 0, "Піни комутатора:"),
            BoolPolicy("full_control", 1, "Повний контроль"),
            switchboard_use_radxa_policy,
            switchboard_serial_port
        ]
        switchboard_use_radxa_policy.addSubPolicy(switchboard_serial_port, [False, "__disabled__"])

        use_radxa_policy = BoolPolicy("use_radxa", 1, "Використовує спільний порт (radxa)")
        radxa_port_policy = StrPolicy("radxa_serial_port", 2, "Спільний серійний порт (radxa)")

        use_radxa_policy.addSubPolicy(radxa_port_policy, [True])
        use_radxa_policy.addSubPolicy(switchboard_use_radxa_policy, [True])
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
            for index in range(len(self.settings["rollers"])):
                roller_settings = self.settings["rollers"][index]
                if roller_settings["type"] == "vertical":
                    vertical_roller_frame = QFrame(self)
                    self.vertical_roller_layout = QVBoxLayout(vertical_roller_frame)
                    vertical_roller_frame.setLayout(self.vertical_roller_layout)
                    self.layout.addWidget(vertical_roller_frame)
                    self.vroller_settings_view = self.__create_roller(roller_settings, self.vertical_roller_layout, use_radxa_policy)
                    self.vroller_settings_view.showView()
                elif roller_settings["type"] == "horizontal":
                    horizontal_roller_frame = QFrame(self)
                    self.horizontal_roller_layout = QVBoxLayout(horizontal_roller_frame)
                    horizontal_roller_frame.setLayout(self.horizontal_roller_layout)
                    self.layout.addWidget(horizontal_roller_frame)
                    self.hroller_settings_view = self.__create_roller(roller_settings, self.horizontal_roller_layout, use_radxa_policy, self.controller.rollers[index])
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

    def __create_roller(self, roller_settings, roller_layout, is_radxa_policy, roller = None):
        '''
        labels = self.stepper_roller_labels if roller_settings["engine"] == "stepper" else self.line_roller_labels
        policies = self.stepper_roller_policies if roller_settings["engine"] == "stepper" else self.line_roller_policies
        settings_view = DictionarySettings(QGroupBox(f"{roller_settings['type']} roller"), labels, roller_settings, policies)
        '''

        no_radxa_engine_policy = ComboPolicy("engine", 1, "тип двигуна", ["line"], False)
        is_radxa_policy.addSubPolicy(no_radxa_engine_policy, [False, "__disabled__"])
        is_radxa_engine_policy = ComboPolicy("engine", 2, "тип двигуна", ["stepper", "line"])
        is_radxa_policy.addSubPolicy(is_radxa_engine_policy, [True])
        current_angle_policy = DoublePolicy("current_angle", 5, "Поточний кут")
        is_radxa_engine_policy.addSubPolicy(current_angle_policy, ["line", "__disabled__"])
        serial_port_policy = StrPolicy("serial_port", 6, "Серійний порт")
        is_radxa_engine_policy.addSubPolicy(serial_port_policy, ["line", "__disabled__"])
        num_steps_policy = IntPolicy("steps", 8, "кроків в повному оберті")

        roller_direction_policy = ComboPolicy("type", 0, "тип ролера", ["vertical", "horizontal"], False)
        view_angle_policy = DoublePolicy("view_angle_shift", 9, "Відхилення шкали ролера (град.)")
        roller_direction_policy.addSubPolicy(view_angle_policy, ["horizontal"])

        is_radxa_engine_policy.addSubPolicy(num_steps_policy, ["stepper"])

        set_stepper_cur_angle_policy = SetCurrentAnglePolicy(10, "Поточний кут", roller)
        is_radxa_engine_policy.addSubPolicy(set_stepper_cur_angle_policy, ["stepper"])

        roller_policies = [
            roller_direction_policy,
            no_radxa_engine_policy,
            is_radxa_engine_policy,
            DoublePolicy("min_angle", 3, "Мін кут"),
            DoublePolicy("max_angle", 4, "Макс кут"),
            current_angle_policy,
            serial_port_policy,
            DoublePolicy("rotation_speed", 7, "Швидкість повертання (градус/с)"),
            num_steps_policy,
            view_angle_policy,
            set_stepper_cur_angle_policy
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
        if self.hroller_settings_view:
            self.hroller_settings_view.save_settings()
        if self.vroller_settings_view:
            self.vroller_settings_view.save_settings()
        self.settings = self.get_settings()
