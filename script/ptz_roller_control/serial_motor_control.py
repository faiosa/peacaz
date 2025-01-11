from periphery import GPIO
import time
import serial

# GPIO pin assignments
EN_GPIO = GPIO(158, "out")
DIR_GPIO = GPIO(133, "out")
PUL_GPIO = GPIO(76, "out")

# Serial port configuration
SERIAL_PORT = "/dev/ttyGS0"
BAUD_RATE = 115200

DATA_FILE = "/home/rock/motor_data"

class StepperSerialControl:
    def __init__(self, ser, delay, cur_step):
        self.ser = ser
        self.cur = cur_step
        self.trg = cur_step
        self.delay = delay / 2.

    def listen(self):
      if self.ser.in_waiting > 0:
        s = self.ser.readline().decode('utf-8').strip()
        if s[0] == 'g':
          code = str(self.cur) + "\n"
          self.ser.write(code.encode('utf-8'))
        elif s[0] == 'c':
          self.cur=int(s[1:])
        elif s[0] == 'p':
          self.trg = int(s[1:])
          if self.cur < self.trg:
              DIR_GPIO.write(True)
          elif self.cur > self.trg:
              DIR_GPIO.write(False)
        elif s[0] == 's':
            self.trg = self.cur
            self.check_stop()

    def do_step(self):
        PUL_GPIO.write(True)
        time.sleep(self.delay)
        PUL_GPIO.write(False)
        time.sleep(self.delay)

    def run(self):
        if self.cur < self.trg:
            self.do_step()
            self.cur += 1
            self.check_stop()
        elif self.cur > self.trg:
            self.do_step()
            self.cur -= 1
            self.check_stop()

    def check_stop(self):
        if self.cur == self.trg:
            write_data(self.cur)

def read_data():
    res = 0
    try:
        f2 = open(DATA_FILE, "r")
        res = int(f2.readline())
        f2.close()
    except FileNotFoundError as e:
        print(f"Data file {DATA_FILE} not found")
    except Exception as _:
        print("Could not read")
    return res

def write_data(num):
    f = open(DATA_FILE, "w")
    f.write(str(num))
    f.close()

control = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    EN_GPIO.write(False)

    delay = 32. / 400.
    control = StepperSerialControl(ser, delay, read_data())
    print(f"Starting motor with cur_step={control.cur}")

    while True:
        control.listen()
        control.run()

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
    if 'PUL_GPIO' in locals():
        PUL_GPIO.close()
    if 'DIR_GPIO' in locals():
        DIR_GPIO.close()
    if 'EN_GPIO' in locals():
        EN_GPIO.close()
    if control:
        write_data(control.cur)

print("Program finished.")