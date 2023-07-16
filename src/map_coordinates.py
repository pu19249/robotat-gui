# 15 pixels to get the center not in the limit but considering the width of the picture (robot)

# def change_coordinate_y(coord, height):
#     new_coords = coord - height/2
#     return new_coords


# def change_coordinate_x(coord, length):
#     x_coord = -1
#     if coord < 0:  # x is negative
#         x_coord = -(coord-380)
#     elif coord > 0:  # x is positive
#         x_coord = abs(coord - length/2)
#     return x_coord

# 15 pixels to get the center not in the limit but considering the width of the picture (robot)
import math


def change_coordinate_y(coord, height):
    if coord == height:
        new_coords = coord - 15
        new_coords = abs(new_coords - height)
    else:
        new_coords = coord + 15
        new_coords = abs(new_coords - height)
    return new_coords


def change_coordinate_x(coord, length):
    if coord == length:
        x_coord = coord - 15
    else:
        x_coord = coord + 15
    return x_coord
