from tkinter import (
    Frame,
    PhotoImage,
    Tk,
)

from apps.controller import Controllers
from apps.switchboard import Switchboard
from utils.position_window import position_window_at_centre
from utils.path import resource_path
from config import ui


def main():
    window = Tk()
    window.geometry(position_window_at_centre(window, width=825, height=730))
    window.title("PTZ Controller")
    window.configure(bg=ui.BG_COLOR)

    main_frame = Frame(window, bg=ui.BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    controllers = Controllers(main_frame)
    controllers.grid(row=0, column=0, padx=10, pady=10)

    # Create the Switchboard and pass the controller values
    switchboard = Switchboard(main_frame, controllers.controller_values)
    switchboard.grid(row=1, column=0, padx=10, pady=10)

    # Set the switchboard reference in Controllers
    controllers.switchboard = switchboard

    # Initialize the switchboard with the current controller
    switchboard.update_controller(controllers.selected_controller_name)

    # switchboard = Switchboard(main_frame)
    # switchboard.grid(row=1, column=0, padx=10, pady=10)

    window.bind("<Up>", controllers.turn_ptz_up)
    window.bind("<Down>", controllers.turn_ptz_down)
    window.bind("<Left>", controllers.turn_ptz_left)
    window.bind("<Right>", controllers.turn_ptz_right)
    window.bind("<space>", controllers.stop_ptz)
    window.bind("<s>", controllers.focus_widget)
    window.bind("<r>", controllers.handle_restore_defaults_bind)

    window.iconphoto(False, PhotoImage(file=resource_path("assets/icon.png")))
    # window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    main()
