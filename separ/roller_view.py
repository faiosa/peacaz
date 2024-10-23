from tkinter import ttk
from tkinter import *
from config import ui
from tkinter import Frame, messagebox
from utils.path import resource_path
import math


class BaseRollerView:
    def __init__(self, roller, frame):
        self.roller = roller
        self.frame = frame
        self.moving_id = None
        Label(
            frame,
            text="Введіть бажаний кут",
            #fill="#000000",
            font=("AnonymousPro Regular", 14)
        ).grid(column=0, row=0, columnspan=2)
        self.desired_angle_entry = Entry(
            frame,
            bd=1,
            relief="ridge",
            font=("AnonymousPro Regular", 14),
            bg="#FFFFFF",
            fg="black"
        )
        self.desired_angle_entry.grid(column=0, row=1, columnspan=2)
        self.desired_angle_entry.bind("<Return>", self.set_desired_angle)

    def set_desired_angle(self, event=None):
        try:
            desired_angle = float(self.desired_angle_entry.get())
            if self.roller.current_angle < desired_angle:
                self.turn_ptz_increase(desired_angle)
            else:
                self.turn_ptz_decrease(desired_angle)
            self.frame.focus()

        except ValueError:
            messagebox.showwarning("Warning", "Введіть коректне число")


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
            self.moving_id = None
            self.enable_buttons()

    def turn_ptz_increase(self, target_angle=360.0):
        self.roller.start_increase_angle()
        if self.roller.is_moving_increase:
            self.disable_buttons()
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
            self.moving_id = None
            self.enable_buttons()

    def turn_ptz_decrease(self, target_angle=-360.0):
        self.roller.start_decrease_angle()
        if self.roller.is_moving_decrease:
            self.disable_buttons()
            self.check_ptz_decrease(target_angle)


    def stop_ptz(self):
        self.roller.ptz_turn_stop()
        self.update_roller_view()
        if self.moving_id:
            self.frame.after_cancel(self.moving_id)
            self.moving_id = None
            self.enable_buttons()

    def update_roller_view(self):
        pass

    def disable_buttons(self):
        self.desired_angle_entry.config(state="disabled")

    def enable_buttons(self):
        self.desired_angle_entry.config(state="normal")

class RollerViewVertical(BaseRollerView):
    def __init__(self, roller, frame):
        super().__init__(roller, frame)
        self.slider_marker = None
        self.slider_canvas = Canvas(
            frame,
            width=60,
            height=250,
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
        slider_height = 250
        for i in range(-9, 10):
            y = slider_height / 2 - (i * slider_height / 20)
            self.slider_canvas.create_line(35, y, 45, y, fill="black")
            self.slider_canvas.create_text(
                15, y, text=f"{i * 10}", font=("AnonymousPro Regular", 12)
            )

    def draw_slider_marker(self):
        if self.slider_marker:
            self.slider_canvas.delete(self.slider_marker)
        slider_height = 250
        # Initial marker
        #diff = self.roller.max_angle - self.roller.min_angle
        center_y = slider_height / 2 - 12.5 * self.roller.current_angle / 10
        self.slider_marker = self.slider_canvas.create_oval(
            35, center_y - 5, 45, center_y + 5, fill="black"
        )

class RollerViewHorizontal(BaseRollerView):
    def __init__(self, roller, frame):
        super().__init__(roller, frame)

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

