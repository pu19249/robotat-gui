# 15 pixels to get the center not in the limit but considering the width of the picture (robot)

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
