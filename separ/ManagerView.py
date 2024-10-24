from tkinter import Frame
from tkinter import ttk
from separ.ControllerView import ControllerView
from config import ui

class ManagerView:
    def __init__(self, manager, frame):
        self.manager = manager
        #s = ttk.Style()
        #s.theme_use('default')
        #s.configure('TNotebook.Tab', background="green3")
        #s.map("TNotebook.Tab", background=[("selected", ui.BG_COLOR)])
        self.tab_control = ttk.Notebook(frame)

        self.controllers_views = []
        for controller in self.manager.controllers:
            tab = Frame(self.tab_control)
            self.tab_control.add(tab, text=controller.name)
            controller_view = ControllerView(controller, tab)
            self.controllers_views.append(controller_view)
        self.tab_control.pack(expand=1, fill="both")
