from separ.settings.dictionary import OptionalDoublePolicy, DoublePolicy


class AzimuthPolicy(OptionalDoublePolicy):
    def __init__(self, key: str, label: str, roller, ridge_angle_policy: DoublePolicy):
        super().__init__(key, label, False)
        self.roller = roller
        self.ridge_angle_policy = ridge_angle_policy

    def _settings_to_widget(self, value):
        if value is None:
            return None
        return value + self.roller.current_angle + self.roller.ridge_angle

    def _widget_to_settings(self, value):
        if value is None:
            return None
        return value - self.roller.current_angle - float(self.ridge_angle_policy.value())