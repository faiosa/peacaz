import math
import time
import os
import sys
from tkinter import (
    Button,
    Canvas,
    Entry,
    Label,
    OptionMenu,
    PhotoImage,
    StringVar,
    Tk,
    messagebox,
)

import ptz_controller
from config.ptz_controls_config import RIGHT, ROTATION_SPEED
from utils.controllers import (
    get_controller_id_by_name,
    get_controller_serial_by_name,
    get_controller_min_angle_by_name,
    get_controller_max_angle_by_name,
    get_rotation_speed_by_name,
)
from utils.settings import load_settings, save_settings
from utils.controls import disable_buttons, enable_buttons
from windows.settings import SettingsWindow
from windows.restore import RestorationProgressWindow
from utils.position_window import position_window_at_centre


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class AngleSelector(Canvas):
    def __init__(self, master, size=200, **kwargs):
        super().__init__(master, width=400, height=750, bg="#FFFFFF", bd=0, **kwargs)

        # Load settings at the beginning of the program
        self.settings = load_settings()
        self.restore_window = RestorationProgressWindow(master)

        self.size = size
        self.x = 400
        self.y = 750
        self.previous_angle = 0
        self.angle = 0
        self.arrow_length = size // 2 - 30
        self.arrow = None
        self.bind("<Button-1>", self._set_angle)
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

        self.controller_menu = OptionMenu(
            master,
            self.selected_controller,
            *[value["name"] for value in self.controller_values.values()],
            command=self.switch_controller,
        )
        self.controller_menu.config(
            bg="#FFFFFF",
            fg="black",
            font=("AnonymousPro Regular", 14),
        )
        self.controller_menu.place(x=120, y=30)

        self.desired_degree_entry = Entry(
            master,
            bd=1,
            relief="ridge",
            font=("AnonymousPro Regular", 14),
            bg="#FFFFFF",
            fg="black",
        )
        self.desired_degree_entry.place(x=100, y=120, width=200, height=30)
        self.desired_degree_entry.bind("<Return>", self.set_desired_degree)

        self.create_text(
            200.0,
            100.0,
            text="Введіть бажаний кут",
            fill="#000000",
            font=("AnonymousPro Regular", 14),
        )

        self.turn_left_image = PhotoImage(file=resource_path("assets\\turn_left.png"))
        self.turn_left_button = Button(
            image=self.turn_left_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.turn_ptz_left(self.selected_controller.get()),
            relief="flat",
        )
        self.turn_left_button.place(x=60.0, y=600.0, width=50, height=50)

        self.turn_right_image = PhotoImage(file=resource_path("assets\\turn_right.png"))
        self.turn_right_button = Button(
            image=self.turn_right_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.turn_ptz_right(self.selected_controller.get()),
            relief="flat",
        )
        self.turn_right_button.place(x=290.0, y=600.0, width=50, height=50)

        self.stop_image = PhotoImage(file=resource_path("assets\\stop.png"))
        self.stop_button = Button(
            image=self.stop_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.stop_ptz(self.selected_controller.get()),
            relief="flat",
        )
        self.stop_button.place(x=175.0, y=600.0, width=50, height=50)

        self.restore_defaults_button = Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.restore_defaults(self.selected_controller.get()),
            text="Відновити початкові значення",
            bg="#FFFFFF",
        )
        self.restore_defaults_button.place(x=76.0, y=680.0, width=250.0, height=33.0)
        self.current_degree_label = Label(
            master,
            bg="#FFFFFF",
            fg="black",
            text="Поточний кут: 0.00",
            font=("AnonymousPro Regular", 14),
            bd=1,
        )

        self.current_degree_label.place(x=100, y=550, width=200, height=30)
        self.update_callbacks.append(self.update_current_degree_text)

        self.settings_image = PhotoImage(file=resource_path("assets\\settings.png"))
        self.settings_button = Button(
            image=self.settings_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_settings_window,
            relief="flat",
        )
        self.settings_button.place(x=370.0, y=723.0, width=24.0, height=24.0)
        self.switch_controller(self.selected_controller.get())

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

    def restore_defaults(self, controller_name: str):
        self.restore_window.start()

        serial_port = get_controller_serial_by_name(
            controller_name, self.controller_values
        )
        max_angle = get_controller_max_angle_by_name(
            controller_name, self.controller_values
        )
        message = ptz_controller.restore_defaults(serial_port, max_angle)
        self.update_current_degree_text(0)
        self.angle = 0
        self.previous_angle = 0
        self.draw_arrow()
        messagebox.showinfo("Success", message)

        self.restore_window.stop()

    def turn_ptz_left(self, event=None):
        if self.is_moving:
            return
        else:
            self.is_moving = True
            disable_buttons(self)

            rotation_speed = get_rotation_speed_by_name(
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
            disable_buttons(self)
            rotation_speed = get_rotation_speed_by_name(
                self.selected_controller_name, self.controller_values
            )
            serial_port = get_controller_serial_by_name(
                self.selected_controller_name, self.controller_values
            )
            ptz_controller.turn_ptz_right(serial_port)
            self.start_continuous_update(rotation_speed)
            self.is_moving = True

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
        center_y = self.y // 2
        radius = self.size // 2 - 40

        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            self.create_oval(x, y, x + 1, y + 1, fill="black")

    def draw_marks(self):
        center_x = self.x // 2
        center_y = self.y // 2
        radius = self.size // 2 - 20

        for angle in range(0, 360, 10):
            adjusted_angle = angle - 90  # Adjust angle to make 0 at the top
            x = center_x + radius * math.cos(math.radians(adjusted_angle))
            y = center_y + radius * math.sin(math.radians(adjusted_angle))
            self.create_text(x, y, text=str(angle), fill="black")

    def draw_arrow(self):
        if self.arrow:
            self.delete(self.arrow)
        center_x = self.x // 2
        center_y = self.y // 2
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
        self.current_degree_label.config(text=f"Поточний кут: {angle:.2f}")
        # Update the controller value with the new degree
        controller_id = get_controller_id_by_name(
            self.selected_controller_name, self.controller_values
        )

        self.controller_values[controller_id]["current_degree"] = float(f"{angle:.2f}")
        self.settings["controller_values"][controller_id]["current_degree"] = float(
            f"{angle:.2f}"
        )
        save_settings(self.settings)

    def set_desired_degree(self, event=None):
        try:
            desired_degree = float(self.desired_degree_entry.get())
            self.turn(desired_degree)

        except ValueError:
            messagebox.showwarning("Warning", "Введіть коректне число")

    def turn(self, desired_degree: float):
        serial_port = get_controller_serial_by_name(
            self.selected_controller_name, self.controller_values
        )
        rotate_direction = ptz_controller.get_rotate_direction(
            desired_degree, self.previous_angle
        )
        rotate_time = ptz_controller.get_rotate_time(
            desired_degree, self.previous_angle, rotate_direction
        )
        time_start = time.time()
        time_end = time_start + rotate_time
        rotation_speed = get_rotation_speed_by_name(
            self.selected_controller_name, self.controller_values
        )

        ptz_controller.turn_ptz(rotate_direction, serial_port)
        self.start_continuous_update(
            rotation_speed if rotate_direction == RIGHT else -rotation_speed,
            time_end=time_end,
        )

    def start_continuous_update(self, rotation_speed, time_end=None):
        # Start continuous update with the given direction (positive or negative rotation_speed)
        self.continuous_update_helper(rotation_speed=rotation_speed, time_end=time_end)

    def stop_continuous_update(self):
        # Stop continuous update by canceling the scheduled updates
        if hasattr(self, "continuous_update_id") and self.continuous_update_id:
            self.after_cancel(self.continuous_update_id)
            self.continuous_update_id = None

    def continuous_update_helper(self, rotation_speed, time_end=None):
        # Calculate the time passed since the last update (in seconds)
        time_passed = 1 / 100  # 60 updates per second

        # Update arrow position continuously with the given rotation speed
        new_angle = self.angle + (rotation_speed * time_passed)
        self.angle = new_angle

        controller_min_angle = get_controller_min_angle_by_name(
            self.selected_controller_name, self.controller_values
        )
        controller_max_angle = get_controller_max_angle_by_name(
            self.selected_controller_name, self.controller_values
        )

        if new_angle <= controller_min_angle or new_angle >= controller_max_angle:
            self.stop_ptz()
            messagebox.showwarning("Warning", "Граничний кут досягнуто")
            self.master.focus_force()
        else:
            self.draw_arrow()
            self.update_current_degree_text(new_angle)
            # Schedule the next update
            self.continuous_update_id = self.after(
                10, self.continuous_update_helper, rotation_speed, time_end
            )
            self.previous_angle = new_angle

        if time_end and time.time() >= time_end:
            self.stop_ptz()


window = Tk()
app_icon = PhotoImage(file=resource_path(".\\assets\\icon.png"))
window.iconphoto(False, app_icon)
window.geometry(position_window_at_centre(window, width=400, height=750))
window.title("PTZ Controller")
window.configure(bg="#FFFFFF")

angle_selector = AngleSelector(window, size=350)
angle_selector.place(x=0, y=0)

# Add bindings to control ptz with arrows
window.bind("<Left>", angle_selector.turn_ptz_left)
window.bind("<Right>", angle_selector.turn_ptz_right)
window.bind("<End>", angle_selector.stop_ptz)

window.resizable(False, False)
window.mainloop()
