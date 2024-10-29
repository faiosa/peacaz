from PyQt5 import QtGui, Qt
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QDoubleValidator, QFont, QPainter, QPen, QBrush, QStaticText, QPolygon, QPolygonF, QIcon

from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame, QWidget, QPushButton
import math


class BaseRollerView:
    def __init__(self, roller, frame, grid, controller_view, index):
        self.roller = roller
        self.frame = frame
        self.controller_view = controller_view
        self.index = index
        self.moving_id = None
        self.canvas_height = 252

        self.roller_font = QFont("AnonymousPro Regular", 12)

        start_row_index = 5 if self.roller.is_vertical else 1
        angle_direction_txt = "вертикальний" if self.roller.is_vertical else "горизонтальний"

        input_label = QLabel(self.frame)
        input_label.setText(f"Введіть бажаний {angle_direction_txt} кут")
        input_label.setFont(self.roller_font)
        grid.addWidget(input_label, start_row_index, 0)

        self.input_field = QLineEdit(self.frame)
        self.input_field.setValidator(QDoubleValidator())
        self.input_field.returnPressed.connect(self.qt5_set_desired_angle)
        self.input_field.setFont(self.roller_font)
        grid.addWidget(self.input_field, start_row_index + 1, 0)

        current_angle_label = QLabel(self.frame)
        current_angle_label.setText(f"Поточний {angle_direction_txt} кут: {self.roller.current_angle:.0f}")
        current_angle_label.setFont(self.roller_font)
        grid.addWidget(current_angle_label, start_row_index + 2, 0)

        stop_button = QPushButton(self.frame)
        stop_button.setIcon(QIcon("assets/stop.png"))
        stop_button.clicked.connect(lambda: self.stop_ptz())
        grid.addWidget(stop_button, 4, 4)

    def stop_ptz(self):
        print("stopping ptz")

    def qt5_set_desired_angle(self):
        desired_angle = self.input_field.text()
        print(f"disired angle is {desired_angle}")

    '''
    def set_desired_angle(self, event=None):
        try:
            desired_angle = float(self.desired_angle_entry.get())
            self.roll_desired_angle(desired_angle)
            self.frame.focus()

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
            self.moving_id = self.frame.after(
                100,
                self.check_ptz_increase,
                target_angle
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
            self.moving_id = self.frame.after(
                100,
                self.check_ptz_decrease,
                target_angle
            )
        else:
            self.__on_finish_move()

    def turn_ptz_decrease(self, target_angle=-360.0):
        self.roller.start_decrease_angle()
        if self.roller.is_moving_decrease:
            self.__on_start_move()
            self.check_ptz_decrease(target_angle)


    def stop_ptz(self):
        self.roller.ptz_turn_stop()
        self.update_roller_view()
        if self.moving_id:
            self.frame.after_cancel(self.moving_id)
            self.__on_finish_move()

    def __on_start_move(self):
        self.controller_view.roller_start(self.index)
        self.disable_buttons()

    def __on_finish_move(self):
        self.moving_id = None
        self.enable_buttons()
        self.controller_view.roller_finish(self.index)

    def update_roller_view(self):
        self.current_angle_label.config(text=f"Поточний кут: {self.roller.current_angle:.0f}")

    def disable_buttons(self):
        self.desired_angle_entry.config(state="disabled")

    def enable_buttons(self):
        self.desired_angle_entry.config(state="normal")
    '''
class RollerViewVertical(BaseRollerView):
    def __init__(self, roller, frame, grid, controller_view, index):
        super().__init__(roller, frame, grid, controller_view, index)

        self.slider_height = self.canvas_height
        self.slider_width = 60



        self.slider_frame = SliderCanvas(frame, roller)
        self.slider_frame.setFixedWidth(self.slider_width)
        self.slider_frame.setFixedHeight(self.slider_height)

        grid.addWidget(self.slider_frame, 0, 1, 8, 1)

    '''
        button_frame = Frame(frame, bg="#FFFFFF")
        self.turn_up_image = PhotoImage(file=resource_path("assets/turn_up.png"))
        self.turn_up_button = Button(
            button_frame,
            image=self.turn_up_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_increase,
            relief="flat",
        )
        self.turn_up_button.grid(column=0, row=0, padx=20, pady=20)

        self.stop_image = PhotoImage(file=resource_path("assets/stop.png"))
        self.stop_button = Button(
            button_frame,
            image=self.stop_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop_ptz,
            relief="flat",
        )
        self.stop_button.grid(column=0, row=1, padx=20, pady=20)

        self.turn_down_image = PhotoImage(file=resource_path("assets/turn_down.png"))
        self.turn_down_button = Button(
            button_frame,
            image=self.turn_down_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_decrease,
            relief="flat",
        )
        self.turn_down_button.grid(column=0, row=2, padx=20, pady=20)
        button_frame.grid(column=1, row=2)

    def update_roller_view(self):
        super().update_roller_view()
        self.draw_slider_marker()

    def disable_buttons(self):
        super().disable_buttons()
        self.turn_up_button.config(state="disabled")
        self.turn_down_button.config(state="disabled")

    def enable_buttons(self):
        super().enable_buttons()
        self.turn_up_button.config(state="normal")
        self.turn_down_button.config(state="normal")

    

    def disable_all_buttons(self):
        self.disable_buttons()
        self.stop_button.config(state="disabled")

    def enable_all_buttons(self):
        self.enable_buttons()
        self.stop_button.config(state="normal")
    '''

