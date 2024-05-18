def disable_buttons(self):
    self.turn_left_button.config(state="disabled")
    self.turn_right_button.config(state="disabled")
    self.desired_degree_entry.config(state="disabled")


def enable_buttons(self):
    self.turn_left_button.config(state="normal")
    self.turn_right_button.config(state="normal")
    self.desired_degree_entry.config(state="normal")
