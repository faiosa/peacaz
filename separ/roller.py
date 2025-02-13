from PyQt5.QtWidgets import QMessageBox
from pearax.client import PearaxClient
from pearax.core import Pearax
from serial.serialutil import SerialException

from config.ptz_controls_config import LEFT, STOP, RIGHT, UP, DOWN
from utils.ptz_controller import send_pelco_command
import serial, time, threading


class BaseRoller:
    def __init__(self, min_angle, max_angle, current_angle, serial_port, is_vertical):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = current_angle
        self.serial_port = serial_port
        self.is_vertical = is_vertical

        self.is_moving_increase = False
        self.is_moving_decrease = False

    def start_increase_angle(self, dst_angle):
        pass
            
    def __update_increase_angle(self):
        pass

    def check_increase_angle(self, dest_angle):
        pass

    def __stop_increase_angle(self, update = True):
        pass

    def start_decrease_angle(self, dst_angle):
        pass

    def __update_decrease_angle(self):
        pass

    def check_decrease_angle(self, dest_angle):
        pass

    def __stop_decrease_angle(self, update=True):
        pass

    def ptz_turn_stop(self):
        pass

    def increase_angle_command(self):
        pass

    def decrease_angle_command(self):
        pass

    def is_moving(self):
        return self.is_moving_increase or self.is_moving_decrease


def enter(s):
    return s.encode('utf-8')


class StepperRoller(BaseRoller):
    def __init__(self, steps, min_angle, max_angle, current_angle, serial_port, is_vertical):
        super().__init__(min_angle, max_angle, current_angle, serial_port, is_vertical)
        self.steps = steps
        self.cur_step = self.angle_to_step(self.current_angle)
        self.trg_step = self.cur_step
        self.pearax = None
        self.ensure_arduino(False)
        #self.arduino = serial.Serial(port=self.serial_port, baudrate=9600)

    def ensure_arduino(self, show_message = True):
        if self.pearax:
            return True
        else:
            try:
                arduino = serial.Serial(port=self.serial_port, baudrate=115200)
                time.sleep(2)#Can't work immediately without a pause (
                connector = Pearax(arduino, 3, [42])
                thread = threading.Thread(target = connector.run, daemon=True, name="PearaxConnector")
                thread.start()

                self.pearax = PearaxClient(42, connector)

                #self.set_current_command(self.cur_step)
                self.cur_step = self.read_current_step()
                self.trg_step = self.cur_step
                self.current_angle = self.step_to_angle(self.cur_step)
                return True
            except SerialException:
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
                return False

    def angle_to_step(self, angle):
        return int(angle * self.steps / 360)

    def step_to_angle(self, step):
        return 360.0 * step / self.steps

    def send_move_command(self, trg_step):
        self.pearax.write(enter(f"p{trg_step}"))

    def send_stop_command(self):
        self.pearax.write(enter("s"))

    def set_current_command(self, cur_step):
        self.pearax.write(enter(f"c{cur_step}"))

    def read_current_step(self):
        self.pearax.write(enter("g"))
        bits = self.pearax.block_read()
        return int(bits.decode("utf-8").strip())

    def start_increase_angle(self, dst_angle):
        if self.ensure_arduino() and not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_increase = True
            self.trg_step = self.angle_to_step(dst_angle)
            self.send_move_command(self.trg_step)

    def __update_increase_angle(self):
        if self.is_moving_increase:
            self.cur_step = self.read_current_step()
            self.current_angle = self.step_to_angle(self.cur_step)

    def check_increase_angle(self, dest_angle):
        if self.is_moving_increase:
            self.__update_increase_angle()
            target_angle = max(dest_angle, self.min_angle)
            if self.cur_step == self.trg_step:
                self.current_angle = target_angle
                self.__stop_increase_angle(False)

    def __stop_increase_angle(self, update=True):
        if self.is_moving_increase:
            if update:
                self.__update_increase_angle()
            self.send_stop_command()
            self.is_moving_increase = False

    def start_decrease_angle(self, trg_angle):
        if self.ensure_arduino() and not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_decrease = True
            self.trg_step = self.angle_to_step(trg_angle)
            self.send_move_command(self.trg_step)

    def __update_decrease_angle(self):
        if self.is_moving_decrease:
            cur_time = time.time()
            self.cur_step = self.read_current_step()
            self.current_angle = self.step_to_angle(self.cur_step)

    def check_decrease_angle(self, dest_angle):
        if self.is_moving_decrease:
            self.__update_decrease_angle()
            target_angle = max(dest_angle, self.min_angle)
            if self.cur_step == self.trg_step:
                self.current_angle = target_angle
                self.__stop_decrease_angle(False)

    def __stop_decrease_angle(self, update=True):
        if self.is_moving_decrease:
            if update:
                self.__update_decrease_angle()
            self.send_stop_command()
            self.is_moving_decrease = False

    def ptz_turn_stop(self):
        if self.is_moving_increase:
            self.__stop_increase_angle()
        if self.is_moving_decrease:
            self.__stop_decrease_angle()

class TimeRoller(BaseRoller):
    def __init__(self, rotation_speed, min_angle, max_angle, current_angle, serial_port, is_vertical):
        super().__init__(min_angle, max_angle, current_angle, serial_port, is_vertical)
        self.rotation_speed = rotation_speed
        self.start_move_time = 0

    def start_increase_angle(self, dst_angle):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_increase = True
            self.start_move_time = time.time()
            send_pelco_command(self.increase_angle_command(), self.serial_port)

    def __update_increase_angle(self):
        if self.is_moving_increase:
            cur_time = time.time()
            self.current_angle = self.current_angle + self.rotation_speed * (cur_time - self.start_move_time)
            self.start_move_time = cur_time

    def check_increase_angle(self, dest_angle=360.0):
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

    def start_decrease_angle(self, dst_angle):
        if not (self.is_moving_increase or self.is_moving_decrease):
            self.is_moving_decrease = True
            self.start_move_time = time.time()
            send_pelco_command(self.decrease_angle_command(), self.serial_port)

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
            send_pelco_command(STOP, self.serial_port)
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






