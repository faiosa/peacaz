from PyQt5 import QtCore
from PyQt5.QtCore import QLocale, QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QFrame, QVBoxLayout, QPushButton, QComboBox, \
    QGroupBox


class DictionarySettings:
    def __init__(self, frame, labels, json_settings, policies):
        self.frame = frame
        self.labels = labels
        self.frame.setStyleSheet('''
            QGroupBox {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #E0E0E0, stop: 1 #FFFFFF);
                border: 2px solid #999999;
                border-radius: 5px;
                margin-top: 1ex;  /*leave space at the top for the title */
                font-size: 13px;
                color: black;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;    /* position at the top center */
                padding: 0 3px;
                font-size: 13px;
                color: black;
            }
        ''')
        self.input_fields = {}
        self.settings = json_settings
        self.layout = QGridLayout(frame)
        row = 0

        for key in labels:
            label = QLabel(frame)
            label.setText(labels.get(key) if key in labels else key)
            self.layout.addWidget(label, row, 0)
            value = self.settings[key] if key in self.settings else None

            policy = policies[key] if key in policies else "str"
            if policy == "immutable":
                self.input_fields[key] = StrItem(frame, value, False)
            elif policy == "int":
                self.input_fields[key] = IntItem(frame, value)
            elif policy == "double":
                self.input_fields[key] = DoubleItem(frame, value)
            elif policy == "bool":
                self.input_fields[key] = BoolItem(frame, value)
            elif policy == "pins":
                self.input_fields[key] = PinListItem(frame, value)
            elif type(policy) is list:
                self.input_fields[key] = ComboItem(frame, policy, value)
            else:
                self.input_fields[key] = StrItem(frame, value)

            self.layout.addWidget(self.input_fields[key].widget, row, 1)
            row += 1

        self.frame.setLayout(self.layout)

    def add_bottom_widget(self, widget):
        self.layout.addWidget(widget, len(self.labels), 0, 1, 2)


    def get_settings(self):
        settings = {}
        for key, ifield in self.input_fields.items():
            settings[key] = ifield.value()
        return settings

    def save_settings(self):
        self.settings = self.get_settings()

class InputItem:
    def __init__(self, widget):
        self.widget = widget

    def input_field(self):
        return self.widget

class IntItem(InputItem):
    def __init__(self, parent_frame, value):
        super().__init__(QLineEdit(parent_frame))
        self.widget.setValidator(QIntValidator())
        self.widget.setText(str(0 if value is None else value))

    def value(self):
        return int(self.widget.text())


class DoubleItem(InputItem):
    def __init__(self, parent_frame, value):
        super().__init__(QLineEdit(parent_frame))
        validator = QDoubleValidator()
        locale = QtCore.QLocale(QLocale.English, QLocale.UnitedStates)
        validator.setLocale(locale)
        self.widget.setValidator(validator)
        self.widget.setText(str(0.0 if value is None else value))

    def value(self):
        return float(self.widget.text())

class StrItem(InputItem):
    def __init__(self, parent_frame, value, enabled = True):
        super().__init__(QLineEdit(parent_frame))

        #regex = QRegExp("[0-9]+.?[0-9]{,2}")
        #validator = QRegExpValidator(regex, self.widget)
        #self.widget.setValidator(validator)
        self.widget.setText(value)
        self.widget.setEnabled(enabled)

    def value(self):
        return str(self.widget.text())

class PinListItem(StrItem):
    def __init__(self, parent_frame, value):
        super().__init__(parent_frame, value)
        regex = QRegExp("[0-9]{1,3}([ ]*,[ ]*[0-9]{1,3})*")
        validator = QRegExpValidator(regex, self.widget)
        self.widget.setValidator(validator)


class BoolItem(InputItem):
    def __init__(self, parent_frame, value):
        super().__init__(QCheckBox(parent_frame))
        self.widget.setChecked(bool(value))

    def value(self):
        return self.widget.isChecked()

class ComboItem(InputItem):
    def __init__(self, parent_frame, values, value):
        combo = QComboBox(parent_frame)
        combo.addItems(values)
        combo.setCurrentText(value)
        super().__init__(combo)

    def value(self):
        return self.widget.currentText()


class SettingsComposer(QFrame):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame)
        self.settings = json_settings

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def get_dictionary_settings(self, frame, labels, policies):
        settings = {}
        for key, label in labels.items():
            if key in self.settings:
                settings[key] = self.settings[key]
        return DictionarySettings(frame, labels, settings, policies)

