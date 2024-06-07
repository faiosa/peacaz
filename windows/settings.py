from tkinter import Toplevel, Label, Entry, Button
from utils.position_window import position_window_at_centre


class SettingsWindow:
    def __init__(self, master, controller_values, angle_selector):
        self.master = master
        self.controller_values = controller_values
        self.angle_selector = angle_selector
        self.window = Toplevel(master)
        self.window.geometry(
            position_window_at_centre(self.window, width=500, height=300)
        )
        self.window.title("Налаштування")

        self.controller_list = {}
        self.create_main_interface()

    def create_main_interface(self):
        row = 0
        for index, values in self.controller_values.items():
            self.add_controller_row(index, values, row)
            row += 1

        self.add_button = Button(
            self.window, text="Додати контролер", command=self.add_controller
        )
        self.add_button.grid(row=row, column=0, columnspan=3, pady=5)

    def add_controller_row(self, index, values, row):
        label = Label(self.window, text=f"{values['name']}")
        label.grid(row=row, column=0, padx=10, pady=5)

        settings_button = Button(
            self.window,
            text="Налаштування",
            command=lambda idx=index: self.open_settings(idx),
        )
        settings_button.grid(row=row, column=1, padx=10, pady=5)

        delete_button = Button(
            self.window,
            text="Видалити",
            command=lambda idx=index: self.remove_controller(idx),
        )
        delete_button.grid(row=row, column=2, padx=10, pady=5)

        self.controller_list[index] = {
            "label": label,
            "settings_button": settings_button,
            "delete_button": delete_button,
        }

    def open_settings(self, index):
        ControllerSettingsWindow(
            self.master, index, self.controller_values, self.angle_selector
        )

    def add_controller(self):
        index = str(len(self.controller_values) + 1)
        self.controller_values[index] = {
            "name": f"Контролер {index}",
            "rotation_speed_horizontally": 0.0,
            "rotation_speed_vertically": 0.0,
            "serial_port": "",
            "current_degree": 0.0,
            "current_tilt": 0.0,
            "min_angle": 0,
            "max_angle": 360,
            "min_tilt": 0,
            "max_tilt": 90,
        }
        self.angle_selector.show_controllers_frame()
        self.refresh_interface()

    def remove_controller(self, index):
        if index in self.controller_values:
            del self.controller_values[index]
            self.angle_selector.show_controllers_frame()
            self.refresh_interface()

    def refresh_interface(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_main_interface()


class ControllerSettingsWindow:
    def __init__(self, master, index, controller_values, angle_selector):
        self.master = master
        self.index = index
        self.controller_values = controller_values
        self.angle_selector = angle_selector
        self.window = Toplevel(master)
        self.window.geometry(
            position_window_at_centre(self.window, width=600, height=400)
        )
        self.window.title(f"Налаштування контролера {index}")
        self.window.bind("<Return>", lambda event: self.save_settings())

        self.create_settings_interface()

    def create_settings_interface(self):
        values = self.controller_values[self.index]

        Label(self.window, text="Назва контролера:").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.name_entry = Entry(self.window)
        self.name_entry.insert(0, values["name"])
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.window, text="Швидкість повертання горизонтально (градус/c):").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.rotation_speed_horizontally_entry = Entry(self.window)
        self.rotation_speed_horizontally_entry.insert(
            0, values["rotation_speed_horizontally"]
        )
        self.rotation_speed_horizontally_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.window, text="Швидкість повертання вертикально (градус/c):").grid(
            row=2, column=0, padx=10, pady=5
        )
        self.rotation_speed_vertically_entry = Entry(self.window)
        self.rotation_speed_vertically_entry.insert(
            0, values["rotation_speed_vertically"]
        )
        self.rotation_speed_vertically_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.window, text="Серійний порт:").grid(row=3, column=0, padx=10, pady=5)
        self.serial_port_entry = Entry(self.window)
        self.serial_port_entry.insert(0, values["serial_port"])
        self.serial_port_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.window, text="Мін. кут:").grid(row=4, column=0, padx=10, pady=5)
        self.min_angle_entry = Entry(self.window)
        self.min_angle_entry.insert(0, values["min_angle"])
        self.min_angle_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(self.window, text="Макс. кут:").grid(row=5, column=0, padx=10, pady=5)
        self.max_angle_entry = Entry(self.window)
        self.max_angle_entry.insert(0, values["max_angle"])
        self.max_angle_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(self.window, text="Мін. кут нахилу:").grid(
            row=6, column=0, padx=10, pady=5
        )
        self.min_tilt_entry = Entry(self.window)
        self.min_tilt_entry.insert(0, values["min_tilt"])
        self.min_tilt_entry.grid(row=6, column=1, padx=10, pady=5)

        Label(self.window, text="Макс. кут нахилу:").grid(
            row=7, column=0, padx=10, pady=5
        )
        self.max_tilt_entry = Entry(self.window)
        self.max_tilt_entry.insert(0, values["max_tilt"])
        self.max_tilt_entry.grid(row=7, column=1, padx=10, pady=5)

        save_button = Button(self.window, text="Зберегти", command=self.save_settings)
        save_button.grid(row=8, column=0, columnspan=2, pady=10)

    def save_settings(self):
        name = self.name_entry.get()
        rotation_speed_horizontally = float(
            self.rotation_speed_horizontally_entry.get()
        )
        rotation_speed_vertically = float(self.rotation_speed_vertically_entry.get())
        serial_port = self.serial_port_entry.get()
        min_angle = int(self.min_angle_entry.get())
        max_angle = int(self.max_angle_entry.get())
        min_tilt = int(self.min_tilt_entry.get())
        max_tilt = int(self.max_tilt_entry.get())

        self.controller_values[self.index] = {
            "name": name,
            "rotation_speed_horizontally": rotation_speed_horizontally,
            "rotation_speed_vertically": rotation_speed_vertically,
            "serial_port": serial_port,
            "current_degree": self.controller_values[self.index]["current_degree"],
            "current_tilt": self.controller_values[self.index]["current_tilt"],
            "min_angle": min_angle,
            "max_angle": max_angle,
            "min_tilt": min_tilt,
            "max_tilt": max_tilt,
        }

        self.angle_selector.update_controller_values(self.controller_values)
        self.window.destroy()
