from PyQt5 import QtGui, Qt
from PyQt5.QtCore import QPointF, QTimer
from PyQt5.QtGui import QDoubleValidator, QFont, QPainter, QPen, QBrush, QStaticText, QPolygon, QPolygonF, QIcon

from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame, QWidget, QPushButton
import math
from pearax.func import func_logger

from separ.patrol_dialog import PatrolDialog


class BaseRollerView:
    def __init__(self, roller, frame, support_patrol = False):
        self.roller = roller
        self.frame = frame
        #self.controller_view = controller_view
        #self.index = index
        self.canvas_height = 232
        self.support_patrol = support_patrol
        #self.canvas_height = 200

        grid = frame.layout()

        self.roller_font = QFont("AnonymousPro Regular", 9)

        start_row_index = 5 if self.roller.is_vertical else 1
        angle_direction_txt = "Вертикальний" if self.roller.is_vertical else "Горизонтальний"

        angle_label_text = QLabel(self.frame)
        angle_label_text.setText(f"{angle_direction_txt}  кут")
        angle_label_text.setFont(self.roller_font)
        grid.addWidget(angle_label_text, start_row_index, 0, 1, 2)#{self.roller.current_angle:.0f}

        current_angle_label_text = QLabel(self.frame)
        current_angle_label_text.setText(f"поточний:")
        current_angle_label_text.setFont(self.roller_font)
        grid.addWidget(current_angle_label_text, start_row_index + 1, 0)  # {self.roller.current_angle:.0f}

        self.current_angle_label = QLabel(self.frame)
        self.current_angle_label.setText(f"{self.roller.current_angle:.1f}")
        self.current_angle_label.setFont(self.roller_font)
        grid.addWidget(self.current_angle_label, start_row_index + 1, 1)

        input_label = QLabel(self.frame)
        input_label.setText(f"встановити:")
        input_label.setFont(self.roller_font)
        grid.addWidget(input_label, start_row_index + 2, 0)

        self.input_field = QLineEdit(self.frame)
        self.input_field.setValidator(QDoubleValidator())
        self.input_field.returnPressed.connect(self.set_desired_angle)
        self.input_field.setFont(self.roller_font)
        self.input_field.setFixedWidth(50)
        grid.addWidget(self.input_field, start_row_index + 2, 1)

        if self.support_patrol:
            self.patrol_button = QPushButton(self.frame)
            self.patrol_button.setText("patrol")
            self.patrol_button.clicked.connect(self.show_patrol_dialog)
            grid.addWidget(self.patrol_button, 8, 3)
        else:
            self.patrol_button = None

    def show_patrol_dialog(self):
        dlg = PatrolDialog(self)
        dlg.exec_()


    def set_desired_angle(self, event=None):
        try:
            desired_angle = float(self.input_field.text())
            self.roll_desired_angle(desired_angle)

        except ValueError:
            print("Введіть коректне число")
            #messagebox.showwarning("Warning", "Введіть коректне число")

    def roll_desired_angle(self, desired_angle):
        self.roller.turn_ptz_move(desired_angle)
    '''
    def check_ptz_move(self, target_angle):
        self.roller.check_move_angle(target_angle)
        self.update_roller_view()
        if self.roller.is_moving():
            QTimer.singleShot(
                20,
                lambda: self.check_ptz_move(target_angle)
            )
        else:
            self.__on_finish_move()
    '''
    #Works for stepper only
    def turn_ptz_patrol(self, patrol_params):
        if self.support_patrol:
            if not self.roller.is_moving():
                self.roller.do_patrol(patrol_params['min_angle'], patrol_params['max_angle'], patrol_params['rotation_speed'])
                #self.check_move_started(patrol_params['min_angle'])
        else:
            func_logger.fatal("Patrol works with stepper roller only")
    '''
    def turn_ptz_move(self, target_angle):
        self.roller.start_move_angle(target_angle)
        self.check_move_started(target_angle)
    
    def check_move_started(self, target_angle):
        if self.roller.is_moving():
            self.__on_start_move()
            self.check_ptz_move(target_angle)
    
    def is_roller_moving(self):
        return self.roller.is_moving()
    '''

    def stop_ptz(self):
        self.roller.stop_ptz()

    def update_roller_view(self):
        self.current_angle_label.setText(f"{self.roller.current_angle:.1f}")

    def disable_buttons(self):
        self.input_field.setEnabled(False)
        if not self.patrol_button is None:
            self.patrol_button.setEnabled(False)

    def enable_buttons(self):
        self.input_field.setEnabled(True)
        if not self.patrol_button is None:
            self.patrol_button.setEnabled(True)