class ControllerSettings(SettingsComposer):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame, json_settings)
        self.switchboard_labels = {
            "switchboard_pins": "Піни комутатора:",
            "switchboard_serial_port": "Серійний порт комутатора:",
            "full_controller": "Повний контроль"
        }
        self.switchboard_policies = {
            "full_controller": "bool",
            "switchboard_pins": "pins"
        }
        self.controller_labels = {
            "name": "Назва контроллера",
            "serial_port": "Серійний порт"
        }
        self.controller_policies = {
            "name": "str",
            "serial_port": "str"
        }
        self.roller_labels = {
            "type": "тип ролера",
            "rotation_speed": "Швидкість повертання (градус/с)",
            "min_angle": "Мін кут",
            "max_angle": "Макс кут",
            "current_angle": "Поточний кут",
            "is_stepper": "кроковий",
            "steps": "кроків в оберті"
        }
        self.roller_policies = {
            "type": "immutable",
            "rotation_speed": "double",
            "min_angle": "double",
            "max_angle": "double",
            "current_angle": "double",
            "is_stepper": "bool",
            "steps": "int"
        }
        self.controller_settings_view = self.get_dictionary_settings(QGroupBox("general"), self.controller_labels, self.controller_policies)
        self.switchboard_settings_view = self.get_dictionary_settings(QGroupBox("switchboard"), self.switchboard_labels, self.switchboard_policies)

        self.vroller_settings_view = None
        self.hroller_settings_view = None

        self.vroller_add_button = None
        self.hroller_add_button = None

        if "rollers" in self.settings:
            for roller in self.settings["rollers"]:
                if roller["type"] == "vertical":
                    self.vroller_settings_view = self.__create_roller(roller)
                elif roller["type"] == "horizontal":
                    self.hroller_settings_view = self.__create_roller(roller)

        self.layout.addWidget(self.controller_settings_view.frame)
        self.layout.addWidget(self.switchboard_settings_view.frame)

        vertical_roller_frame = QFrame(self)
        self.vertical_roller_layout = QVBoxLayout(vertical_roller_frame)
        vertical_roller_frame.setLayout(self.vertical_roller_layout)
        self.layout.addWidget(vertical_roller_frame)

        horizontal_roller_frame = QFrame(self)
        self.horizontal_roller_layout = QVBoxLayout(horizontal_roller_frame)
        horizontal_roller_frame.setLayout(self.horizontal_roller_layout)
        self.layout.addWidget(horizontal_roller_frame)

        if self.vroller_settings_view:
            self.vertical_roller_layout.addWidget(self.vroller_settings_view.frame)
        else:
            self.vroller_add_button = QPushButton()
            self.vroller_add_button.setText("Додати вертикальний ролер")
            self.vroller_add_button.clicked.connect(lambda: self._new_roller("vertical"))
            self.vertical_roller_layout.addWidget(self.vroller_add_button)

        if self.hroller_settings_view:
            self.horizontal_roller_layout.addWidget(self.hroller_settings_view.frame)
        else:
            self.hroller_add_button = QPushButton()
            self.hroller_add_button.setText("Додати горизонтальний ролер")
            self.hroller_add_button.clicked.connect(lambda: self._new_roller("horizontal"))
            self.horizontal_roller_layout.addWidget(self.hroller_add_button)

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

    def __create_roller(self, roller_settings):
        settings_view = DictionarySettings(QGroupBox(f"{roller_settings['type']} roller"), self.roller_labels, roller_settings, self.roller_policies)
        del_button = QPushButton("Видалити", self)
        del_button.clicked.connect(lambda: self.__remove_roller(settings_view))
        settings_view.add_bottom_widget(del_button)
        return settings_view

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

    def get_settings(self):
        settings = {}
        settings.update(self.controller_settings_view.get_settings())
        settings.update(self.switchboard_settings_view.get_settings())
        if self.hroller_settings_view or self.vroller_settings_view:
            settings["rollers"] = list()
            if self.hroller_settings_view:
                settings["rollers"].append(self.hroller_settings_view.get_settings())
            if self.vroller_settings_view:
                settings["rollers"].append(self.vroller_settings_view.get_settings())
        return settings

    def save_settings(self):
        self.settings = self.get_settings()






