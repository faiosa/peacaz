import json

from PyQt5.QtCore import QTimer
from pearax import STEPPER_MOTOR_INDEX, WORKER_MAIL_INDEX, COMPASS_MAIL_INDEX, DATA_STORE_MAIL_INDEX
from config.ptz_controls_config import LEFT, STOP, RIGHT, UP, DOWN
from separ.qt5_roller_view import RollerViewVertical, RollerViewHorizontal
from utils.ptz_controller import send_pelco_command
import time

class BaseRoller:
    def __init__(self, controller, roller_index):#, min_angle, max_angle, is_vertical):
        self.roller_index = roller_index
        self.controller = controller
        self.min_angle = self.controller.settings["rollers"][self.roller_index]["min_angle"]
        self.max_angle = self.controller.settings["rollers"][self.roller_index]["max_angle"]
        self.is_vertical = self.controller.settings["rollers"][self.roller_index]["type"] == "vertical"
        self.view = None

        self.current_angle = 0.
        self.moving = False
        self.connected = True
        self.ms_to_wait = 20

        self.zero_azimuth = None
        self.ridge_angle = 0.0

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
            view_angle_shift = self.controller.settings["rollers"][self.roller_index]["view_angle_shift"] if "view_angle_shift" in self.controller.settings["rollers"][self.roller_index] else 0
            self.view = RollerViewHorizontal(self, parent_frame, view_angle_shift, True)

    def tune_zero_azimuth(self):
        pass

    def on_motor_connect(self):
        pass

    def show_angle(self):
        return self.current_angle

    def real_angle(self, view_angle):
        return view_angle

    @staticmethod
    def enter(s):
        return s.encode('utf-8')

STEPPER_ROLLER_INDEX = 21

