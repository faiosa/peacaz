from tkinter import Toplevel, Label, ttk
from utils.position_window import position_window_at_centre


class RestorationProgressWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Відновлення початкових значень")
        self.geometry(position_window_at_centre(self, width=300, height=100))
        self.resizable(False, False)
        self.withdraw()

        self.label = Label(
            self, text="Відновлюємо початкові значення...", font=("Arial", 12)
        )
        self.label.pack(pady=10)

        self.progressbar = ttk.Progressbar(
            self, orient="horizontal", length=200, mode="indeterminate"
        )
        self.progressbar.pack(pady=5)

    def start(self):
        self.progressbar.start()
        self.deiconify()

    def stop(self):
        self.progressbar.stop()
        self.withdraw()
