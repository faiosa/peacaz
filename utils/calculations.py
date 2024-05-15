def get_azimuth_from_angle(angle):
    return (angle + 90) % 360


def get_angle_from_azimuth(azimuth):
    return (azimuth - 90) % 360