class StepperRoller(BaseRoller):
    def __init__(self, controller, roller_index):
        super().__init__(controller, roller_index)
        assert self.controller.radxa is not None
        self.rotation_speed = self.controller.settings["rollers"][self.roller_index]["rotation_speed"]

        self.steps = self.controller.settings["rollers"][self.roller_index]["steps"]
        self.cur_step = self.angle_to_step(self.current_angle)
        self.ridge_angle = self.controller.settings["rollers"][self.roller_index]["ridge_angle"]
        self.zero_azimuth = self.controller.settings["rollers"][self.roller_index]["current_zero_azimuth"]
        assert self.zero_azimuth is None

        self.current_angle = self.ridge_angle

        self._communicator = self.controller.radxa.provide_proxy_mail_post(STEPPER_ROLLER_INDEX, [STEPPER_MOTOR_INDEX, WORKER_MAIL_INDEX, DATA_STORE_MAIL_INDEX])
        self.moving = False

        self.min_angle, self.max_angle = self.normalize_angles(self.min_angle, self.max_angle)

    def _start_move_angle(self, dst_angle):
        if dst_angle > self.max_angle:
            dst_angle = self.max_angle
        if dst_angle < self.min_angle:
            dst_angle = self.min_angle
        trg_step = self.angle_to_step(dst_angle)
        self.send_move_command(trg_step)
        assert self.connected
        self.state_update(True, True)

    #angles should be real, not show angles!
    def do_patrol(self, angle_1: float, angle_2: float, rotation_speed: float):
        min_angle, max_angle = self.normalize_angles(angle_1, angle_2)
        if self.connected and not self.is_moving():
            trg_step_1 = self.angle_to_step(max(min_angle, self.min_angle))
            trg_step_2 = self.angle_to_step(min(max_angle, self.max_angle))
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
            self._communicator.send_to(self.enter(json.dumps(j_patrol_task)), STEPPER_MOTOR_INDEX)
            self.state_update(True, True)

    @staticmethod
    def normalize_angles(angle_1, angle_2):
        assert not angle_1 == angle_2
        min_angle = min(angle_1, angle_2)
        max_angle = max(angle_1, angle_2)
        while min_angle > 360.:
            min_angle -= 360.
            max_angle -= 360.
        while max_angle < 0.:
            min_angle += 360.
            max_angle += 360.
        return min_angle, max_angle

    def tune_zero_azimuth(self):
        if self.connected and not self.is_moving():
            j_azimuth_task = {
                "type": "DataJob",
                "tasks": [
                    #{"class": "SendCommandTask", "mail_index": DATA_STORE_MAIL_INDEX, "bytes": json.dumps({"cmd": "del", "key": "zero_azimuth"})},
                    {"class": "SendCommandTask", "mail_index": COMPASS_MAIL_INDEX, "bytes": " "},
                    {"class": "ReceiveAzimuthTask"},
                    {"class": "SendCommandTask", "mail_index": STEPPER_MOTOR_INDEX, "bytes": "g"},
                    {"class": "ReceiveMotorStep"},
                    {"class": "CalcZeroAzimuth", "steps": self.steps}
                ]
            }
            self._communicator.send_to(json.dumps({"cmd": "del", "key": "zero_azimuth"}).encode('utf-8'), DATA_STORE_MAIL_INDEX)
            self._communicator.send_to(self.enter(json.dumps(j_azimuth_task)), WORKER_MAIL_INDEX)
            self.__check_zero_azimuth()

    def __check_zero_azimuth(self, retry = 16):
        msg = self._communicator.receive_from(DATA_STORE_MAIL_INDEX)
        if msg:
            jdata = json.loads(msg.decode("utf-8"))
            if "zero_azimuth" in jdata:
                if jdata["zero_azimuth"] is None:
                    self.zero_azimuth = None
                else:
                    self.zero_azimuth = float(jdata["zero_azimuth"])
                    retry = 0

        if retry > 0:
            self._communicator.send_to(self.enter(json.dumps({"cmd": "get", "key": "zero_azimuth"})), DATA_STORE_MAIL_INDEX)
            QTimer.singleShot(
                self.ms_to_wait * 2,
                lambda: self.__check_zero_azimuth(retry - 1)
            )
        else:
            self.view.update_roller_view()

    def _check_move_angle(self):
        while True:
            resp = self._communicator.receive_from(STEPPER_MOTOR_INDEX)
            if resp is None:
                break
            else:
                s = resp.decode("utf-8").strip()
                status = s[:1]
                cur_step = int(s[1:])
                self.state_update(True, status == 'r', self.step_to_angle(cur_step))
                self.view.update_roller_view()
        if self.is_moving():
            self._communicator.send_to(self.enter("g"), STEPPER_MOTOR_INDEX)

    def _stop_move_angle(self):
        self._communicator.send_to(self.enter("s"), STEPPER_MOTOR_INDEX)

    def is_moving(self):
        return self.moving
    '''
    def show_angle(self):
        return self.current_angle - self.ridge_angle

    def real_angle(self, view_angle):
        return view_angle + self.ridge_angle
    '''
    def angle_to_step(self, angle):
        return int((angle + self.ridge_angle) * self.steps / 360.0)

    def step_to_angle(self, step):
        return 360.0 * step / self.steps - self.ridge_angle

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
        self._communicator.send_to(self.enter(json.dumps(j_move_task)), STEPPER_MOTOR_INDEX)

    def send_stop_command(self):
        self._communicator.send_to(self.enter("s"), STEPPER_MOTOR_INDEX)
    '''
    def set_cur_angle_command(self, new_cur_angle):
        new_cur_step = self.angle_to_step(new_cur_angle)
        self._communicator.send_to(self.enter(f"c{new_cur_step}"), STEPPER_MOTOR_INDEX)
    '''
    def on_motor_connect(self):
        self.__check_zero_azimuth(4)


class TimeRoller(BaseRoller):
    def __init__(self, controller, roller_index):
        super().__init__(controller, roller_index)
        self.current_angle = self.controller.settings["rollers"][self.roller_index]["current_angle"]
        self.serial_port = self.controller.settings["rollers"][self.roller_index]["serial_port"]
        self.rotation_speed = self.controller.settings["rollers"][self.roller_index]["rotation_speed"]
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
    def __init__(self, controller, roller_index):
        super().__init__(controller, roller_index)
        assert self.is_vertical

    def increase_angle_command(self):
        return UP

    def decrease_angle_command(self):
        return DOWN


class HorizontalRoller(TimeRoller):
    def __init__(self, controller, roller_index):
        super().__init__(controller, roller_index)
        assert not self.is_vertical

    def increase_angle_command(self):
        return RIGHT

    def decrease_angle_command(self):
        return LEFT






