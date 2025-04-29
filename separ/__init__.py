import pathlib


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


def get_asset(asset_name: str):
    """
    Get the absolute path to 'assets/icon.png' located in the parent directory
    of the directory containing the current file.

    This function uses pathlib, which is more modern and readable.
    Works on both Windows and Linux.

    Returns:
        str: Absolute path to the assets/icon.png file
    """
    # Get the absolute path of the current file
    current_file = pathlib.Path(__file__).resolve()

    # Get parent directory of the directory containing the current file
    parent_dir = current_file.parent.parent

    # Create path to assets/icon.png
    icon_path = parent_dir / 'assets' / asset_name

    # Return as string
    return str(icon_path)