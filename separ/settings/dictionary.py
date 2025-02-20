from PyQt5 import QtCore
from PyQt5.QtCore import QLocale, QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QFrame, QVBoxLayout, QPushButton, QComboBox, \
    QGroupBox



class DictionarySettings:
    def __init__(self, frame, json_settings, policies):
        self.frame = frame
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
        self.settings = json_settings
        self.layout = QGridLayout(frame)
        self.policies = policies

        for policy in policies:
            policy.apply(self)
            self.showPolicy(policy)

        self.frame.setLayout(self.layout)

    def showPolicy(self, policy):
        self.layout.addWidget(policy.getQLabel(), policy.index, 0)
        self.layout.addWidget(policy.getQWidget(), policy.index, 1)
        self.policies[policy.index] = policy

    def hidePolicy(self, policy):
        assert self.policies[policy.index] == policy
        self.layout.removeWidget(policy.getQLabel())
        self.layout.removeWidget(policy.getQWidget())
        self.policies[policy.index] = None


    def add_bottom_widget(self, widget):
        self.layout.addWidget(widget, len(self.labels), 0, 1, 2)


    def get_settings(self):
        settings = {}
        for policy in self.policies:
            if not policy is None:
                settings[policy.key] = policy.value()
        return settings

    def save_settings(self):
        self.settings = self.get_settings()




class SettingsComposer(QFrame):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame)
        self.settings = json_settings

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
    '''
    def get_dictionary_settings(self, frame, labels, policies, src=None):
        if src is None:
            src = self.settings
        settings = {}
        for key, label in labels.items():
            if key in src:
                settings[key] = src[key]
        return DictionarySettings(frame, labels, settings, policies)
    '''

class Policy:
    def __init__(self, key: str, index: int, label: str):
        self.key = key
        self.index = index
        self.label = label
        self.ds = None
        self.qWidget = None
        self.qLabel = None
        self.subp = []

    def addSubPolicy(self, policy, val):
        self.subp.append((policy, val))

    def normalizeSubPolicies(self):
        for policy, val in self.subp:
            if self.value() == val:
                policy.ds.showPolicy(policy)
            else:
                policy.ds.hidePolicy(policy)

    def create_widget(self):
        pass

    def apply(self, ds: DictionarySettings):
        self.ds = ds
        self.qWidget = self.create_widget()
        self.qLabel = QLabel(self.ds.frame)
        self.qLabel.setText(self.label)

    def getQLabel(self):
        return self.qLabel

    def getQWidget(self):
        return self.qWidget

    def value(self):
        pass


class IntPolicy(Policy):
    def __init__(self, key: str, index: int, label: str):
        super().__init__(key, index, label)

    def create_widget(self):
        widget = QLineEdit(self.ds.frame)
        widget.setValidator(QIntValidator())
        value = str(self.ds.settings[self.key] if self.key in self.ds.settings else 0)
        widget.setText(value)
        return widget

    def value(self):
        return int(self.qWidget.text())

class DoublePolicy(Policy):
    def __init__(self, key: str, index: int, label: str):
        super().__init__(key, index, label)

    def create_widget(self):
        widget = QLineEdit(self.ds.frame)
        validator = QDoubleValidator()
        locale = QtCore.QLocale(QLocale.English, QLocale.UnitedStates)
        validator.setLocale(locale)
        widget.setValidator(validator)
        value = str(self.ds.settings[self.key] if self.key in self.ds.settings else 0.0)
        widget.setText(value)
        return widget

    def value(self):
        return float(self.qWidget.text())

class StrPolicy(Policy):
    def __init__(self, key: str, index: int, label: str, enabled = True):
        super().__init__(key, index, label)
        self.enabled = enabled

    def create_widget(self):
        widget = QLineEdit(self.ds.frame)
        widget.setValidator(QIntValidator())
        value = str(self.ds.settings[self.key] if self.key in self.ds.settings else "")
        widget.setText(value)
        widget.setEnabled(self.enabled)
        return widget

    def value(self):
        return str(self.qWidget.text())

class PinsPolicy(StrPolicy):
    def __init__(self, key: str, index: int, label: str):
        super().__init__(key, index, label)

    def create_widget(self):
        widget = QLineEdit(self.ds.frame)
        regex = QRegExp("[0-9]{1,3}([ ]*,[ ]*[0-9]{1,3})*")
        validator = QRegExpValidator(regex, self.qWidget)
        value = str(self.ds.settings[self.key] if  self.key in self.ds.settings else "")
        widget.setText(value)
        return widget

class BoolPolicy(Policy):
    def __init__(self, key: str, index: int, label: str):
        super().__init__(key, index, label)

    def create_widget(self):
        widget = QCheckBox(self.ds.frame)
        widget.setChecked(self.ds.settings[self.key] if self.key in self.ds.settings else False)
        return widget

    def value(self):
        return self.getQWidget().isChecked()

class ComboPolicy(Policy):
    def __init__(self, key: str, index: int, label: str, items, enabled = True):
        super().__init__(key, index, label)
        self.items = items
        self.enabled = enabled

    def create_widget(self):
        combo = QComboBox(self.ds.frame)
        combo.addItems(self.items)
        if self.key in self.ds.settings:
            combo.setCurrentText(self.ds.settings[self.key])
        combo.setEnabled(self.enabled)
        return combo

    def value(self):
        return self.getQWidget().currentText()







