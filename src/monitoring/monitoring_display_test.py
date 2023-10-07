import sys
sys.path.append('C:\\Users\\jpu20\\Documents\\robotat-gui\\src')

from windows.animation_window import *
from robotat_3pi_Python import *


# Establish connection with Robotat
robotat = robotat_connect()
robotat.recv(2048)
animation_window = py_game_animation(850, 960)
# Get real time data
# while(1): 
for pose_data in get_pose_continuous(robotat, [7], 'quat', max_attempts=5):
    if pose_data is not None:
        print(pose_data)
    x_vals_real_time = pose_data[0]
    y_vals_real_time = pose_data[1]
    theta_vals_real_time = pose_data[2]
    print("x: {x_vals_real_time}, y: {y_vals_real_time}, theta: {theta_vals_real_time}")

    animation_window.update_robot_characters(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
    animation_window.animate(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
    animation_window.start_animation(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
    # else:
    #     break
time.sleep(0.5)