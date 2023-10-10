import sys
sys.path.append('C:\\Users\\jpu20\\Documents\\robotat-gui\\src')

from windows.animation_window import *
from robotat_3pi_Python import *

import threading
import time

animation_window = py_game_animation(850, 960)
animation_window.start_animation
animation_window.initialize()
robotat = robotat_connect()
robotat.recv(2048)
x_data = []
y_data = []
theta_data = []

def get_and_process_data():
    for pose_data in get_pose_continuous(robotat, [1], 'quat', max_attempts=5):
        # if pose_data is not None:
        #     print(pose_data)
        # else:
        #     print('no data')
        x_vals_real_time = [pose_data[0][0]]
        y_vals_real_time = [pose_data[0][1]]
        theta_vals_real_time = [pose_data[0][2]]
        x_data.append(x_vals_real_time)
        y_data.append(y_vals_real_time)
        theta_data.append(theta_vals_real_time)
        print(f"x: {x_vals_real_time}, y: {y_vals_real_time}, theta: {theta_vals_real_time}")

        # animation_window.start_animation(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
        time.sleep(0.5)
        return x_vals_real_time, y_vals_real_time, theta_vals_real_time

def start_animation(x_data, y_data, theta_data):
    # Add code to start animation here
    animation_window.update_robot_characters(x_data, y_data, theta_data)
    animation_window.animate(x_data, y_data, theta_data)

# Create a thread for data retrieval and processing
data_thread = threading.Thread(target=get_and_process_data)

# Start the data thread
data_thread.start()

# Retrieve the values from get_and_process_data
x_vals, y_vals, theta_vals = get_and_process_data()

# Start the animation with the retrieved values
start_animation(x_vals, y_vals, theta_vals)

# Wait for the data thread to finish (if necessary)
data_thread.join()
