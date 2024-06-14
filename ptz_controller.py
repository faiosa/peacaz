import serial
import time

from config.ptz_controls_config import LEFT, STOP, RIGHT, UP, DOWN


def turn_ptz_up(selected_controller: str):
    send_pelco_command(UP, selected_controller)


def turn_ptz_down(selected_controller: str):
    send_pelco_command(DOWN, selected_controller)


def turn_ptz_left(selected_controller: str):
    send_pelco_command(LEFT, selected_controller)


def turn_ptz_right(selected_controller: str):
    send_pelco_command(RIGHT, selected_controller)


def turn_ptz(direction: bytes, selected_controller: str):
    send_pelco_command(direction, selected_controller)


def stop_ptz(selected_controller: str):
    send_pelco_command(STOP, selected_controller)


def stop_ptz_with_time(time_end: float, selected_controller: str):
    if time_end >= time.time():
        send_pelco_command(STOP, selected_controller)


def restore_defaults(
    controller_serial: bytes,
    max_angle: int,
    rotation_speed: float,
    max_tilt: int,
    min_tilt: int,
    tilt_speed: float,
) -> str:
    rotate_time = get_rotate_time(0, max_angle, LEFT, rotation_speed)
    tilt_time = get_rotate_time(min_tilt, max_tilt, UP, tilt_speed)

    turn_ptz_left(controller_serial)
    time.sleep(float(f"{rotate_time:.2f}"))
    stop_ptz(controller_serial)

    turn_ptz_down(controller_serial)
    time.sleep(float(f"{tilt_time:.2f}"))
    stop_ptz(controller_serial)

    return "PTZ restored to default position"


def get_rotate_time(
    new_angle: float,
    previous_angle: float,
    rotate_direction: bytes,
    rotation_speed: float,
) -> float:
    if rotate_direction == RIGHT or rotate_direction == UP:
        rotate_angle = new_angle - previous_angle
    else:
        rotate_angle = previous_angle - new_angle

    return rotate_angle / rotation_speed


def get_rotate_angle(time_spend: float, rotation_speed: float) -> float:
    rotate_angle = time_spend * rotation_speed
    return rotate_angle


def get_rotate_direction(new_angle: float, previous_angle: float) -> bytes:
    if new_angle > previous_angle:
        return RIGHT
    else:
        return LEFT


def update_ptz_angle(selected_controller: str, new_angle: float, previous_angle: float):
    # Calculate how much time PTZ should rotate
    if new_angle > previous_angle:
        rotation_direction = RIGHT
        rotate_angle = new_angle - previous_angle
    else:
        rotation_direction = LEFT
        rotate_angle = previous_angle - new_angle

    # time_to_rotate = rotate_angle / ROTATION_SPEED

    send_pelco_command(rotation_direction, selected_controller)
    # time.sleep(float(f"{time_to_rotate:.2f}"))
    send_pelco_command(STOP, selected_controller)


# Function to calculate Pelco-D checksum
def calculate_checksum(command):
    checksum = sum(command[1:]) & 0xFF  # Calculate sum and mask to 8 bits
    return bytes([checksum])


# Function to send a Pelco-D command
def send_pelco_command(command: bytes, selected_controller: str) -> None:
    try:
        checksum = calculate_checksum(command)
        full_command = command + checksum
        # Replace with your serial port settings (consult camera manual)
        with serial.Serial(
            port=selected_controller, baudrate=2400, bytesize=8, timeout=0.02
        ) as ser:
            ser.write(full_command)
            ser.read(size=8)
            print(f"Sent command: {command.hex()}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
