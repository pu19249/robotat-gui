# 15 pixels to get the center not in the limit but considering the width of the picture (robot)

def change_coordinate_y(coord, height):
    print(coord, height)
    if coord == height:
        new_coords = coord - 15
    else:
        new_coords = coord + 15
    print(new_coords)
    return new_coords


def change_coordinate_x(coord, length):
    if coord == length:
        x_coord = coord - 15
    else:
        x_coord = coord + 15
    return x_coord