class RollerViewVertical(BaseRollerView):
    def __init__(self, roller, frame, support_patrol = False):
        super().__init__(roller, frame, support_patrol)

        self.slider_height = self.canvas_height
        self.slider_width = 60

        self.slider_frame = SliderCanvas(frame, self)
        self.slider_frame.setFixedWidth(self.slider_width)
        self.slider_frame.setFixedHeight(self.slider_height)

        grid = frame.layout()
        grid.addWidget(self.slider_frame, 0, 2, 8, 1)
        '''
        self.turn_up_button = QPushButton(self.frame)
        self.turn_up_button.setIcon(QIcon("assets/turn_up.png"))
        self.turn_up_button.clicked.connect(lambda: self.turn_ptz_increase(self.roller.max_angle))
        grid.addWidget(self.turn_up_button, 3, 6)

        self.turn_down_button = QPushButton(self.frame)
        self.turn_down_button.setIcon(QIcon("assets/turn_down.png"))
        self.turn_down_button.clicked.connect(lambda: self.turn_ptz_decrease(self.roller.min_angle))
        grid.addWidget(self.turn_down_button, 5, 6)
        '''
        #self.roller.check_move_started(None)

    def update_roller_view(self):
        super().update_roller_view()
        self.slider_frame.update()

    '''
    def disable_buttons(self):
        super().disable_buttons()
        self.turn_up_button.setEnabled(False)
        self.turn_down_button.setEnabled(False)

    def enable_buttons(self):
        super().enable_buttons()
        self.turn_up_button.setEnabled(True)
        self.turn_down_button.setEnabled(True)
    '''
class SliderCanvas(QFrame):
    def __init__(self, widget, roller_view):
        super().__init__(widget)
        self.roller_view = roller_view

    def paintEvent(self, event):
        def drawMark():
            mqp = QPainter()
            mqp.begin(self)
            mqp.setBrush(QBrush(Qt.QColor(5, 2, 2)))
            mheight = self.size().height()
            mcenter_y = mheight / 2 - (mheight / 20) * self.roller_view.roller.current_angle / 10
            mdiff = int(height / 25)
            mqp.drawEllipse(35, int(mcenter_y - mdiff / 2) , mdiff, mdiff)
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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.roller_view.roller.controller.is_moving():
            return
        height = self.size().height()
        dy = height / 2 - event.y()
        dangle = dy * 10 * 20 / height

        if dangle > self.roller_view.roller.max_angle:
            dangle = self.roller_view.roller.max_angle
        if dangle < self.roller_view.roller.min_angle:
            dangle = self.roller_view.roller.min_angle

        self.roller_view.input_field.setText(f"{dangle:.1f}")
        self.roller_view.roller.turn_ptz_move(dangle)

