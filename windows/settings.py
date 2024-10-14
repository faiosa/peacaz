import tkinter as tk
from tkinter import (
    ttk,
    Toplevel,
    Label,
    Entry,
    Button,
    LabelFrame,
    Scrollbar,
    BooleanVar,
    Checkbutton,
)
from utils.position_window import position_window_at_centre
from utils.settings import load_settings, save_settings


class GlobalSettings:
    def __init__(self, master):
        self.frame = LabelFrame(master, text="Налаштування")
        self.frame.pack(fill="x", padx=10, pady=10)

        self.settings = load_settings()
        self.create_interface()

    def create_interface(self):
        Label(self.frame, text="Тема інтерфейсу:").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.theme_var = tk.StringVar(value=self.settings["global_settings"]["theme"])
        theme_menu = ttk.Combobox(
            self.frame, textvariable=self.theme_var, values=["Світла", "Темна"]
        )
        theme_menu.grid(row=0, column=1, padx=10, pady=5)
        self.theme_var.trace_add("write", self.save_settings)

        Label(self.frame, text="Мова інтерфейсу:").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.language_var = tk.StringVar(
            value=self.settings["global_settings"]["language"]
        )
        language_menu = ttk.Combobox(
            self.frame,
            textvariable=self.language_var,
            values=["Англійська", "Українська"],
        )
        language_menu.grid(row=1, column=1, padx=10, pady=5)
        self.language_var.trace_add("write", self.save_settings)

    def save_settings(self, *args):
        self.settings["global_settings"]["theme"] = self.theme_var.get()
        self.settings["global_settings"]["language"] = self.language_var.get()

        save_settings(self.settings)


