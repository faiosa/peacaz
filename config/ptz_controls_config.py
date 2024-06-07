ROTATION_SPEED_HORIZONTALLY_SETTING = "rotation_speed_horizontally"
ROTATION_SPEED_VERTICALLY_SETTING = "rotation_speed_vertically"
SERIAL_PORT_SETTING = "serial_port"
MIN_ANGLE_SETTING = "min_angle"
MAX_ANGLE_SETTING = "max_angle"
MIN_TILT_SETTING = "min_tilt"
MAX_TILT_SETTING = "max_tilt"
CURRENT_DEGREE_SETTING = "current_degree"
CURRENT_TILT_SETTING = "current_tilt"


# PTZ Controls
UP = b"\xFF\x01\x00\x08\x00\x3f"
DOWN = b"\xFF\x01\x00\x10\x00\x3f"
RIGHT = b"\xFF\x01\x00\x02\x3f\x00"
LEFT = b"\xFF\x01\x00\x04\x3f\x00"
STOP = b"\xFF\x01\x00\x00\x00\x00"
