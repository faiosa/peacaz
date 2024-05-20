from tkinter import Toplevel, Label, Entry, Button


class SettingsWindow:
    def __init__(self, master, controller_values, angle_selector):
        self.master = master
        self.controller_values = controller_values
        self.angle_selector = angle_selector
        self.window = Toplevel(master)

        self.window.title("Налаштування")

        self.controller_entries = {}
        self.delete_buttons = {}

        self.create_controller_entries()

        self.add_button = Button(
            self.window, text="Додати контролер", command=self.add_controller
        )
        self.add_button.grid(row=len(self.controller_values) + 1, columnspan=2, pady=5)

        save_button = Button(self.window, text="Зберегти", command=self.save_settings)
        save_button.grid(row=len(self.controller_values) + 6, columnspan=8, pady=10)

    def create_controller_entries(self):
        self.controller_entries = {}
        self.delete_buttons = {}
        for i, (index, values) in enumerate(self.controller_values.items()):
            self.add_controller_entry(index, values, i)

    def add_controller_entry(self, index, values, row):
        Label(self.window, text=f"Назва контролера {index}:").grid(
            row=row, column=0, padx=10, pady=5
        )
        name_entry = Entry(self.window)
        name_entry.insert(0, values["name"])
        name_entry.grid(row=row, column=1, padx=10, pady=5)

        Label(self.window, text="Швидкість повертання (градус/c ):").grid(
            row=row, column=2, padx=10, pady=5
        )
        rotation_speed_entry = Entry(self.window)
        rotation_speed_entry.insert(0, values["rotation_speed"])
        rotation_speed_entry.grid(row=row, column=3, padx=10, pady=5)

        Label(self.window, text="Серійний порт:").grid(
            row=row, column=4, padx=10, pady=5
        )
        port_entry = Entry(self.window)
        port_entry.insert(0, values["serial_port"])
        port_entry.grid(row=row, column=5, padx=10, pady=5)

        Label(self.window, text="Мін. кут:").grid(row=row, column=6, padx=10, pady=5)
        min_entry = Entry(self.window)
        min_entry.insert(0, values["min_angle"])
        min_entry.grid(row=row, column=7, padx=10, pady=5)

        Label(self.window, text="Макс. кут:").grid(row=row, column=8, padx=10, pady=5)
        max_entry = Entry(self.window)
        max_entry.insert(0, values["max_angle"])
        max_entry.grid(row=row, column=9, padx=10, pady=5)

        delete_button = Button(
            self.window,
            text="Видалити",
            command=lambda idx=index: self.remove_controller(idx),
        )
        delete_button.grid(row=row, column=10, padx=10, pady=5)

        self.controller_entries[index] = {
            "name": name_entry,
            "serial_port": port_entry,
            "rotation_speed": rotation_speed_entry,
            "min_angle": min_entry,
            "max_angle": max_entry,
        }
        self.delete_buttons[index] = delete_button

    def save_settings(self):
        updated_controller_values = {}
        for i, (index, _) in enumerate(self.controller_values.items()):
            name = self.controller_entries[index]["name"].get()
            rotation_speed = float(
                self.controller_entries[index]["rotation_speed"].get()
            )
            serial_port = self.controller_entries[index]["serial_port"].get()
            min_angle = int(self.controller_entries[index]["min_angle"].get())
            max_angle = int(self.controller_entries[index]["max_angle"].get())
            updated_controller_values[index] = {
                "name": name,
                "rotation_speed": rotation_speed,
                "serial_port": serial_port,
                "current_degree": self.controller_values[index]["current_degree"],
                "current_azimuth": self.controller_values[index]["current_azimuth"],
                "min_angle": min_angle,
                "max_angle": max_angle,
            }

        self.angle_selector.update_controller_values(updated_controller_values)
        self.window.destroy()

    def add_controller(self):
        index = str(len(self.controller_values) + 1)
        self.controller_values[index] = {
            "name": "",
            "rotation_speed": 0.0,
            "serial_port": "",
            "current_degree": 0.0,
            "current_azimuth": 0.0,
            "min_angle": 0,
            "max_angle": 360,
        }
        self.add_controller_entry(
            index, self.controller_values[index], len(self.controller_values) - 1
        )
        self.window.destroy()
        SettingsWindow(self.master, self.controller_values, self.angle_selector)

    def remove_controller(self, index):
        if index in self.controller_values:
            del self.controller_values[index]
            for entry in self.controller_entries[index].values():
                entry.destroy()
            self.delete_buttons[index].destroy()
            del self.controller_entries[index]
            del self.delete_buttons[index]
            self.save_settings()
            self.window.destroy()
            SettingsWindow(self.master, self.controller_values, self.angle_selector)
