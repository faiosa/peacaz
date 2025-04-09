from PyQt5 import QtCore
from PyQt5.QtCore import QLocale, QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QFrame, QVBoxLayout, QPushButton, QComboBox, \
    QGroupBox



class DictionarySettings:
    def __init__(self, title, parent_layout, json_settings, policies):
        self.title = title
        self.parent_layout = parent_layout

        self.settings = json_settings
        self.policies = policies

        for index in range(len(self.policies)):
            policy = self.policies[index]
            policy.ds = self
            policy.set_index(index)

        self.view = None
        self.need_refresh = False

    def showView(self):
        self.view = SettingsView(self.title)
        for policy in self.policies:
            if not policy is None:
                self.view.addPolicyWidget(policy)
        self.parent_layout.addWidget(self.view.frame)

    def refreshView(self):
        if self.need_refresh:
            self.settings = self.get_settings()
            new_view = SettingsView(self.title)
            for policy in self.policies:
                if not policy is None:
                    new_view.addPolicyWidget(policy)
            self.parent_layout.replaceWidget(self.view.frame, new_view.frame)

            self.view.frame.deleteLater()
            self.view.frame.setFixedWidth(0)
            self.view.frame.setFixedHeight(0)
            self.view.frame = None

            self.view = new_view
            self.need_refresh = False

    def normalizeSubPolicies(self):
        for index in range(len(self.policies)):
            if not self.policies[index] is None:
                self.policies[index].normalizeSubPolicies()

    def enablePolicy(self, policy):
        if self.policies[policy.index] is None:
            self.policies[policy.index] = policy
            self.need_refresh = True

    def disablePolicy(self, policy):
        if self.policies[policy.index] == policy:
            policy.disabled_value = policy.value()
            self.policies[policy.index] = None
            self.need_refresh = True


    def add_bottom_widget(self, widget):
        self.layout.addWidget(widget, len(self.labels), 0, 1, 2)


    def get_settings(self):
        settings = {}
        for policy in self.policies:
            if (not policy is None) and not policy.spec:
                settings[policy.key] = policy.value()
        return settings

    def save_settings(self):
        self.settings = self.get_settings()
        for policy in self.policies:
            if (not policy is None) and policy.spec:
                policy.save()

class SettingsView:
    def __init__(self, title):
        self.frame = QGroupBox(title)
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
        self.layout = QGridLayout(self.frame)
        self.frame.setLayout(self.layout)
        self.widgets = {}

    def addPolicyWidget(self, policy):
        qWidget = policy.create_widget(self.frame)
        qLabel = QLabel(self.frame)
        qLabel.setText(policy.label)
        self.widgets[policy.index] = qWidget
        self.layout.addWidget(qLabel, policy.index, 0)
        self.layout.addWidget(qWidget, policy.index, 1)


class Policy:
    def __init__(self, key: str, label: str, spec = False):
        self.key = key
        self.index = None
        self.label = label
        self.ds = None
        self.subp = []
        self.disabled_value = None
        self.spec = spec #means that policy value is not saved within tweak file, have its own save method

    def set_index(self, index):
        if self.index is None:
            self.index = index
        else:
            raise Exception("Policy index is already set")

    def addSubPolicy(self, policy, enable_val_list):
        self.subp.append((policy, enable_val_list))

    def normalizeSubPolicies(self, refresh_ds=[], do_refresh=True):
        for policy, enable_val_list in self.subp:
            if self.status() in enable_val_list:
                policy.ds.enablePolicy(policy)
            else:
                policy.ds.disablePolicy(policy)
            if not policy.ds in refresh_ds:
                refresh_ds.append(policy.ds)
            policy.normalizeSubPolicies(refresh_ds, do_refresh=False)
        if do_refresh:
            for ds in refresh_ds:
                ds.refreshView()

    def create_widget(self, frame):
        pass

    def __find_my_widget(self):
        if self.index in self.ds.view.widgets:
            return self.ds.view.widgets[self.index]
        else:
            return None

    def _widget_value(self, widget):
        pass

    def status(self):
        if self in self.ds.policies:
            return self.value()
        else:
            return "__disabled__"

    def value(self):
        widget = self.__find_my_widget()
        if widget is None:
            return self.disabled_value
        else:
            return self._widget_value(widget)

    def _initial_value(self, default = None): #used within create_widget to set initial value
        return str(self.ds.settings[self.key] if self.key in self.ds.settings else default)

    def save(self):
        assert self.spec #only specific policies has special way to be saved

