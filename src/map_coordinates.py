# 15 pixels to get the center not in the limit but considering the width of the picture (robot)

def change_coordinate_y(coord, height):
    new_coords = coord - height/2
    return new_coords


def change_coordinate_x(coord, length):
    x_coord = -1
    if coord < 0:  # x is negative
        x_coord = -(coord-380)
    elif coord > 0:  # x is positive
        x_coord = abs(coord - length/2)
    return x_coord

# 15 pixels to get the center not in the limit but considering the width of the picture (robot)


def change_coordinates(x, y, height, length):
    if x < 0 and y < 0:
        x_new = -(x-380)
        y_new = y - 480
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
    if x_new < 0 and y_new < 0:
        x = 380 + abs(x_new)
        y = y_new + height / 2
    elif x_new > 0 and y_new < 0:
        x = 380 - x_new
        y = y_new + height / 2
    elif x_new < 0 and y_new > 0:
        x = 380 + abs(x_new)
        y = y_new + height / 2
    else:
        x = 380 - x_new
        y = y_new + height / 2
    return x, y
