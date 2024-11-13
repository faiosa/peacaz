from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QFrame, QVBoxLayout, QPushButton, QComboBox


class DictionarySettings:
    def __init__(self, frame, labels, json_settings, policies):
        self.frame = frame
        self.input_fields = {}
        self.settings = json_settings
        layout = QGridLayout(frame)
        row = 0
        if "header" in labels:
            header_label = QLabel(frame)
            header_label.setText(labels["header"])
            layout.addItem(header_label, row, 0, 1, 2)
            row += 1

        for key, value in json_settings.items():
            label = QLabel(frame)
            label.setText(labels.get(key) if key in labels else key)
            layout.addWidget(label, row, 0)

            policy = policies[key] if key in policies else "str"
            if policy == "immutable":
                self.input_fields[key] = StrItem(frame, value, False)
            elif policy == "int":
                self.input_fields[key] = IntItem(frame, value)
            elif policy == "double":
                self.input_fields[key] = DoubleItem(frame, value)
            elif policy == "bool":
                self.input_fields[key] = BoolItem(frame, value)
            elif type(policy) is list:
                self.input_fields[key] = ComboItem(frame, policy, value)
            else:
                self.input_fields[key] = StrItem(frame, value)

            layout.addWidget(self.input_fields[key].widget)
        self.frame.setLayout(layout)

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
        self.widget.setText(str(value))

    def value(self):
        return int(self.widget.text())


class DoubleItem(InputItem):
    def __init__(self, parent_frame, value):
        super().__init__(QLineEdit(parent_frame))
        self.widget.setValidator(QDoubleValidator())
        self.widget.setText(str(value))

    def value(self):
        return float(self.widget.text())

class StrItem(InputItem):
    def __init__(self, parent_frame, value, enabled = True):
        super().__init__(QLineEdit(parent_frame))
        self.widget.setValidator(QDoubleValidator())
        self.widget.setText(value)
        self.widget.setEnabled(enabled)

    def value(self):
        return str(self.widget.text())

class BoolItem(InputItem):
    def __init__(self, parent_frame, value):
        super().__init__(QCheckBox(parent_frame))
        self.widget.setChecked(value)

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
            "full_controller": "bool"
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
            "current_angle": "Поточний кут"
        }
        self.roller_policies = {
            "type": "immutable",
            "rotation_speed": "double",
            "min_angle": "double",
            "max_angle": "double",
            "current_angle": "double"
        }
        self.controller_settings_view = self.get_dictionary_settings(QFrame(self), self.controller_labels, self.controller_policies)
        self.switchboard_settings_view = self.get_dictionary_settings(QFrame(self), self.switchboard_labels, self.switchboard_policies)
        self.vroller_settings_view = None
        self.hroller_settings_view = None
        if "rollers" in self.settings:
            for roller in self.settings["rollers"]:
                if roller["type"] == "vertical":
                    self.vroller_settings_view = DictionarySettings(QFrame(self), self.roller_labels, roller, self.roller_policies)
                elif roller["type"] == "horizontal":
                    self.hroller_settings_view = DictionarySettings(QFrame(self), self.roller_labels, roller, self.roller_policies)

    def _new_roller(self, roller_type):
        roller_settings = {
            "type": roller_type,
            "rotation_speed": 0.0,
            "min_angle": 0.0,
            "max_angle": 0.0,
            "current_angle": 0.0
        }
        if roller_type == "vertical":
            self.vroller_settings_view = DictionarySettings(QFrame(self), self.roller_labels, roller_settings, self.roller_policies)
        else:
            self.hroller_settings_view = DictionarySettings(QFrame(self), self.roller_labels, roller_settings, self.roller_policies)

    def paintEvent(self, event):
        self.layout.addWidget(self.controller_settings_view.frame)
        self.layout.addWidget(self.switchboard_settings_view)
        if self.vroller_settings_view:
            self.layout.addWidget(self.vroller_settings_view.frame)
        else:
            add_button = QPushButton(self)
            add_button.setText("Додати вертикальний ролер")
            add_button.clicked.connect(lambda: self._new_roller("vertical"))
            self.layout.addWidget(add_button)
        if self.hroller_settings_view:
            self.layout.addWidget(self.hroller_settings_view)

        else:
            add_button = QPushButton(self)
            add_button.setText("Додати горизонтальний ролер")
            add_button.clicked.connect(lambda: self._new_roller("horizontal"))
            self.layout.addWidget(add_button)

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






