from config.ptz_controls_config import ROTATION_SPEED, LEFT, STOP, RIGHT
import time
import serial


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


def restore_defaults(controller_serial: bytes, max_angle: int) -> str:
    rotate_time = get_rotate_time(0, max_angle, LEFT)
    turn_ptz_left(controller_serial)
    time.sleep(float(f"{rotate_time:.2f}"))
    stop_ptz(controller_serial)
    return "PTZ restored to default position"


def get_rotate_time(
    new_angle: float, previous_angle: float, rotate_direction: bytes
) -> float:
    if rotate_direction == RIGHT:
        rotate_angle = new_angle - previous_angle
    else:
        rotate_angle = previous_angle - new_angle

    return rotate_angle / ROTATION_SPEED


def get_rotate_angle(time_spend: float):
    rotate_angle = time_spend * ROTATION_SPEED
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

    time_to_rotate = rotate_angle / ROTATION_SPEED

    send_pelco_command(rotation_direction, selected_controller)
    time.sleep(float(f"{time_to_rotate:.2f}"))
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
        with serial.Serial(selected_controller, 2400, timeout=1) as ser:
            ser.write(full_command)
            print(f"Sent command: {command.hex()}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
