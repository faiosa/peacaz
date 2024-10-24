from separ.roller import HorizontalRoller, VerticalRoller


class Controller:
    def __init__(self, json_settings):
        self.name = json_settings.get("name")
        self.settings = json_settings
        self.rollers = [
            VerticalRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=json_settings.get("serial_port")
            ) if json.get("type") == "vertical" else HorizontalRoller(
                rotation_speed=json.get("rotation_speed"),
                min_angle=json.get("min_angle"),
                max_angle=json.get("max_angle"),
                current_angle=json.get("current_angle"),
                serial_port=json_settings.get("serial_port")
            )
            for json in json_settings.get("rollers")
        ]
