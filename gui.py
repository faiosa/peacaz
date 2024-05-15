from tkinter import Tk, Canvas, Button, PhotoImage, Label, Entry
from pathlib import Path
import math
import ptz_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    "C:\ptz_controller-main\\build\\assets\\frame0"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class AngleSelector(Canvas):
    def __init__(self, master, size=200, **kwargs):
        super().__init__(master, width=size, height=size, bg="#FFFFFF", **kwargs)
        self.size = size
        self.previous_angle = 0
        self.angle = 0
        self.arrow_length = size // 2 - 5
        self.arrow = None
        self.bind("<Button-1>", self._set_angle)
        self.draw_circle()
        self.draw_marks()
        self.draw_arrow()
        self.update_callbacks = []

    def draw_circle(self):
        center_x = self.size // 2
        center_y = self.size // 2
        radius = self.size // 2 - 5

        for angle in range(0, 360, 10):
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            self.create_oval(x, y, x + 1, y + 1, fill="black")

    def draw_marks(self):
        center_x = self.size // 2
        center_y = self.size // 2
        radius = self.size // 2 - 20

        for angle in range(0, 360, 10):
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            self.create_text(x, y, text=str(angle), fill="black")

    def draw_arrow(self):
        if self.arrow:
            self.delete(self.arrow)
        center_x = self.size // 2
        center_y = self.size // 2
        angle_rad = math.radians(self.angle)
        x = center_x + self.arrow_length * math.cos(angle_rad)
        y = center_y + self.arrow_length * math.sin(angle_rad)
        self.arrow = self.create_line(center_x, center_y, x, y, arrow="last")
        self.update_labels()

    def _set_angle(self, event):
        center_x = self.size // 2
        center_y = self.size // 2
        dx = event.x - center_x
        dy = event.y - center_y
        self.angle = math.degrees(math.atan2(dy, dx))
        print(self.angle)
        self.draw_arrow()
        for callback in self.update_callbacks:
            callback(self.angle)

        ptz_controller.update_ptz_angle(self.angle, self.previous_angle)
        self.previous_angle = self.angle

    def update_labels(self):
        pass  # No need to update labels here


window = Tk()

window.geometry("386x832")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=832,
    width=386,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_text(
    119.0,
    13.0,
    anchor="nw",
    text="Select Controller",
    fill="#000000",
    font=("AnonymousPro Regular", 16),
)

canvas.create_rectangle(38.0, 50.0, 348.0, 234.0, fill="#FFFFFF", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat",
)
button_1.place(x=59.0, y=69.0, width=105.0, height=16.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat",
)
button_2.place(x=58.0, y=99.0, width=105.0, height=16.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
)
button_3.place(x=58.0, y=129.0, width=105.0, height=16.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
)
button_5.place(x=86.0, y=450.0, width=214.0, height=33.0)

angle_selector = AngleSelector(window, size=350)
angle_selector.place(x=18, y=320)


def update_current_degree_text(angle):
    current_degree_label.config(text=f"Current Degree: {angle:.2f}")


current_degree_label = Label(
    window,
    text="Current Degree: 0.00",
    font=("AnonymousPro Regular", 16),
    bg="#FFFFFF",
)
current_degree_label.place(x=100, y=250)
angle_selector.update_callbacks.append(update_current_degree_text)


def update_current_azimuth_text(angle):
    azimuth = (angle + 90) % 360  # Example calculation, adjust as needed
    current_azimuth_label.config(text=f"Current Azimuth: {azimuth:.2f}")


current_azimuth_label = Label(
    window,
    text="Current Azimuth: 90.00",
    font=("AnonymousPro Regular", 16),
    bg="#FFFFFF",
)
current_azimuth_label.place(x=100, y=280)
angle_selector.update_callbacks.append(update_current_azimuth_text)


button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
)
button_4.place(x=86.0, y=740.0, width=214.0, height=33.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
)
button_5.place(x=86.0, y=690.0, width=214.0, height=33.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat",
)
button_6.place(x=348.0, y=798.0, width=24.0, height=24.0)

desired_degree_entry = Entry(
    window,
    bd=2,
    relief="ridge",
    font=("AnonymousPro Regular", 16),
)
desired_degree_entry.place(x=290, y=250, width=50, height=30)


def set_desired_degree(event=None):
    try:
        desired_degree = float(desired_degree_entry.get())
        angle_selector.angle = desired_degree
        angle_selector.draw_arrow()
        update_current_degree_text(desired_degree)
        update_current_azimuth_text(desired_degree)
        ptz_controller.update_ptz_angle(desired_degree)
    except ValueError:
        pass  # Handle invalid input


desired_degree_entry.bind("<Return>", set_desired_degree)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
)
button_4.place(x=86.0, y=740.0, width=214.0, height=33.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
)
button_5.place(x=86.0, y=690.0, width=214.0, height=33.0)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat",
)
button_6.place(x=348.0, y=798.0, width=24.0, height=24.0)

window.resizable(False, False)
window.mainloop()
