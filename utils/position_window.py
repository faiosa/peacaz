def position_window_at_centre(app, window_width, window_height):
    # Calculate the position to center the window on the screen
    screen_size = app.primaryScreen().size()
    x = (screen_size.width() - window_width) // 2
    y = (screen_size.height() - window_height) // 2
    return x, y, window_width, window_height
