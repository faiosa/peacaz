from tkinter import Frame, ttk
from separ.roller_view import RollerViewHorizontal, RollerViewVertical
from config import ui

class ControllerView:
    def __init__(self, controller, frame):
        self.controller = controller
        self.frame = frame
        self.roller_views = []
        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller_frame = Frame(frame, bg=ui.BG_COLOR, highlightbackground="black", highlightthickness=2)
            #roller_frame.pack(expand="y", fill="y", anchor="nw")
            roller_frame.grid(column=indx, row=1, padx=10, pady=10)
            roller_view = RollerViewVertical(roller, roller_frame) if roller.is_vertical else RollerViewHorizontal(roller, roller_frame)
            self.roller_views.append(roller_view)
