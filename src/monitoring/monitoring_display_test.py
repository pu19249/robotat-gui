import sys
import threading
import time
import random
import os
# sys.path.append('C:\\Users\\jpu20\\Documents\\robotat-gui\\src')
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from windows.animation_window import *
from robotat_3pi_Python import *
from windows.map_coordinates import inverse_change_coordinates


pictures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pictures')

# Initialize animation window child class
animation_window = py_game_animation(760, 960)
animation_window.initialize()

# Connect to robotat
robotat = robotat_connect()
robotat.recv(2048)
# robotat = Robotat()


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
animation_window.add_robot_character(*character)

x_test = [[10,20]]
y_test = [[30,40]]
theta_test = [[50,60]]

# Prepare data as the animation window expects it (list of lists for each x, y, theta for each robot) according to how its received from the server (list of x, y, orientation)
def get_and_process_data():
    for pose_data in get_pose_continuous(robotat, [19], 'quat', max_attempts=5):
        # if pose_data is not None:
        #     print(pose_data)
        # else:
        #     print('no data')
        print(pose_data)
        x_vals_real_time = [pose_data[0][0]]
        y_vals_real_time = [pose_data[0][1]]
        theta_vals_real_time = [pose_data[0][2]]
        x_data.append(x_vals_real_time)
        y_data.append(y_vals_real_time)
        theta_data.append(theta_vals_real_time)
        print(f"x: {x_vals_real_time}, y: {y_vals_real_time}, theta: {theta_vals_real_time}")

        # animation_window.start_animation(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
        time.sleep(1)
    return x_vals_real_time, y_vals_real_time, theta_vals_real_time

def map_data(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
    # this part makes the mapping to display in the complete animation window 
    for x, y, theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
        for x_val, y_val, theta_val in zip(x, y, theta):
            x_raw, y_raw = x_val, y_val
            x_new_val, y_new_val = inverse_change_coordinates(x_val, y_val, 960, 760)
            
            theta_new_val = np.rad2deg(theta_val)  # theta_val, not just theta
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
    
    return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot

# animation_window.animate(x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot)

def real_time_data_generator(num_robots):
    while True:
        x_values = [[random.randint(0, 100) for _ in range(num_robots)]]
        y_values = [[random.randint(0, 100) for _ in range(num_robots)]]
        theta_values = [[random.uniform(0, 2 * 3.14159265359) for _ in range(num_robots)]]
        yield x_values, y_values, theta_values




# MAIN TEST LOOP
run_animation = True
# while run_animation == True:
    # data_generator = real_time_data_generator(1)
    # animation_window.start_animation(data_generator)
x_vals_real_time, y_vals_real_time, theta_vals_real_time = get_and_process_data()
x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = map_data(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
animation_window.start_animation((x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot))
run_animation = False

# while(1):
#     x_vals_real_time, y_vals_real_time, theta_vals_real_time = get_and_process_data()
# def start_animation(x_data, y_data, theta_data):
#     # Add code to start animation here
#     animation_window.update_robot_characters(x_data, y_data, theta_data)
#     animation_window.animate(x_data, y_data, theta_data)

# # Create a thread for data retrieval and processing
# data_thread = threading.Thread(target=get_and_process_data)

# # Start the data thread
# data_thread.start()

# # Retrieve the values from get_and_process_data
# x_vals, y_vals, theta_vals = get_and_process_data()

# # Start the animation with the retrieved values
# start_animation(x_vals, y_vals, theta_vals)

# # Wait for the data thread to finish (if necessary)
# data_thread.join()
