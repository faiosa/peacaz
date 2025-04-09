from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QGridLayout, QLabel

from separ.settings.dictionary import DoublePolicy, DictionarySettings


def _patrol_policies():
    return [
        DoublePolicy("min_angle", "Мін кут"),
        DoublePolicy("max_angle", "Макс кут"),
        DoublePolicy("rotation_speed", "Швидкість патрулювання (градус/с)")
    ]


class PatrolDialog(QDialog):
    def __init__(self, roller_view):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.roller_view = roller_view

        settings = self.__patrol_settings()
        policies = _patrol_policies()
        self.dictionary = DictionarySettings("Параметри патрулювання", self.layout, settings, policies)
        self.dictionary.showView()


        self.layout.addWidget(self.__buttons_frame())



    def __patrol_settings(self):
        return {
            "min_angle": self.roller_view.roller.min_angle,
            "max_angle": self.roller_view .roller.max_angle,
            "rotation_speed": self.roller_view.roller.rotation_speed
        }

    def __do_patrol(self):
        patrol_settings = self.dictionary.get_settings()
        self.roller_view.turn_ptz_patrol(patrol_settings)
        self.close()

    def __buttons_frame(self):
        buttons_frame = QFrame(self)
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_frame.setLayout(buttons_layout)

        ok_button = QPushButton(buttons_frame)
        ok_button.setText("патрулювати")
        ok_button.clicked.connect(self.__do_patrol)

        cancel_button = QPushButton(buttons_frame)
        cancel_button.setText("відмінити")
        cancel_button.clicked.connect(self.close)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        return buttons_frame

