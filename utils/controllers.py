def get_controller_id_by_name(controller_name, controller_values):
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_id


def get_controller_serial_by_name(controller_name, controller_values):
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_info["serial_port"]


def get_controller_min_angle_by_name(
    controller_name: str, controller_values: dict
) -> int:
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_info["min_angle"]


def get_controller_max_angle_by_name(
    controller_name: str, controller_values: dict
) -> int:
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_info["max_angle"]


def get_rotation_speed_horizontally_by_name(
    controller_name: str, controller_values: dict
):
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_info["rotation_speed_horizontally"]


def get_rotation_speed_by_name(controller_name: str, controller_values: dict):
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_info["rotation_speed"]


def get_controller_setting_by_name(
    controller_name: str, controller_values: dict, setting_name: str
) -> str:
    for controller_id, controller_info in controller_values.items():
        if controller_info["name"] == controller_name:
            return controller_info[setting_name]
