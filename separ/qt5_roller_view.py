from PyQt5 import QtGui, Qt
from PyQt5.QtCore import QPointF, QTimer
from PyQt5.QtGui import QDoubleValidator, QFont, QPainter, QPen, QBrush, QStaticText, QPolygon, QPolygonF, QIcon

from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame, QWidget, QPushButton
import math

class BaseRollerView:
    def __init__(self, roller, frame, grid, controller_view, index):
        self.roller = roller
        self.frame = frame
        self.controller_view = controller_view
        self.index = index
        self.canvas_height = 232
        #self.canvas_height = 200

        self.roller_font = QFont("AnonymousPro Regular", 9)

        start_row_index = 5 if self.roller.is_vertical else 1
        angle_direction_txt = "вертикальний" if self.roller.is_vertical else "горизонтальний"

        current_angle_label_text = QLabel(self.frame)
        current_angle_label_text.setText(f"Поточний  {angle_direction_txt}  кут:")
        current_angle_label_text.setFont(self.roller_font)
        grid.addWidget(current_angle_label_text, start_row_index, 0)#{self.roller.current_angle:.0f}

        self.current_angle_label = QLabel(self.frame)
        self.current_angle_label.setText(f"{self.roller.current_angle:.1f}")
        self.current_angle_label.setFont(self.roller_font)
        grid.addWidget(self.current_angle_label, start_row_index, 1)

        input_label = QLabel(self.frame)
        input_label.setText(f"Встановіть {angle_direction_txt} кут:")
        input_label.setFont(self.roller_font)
        grid.addWidget(input_label, start_row_index + 1, 0)

        self.input_field = QLineEdit(self.frame)
        self.input_field.setValidator(QDoubleValidator())
        self.input_field.returnPressed.connect(self.set_desired_angle)
        self.input_field.setFont(self.roller_font)
        self.input_field.setFixedWidth(50)
        grid.addWidget(self.input_field, start_row_index + 1, 1)



    def set_desired_angle(self, event=None):
        try:
            desired_angle = float(self.input_field.text())
            self.roll_desired_angle(desired_angle)

        except ValueError:
            print("Введіть коректне число")
            #messagebox.showwarning("Warning", "Введіть коректне число")

    def roll_desired_angle(self, desired_angle):
        if self.roller.current_angle < desired_angle:
            self.turn_ptz_increase(desired_angle)
        else:
            self.turn_ptz_decrease(desired_angle)

    def check_ptz_increase(self, target_angle=360.0):
        self.roller.check_increase_angle(target_angle)
        self.update_roller_view()
        if self.roller.is_moving_increase:
            QTimer.singleShot(
                100,
                lambda: self.check_ptz_increase(target_angle)
            )
        else:
            self.__on_finish_move()

    def turn_ptz_increase(self, target_angle=360.0):
        self.roller.start_increase_angle()
        if self.roller.is_moving_increase:
            self.__on_start_move()
            self.check_ptz_increase(target_angle)

    def check_ptz_decrease(self, target_angle=-360.0):
        self.roller.check_decrease_angle(target_angle)
        self.update_roller_view()
        if self.roller.is_moving_decrease:
            QTimer.singleShot(
                100,
                lambda: self.check_ptz_decrease(target_angle)
            )
        else:
            self.__on_finish_move()

    def turn_ptz_decrease(self, target_angle=-360.0):
        self.roller.start_decrease_angle()
        if self.roller.is_moving_decrease:
            self.__on_start_move()
            self.check_ptz_decrease(target_angle)

    def is_roller_moving(self):
        return self.roller.is_moving_increase or self.roller.is_moving_decrease


    def stop_ptz(self):
        if self.is_roller_moving():
            self.roller.ptz_turn_stop()
            self.update_roller_view()
            self.__on_finish_move()

    def __on_start_move(self):
        self.controller_view.roller_start(self.index)
        self.disable_buttons()

    def __on_finish_move(self):
        self.enable_buttons()
        self.controller_view.roller_finish(self.index)

    def update_roller_view(self):
        self.current_angle_label.setText(f"{self.roller.current_angle:.1f}")

    def disable_buttons(self):
        self.input_field.setEnabled(False)

    def enable_buttons(self):
        self.input_field.setEnabled(True)

class RollerViewVertical(BaseRollerView):
    def __init__(self, roller, frame, grid, controller_view, index):
        super().__init__(roller, frame, grid, controller_view, index)

        self.slider_height = self.canvas_height
        self.slider_width = 60

        self.slider_frame = SliderCanvas(frame, roller)
        self.slider_frame.setFixedWidth(self.slider_width)
        self.slider_frame.setFixedHeight(self.slider_height)

        grid.addWidget(self.slider_frame, 0, 2, 8, 1)

        self.turn_up_button = QPushButton(self.frame)
        self.turn_up_button.setIcon(QIcon("assets/turn_up.png"))
        self.turn_up_button.clicked.connect(lambda: self.turn_ptz_increase())
        grid.addWidget(self.turn_up_button, 3, 6)

        self.turn_down_button = QPushButton(self.frame)
        self.turn_down_button.setIcon(QIcon("assets/turn_down.png"))
        self.turn_down_button.clicked.connect(lambda: self.turn_ptz_decrease())
        grid.addWidget(self.turn_down_button, 5, 6)


    def update_roller_view(self):
        super().update_roller_view()
        self.slider_frame.update()

    def disable_buttons(self):
        super().disable_buttons()
        self.turn_up_button.setEnabled(False)
        self.turn_down_button.setEnabled(False)

    def enable_buttons(self):
        super().enable_buttons()
        self.turn_up_button.setEnabled(True)
        self.turn_down_button.setEnabled(True)

