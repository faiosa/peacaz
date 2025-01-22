import math
import time
from tkinter import (
    Button,
    Canvas,
    Entry,
    Frame,
    Label,
    PhotoImage,
    StringVar,
    messagebox,
)

from config import ui
from utils import ptz_controller
from config.ptz_controls_config import (
    MAX_ANGLE_SETTING,
    MAX_TILT_SETTING,
    MIN_ANGLE_SETTING,
    MIN_TILT_SETTING,
    RIGHT,
    ROTATION_SPEED_VERTICALLY_SETTING,
)
from utils.controllers import (
    get_controller_id_by_name,
    get_controller_max_angle_by_name,
    get_controller_serial_by_name,
    get_controller_setting_by_name,
    get_rotation_speed_horizontally_by_name,
)
from utils.controls import disable_buttons, enable_buttons
from utils.path import resource_path
from utils.settings import load_settings, save_settings
from windows.restore import RestorationProgressWindow
from windows.settings import SettingsWindow


class Controllers(Canvas):
    def __init__(self, master, size=350, **kwargs):
        super().__init__(
            master,
            width=800,
            height=600,
            bg=ui.BG_COLOR,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            **kwargs,
        )

        # Load settings at the beginning of the program
        self.settings = load_settings()
        self.restore_window = RestorationProgressWindow(master)

        self.switchboard = None

        self.size = size
        self.x = 400
        self.y = 750
        self.angle = 0
        self.tilt_angle = 0
        self.previous_angle = 0
        self.previous_tilt = 0
        self.arrow = None
        self.arrow_length = size // 2 - 30
        # self.bind("<Button-1>", self._set_angle)
        self.draw_circle()
        self.draw_marks()
        self.draw_arrow()
        self.update_callbacks = []
        self.stop_turn = False
        self.time_start = time.time()
        self.is_moving = False

        self.controller_values = self.settings.get("controller_values", {})
        self.selected_controller = StringVar(master)
        self.selected_controller.set(self.controller_values["1"]["name"])
        self.selected_controller_name = self.selected_controller.get()

        self.desired_degree_entry = Entry(
            master,
            bd=1,
            relief="ridge",
            font=("AnonymousPro Regular", 14),
            bg="#FFFFFF",
            fg="black",
        )
        self.desired_degree_entry.place(x=100, y=99, width=200, height=30)
        self.desired_degree_entry.bind("<Return>", self.set_desired_degree)
        self.desired_degree_entry.bind("<FocusIn>", self.on_entry_focus)
        self.desired_degree_entry.bind("<FocusOut>", self.on_entry_focus_out)

        self.create_text(
            200.0,
            80.0,
            text="Введіть бажаний кут",
            fill="#000000",
            font=("AnonymousPro Regular", 14),
        )
        self.controllers_frame = Frame(master, bg="#FFFFFF")
        self.controllers_frame.place(x=450, y=70, width=330, height=300)

        self.turn_up_image = PhotoImage(file=resource_path("assets/turn_up.png"))
        self.turn_up_button = Button(
            image=self.turn_up_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_up,
            relief="flat",
        )
        self.turn_up_button.place(x=575.0, y=330.0, width=50, height=50)

        self.turn_down_image = PhotoImage(file=resource_path("assets/turn_down.png"))
        self.turn_down_button = Button(
            image=self.turn_down_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_down,
            relief="flat",
        )
        self.turn_down_button.place(x=575.0, y=470.0, width=50, height=50)

        self.turn_left_image = PhotoImage(file=resource_path("assets/turn_left.png"))
        self.turn_left_button = Button(
            image=self.turn_left_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_left,
            relief="flat",
        )
        self.turn_left_button.place(x=505.0, y=400.0, width=50, height=50)

        self.turn_right_image = PhotoImage(file=resource_path("assets/turn_right.png"))
        self.turn_right_button = Button(
            image=self.turn_right_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.turn_ptz_right,
            relief="flat",
        )
        self.turn_right_button.place(x=645.0, y=400.0, width=50, height=50)

        self.stop_image = PhotoImage(file=resource_path("assets/stop.png"))
        self.stop_button = Button(
            image=self.stop_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop_ptz,
            relief="flat",
        )
        self.stop_button.place(x=575.0, y=400.0, width=50, height=50)

        self.restore_defaults_button = Button(
            borderwidth=1,
            highlightthickness=0,
            command=lambda: self.restore_defaults(self.selected_controller.get()),
            text="Відновити початкові значення",
            bg="#FFFFFF",
        )
        self.restore_defaults_button.place(x=76.0, y=530.0, width=250.0, height=33.0)
        self.current_degree_label = Label(
            master,
            bg="#FFFFFF",
            fg="black",
            text="Поточний кут: 0.00",
            font=("AnonymousPro Regular", 14),
            bd=1,
        )

        self.current_degree_label.place(x=100, y=490, width=200, height=30)
        self.update_callbacks.append(self.update_current_degree_text)

        self.settings_image = PhotoImage(file=resource_path("assets/settings.png"))
        self.settings_button = Button(
            image=self.settings_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_settings_window,
            relief="flat",
        )
        self.settings_button.place(x=790.0, y=10.0, width=24.0, height=24.0)

        # Create slider canvas
        self.slider_canvas = Canvas(
            master,
            width=60,
            height=250,
            bg=ui.BG_COLOR,
            bd=1,
            highlightthickness=0,
            relief="ridge",
        )
        self.slider_canvas.place(x=380, y=190)
        self.draw_slider()
        self.current_slider_value = 0

        self.switch_controller(self.selected_controller.get())
        self.bind_controller_change()

    def draw_slider(self):
        self.slider_canvas.delete("all")
        slider_height = 250
        for i in range(-9, 10):
            y = slider_height / 2 - (i * slider_height / 20)
            self.slider_canvas.create_line(35, y, 45, y, fill="black")
            self.slider_canvas.create_text(
                15, y, text=f"{i * 10}", font=("AnonymousPro Regular", 12)
            )

        # Initial marker
        self.slider_marker = self.slider_canvas.create_oval(
            35, slider_height / 2 - 5, 45, slider_height / 2 + 5, fill="black"
        )

    def update_slider(self, value):
        self.slider_canvas.delete(self.slider_marker)
        slider_height = 250
        y = slider_height / 2 - (value / 90.0 * slider_height / 2)
        self.slider_marker = self.slider_canvas.create_oval(
            35, y - 5, 45, y + 5, fill="black"
        )

    def focus_widget(self, event=None) -> None:
        self.desired_degree_entry.focus()

    def open_settings_window(self):
        # Open the settings window
        SettingsWindow(self.master, self.controller_values, self)

    def update_controller_values(self, controller_values):
        # Update controller values
        self.controller_values = controller_values
        self.settings["controller_values"] = self.controller_values
        save_settings(self.settings)

    def switch_controller(self, controller_name):
        print("Switching to", controller_name)
        self.selected_controller_name = controller_name
        # Get values for the selected controller
        controller_id = get_controller_id_by_name(
            controller_name, self.controller_values
        )
        angle = self.controller_values[controller_id]["current_degree"]
        # Update labels with values for the selected controller
        self.update_current_degree_text(angle)
        self.angle = angle
        self.previous_angle = angle
        self.draw_arrow()

        tilt = self.controller_values[controller_id]["current_tilt"]
        self.update_current_tilt(tilt)
        self.tilt_angle = tilt
        self.previous_tilt = tilt
        self.update_slider(tilt)

        self.show_controllers_frame()
        if self.switchboard:
            self.switchboard.update_controller(controller_name)

    def bind_controller_change(self):
        """Bind controller change to keys 1 to 9"""
        for i in range(1, 10):  # Bind keys 1 to 9
            self.master.bind(f"{i}", self.handle_controller_change)

    def unbind_controller_change(self):  # TODO: Test this
        """Unbind controller change from keys 1 to 9"""
        for i in range(1, 10):  # Bind keys 1 to 9
            self.master.unbind(f"{i}")

    def handle_controller_change(self, event):
        """Handle controller change by pressing keys 1 to 9"""
        key = int(event.char)
        if key <= len(self.controller_values):
            controller_id = list(self.controller_values.keys())[key - 1]
            controller_name = self.controller_values[controller_id]["name"]
            self.switch_controller(controller_name)

    def show_controllers_frame(self):
        for widget in self.controllers_frame.winfo_children():
            widget.destroy()

        for controller_id, values in self.controller_values.items():
            frame = Frame(self.controllers_frame, bg="#f9f9f9", bd=2, relief="ridge")
            frame.pack(fill="x", pady=7, padx=5)

            if values["name"] == self.selected_controller_name:
                frame.config(bg="#d6d6d6")  # Highlight the selected controller

            frame.bind(
                "<Button-1>",
                lambda e, name=values["name"]: self.switch_controller(name),
            )

            name_label = Label(
                frame,
                text=f"{values['name']}",
                bg=frame["bg"],
                font=("AnonymousPro Regular", 12),
            )
            name_label.pack(side="left", padx=5)
            name_label.bind(
                "<Button-1>",
                lambda e, name=values["name"]: self.switch_controller(name),
            )

            degree_label = Label(
                frame,
                text=f"H:{values['current_degree']:.2f}°, V:{values['current_tilt']:.2f}°",
                bg=frame["bg"],
                font=("AnonymousPro Regular", 12),
            )
            degree_label.pack(side="right", padx=5)

    def restore_defaults(self, controller_name: str):
        self.restore_window.start()

        serial_port = get_controller_serial_by_name(
            controller_name, self.controller_values
        )
        max_angle = get_controller_max_angle_by_name(
            controller_name, self.controller_values
        )
        min_tilt = get_controller_setting_by_name(
            controller_name, self.controller_values, MIN_TILT_SETTING
        )
        max_tilt = get_controller_setting_by_name(
            controller_name, self.controller_values, MAX_TILT_SETTING
        )
        rotation_speed = get_rotation_speed_horizontally_by_name(
            controller_name, self.controller_values
        )
        tilt_speed = get_controller_setting_by_name(
            controller_name, self.controller_values, ROTATION_SPEED_VERTICALLY_SETTING
        )
        message = ptz_controller.restore_defaults(
            serial_port, max_angle, rotation_speed, min_tilt, max_tilt, tilt_speed
        )
        self.update_current_degree_text(0)
        self.angle = 0
        self.previous_angle = 0
        self.draw_arrow()

        self.update_current_tilt(min_tilt)
        self.tilt_angle = min_tilt
        self.previous_tilt = min_tilt  # TODO: move this to update_current_tilt func
        self.update_slider(min_tilt)

        self.show_controllers_frame()

        self.restore_window.stop()
        messagebox.showinfo("Success", message)
        self.master.focus_force()

    def handle_restore_defaults_bind(self, event=None):
        self.restore_defaults(self.selected_controller_name)

    def turn_ptz_up(self, event=None):
        if self.is_moving:
            return
        else:
            self.is_moving = True
            disable_buttons(self)

            rotation_speed = get_controller_setting_by_name(
                self.selected_controller_name,
                self.controller_values,
                ROTATION_SPEED_VERTICALLY_SETTING,
            )
            serial_port = get_controller_serial_by_name(
                self.selected_controller_name, self.controller_values
            )
            ptz_controller.turn_ptz_up(serial_port)
            self.start_continuous_update(rotation_speed, tilt=True)

    def turn_ptz_down(self, event=None):
        if self.is_moving:
            return
        else:
            self.is_moving = True
            disable_buttons(self)

            rotation_speed = get_controller_setting_by_name(
                self.selected_controller_name,
                self.controller_values,
                ROTATION_SPEED_VERTICALLY_SETTING,
            )
            serial_port = get_controller_serial_by_name(
                self.selected_controller_name, self.controller_values
            )
            ptz_controller.turn_ptz_down(serial_port)
            self.start_continuous_update(-rotation_speed, tilt=True)

    def turn_ptz_left(self, event=None):
        if self.is_moving:
            return
        else:
            self.is_moving = True
            disable_buttons(self)

            rotation_speed = get_rotation_speed_horizontally_by_name(
                self.selected_controller_name, self.controller_values
            )
            serial_port = get_controller_serial_by_name(
                self.selected_controller_name, self.controller_values
            )
            ptz_controller.turn_ptz_left(serial_port)
            self.start_continuous_update(-rotation_speed)

    def turn_ptz_right(self, event=None):
        if self.is_moving:
            return
        else:
            self.is_moving = True
            disable_buttons(self)

            rotation_speed = get_rotation_speed_horizontally_by_name(
                self.selected_controller_name, self.controller_values
            )
            serial_port = get_controller_serial_by_name(
                self.selected_controller_name, self.controller_values
            )
            ptz_controller.turn_ptz_right(serial_port)
            self.start_continuous_update(rotation_speed)

    def stop_ptz(self, event=None, time_end=None):
        self.is_moving = False
        enable_buttons(self)

        serial_port = get_controller_serial_by_name(
            self.selected_controller_name, self.controller_values
        )
        if time_end:
            if time_end <= time.time():
                print("Stopping PTZ with time")
                # Stop continuous update when the button is released
                self.stop_continuous_update()
                ptz_controller.stop_ptz(serial_port)
        else:
            print("Stopping PTZ")
            # Stop continuous update when the button is released
            self.stop_continuous_update()
            ptz_controller.stop_ptz(serial_port)

    def draw_circle(self):
        center_x = self.x // 2
        center_y = self.y // 2 - 60
        radius = self.size // 2 - 50

        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            self.create_oval(x, y, x + 1, y + 1, fill="black")

    def draw_marks(self):
        center_x = self.x // 2
        center_y = self.y // 2 - 60
        radius = self.size // 2 - 30

        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            self.create_text(
                x, y, text=str(angle), fill="black", font=("AnonymousPro Regular", 11)
            )

    def draw_arrow(self):
        if self.arrow:
            self.delete(self.arrow)
        center_x = self.x // 2
        center_y = self.y // 2 - 60
        adjusted_angle_rad = math.radians(
            self.angle - 90
        )  # Adjust angle to make 0 at the top
        x = center_x + self.arrow_length * math.cos(adjusted_angle_rad)
        y = center_y + self.arrow_length * math.sin(adjusted_angle_rad)
        self.arrow = self.create_line(
            center_x, center_y, x, y, arrow="last", fill="black"
        )
        self.update_labels()

    def _set_angle(self, event):
        center_x = self.x // 2
        center_y = self.y // 2
        dx = event.x - center_x
        dy = event.y - center_y
        angle = math.degrees(math.atan2(dy, dx))
        angle = (angle + 360) % 360  # Ensure angle is positive
        self.turn(angle)

    def update_labels(self):
        pass  # No need to update labels here

    def update_current_degree_text(self, angle):
        self.current_degree_label.config(text=f"Поточний кут: {angle:.0f}")
        # Update the controller value with the new degree
        controller_id = get_controller_id_by_name(
            self.selected_controller_name, self.controller_values
        )

        self.controller_values[controller_id]["current_degree"] = float(f"{angle:.2f}")
        self.settings["controller_values"][controller_id]["current_degree"] = float(
            f"{angle:.2f}"
        )
        save_settings(self.settings)
        self.show_controllers_frame()

    def update_current_tilt(self, angle):
        # self.current_tilt_label.config(text=f"Поточний кут: {angle:.0f}")
        # Update the controller value with the new degree
        controller_id = get_controller_id_by_name(
            self.selected_controller_name, self.controller_values
        )

        self.controller_values[controller_id]["current_tilt"] = float(f"{angle:.2f}")
        self.settings["controller_values"][controller_id]["current_tilt"] = float(
            f"{angle:.2f}"
        )
        save_settings(self.settings)
        self.show_controllers_frame()

    def on_entry_focus(self, event):
        self.unbind_controller_change()

    def on_entry_focus_out(self, event):
        self.bind_controller_change()

    def set_desired_degree(self, event=None):
        try:
            desired_degree = float(self.desired_degree_entry.get())
            self.turn(desired_degree)
            self.master.focus()

        except ValueError:
            messagebox.showwarning("Warning", "Введіть коректне число")

    def turn(self, desired_degree: float):
        serial_port = get_controller_serial_by_name(
            self.selected_controller_name, self.controller_values
        )
        rotate_direction = ptz_controller.get_rotate_direction(
            desired_degree, self.previous_angle
        )
        rotation_speed = get_rotation_speed_horizontally_by_name(
            self.selected_controller_name, self.controller_values
        )
        rotate_time = ptz_controller.get_rotate_time(
            desired_degree, self.previous_angle, rotate_direction, rotation_speed
        )
        time_start = time.time()
        time_end = time_start + rotate_time

        self.start_continuous_update(
            rotation_speed if rotate_direction == RIGHT else -rotation_speed,
            time_end=time_end,
        )
        ptz_controller.turn_ptz(rotate_direction, serial_port)

    def start_continuous_update(self, rotation_speed, time_end=None, tilt=False):
        # Start continuous update with the given direction (positive or negative rotation_speed)
        if tilt:
            min_angle_setting = MIN_TILT_SETTING
            max_angle_setting = MAX_TILT_SETTING
        else:
            min_angle_setting = MIN_ANGLE_SETTING
            max_angle_setting = MAX_ANGLE_SETTING
        controller_min_angle = get_controller_setting_by_name(
            self.selected_controller_name, self.controller_values, min_angle_setting
        )
        controller_max_angle = get_controller_setting_by_name(
            self.selected_controller_name, self.controller_values, max_angle_setting
        )

        self.continuous_update_helper(
            rotation_speed=rotation_speed,
            time_end=time_end,
            min_angle=controller_min_angle,
            max_angle=controller_max_angle,
            tilt=tilt,
        )

    def stop_continuous_update(self):
        # Stop continuous update by canceling the scheduled updates
        if hasattr(self, "continuous_update_id") and self.continuous_update_id:
            self.after_cancel(self.continuous_update_id)
            self.continuous_update_id = None

    def continuous_update_helper(
        self,
        rotation_speed,
        time_end=None,
        min_angle=0,
        max_angle=360,
        tilt=False,
    ):
        # Calculate the time passed since the last update (in seconds)
        time_passed = 1 / 10  # 10 updates per second

        if tilt:
            new_angle = self.tilt_angle + (rotation_speed * time_passed)
            if new_angle <= min_angle or new_angle >= max_angle:
                self.stop_ptz()
                messagebox.showwarning("Warning", "Граничний кут досягнуто")
                self.master.focus_force()
            else:
                self.tilt_angle = new_angle
                self.update_slider(new_angle)
                self.update_current_tilt(new_angle)
                self.previous_tilt = new_angle
                self.continuous_update_id = self.after(
                    100,
                    self.continuous_update_helper,
                    rotation_speed,
                    time_end,
                    min_angle,
                    max_angle,
                    tilt,
                )
        else:
            # Update arrow position continuously with the given rotation speed
            new_angle = self.angle + (rotation_speed * time_passed)
            if new_angle <= min_angle or new_angle >= max_angle:
                self.stop_ptz()
                messagebox.showwarning("Warning", "Граничний кут досягнуто")
                self.master.focus_force()
            else:
                self.angle = new_angle
                self.draw_arrow()
                self.update_current_degree_text(new_angle)
                self.previous_angle = new_angle
                self.continuous_update_id = self.after(
                    100,
                    self.continuous_update_helper,
                    rotation_speed,
                    time_end,
                    min_angle,
                    max_angle,
                    tilt,
                )

        if time_end and time.time() >= time_end:
            self.stop_ptz()
