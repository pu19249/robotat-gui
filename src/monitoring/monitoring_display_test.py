import sys
sys.path.append('C:\\Users\\jpu20\\Documents\\robotat-gui\\src')

from windows.animation_window import *
from robotat_3pi_Python import *
from windows.map_coordinates import inverse_change_coordinates

import threading
import time
pictures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pictures')
animation_window = py_game_animation(850, 960)
# animation_window.start_animation
animation_window.initialize()
# robotat = robotat_connect()
# robotat.recv(2048)
x_data = []
y_data = []
theta_data = []

# First we need to create the object that represents and updates the position and rotation of the Pololu img (first one robot only)
character = (os.path.join(pictures_dir, "pololu_img_x.png"), 0, 0, 0) 
animation_window.add_robot_character(*character)
x_test = [[10,20]]
y_test = [[30,40]]
theta_test = [[50,60]]
x_vals_display_robot = []
y_vals_display_robot = []
theta_vals_display_robot = []
x_results_raw = []
y_results_raw = []

# this part makes the mapping to display in the complete animation window 
for x, y, theta in zip(x_test, y_test, theta_test):
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

animation_window.animate(x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot)



# def get_and_process_data():
#     for pose_data in get_pose_continuous(robotat, [1], 'quat', max_attempts=5):
#         # if pose_data is not None:
#         #     print(pose_data)
#         # else:
#         #     print('no data')
#         x_vals_real_time = [pose_data[0][0]]
#         y_vals_real_time = [pose_data[0][1]]
#         theta_vals_real_time = [pose_data[0][2]]
#         x_data.append(x_vals_real_time)
#         y_data.append(y_vals_real_time)
#         theta_data.append(theta_vals_real_time)
#         print(f"x: {x_vals_real_time}, y: {y_vals_real_time}, theta: {theta_vals_real_time}")

#         # animation_window.start_animation(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
#         time.sleep(0.5)
#         return x_vals_real_time, y_vals_real_time, theta_vals_real_time

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