class SliderCanvas(QFrame):
    def __init__(self, widget, roller):
        super().__init__(widget)
        self.roller = roller

    def paintEvent(self, event):
        def drawMark():
            mqp = QPainter()
            mqp.begin(self)
            mqp.setBrush(QBrush(Qt.QColor(5, 2, 2)))
            mheight = self.size().height()
            mcenter_y = mheight / 2 - (mheight / 20) * self.roller.current_angle / 10
            mdiff = height / 25
            mqp.drawEllipse(35, mcenter_y - mdiff / 2, mdiff, mdiff)
            mqp.end()

        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.QColor(5, 2, 2), 2)
        qp.setPen(pen)
        qp.setFont(QFont("AnonymousPro Regular", 9))

        height = self.size().height()

        for i in range(-9, 10):
            y = height // 2 - (i * height // 20)
            qp.drawLine(35, y, 45, y)
            qp.drawText(15, y + height // 60, f"{i * 10}")
        qp.end()
        drawMark()

class RollerViewHorizontal(BaseRollerView):
    def __init__(self, roller, frame, grid, controller_view, index):
        super().__init__(roller, frame, grid, controller_view, index)

        self.slider_height = self.canvas_height
        self.slider_width = self.canvas_height + 30

        self.canvas_frame = ArrowCanvas(frame, roller)
        self.canvas_frame.setFixedWidth(self.slider_width)
        self.canvas_frame.setFixedHeight(self.slider_height)

        grid.addWidget(self.canvas_frame, 0, 3, 8, 2)

        self.turn_left_button = QPushButton(self.frame)
        self.turn_left_button.setIcon(QIcon("assets/turn_left.png"))
        self.turn_left_button.clicked.connect(lambda: self.turn_ptz_decrease())
        grid.addWidget(self.turn_left_button, 4, 5)

        self.turn_right_button = QPushButton(self.frame)
        self.turn_right_button.setIcon(QIcon("assets/turn_right.png"))
        self.turn_right_button.clicked.connect(lambda: self.turn_ptz_increase())
        grid.addWidget(self.turn_right_button, 4, 7)

    def update_roller_view(self):
        super().update_roller_view()
        self.canvas_frame.update()


    def disable_buttons(self):
        super().disable_buttons()
        self.turn_right_button.setEnabled(False)
        self.turn_left_button.setEnabled(False)

    def enable_buttons(self):
        super().enable_buttons()
        self.turn_right_button.setEnabled(True)
        self.turn_left_button.setEnabled(True)

class ArrowCanvas(QFrame):
    def __init__(self, widget, roller):
        super().__init__(widget)
        self.roller = roller

    def paintEvent(self, event):
        def draw_direction():
            mqp = QPainter()
            mqp.begin(self)
            mpen = QPen(Qt.QColor(5, 2, 2), 2)
            mqp.setPen(mpen)
            mqp.setBrush(QBrush(Qt.QColor(5, 2, 2)))

            msize = self.size()

            mcenter_x = msize.width() // 2
            mcenter_y = msize.height() // 2
            marrow_length = msize.height() // 2 - 20
            madjusted_angle_rad = math.radians(self.roller.current_angle - 90)  # Adjust angle to make 0 at the top
            mx = mcenter_x + marrow_length * math.cos(madjusted_angle_rad)
            my = mcenter_y + marrow_length * math.sin(madjusted_angle_rad)
            #mqp.drawLine(mcenter_x, mcenter_y, mx, my)
            def draw_arrow(fx, fy, angle_diff, len_diff):
                angle_1 = madjusted_angle_rad + math.radians(angle_diff) + math.pi
                x_1 = fx + len_diff * math.cos(angle_1)
                y_1 = fy + len_diff * math.sin(angle_1)
                angle_2 = madjusted_angle_rad - math.radians(angle_diff) + math.pi
                x_2 = fx + len_diff * math.cos(angle_2)
                y_2 = fy + len_diff * math.sin(angle_2)
                polygon = QPolygonF()
                polygon.append(QPointF(fx, fy))
                polygon.append(QPointF(x_1, y_1))
                polygon.append(QPointF(mcenter_x, mcenter_y))
                polygon.append(QPointF(x_2, y_2))
                mqp.drawPolygon(polygon)
            draw_arrow(mx, my, 5, 105 * marrow_length // 100)
            mqp.end()

        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.QColor(5, 2, 2), 2)
        qp.setPen(pen)
        qp.setFont(QFont("AnonymousPro Regular", 10))
        size = self.size()
        center_x = size.width() // 2
        center_y = size.height() // 2
        radius = center_y - 15
        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            qp.drawEllipse(x, y, 3, 3)
            text = QStaticText(str(angle))
            tsize = text.size()
            tx = center_x + (radius + 2 + tsize.width() / 2) * math.cos(math.radians(adjusted_angle))
            ty = center_y + (radius + 2 + tsize.height()/ 2) * math.sin(math.radians(adjusted_angle))

            #qp.drawEllipse(tx, ty, 3, 3)
            qp.drawStaticText(tx - tsize.width() / 2, ty - tsize.height() / 2, text)
        qp.end()
        draw_direction()


