from tkinter import (
    Frame,
    PhotoImage,
    Tk,
    ttk
)

from apps.controller import Controllers
from apps.switchboard import Switchboard
from utils.position_window import position_window_at_centre
from utils.path import resource_path
from config import ui
from utils.settings import *
from separ.Manager import Manager
from separ.ManagerView import ManagerView


def main():
    window = Tk()
    window.geometry(position_window_at_centre(window, width=825, height=730))
    window.title("PTZ Controller")
    window.configure(bg=ui.BG_COLOR)

    main_frame = Frame(window, bg=ui.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    json_settings = load_settings_from_file(SEPAR_SETTINGS_FILE)
    manager = Manager(json_settings)
    manager_view = ManagerView(manager, main_frame)

    # window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    main()
