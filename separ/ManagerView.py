from tkinter import ttk
from separ.ControllerView import ControllerView

class ManagerView:
    def __init__(self, manager, frame):
        self.manager = manager
        self.tab_control = ttk.Notebook(frame)
        self.controllers_views = []
        for controller in self.manager.controllers:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=controller.name)
            controller_view = ControllerView(controller, tab)
            self.controllers_views.append(controller_view)
        self.tab_control.pack(expand=1, fill="both")
