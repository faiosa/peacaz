from tkinter import Toplevel, Label, Entry, Button


class SettingsWindow:
    def __init__(self, master, controller_values, angle_selector):
        self.master = master
        self.controller_values = controller_values
        self.angle_selector = angle_selector
        self.window = Toplevel(master)
        self.window.title("Налаштування")

        # Create labels and entry fields for controller values
        self.controller_labels = []
        self.serial_port_entries = []
        self.min_angle_entries = []
        self.max_angle_entries = []
        for i, (index, values) in enumerate(self.controller_values.items()):
            Label(self.window, text=f"Назва контролера {index}:").grid(
                row=i, column=0, padx=10, pady=5
            )
            name_entry = Entry(self.window)
            name_entry.insert(0, values["name"])
            name_entry.grid(row=i, column=1, padx=10, pady=5)
            self.controller_labels.append(name_entry)

            Label(self.window, text="Серійний порт:").grid(
                row=i, column=2, padx=10, pady=5
            )
            port_entry = Entry(self.window)
            port_entry.insert(0, values["serial_port"])
            port_entry.grid(row=i, column=3, padx=10, pady=5)
            self.serial_port_entries.append(port_entry)

            Label(self.window, text="Мін. кут:").grid(row=i, column=4, padx=10, pady=5)
            min_entry = Entry(self.window)
            min_entry.insert(0, values["min_angle"])
            min_entry.grid(row=i, column=5, padx=10, pady=5)
            self.min_angle_entries.append(min_entry)

            Label(self.window, text="Макс. кут:").grid(row=i, column=6, padx=10, pady=5)
            max_entry = Entry(self.window)
            max_entry.insert(0, values["max_angle"])
            max_entry.grid(row=i, column=7, padx=10, pady=5)
            self.max_angle_entries.append(max_entry)

        # Create a button to save settings
        save_button = Button(self.window, text="Зберегти", command=self.save_settings)
        save_button.grid(row=len(self.controller_values) * 2, columnspan=8, pady=10)

    def save_settings(self):
        # Update controller values from entry fields
        updated_controller_values = {}
        for i, (index, _) in enumerate(self.controller_values.items()):
            name = self.controller_labels[i].get()
            serial_port = self.serial_port_entries[i].get()
            min_angle = int(self.min_angle_entries[i].get())
            max_angle = int(self.max_angle_entries[i].get())
            updated_controller_values[index] = {
                "name": name,
                "serial_port": serial_port,
                "current_degree": self.controller_values[index]["current_degree"],
                "current_azimuth": self.controller_values[index]["current_azimuth"],
                "min_angle": min_angle,
                "max_angle": max_angle,
            }

        # Update AngleSelector with new controller values
        self.angle_selector.update_controller_values(updated_controller_values)

        # Close the settings window
        self.window.destroy()
