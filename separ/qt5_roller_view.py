from PyQt5.QtGui import QDoubleValidator, QFont

from config import ui
from utils.path import resource_path
import math
from PyQt5.QtWidgets import QLabel, QLineEdit


class BaseRollerView:
    def __init__(self, roller, frame, grid, controller_view, index):
        self.roller = roller
        self.frame = frame
        self.controller_view = controller_view
        self.index = index
        self.moving_id = None

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
    '''    
        self.slider_height = 352
        self.slider_marker = None
        
        self.slider_canvas = Canvas(
            frame,
            width=60,
            height=self.slider_height,
            bg=ui.BG_COLOR,
            bd=1,
            highlightthickness=0,
            relief="ridge",
        )
        self.slider_canvas.grid(column=0, row=2, padx=40, pady=40)
        self.draw_slider()
        self.draw_slider_marker()

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

    def draw_slider(self):
        self.slider_canvas.delete("all")
        #slider_height = 250
        for i in range(-9, 10):
            y = self.slider_height / 2 - (i * self.slider_height / 20)
            self.slider_canvas.create_line(35, y, 45, y, fill="black")
            self.slider_canvas.create_text(
                15, y, text=f"{i * 10}", font=("AnonymousPro Regular", 12)
            )

    def draw_slider_marker(self):
        if self.slider_marker:
            self.slider_canvas.delete(self.slider_marker)
        #slider_height = 250
        # Initial marker
        #diff = self.roller.max_angle - self.roller.min_angle
        center_y = self.slider_height / 2 - (self.slider_height / 20) * self.roller.current_angle / 10
        self.slider_marker = self.slider_canvas.create_oval(
            35, center_y - 5, 45, center_y + 5, fill="black"
        )

    def disable_all_buttons(self):
        self.disable_buttons()
        self.stop_button.config(state="disabled")

    def enable_all_buttons(self):
        self.enable_buttons()
        self.stop_button.config(state="normal")
    '''
class RollerViewHorizontal(BaseRollerView):
    def __init__(self, roller, frame, grid, controller_view, index):
        super().__init__(roller, frame, grid, controller_view, index)
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
