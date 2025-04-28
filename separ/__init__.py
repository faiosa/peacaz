
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