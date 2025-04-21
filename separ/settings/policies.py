import json
import time

from pearax import DATA_STORE_MAIL_INDEX

from separ.settings.dictionary import OptionalDoublePolicy, DoublePolicy


class AzimuthPolicy(OptionalDoublePolicy):
    def __init__(self, key: str, label: str, roller, ridge_angle_policy: DoublePolicy):
        super().__init__(key, label, True)
        self.roller = roller
        self.ridge_angle_policy = ridge_angle_policy
        self.__edit = False

    def __edit_save(self):
        self.__edit = True

    def _settings_value(self, default=None):
        try:
            result = self.roller.zero_azimuth
        except Exception:
            result = default
        return result

    def _settings_to_widget(self, value):
        if value is None:
            return None
        return value + self.roller.current_angle + self.roller.ridge_angle

    def _widget_to_settings(self, value):
        if value is None:
            return None
        return value - self.roller.current_angle - float(self.ridge_angle_policy.value())

    def create_widget(self, frame):
        widget = super().create_widget(frame)
        widget.textChanged.connect(self.__edit_save)
        return widget

    def save(self):
        assert not getattr(self.roller, "send_command", None) is None
        if self.__edit:
            val = self.value()
            if val is None:
                jcommand = {"cmd": "del", "key": "zero_azimuth"}
            else:
                jcommand = {"cmd": "set", "key": "zero_azimuth", "val": val}
            self.roller.send_command(json.dumps(jcommand).encode('utf-8'), DATA_STORE_MAIL_INDEX, time.time(), 0.7)
            time.sleep(0.1)#to be sure the command sent before pearax is closed