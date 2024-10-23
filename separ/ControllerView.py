from tkinter import Frame, Label
from separ.BaseRollerView import RollerViewHorizontal, RollerViewVertical
from separ.BaseRoller import BaseRoller

class ControllerView:
    def __init__(self, controller, frame):
        self.controller = controller
        self.frame = frame
        self.roller_views = []
        Label(
            frame,
            text= "Налаштуйте " + controller.name,
            font=("AnonymousPro Regular", 14)
        ).grid(column=0, row=0, padx=40, pady=40)
        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller_frame = Frame(frame)
            roller_frame.grid(column=indx, row=1)
            roller_view = RollerViewVertical(roller, roller_frame) if roller.is_vertical else RollerViewHorizontal(roller, roller_frame)
            self.roller_views.append(roller_view)