class SliderCanvas(QFrame):
    def __init__(self, widget, roller):
        super().__init__(widget)
        self.roller = roller

    def paintEvent(self, event):
        def drawMark():
            mqp = QPainter()
            mqp.begin(self)
            #mpen = QPen(Qt.QColor(5, 2, 2), 3)
            mqp.setBrush(QBrush(Qt.QColor(5, 2, 2)))
            #mqp.setPen(mpen)
            mheight = self.size().height()
            mcenter_y = mheight / 2 - (mheight / 20) * self.roller.current_angle / 10
            mdiff = height / 25
            mqp.drawEllipse(35, mcenter_y - mdiff / 2, mdiff, mdiff)
            mqp.end()

        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.QColor(5, 2, 2), 2)
        qp.setPen(pen)
        qp.setFont(QFont("AnonymousPro Regular", 10))

        height = self.size().height()

        for i in range(-9, 10):
            y = height / 2 - (i * height / 20)
            qp.drawLine(35, y, 45, y)
            qp.drawText(15, y + height / 60, f"{i * 10}")
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

        grid.addWidget(self.canvas_frame, 0, 2, 8, 1)
    '''
        self.arrow = None

        button_frame = Frame(frame, bg="#FFFFFF")

        self.turn_left_image = PhotoImage(file=resource_path("assets/turn_left.png"))
        self.turn_left_button = Button(
            button_frame,
            image=self.turn_left_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_decrease,
            relief="flat",
        )
        self.turn_left_button.grid(column=0, row=0, padx=20, pady=20)

        self.stop_image = PhotoImage(file=resource_path("assets/stop.png"))
        self.stop_button = Button(
            button_frame,
            image=self.stop_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop_ptz,
            relief="flat",
        )
        self.stop_button.grid(column=1, row=0, padx=20, pady=20)

        self.turn_right_image = PhotoImage(file=resource_path("assets/turn_right.png"))
        self.turn_right_button = Button(
            button_frame,
            image=self.turn_right_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_increase,
            relief="flat",
        )
        self.turn_right_button.grid(column=2, row=0, padx=20, pady=20)

        button_frame.grid(column=0, row=2, columnspan=2)

        self.circle_canvas = Canvas(
            frame,
            width=320,
            height=300,
            bg=ui.BG_COLOR,
            bd=1,
            highlightthickness=0,
            relief="ridge",
        )
        self.circle_canvas.grid(column=0, row=3, padx=20, pady=20)
        self.draw_circle()
        self.draw_marks()
        self.draw_arrow()

    def update_roller_view(self):
        super().update_roller_view()
        self.draw_arrow()

    def draw_circle(self):
        center_x = 160
        center_y = 150
        radius = 140

        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            self.circle_canvas.create_oval(x, y, x + 1, y + 1, fill="black")

    def draw_marks(self):
        center_x = 160
        center_y = 150
        radius = 140

        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            self.circle_canvas.create_text(
                x, y, text=str(angle), fill="black", font=("AnonymousPro Regular", 11)
            )

    def draw_arrow(self):
        if self.arrow:
            self.circle_canvas.delete(self.arrow)
        center_x = 160
        center_y = 150
        arrow_length = 130
        adjusted_angle_rad = math.radians(self.roller.current_angle - 90)  # Adjust angle to make 0 at the top
        x = center_x + arrow_length * math.cos(adjusted_angle_rad)
        y = center_y + arrow_length * math.sin(adjusted_angle_rad)
        self.arrow = self.circle_canvas.create_line(
            center_x, center_y, x, y, arrow="last", fill="black"
        )

    def disable_buttons(self):
        super().disable_buttons()
        self.turn_right_button.config(state="disabled")
        self.turn_left_button.config(state="disabled")

    def enable_buttons(self):
        super().enable_buttons()
        self.turn_right_button.config(state="normal")
        self.turn_left_button.config(state="normal")

    def disable_all_buttons(self):
        self.disable_buttons()
        self.stop_button.config(state="disabled")

    def enable_all_buttons(self):
        self.enable_buttons()
        self.stop_button.config(state="normal")
    '''

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
                polygon.append(QPointF(x_2, y_2))
                mqp.drawPolygon(polygon)
            draw_arrow(mx, my, 22, marrow_length / 10)
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

            qp.drawStaticText(tx - tsize.width() / 2, ty - tsize.height() / 2, text)
        qp.end()
        draw_direction()