class RollerViewHorizontal(BaseRollerView):
    def __init__(self, roller, frame, support_patrol = False):
        super().__init__(roller, frame, support_patrol)

        self.slider_height = self.canvas_height
        self.slider_width = self.canvas_height + 30

        self.canvas_frame = ArrowCanvas(frame, self)
        self.canvas_frame.setFixedWidth(self.slider_width)
        self.canvas_frame.setFixedHeight(self.slider_height)

        start_canvas_col = 1 + len(self.roller.controller.rollers)
        grid = frame.layout()
        grid.addWidget(self.canvas_frame, 0, start_canvas_col, 8, 3)
        '''
        self.turn_left_button = QPushButton(self.frame)
        self.turn_left_button.setIcon(QIcon("assets/turn_left.png"))
        self.turn_left_button.clicked.connect(lambda: self.turn_ptz_decrease(self.roller.min_angle))
        grid.addWidget(self.turn_left_button, 4, 5)

        self.turn_right_button = QPushButton(self.frame)
        self.turn_right_button.setIcon(QIcon("assets/turn_right.png"))
        self.turn_right_button.clicked.connect(lambda: self.turn_ptz_increase(self.roller.max_angle))
        grid.addWidget(self.turn_right_button, 4, 7)
        '''
        #self.roller.check_move_started(None)

    def update_roller_view(self):
        super().update_roller_view()
        self.canvas_frame.update()

    '''
    def disable_buttons(self):
        super().disable_buttons()
        self.turn_right_button.setEnabled(False)
        self.turn_left_button.setEnabled(False)

    def enable_buttons(self):
        super().enable_buttons()
        self.turn_right_button.setEnabled(True)
        self.turn_left_button.setEnabled(True)
    '''
class ArrowCanvas(QFrame):
    def __init__(self, widget, roller_view):
        super().__init__(widget)
        self.roller_view = roller_view

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.roller_view.roller.controller.is_moving():
            return
        size = self.size()
        dx = event.x() - size.width() / 2
        dy = event.y() - size.height() / 2
        sin = dy / math.sqrt(dy * dy + dx * dx)
        trad = math.asin(sin)
        if dx < 0:
            if trad < 0:
                trad = -math.pi - trad
            else:
                trad = math.pi - trad

        trad = trad + math.pi / 2
        if trad > 2 * math.pi:
            trad = trad - 2 * math.pi
        if trad < 0:
            trad = trad + 2 * math.pi

        tangle = trad * 180 / math.pi
        self.roller_view.input_field.setText(f"{tangle:.1f}")
        self.roller_view.roller.turn_ptz_move(tangle)


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
            madjusted_angle_rad = math.radians(self.roller_view.roller.current_angle - 90)  # Adjust angle to make 0 at the top
            mx = int(mcenter_x + marrow_length * math.cos(madjusted_angle_rad))
            my = int(mcenter_y + marrow_length * math.sin(madjusted_angle_rad))
            mqp.drawLine(mcenter_x, mcenter_y, mx, my)
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
                #polygon.append(QPointF(mcenter_x, mcenter_y))
                polygon.append(QPointF(x_2, y_2))
                mqp.drawPolygon(polygon)
            draw_arrow(mx, my, 25, 10 * marrow_length // 100)
            mqp.end()

        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.QColor(5, 2, 2), 2)
        qp.setPen(pen)
        qp.setFont(QFont("AnonymousPro Regular", 9))
        size = self.size()
        center_x = size.width() // 2
        center_y = size.height() // 2
        radius = center_y - 15
        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = int(center_x + radius * math.cos(math.radians(adjusted_angle)))
            y = int(center_y + radius * math.sin(math.radians(adjusted_angle)))
            qp.drawEllipse(x, y, 3, 3)
            if angle % 30 == 0:
                text = QStaticText(str(angle))
                tsize = text.size()
                tx = center_x + (radius + 2 + tsize.width() / 2) * math.cos(math.radians(adjusted_angle))
                ty = center_y + (radius + 2 + tsize.height()/ 2) * math.sin(math.radians(adjusted_angle))

                #qp.drawEllipse(tx, ty, 3, 3)
                qp.drawStaticText( int(tx - tsize.width() / 2), int(ty - tsize.height() / 2), text)
        qp.end()
        draw_direction()


