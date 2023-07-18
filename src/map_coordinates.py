# 15 pixels to get the center not in the limit but considering the width of the picture (robot)


def change_coordinates(x, y, height, length):
    if x < 0 and y < 0:
        x_new = -(x-length/2)
        y_new = y - height/2
    elif x > 0 and y < 0:
        x_new = abs(x-380)
        y_new = y - 480
    elif x < 0 and y > 0:
        x_new = -(x-380)
        y_new = y - 480
    else:
        x_new = abs(x-380)
        y_new = y - 480
    return x_new, y_new


def inverse_change_coordinates(x_new, y_new, height, length):
    x_new = x_new*2  # the scale needed because the canva is doubled of the real size
    y_new = y_new*2
    if x_new < 0 and y_new < 0:
        x = 380 + abs(x_new)
        y = y_new + height / 2
        if (x_new == -length/2) or (y_new == -height/2):
            x = 380 + abs(x_new)-15
            y = y_new + height / 2 + 15
    elif x_new > 0 and y_new < 0:
        x = 380 - x_new
        y = y_new + height / 2
        if (x_new == length/2) or (y_new == -height/2):
            x = 380 - x_new + 15
            y = y_new + height / 2 + 15
    elif x_new < 0 and y_new > 0:
        x = 380 + abs(x_new)
        y = y_new + height / 2
        if (x_new == -length/2) or (y_new == height/2):
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
        if (x_new == length/2) or (y_new == height/2):
            x = 380 - x_new + 15
            y = y_new + height / 2 - 15

    return x, y
