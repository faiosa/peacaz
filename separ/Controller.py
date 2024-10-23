from separ.BaseRoller import BaseRoller


class Controller:
    def __init__(self, json_settings):
        self.name = json_settings.get("name")
        self.rollers = [
            BaseRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                is_vertical=json.get("type") == "vertical"
            )
            for json in json_settings.get("rollers")
        ]
