from PyQt5.QtGui import QPalette, QColor

def getPalette():
    palette = QPalette()
    inactive_color = QColor(255, 255, 255)
    active_color = QColor(200, 200, 200)
    palette.setColor(QPalette.Active, QPalette.Window, active_color)
    palette.setColor(QPalette.Inactive, QPalette.Window, inactive_color)
    return palette