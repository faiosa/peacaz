from tkinter import Frame, Button
from separ.roller_view import RollerViewHorizontal, RollerViewVertical
from config import ui

class ControllerView:
    def __init__(self, controller, frame):
        self.controller = controller
        self.frame = frame
        self.roller_views = []
        self.lambda_queue = []
        for indx in range(0, len(self.controller.rollers)):
            roller = self.controller.rollers[indx]
            roller_frame = Frame(frame, bg=ui.BG_COLOR, highlightbackground="black", highlightthickness=2)
            roller_frame.grid(column=indx, row=1, padx=5, pady=5)
            roller_view = RollerViewVertical(roller, roller_frame, self, indx) if roller.is_vertical else RollerViewHorizontal(roller, roller_frame, self, indx)
            self.roller_views.append(roller_view)
        #self.common_frame = Frame(frame, bg=ui.BG_COLOR, highlightbackground="black", highlightthickness=2)
        #self.common_frame.grid(column=0, row=2, columnspan=2, padx=5, pady=5)
        self.restore_defaults_button = Button(
            self.frame,
            borderwidth=1,
            highlightthickness=0,
            command=self.__tune_angles,
            text="Відновити початкові значення",
            bg=ui.BG_COLOR,
        )
        self.restore_defaults_button.grid(column=0, row=2, padx=40, pady=20)

    def roller_start(self, roller_index):
        for i in range(0, len(self.roller_views)):
            if i != roller_index:
                self.roller_views[i].disable_all_buttons()

    def roller_finish(self, roller_index):
        for i in range(0, len(self.roller_views)):
            if i != roller_index:
                self.roller_views[i].enable_all_buttons()
        self.__check_lambdas()

    def __check_lambdas(self):
        if len(self.lambda_queue) > 0:
            my_lambda = self.lambda_queue.pop(0)
            my_lambda()

    def __tune_angles(self):
        angles = [json.get("current_angle") for json in self.controller.settings.get("rollers")]
        for i in range(0, min(len(self.roller_views), len(angles))):
            if self.roller_views[i].moving_id:
                self.roller_views[i].stop_ptz()
            my_lambda = lambda: self.roller_views[len(self.roller_views) - len(angles)].roll_desired_angle(angles.pop(0))
            self.lambda_queue.append(my_lambda)
        self.__check_lambdas()