class IntPolicy(Policy):
    def __init__(self, key: str, label: str):
        super().__init__(key, label)

    def create_widget(self, frame):
        widget = QLineEdit(frame)
        widget.setValidator(QIntValidator())
        value = self._initial_value(0)
        widget.setText(value)
        return widget

    def _widget_value(self, widget):
        return int(widget.text())

class DoublePolicy(Policy):
    def __init__(self, key: str, label: str, specific = False):
        super().__init__(key, label, specific)

    def create_widget(self, frame):
        widget = QLineEdit(frame)
        validator = QDoubleValidator()
        locale = QtCore.QLocale(QLocale.English, QLocale.UnitedStates)
        validator.setLocale(locale)
        widget.setValidator(validator)
        value = self._initial_value(0.0)
        widget.setText(value)
        return widget

    def _widget_value(self, widget):
        return float(widget.text())

class StrPolicy(Policy):
    def __init__(self, key: str, label: str, enabled = True):
        super().__init__(key, label)
        self.enabled = enabled

    def create_widget(self, frame):
        widget = QLineEdit(frame)
        value = self._initial_value("")
        widget.setText(value)
        widget.setEnabled(self.enabled)
        return widget

    def _widget_value(self, widget):
        return str(widget.text())

class RegExpPolicy(StrPolicy):
    def __init__(self, key: str, label: str, regex_str: str):
        super().__init__(key, label)
        self.regex_str = regex_str

    def create_widget(self, frame):
        widget = QLineEdit(self.ds.view.frame)
        regex = QRegExp(self.regex_str)
        validator = QRegExpValidator(regex, widget)
        widget.setValidator(validator)
        value = self._initial_value("")
        widget.setText(value)
        return widget

class PinsPolicy(RegExpPolicy):
    def __init__(self, key: str, label: str):
        super().__init__(key, label, "[0-9]{1,3}([ ]*,[ ]*[0-9]{1,3})*")

class IpHostPolicy(RegExpPolicy):
    def __init__(self, key: str, label: str):
        super().__init__(key, label, "^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$")

class BoolPolicy(Policy):
    def __init__(self, key: str, label: str):
        super().__init__(key, label)

    def create_widget(self, frame):
        widget = QCheckBox(self.ds.view.frame)
        widget.setChecked(self.ds.settings[self.key] if self.key in self.ds.settings else False)
        #widget.setChecked(self._initial_value(False))
        widget.stateChanged.connect(lambda idx: self.normalizeSubPolicies())
        return widget

    def _widget_value(self, widget):
        return widget.isChecked()

class ComboPolicy(Policy):
    def __init__(self, key: str, label: str, items, enabled = True):
        super().__init__(key, label)
        self.items = items
        self.enabled = enabled

    def create_widget(self, frame):
        combo = QComboBox(frame)
        combo.addItems(self.items)
        combo.setEnabled(self.enabled)
        if self.key in self.ds.settings:
            if self.ds.settings[self.key] in self.items:
                combo.setCurrentText(self.ds.settings[self.key])
        combo.currentIndexChanged.connect(lambda idx: self.normalizeSubPolicies())
        return combo

    def _widget_value(self, widget):
        return widget.currentText()


class SettingsComposer(QFrame):
    def __init__(self, parent_frame, json_settings):
        super().__init__(parent_frame)
        self.settings = json_settings

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)







