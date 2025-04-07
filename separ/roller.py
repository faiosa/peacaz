import json

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from pearax.client import PearaxClient
from pearax import STEPPER_MOTOR_INDEX
from config.ptz_controls_config import LEFT, STOP, RIGHT, UP, DOWN
from separ.qt5_roller_view import RollerViewVertical, RollerViewHorizontal
from utils.ptz_controller import send_pelco_command
import time

class BaseRoller:
    def __init__(self, controller, min_angle, max_angle, is_vertical):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.is_vertical = is_vertical
        self.controller = controller
        self.view = None

        self.current_angle = 0.
        self.moving = False
        self.connected = True
        self.ms_to_wait = 20

    def turn_ptz_move(self, target_angle):
        if self.connected and not self.moving:
            self._start_move_angle(target_angle)

    def stop_ptz(self):
        if self.connected and self.moving:
            self._stop_move_angle()

    def state_update(self, is_connected, is_moving = None, current_angle=None):
        if self.connected and not is_connected:
            if self.moving and (not is_moving is None) and not is_moving:
                self.on_move_off()
                self.moving = False
            self.connected = False
            self.on_connection_off()
        elif not self.connected and is_connected:
            self.connected = True
            self.on_connection_on()

        if self.connected:
            if not is_moving is None:
                if self.moving and not is_moving:
                    self.moving = False
                    self.on_move_off()
                elif not self.moving and is_moving:
                    self.moving = True
                    self.on_move_on()

            if not current_angle is None:
                self.current_angle = current_angle

    def on_connection_on(self):
        self.view.enable_buttons()
        self.view.update_roller_view()

    def on_connection_off(self):
        self.view.disable_buttons()

    def on_move_on(self):
        self.view.disable_buttons()
        self.controller.roller_start(self)
        self._check_move()


    def on_move_off(self):
        self.view.enable_buttons()
        self.controller.roller_finish(self)

    def _start_move_angle(self, dst_angle):
        #should call self.state_update
        pass

    def _stop_move_angle(self):
        pass

    def _check_move_angle(self):
        #shold call self.state_update
        pass

    def _check_move(self):
        self._check_move_angle()
        if self.connected and self.moving:
            QTimer.singleShot(
                self.ms_to_wait,
                lambda: self._check_move()
            )

    def show(self, parent_frame):
        if self.is_vertical:
            self.view = RollerViewVertical(self, parent_frame, True)
        else:
            self.view = RollerViewHorizontal(self, parent_frame, True)

def enter(s):
    return s.encode('utf-8')

class StepperRoller(BaseRoller):
    def __init__(self, controller, rotation_speed, steps, min_angle, max_angle, is_vertical):
        super().__init__(controller, min_angle, max_angle, is_vertical)
        assert self.controller.radxa is not None
        self.rotation_speed = rotation_speed
        self.steps = steps
        self.cur_step = self.angle_to_step(self.current_angle)
        self.serial_client = PearaxClient(self.controller.radxa.mail_agent(STEPPER_MOTOR_INDEX))
        self.moving = False

    def _start_move_angle(self, dst_angle):
        trg_step = self.angle_to_step(dst_angle)
        self.send_move_command(trg_step)
        assert self.connected
        self.state_update(True, True)

    def do_patrol(self, min_angle: float, max_angle: float, rotation_speed: float):
        if self.connected and not self.is_moving():
            trg_step_1 = self.angle_to_step(min_angle)
            trg_step_2 = self.angle_to_step(max_angle)
            velocity_delay = 360.0 / (float(self.steps) * rotation_speed)
            j_patrol_task = {
                "run_final_on_stop": 2,
                "tasks": [
                    {"class": "RememberOldVelocity"},
                    {"class": "StepperParametersTask", "velocity_delay": velocity_delay},
                    {"class": "StepperParametersTask", "target_step": trg_step_1},
                    {"class": "MoveToTargetStep", "target_step": trg_step_1},
                    {"class": "StepperParametersTask", "target_step": trg_step_2},
                    {"class": "MoveToTargetStep", "target_step": trg_step_2},
                    {"class": "GoToTask", "goto_index": 2},
                    {"class": "EnsureOddStep"},
                    {"class": "RecallOldVelocity"}
                ]
            }
            self.serial_client.write(enter(json.dumps(j_patrol_task)))
            self.state_update(True, True)

    def _check_move_angle(self):
        while True:
            resp = self.serial_client.read()
            if resp is None:
                break
            else:
                s = resp.decode("utf-8").strip()
                status = s[:1]
                cur_step = int(s[1:])
                self.state_update(True, status == 'r', self.step_to_angle(cur_step))
                self.view.update_roller_view()
        if self.is_moving():
            self.serial_client.write(enter("g"))

    def _stop_move_angle(self):
        self.serial_client.write(enter("s"))

    def is_moving(self):
        return self.moving

    def angle_to_step(self, angle):
        return int(angle * self.steps / 360)

    def step_to_angle(self, step):
        return 360.0 * step / self.steps

    def send_move_command(self, trg_step):
        motor_delay = 360.0 / (float(self.steps) * self.rotation_speed)
        j_move_task = {
            "run_final_on_stop": 0,
            "tasks": [
                {"class": "StepperParametersTask", "velocity_delay": motor_delay},
                {"class": "StepperParametersTask", "target_step": trg_step},
                {"class": "MoveToTargetStep", "target_step": trg_step}
            ]
        }
        self.serial_client.write(enter(json.dumps(j_move_task)))

    def send_stop_command(self):
        self.serial_client.write(enter("s"))


