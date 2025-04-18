from separ.settings.dictionary import OptionalDoublePolicy


class AzimuthPolicy(OptionalDoublePolicy):
    def __init__(self, key: str, label: str, roller):
        super().__init__(key, label, False)
        self.roller = roller

    def _settings_to_widget(self, value):
        return value

    def _widget_to_settings(self, value):
        return value