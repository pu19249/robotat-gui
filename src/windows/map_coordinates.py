from typing import *
import numpy

def inverse_change_coordinates(x_new: numpy.float64, y_new: numpy.float64, height: int, length: int):
    """
    It takes each x and y value for objects that want to be displayed on the pygame window, 
    and makes the needed transformation to match the scaling of the screen (pygame animation window).
    It takes into account the cartesian quadrants of the Robotat platform, and locates the object on the
    corresponding block of the platform.
    For example, if the calculated position is (-100, -100) it would correspond to (580, 280) due to the
    way that pygame handles coordinates (0, 0) in the upper left corner, and grows positive to the left
    and down and also due to the scaling of the pygame window.

    Attributes:
    -----------
    x_new : numpy.float64
    y_new : numpy.float64
        Values that want to be mapped.
    height : int
    length : int
        Values of the window the objects want to be displayed, base values for the transformation

    Returns:
    -----------
    x : numpy.float64
    y : numpy.float64
        Transformed data, ready to be displayed.
    """
    # 15 pixels to get the center not in the limit but considering the width of the picture (robot)
    x_new = x_new * 2  # the scale needed because the canva is doubled of the real size
    y_new = y_new * 2

    if x_new < 0 and y_new < 0:
        x = 380 + abs(x_new)
        y = y_new + height / 2
        if (x_new == -length / 2) or (y_new == -height / 2):
            x = 380 + abs(x_new) - 15
            y = y_new + height / 2 + 15
    elif x_new > 0 and y_new < 0:
        x = 380 - x_new
        y = y_new + height / 2
        if (x_new == length / 2) or (y_new == -height / 2):
            x = 380 - x_new + 15
            y = y_new + height / 2 + 15
    elif x_new < 0 and y_new > 0:
        x = 380 + abs(x_new)
        y = y_new + height / 2
        if (x_new == -length / 2) or (y_new == height / 2):
            x = 380 + abs(x_new) - 15
            y = y_new + height / 2 - 15
    elif x_new < 0 and y_new == 0:
        x = 380 + abs(x_new) - 15
        y = y_new + height / 2 + 15
    elif x_new == 0 and y_new < 0:
        x = 380 - x_new + 15
        y = y_new + height / 2 + 15
    else:
        x = 380 - x_new
        y = y_new + height / 2
        if (x_new == length / 2) or (y_new == height / 2):
            x = 380 - x_new + 15
            y = y_new + height / 2 - 15

    return x, y