class Controllers:
    def __init__(self, master, controller_values, controllers):
        self.controller_values = controller_values
        self.controllers = controllers

        self.frame = ttk.Frame(master)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_interface()

    def create_interface(self):
        self.controller_list = {}
        self.controller_frame = LabelFrame(self.frame, text="Контролери")
        self.controller_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollbar = Scrollbar(self.controller_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(
            self.controller_frame, yscrollcommand=self.scrollbar.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.scrollbar.config(command=self.canvas.yview)

        self.create_controller_interface()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_controller_interface(self):
        row = 0
        for index, values in self.controller_values.items():
            self.add_controller_row(index, values, row)
            row += 1

        self.add_button = Button(
            self.inner_frame, text="Додати контролер", command=self.add_controller
        )
        self.add_button.grid(row=row, column=0, columnspan=3, pady=5)

    def add_controller_row(self, index, values, row):
        label = Label(self.inner_frame, text=f"{values['name']}")
        label.grid(row=row, column=0, padx=10, pady=5)

        settings_button = Button(
            self.inner_frame,
            text="Налаштування",
            command=lambda idx=index: self.open_settings(idx),
        )
        settings_button.grid(row=row, column=1, padx=10, pady=5)

        delete_button = Button(
            self.inner_frame,
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
            self.frame.master, index, self.controller_values, self.controllers
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
            "switchboard_pins": "",
            "switchboard_serial_port": "",
            "full_controller": False,
        }
        self.controllers.show_controllers_frame()
        self.controllers.update_controller_values(self.controller_values)
        self.refresh_interface()

    def remove_controller(self, index):
        if index in self.controller_values:
            del self.controller_values[index]
            self.controllers.update_controller_values(self.controller_values)
            self.controllers.show_controllers_frame()
            self.refresh_interface()

    def refresh_interface(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.create_controller_interface()


class Switchboard:
    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.settings = load_settings()

        self.create_interface()

    def create_interface(self):
        switchboard_frame = LabelFrame(self.frame, text="Налаштування комутатора")
        switchboard_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Label(switchboard_frame, text="Серійний порт:").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.serial_port_entry = Entry(switchboard_frame)
        self.serial_port_entry.grid(row=0, column=1, padx=10, pady=5)
        self.serial_port_entry.insert(
            0, self.settings["switchboard_settings"]["serial_port"]
        )
        self.serial_port_entry.bind("<KeyRelease>", self.save_settings)

        # Add additional settings as needed

    def save_settings(self, event):
        self.settings["switchboard_settings"]["serial_port"] = (
            self.serial_port_entry.get()
        )
        save_settings(self.settings)


class SettingsWindow:
    def __init__(self, master, controller_values, controllers):
        self.master = master
        self.controller_values = controller_values
        self.controllers = controllers
        self.window = Toplevel(master)
        self.window.geometry(
            position_window_at_centre(self.window, width=800, height=600)
        )
        self.window.title("Налаштування")

        self.global_settings = GlobalSettings(self.window)
        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self.window)
        tab_control.pack(expand=1, fill="both")

        # Controllers Tab
        controllers_tab = ttk.Frame(tab_control)
        tab_control.add(controllers_tab, text="Контролери")
        self.controllers = Controllers(
            controllers_tab, self.controller_values, self.controllers
        )

        # Switchboard Tab
        # switchboard_tab = ttk.Frame(tab_control)
        # tab_control.add(switchboard_tab, text="Комутатор")
        # self.switchboard = Switchboard(switchboard_tab)


class ControllerSettingsWindow:
    def __init__(self, master, index, controller_values, controllers):
        self.master = master
        self.index = index
        self.controller_values = controller_values
        self.controllers = controllers
        self.window = Toplevel(master)
        self.window.geometry(
            position_window_at_centre(self.window, width=600, height=500)
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

        Label(self.window, text="Піни комутатора").grid(
            row=8, column=0, padx=10, pady=5
        )
        self.switchboard_pins_entry = Entry(self.window)
        self.switchboard_pins_entry.insert(0, values["switchboard_pins"])
        self.switchboard_pins_entry.grid(row=8, column=1, padx=10, pady=5)

        Label(self.window, text="Серійний порт комутатора:").grid(
            row=9, column=0, padx=10, pady=5
        )
        self.switchboard_serial_port_entry = Entry(self.window)
        self.switchboard_serial_port_entry.insert(0, values["switchboard_serial_port"])
        self.switchboard_serial_port_entry.grid(row=9, column=1, padx=10, pady=5)

        Label(self.window, text="Великий контролер:").grid(
            row=10, column=0, padx=10, pady=5
        )

        # Add checkbox for full controller
        self.full_controller_var = BooleanVar(
            value=values.get("full_controller", False)
        )
        self.full_controller_checkbox = Checkbutton(
            self.window, text="", variable=self.full_controller_var
        )
        self.full_controller_checkbox.grid(row=10, column=1, columnspan=2, pady=5)

        save_button = Button(self.window, text="Зберегти", command=self.save_settings)
        save_button.grid(row=11, column=0, columnspan=2, pady=10)

    def save_settings(self):
        self.controller_values[self.index] = {
            "name": self.name_entry.get(),
            "rotation_speed_horizontally": float(
                self.rotation_speed_horizontally_entry.get()
            ),
            "rotation_speed_vertically": float(
                self.rotation_speed_vertically_entry.get()
            ),
            "serial_port": self.serial_port_entry.get(),
            "current_degree": self.controller_values[self.index]["current_degree"],
            "current_tilt": self.controller_values[self.index]["current_tilt"],
            "min_angle": int(self.min_angle_entry.get()),
            "max_angle": int(self.max_angle_entry.get()),
            "min_tilt": int(self.min_tilt_entry.get()),
            "max_tilt": int(self.max_tilt_entry.get()),
            "switchboard_pins": self.switchboard_pins_entry.get(),
            "switchboard_serial_port": self.switchboard_serial_port_entry.get(),
            "full_controller": self.full_controller_var.get(),
        }

        self.controllers.update_controller_values(self.controller_values)
        self.window.destroy()