class TimeRoller(BaseRoller):
    def __init__(self, controller, rotation_speed, min_angle, max_angle, current_angle, serial_port, is_vertical):
        super().__init__(controller, min_angle, max_angle, is_vertical)
        self.current_angle = current_angle
        self.serial_port = serial_port
        self.rotation_speed = rotation_speed
        self.start_move_time = 0
        self.is_moving_increase = False
        self.is_moving_decrease = False


    def _start_move_angle(self, dst_angle):
        if self.current_angle > dst_angle:
            self.__start_decrease_angle(dst_angle)
        elif self.current_angle < dst_angle:
            self.__start_increase_angle(dst_angle)

    def _check_move_angle(self, dest_angle=360.0):
        if self.is_moving_increase:
            assert not self.is_moving_decrease
            self.__check_increase_angle(dest_angle)
        elif self.is_moving_decrease:
            self.__check_decrease_angle()

    def __start_increase_angle(self, dst_angle):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.start_move_time = time.time()
            if send_pelco_command(self.increase_angle_command(), self.serial_port):
                self.is_moving_increase = True
                self.state_update(True, True)
            else:
                self.state_update(False)


    def __update_increase_angle(self):
        if self.is_moving_increase:
            cur_time = time.time()
            self.current_angle = self.current_angle + self.rotation_speed * (cur_time - self.start_move_time)
            self.start_move_time = cur_time

    def __check_increase_angle(self, dest_angle=360.0):
        if self.is_moving_increase:
            self.__update_increase_angle()
            target_angle = min(dest_angle, self.max_angle)
            if self.current_angle >= target_angle:
                self.current_angle = target_angle
                self.__stop_increase_angle(False)

    def __stop_increase_angle(self, update=True):
        if self.is_moving_increase:
            if update:
                self.__update_increase_angle()
            if send_pelco_command(STOP, self.serial_port):
                self.is_moving_increase = False
                self.state_update(True, False)
            else:
                self.state_update(False)

    def __start_decrease_angle(self, dst_angle):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.start_move_time = time.time()
            if send_pelco_command(self.decrease_angle_command(), self.serial_port):
                self.is_moving_decrease = True
                self.state_update(True, True)
            else:
                self.state_update(False)

    def __update_decrease_angle(self):
        if self.is_moving_decrease:
            cur_time = time.time()
            self.current_angle = self.current_angle - self.rotation_speed * (cur_time - self.start_move_time)
            self.start_move_time = cur_time

    def __check_decrease_angle(self, dest_angle=-360.0):
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
            if send_pelco_command(STOP, self.serial_port):
                self.is_moving_decrease = False
                self.state_update(True, False)
            else:
                self.state_update(False)

    def _stop_move_angle(self):
        if self.is_moving_increase:
            self.__stop_increase_angle()
        if self.is_moving_decrease:
            self.__stop_decrease_angle()

    def is_moving(self):
        return self.is_moving_increase or self.is_moving_decrease

    def increase_angle_command(self):
        return bytearray(0)

    def decrease_angle_command(self):
        return bytearray(0)
            

class VerticalRoller(TimeRoller):
    def __init__(self, controller, rotation_speed, min_angle, max_angle, current_angle, serial_port):
        super().__init__(controller, rotation_speed, min_angle, max_angle, current_angle, serial_port, True)

    def increase_angle_command(self):
        return UP

    def decrease_angle_command(self):
        return DOWN


class HorizontalRoller(TimeRoller):
    def __init__(self, controller, rotation_speed, min_angle, max_angle, current_angle, serial_port):
        super().__init__(controller, rotation_speed, min_angle, max_angle, current_angle, serial_port, False)

    def increase_angle_command(self):
        return RIGHT

    def decrease_angle_command(self):
        return LEFT






