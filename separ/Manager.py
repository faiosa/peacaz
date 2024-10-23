from separ.Controller import Controller

class Manager:
    def __init__(self, json_settings):
        controller_values = json_settings.get("controller_values")
        self.controllers = [
            Controller(controller_values.get(key))
            for key in controller_values
        ]