from separ.settings.dictionary import DoublePolicy

class SetCurrentAnglePolicy(DoublePolicy):
    def __init__(self, label, roller):
        super().__init__("set_stepper_cur_angle", label, True)
        self.roller = roller
        self.edit = False

    def __edit_save(self):
        self.edit = True

    def _initial_value(self, default=None):
        try:
            result = self.roller.current_angle
        except Exception:
            result = default
        return str(result)

    def create_widget(self, frame):
        widget = super().create_widget(frame)
        widget.textChanged.connect(self.__edit_save)
        return widget

    def save(self):
        assert not getattr(self.roller, "set_cur_angle_command", None) is None
        if self.edit:
            self.roller.set_cur_angle_command(self.value())