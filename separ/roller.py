import time

from config.ptz_controls_config import LEFT, STOP, RIGHT, UP, DOWN

class BaseRoller:
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port, is_vertical):
        self.rotation_speed = rotation_speed
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = current_angle
        self.serial_port = serial_port
        self.is_vertical = is_vertical

        self.is_moving_increase = False
        self.is_moving_decrease = False
        self.start_move_time = 0

    def start_increase_angle(self):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_increase = True
            self.start_move_time = time.time()
            #send_pelco_command(self.increase_angle_command(), self.serial_port)
            
    def __update_increase_angle(self):
        if self.is_moving_increase:
            cur_time = time.time()
            self.current_angle = self.current_angle + self.rotation_speed * (cur_time - self.start_move_time)
            self.start_move_time = cur_time

    def check_increase_angle(self, dest_angle = 360.0):
        if self.is_moving_increase:
            self.__update_increase_angle()
            target_angle = min(dest_angle, self.max_angle)
            if self.current_angle >= target_angle:
                self.current_angle = target_angle
                self.__stop_increase_angle(False)

    def __stop_increase_angle(self, update = True):
        if self.is_moving_increase:
            if update:
                self.__update_increase_angle()
            #send_pelco_command(STOP, self.serial_port)
            self.is_moving_increase = False

    def start_decrease_angle(self):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_decrease = True
            self.start_move_time = time.time()
            #send_pelco_command(self.decrease_angle_command(), self.serial_port)

    def __update_decrease_angle(self):
        if self.is_moving_decrease:
            cur_time = time.time()
            self.current_angle = self.current_angle - self.rotation_speed * (cur_time - self.start_move_time)
            self.start_move_time = cur_time

    def check_decrease_angle(self, dest_angle=-360.0):
        if self.is_moving_decrease:
            self.__update_decrease_angle()
            target_angle = max(dest_angle, self.min_angle)
            if self.current_angle <= target_angle:
                self.current_angle = target_angle
                self.__stop_decrease_angle(False)

    def __stop_decrease_angle(self, update=True):
        if self.is_moving_decrease:
            if update:
                self.__update_decrease_angle()
            #send_pelco_command(STOP, self.serial_port)
            self.is_moving_decrease = False

    def ptz_turn_stop(self):
        if self.is_moving_increase:
            self.__stop_increase_angle()
        if self.is_moving_decrease:
            self.__stop_decrease_angle()

    def increase_angle_command(self):
        return STOP

    def decrease_angle_command(self):
        return STOP
            

class VerticalRoller(BaseRoller):
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port):
        super().__init__(rotation_speed, min_angle, max_angle, current_angle, serial_port, True)

    def increase_angle_command(self):
        return UP

    def decrease_angle_command(self):
        return DOWN


class HorizontalRoller(BaseRoller):
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port):
        super().__init__(rotation_speed, min_angle, max_angle, current_angle, serial_port, False)

    def increase_angle_command(self):
        return RIGHT

    def decrease_angle_command(self):
        return LEFT






