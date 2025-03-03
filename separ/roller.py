import json

from PyQt5.QtWidgets import QMessageBox
from pearax.client import PearaxClient
from pearax.core import Pearax
from pearax import STEPPER_MOTOR_INDEX
from config.ptz_controls_config import LEFT, STOP, RIGHT, UP, DOWN
from utils.ptz_controller import send_pelco_command
import time


class BaseRoller:
    def __init__(self, min_angle, max_angle, current_angle, serial_port, is_vertical):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = current_angle
        self.serial_port = serial_port
        self.is_vertical = is_vertical


    def start_move_angle(self, dst_angle):
        pass

    def __update_move_angle(self):
        pass

    def check_move_angle(self, dest_angle):
        pass

    def __stop_move_angle(self, update=True):
        pass

    def ptz_turn_stop(self):
        pass


    def is_moving(self):
        pass


def enter(s):
    return s.encode('utf-8')


class StepperRoller(BaseRoller):
    def __init__(self, radxa: Pearax, rotation_speed, steps, min_angle, max_angle, is_vertical):
        super().__init__(min_angle, max_angle, 0., None, is_vertical)
        assert radxa is not None
        self.rotation_speed = rotation_speed
        self.steps = steps
        self.cur_step = self.angle_to_step(self.current_angle)
        #self.trg_step = self.cur_step
        self.serial_client = PearaxClient(STEPPER_MOTOR_INDEX, radxa)
        self.moving = False
        self.ensure_arduino(False)

    def is_moving(self):
        return self.moving

    def ensure_arduino(self, show_message = False, retry=5):
        resp = False
        if self.serial_client.pearax.is_serial_alive():
            _, cs = self.read_current_step()
            if not cs is None:
                self.cur_step = cs
                self.current_angle = self.step_to_angle(self.cur_step)
                self.send_rotation_speed()
                resp = True
        if not resp:
            if retry > 0:
                time.sleep(0.01)
                return self.ensure_arduino(show_message, retry - 1)
            text = f"Не вдається підключитись до серійного порта контролера {self.serial_port}. Підключіть девайс або змініть адресу порта в налаштуваннях."
            if show_message:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Не підключено серійний порт контролера")
                msg.setInformativeText(text)
                msg.setWindowTitle("Помилка конфігурації")
                msg.exec_()
            else:
                print(text)
        return resp

    def send_rotation_speed(self):
        motor_delay =  360.0 / (float(self.steps) * self.rotation_speed)
        self.serial_client.write(enter(f"v{motor_delay}"))


    def angle_to_step(self, angle):
        return int(angle * self.steps / 360)

    def step_to_angle(self, step):
        return 360.0 * step / self.steps

    def send_move_command(self, trg_step):
        j_move_task = {
            "run_final_on_stop": False,
            "tasks": [
                {"class": "StepperParametersTask", "target_step": trg_step},
                {"class": "MoveToTargetStep", "target_step": trg_step}
            ]
        }
        self.serial_client.write(enter(json.dumps(j_move_task)))

    def send_stop_command(self):
        self.serial_client.write(enter("s"))

    def set_current_command(self, cur_step):
        self.serial_client.write(enter(f"c{cur_step}"))

    def read_current_step(self):
        self.serial_client.write(enter("g"))
        bits = self.serial_client.block_read()
        s = bits.decode("utf-8").strip()
        return s[:1], int(s[1:])

    def start_move_angle(self, dst_angle):
        if self.ensure_arduino() and not self.is_moving():
            self.moving = True
            trg_step = self.angle_to_step(dst_angle)
            self.send_move_command(trg_step)

    def __update_move_angle(self):
        if self.is_moving():
            status, self.cur_step = self.read_current_step()
            self.moving = True if status == 'r' else False
            self.current_angle = self.step_to_angle(self.cur_step)

    def check_move_angle(self, dest_angle):
        if self.is_moving():
            self.__update_move_angle()

    def ptz_turn_stop(self):
        if self.is_moving():
            self.send_stop_command()

    def do_patrol(self, min_angle: float, max_angle: float, rotation_speed: float):
        if self.ensure_arduino() and not self.is_moving():
            self.moving = True
            trg_step_1 = self.angle_to_step(min_angle)
            trg_step_2 = self.angle_to_step(max_angle)
            velocity_delay = 360.0 / (float(self.steps) * rotation_speed)
            j_patrol_task = {
                "run_final_on_stop": True,
                "tasks": [
                    {"class": "RememberOldVelocity"},
                    {"class": "StepperParametersTask", "velocity_delay": velocity_delay},
                    {"class": "StepperParametersTask", "target_step": trg_step_1},
                    {"class": "MoveToTargetStep", "target_step": trg_step_1},
                    {"class": "StepperParametersTask", "target_step": trg_step_2},
                    {"class": "MoveToTargetStep", "target_step": trg_step_2},
                    {"class": "GoToTask", "goto_index": 2},
                    {"class": "RecallOldVelocity"}
                ]
            }
            self.serial_client.write(enter(json.dumps(j_patrol_task)))

class TimeRoller(BaseRoller):
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port, is_vertical):
        super().__init__(min_angle, max_angle, current_angle, serial_port, is_vertical)
        self.rotation_speed = rotation_speed
        self.start_move_time = 0
        self.is_moving_increase = False
        self.is_moving_decrease = False


    def start_move_angle(self, dst_angle):
        if self.current_angle > dst_angle:
            self.__start_decrease_angle(dst_angle)
        elif self.current_angle < dst_angle:
            self.__start_increase_angle(dst_angle)

    def check_move_angle(self, dest_angle=360.0):
        if self.is_moving_increase:
            assert not self.is_moving_decrease
            self.__check_increase_angle(dest_angle)
        elif self.is_moving_decrease:
            self.__check_decrease_angle()

    def __start_increase_angle(self, dst_angle):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_increase = True
            self.start_move_time = time.time()
            send_pelco_command(self.increase_angle_command(), self.serial_port)

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
            send_pelco_command(STOP, self.serial_port)
            self.is_moving_increase = False

    def __start_decrease_angle(self, dst_angle):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_decrease = True
            self.start_move_time = time.time()
            send_pelco_command(self.decrease_angle_command(), self.serial_port)

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
            send_pelco_command(STOP, self.serial_port)
            self.is_moving_decrease = False

    def ptz_turn_stop(self):
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
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port):
        super().__init__(rotation_speed, min_angle, max_angle, current_angle, serial_port, True)

    def increase_angle_command(self):
        return UP

    def decrease_angle_command(self):
        return DOWN


class HorizontalRoller(TimeRoller):
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port):
        super().__init__(rotation_speed, min_angle, max_angle, current_angle, serial_port, False)

    def increase_angle_command(self):
        return RIGHT

    def decrease_angle_command(self):
        return LEFT






