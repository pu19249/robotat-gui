import ctypes
import sys
import os
import csv

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from windows.animation_window import *
from robotat_3pi_Python import *
from windows.map_coordinates import inverse_change_coordinates

################ END OF IMPORTS ##############################

# This solves scaling issues for the independent pygame window
ctypes.windll.user32.SetProcessDPIAware()


pictures_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures"
)


robotat = robotat_connect()
robotat.recv(2048)

# Initialize arrays to display and save data
x_data = []
y_data = []
theta_data = []
x_vals_display_robot = []
y_vals_display_robot = []
theta_vals_display_robot = []
x_results_raw = []
y_results_raw = []


# First we need to create the object that represents and updates the position and rotation of the Pololu img (first one robot only)
character = (os.path.join(pictures_dir, "pololu_img_x.png"), 0, 0, 0)


# Prepare data as the animation window expects it (list of lists for each x, y, theta for each robot) according to how its received from the server (list of x, y, orientation)
def get_and_process_data():
    for pose_data in get_pose_continuous(robotat, [7], "eulxyz", max_attempts=5):
        # if pose_data is not None:
        #     print(pose_data)
        # else:
        #     print('no data')
        # print(pose_data)
        x_vals_real_time = [pose_data[0][0]]
        y_vals_real_time = [pose_data[0][1]]
        theta_vals_real_time = [pose_data[0][5]]
        # print(theta_vals_real_time)
        x_data.append(x_vals_real_time)
        y_data.append(y_vals_real_time)
        theta_data.append(theta_vals_real_time)
        # print(f"x: {x_vals_real_time}, y: {y_vals_real_time}, theta: {theta_vals_real_time}")
        print(f"theta: {theta_vals_real_time}")
        # animation_window.start_animation(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
        # time.sleep(0.5)
        break
    # print(theta_vals_real_time)
    return x_vals_real_time, y_vals_real_time, theta_vals_real_time


def map_data(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
    x_vals_display_robot = []
    y_vals_display_robot = []
    theta_vals_display_robot = []
    # this part makes the mapping to display in the complete animation window
    for x, y, theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
        # for x_val, y_val, theta_val in zip(x, y, theta):
        x_raw, y_raw = x, y
        x_new_val, y_new_val = inverse_change_coordinates(
            x_raw * 100, y_raw * 100, 960, 760
        )

        theta_new_val = theta  # theta_val, not just theta

        x_vals_display_robot.append(x_new_val)
        y_vals_display_robot.append(y_new_val)
        theta_vals_display_robot.append(theta_new_val)
        x_results_raw.append(x_raw)
        y_results_raw.append(y_raw)
        # Print statement for debugging
        # print(f"x: {x_val}, y: {y_val} => x_new: {x_new_val}, y_new: {y_new_val}")

    # Wrap the final arrays in a list
    x_vals_display_robot = [x_vals_display_robot]
    y_vals_display_robot = [y_vals_display_robot]
    theta_vals_display_robot = [theta_vals_display_robot]

    # print(f"X: {x_vals_display_robot}, Y: {y_vals_display_robot}, THETA: {theta_vals_display_robot}")
    return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot




# MAIN TEST LOOP
run_animation = True

# Initialize animation window child class


def get_data():
    x_vals_real_time, y_vals_real_time, theta_vals_real_time = get_and_process_data()
    x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = map_data(
        x_vals_real_time, y_vals_real_time, theta_vals_real_time
    )
    # print(theta_vals_display_robot)
    return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot, \
        x_vals_real_time, y_vals_real_time, theta_vals_real_time


data_source = lambda: get_data()
animation_window = py_game_monitoring(850, 960, get_data)
animation_window.add_robot_character(*character)
animation_window.initialize()
# Open the file in append mode once, outside the loop




def animation_function():
    while True:
        
        animation_window.start_animation()
        
        # Assuming x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot are your data
        # writer.writerow([x_vals_display_robot[0][0], y_vals_display_robot[0][1], theta_vals_display_robot[0][5]])

def save_csv():
    # file_name = input('Type file name for the csv: ')
    x_values, y_values, theta_values = get_data()
    print(x_values, y_values, theta_values)
    with open('110923'+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        field = ["x position", "y position", "orientation"] # titles of the columns

        # Write the field names only once, not in every iteration
        writer.writerow(field)


if __name__ == "__main__":
    animation_function()