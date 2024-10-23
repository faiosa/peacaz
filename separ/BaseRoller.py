

class BaseRoller:
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, is_vertical = False):
        self.rotation_speed = rotation_speed
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = current_angle
        self.is_vertical = is_vertical


