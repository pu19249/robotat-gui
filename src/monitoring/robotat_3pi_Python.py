import socket
import json
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
import warnings
import struct
import sys
import threading
import random
import os
import ctypes
import queue
# This solves scaling issues for the independent pygame window
ctypes.windll.user32.SetProcessDPIAware()

# sys.path.append('C:\\Users\\jpu20\\Documents\\robotat-gui\\src')
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from windows.animation_window import *
from robotat_3pi_Python import *
from windows.map_coordinates import inverse_change_coordinates, change_coordinates


pictures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pictures')
xtemp = 100
ytemp = 100
data_queue = queue.Queue()


def robotat_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.50.200', 1883)

    print("Connecting to %s port %s" % server_address)
    try:
        sock.connect(server_address)
        sock.settimeout(1)
    except:
        print('No response from server')
        quit()
    return sock

def robotat_disconnect(tcp_obj):
    tcp_obj.sendall(tcp_obj, b'EXIT')
    print('Disconnected from Robotat Server.')

def get_pose_continuous(tcp_obj, agents_ids, rotrep, max_attempts=10):
    # tcp_obj.settimeout(1)
    #tcp_obj.recv(2048)
    for attempt in range(max_attempts):
        try:
            #print("DEB1")
            #print(len(tcp_obj.recv(2048)))
            
            if min(agents_ids) > 0 and max(agents_ids) <= 100:
                s = {
                    "dst": 1,
                    "cmd": 1,
                    "pld": agents_ids
                }

                tcp_obj.send(json.dumps(s).encode())
                data_str = tcp_obj.recv(2048)
                mocap_data = json.loads(data_str)

                mocap_data = np.array(mocap_data)
                num_agents = len(agents_ids)
                mocap_data = mocap_data.reshape(num_agents, 7)

                if rotrep != 'quat':
                    try:
                        euler_angles = np.rad2deg(R.from_quat(mocap_data[:, 3:]).as_euler('xyz', degrees=True))
                        mocap_data[:, 3:6] = euler_angles
                        mocap_data = mocap_data[:, :-1]
                    except ValueError as e:
                        print("Invalid Euler angle sequence:", e)


                yield mocap_data
                break

            else:
                print('ERROR: Invalid ID(s).')
                

        except socket.timeout:
            print("Timeout count:", attempt + 1)
            time.sleep(0.1)
            

    #print("Reached maximum number of attempts. Exiting.")
    yield None


def robotat_3pi_connect(tcp_obj, agent_id):
    if len(agent_id) != 1:
        raise ValueError('Can only pair with a single 3Pi agent.')

    agent_id = agent_id[0]
    if (agent_id < 0) or (agent_id > 19):
        raise ValueError('Invalid agent ID. Allowed IDs: 0 - 19.')

    id = agent_id

    if agent_id > 9:
        ip = '192.168.50.1'
    else:
        ip = '192.168.50.10'

    ip = f"{ip}{agent_id}"
    port = 8888
    
    
    try:
        robot_connection = tcp_obj.connect((ip, port))
    except Exception as e:
        print(f'ERROR: Could not connect to the robot. {e}')
    
    robot = {
        "ip": ip,
        "id": id,
        "port": port,
        "tcpsock": robot_connection
    }
    return robot


def robotat_3pi_disconnect(robot):
    del robot
    print('Disconnected from robot.')


def robotat_3pi_set_wheel_velocities(tcp_obj, robot, dphiL, dphiR):
    wheel_maxvel_rpm = 850
    wheel_minvel_rpm = -850
    
    if(dphiL > wheel_maxvel_rpm):
        message = f"Left wheel speed saturated to  {wheel_maxvel_rpm} rpm"
        warnings.warn(message)
        dphiL = wheel_maxvel_rpm
    

    if(dphiR > wheel_maxvel_rpm):
        message = f"Right wheel speed saturated to  {wheel_maxvel_rpm} rpm"
        warnings.warn(message)
        dphiR = wheel_maxvel_rpm
    

    if(dphiL < wheel_minvel_rpm):
        message = f"Left wheel speed saturated to  {wheel_minvel_rpm} rpm"
        warnings.warn(message)
        dphiL = wheel_minvel_rpm
    

    if(dphiR < wheel_minvel_rpm):
        message = f"Right wheel speed saturated to  {wheel_minvel_rpm} rpm"
        warnings.warn(message)
        dphiR = wheel_minvel_rpm
    

    # encode to a simple CBOR array
    cbormsg = np.zeros((1,11))
    cbormsg[0] = 130
    cbormsg[1] = 250
    # Convert to bytes
    dphiL_bytes = struct.pack('f', dphiL)
    # Extract the first byte (8-bit unsigned integer)
    dphiL_uint8 = dphiL_bytes[0]
    cbormsg[2:5] = np.fliplr(dphiL_uint8)
    cbormsg[6] = 250
    dphiR_bytes = struct.pack('f', dphiR)
    # Extract the first byte (8-bit unsigned integer)
    dphiR_uint8 = dphiR_bytes[0]
    cbormsg[7:10] = np.fliplr(dphiR_uint8)
    
    tcp_obj.send(robot.tcpsock, cbormsg)

def robotat_3pi_force_stop(tcp_obj, robot):
    dphiL = 0
    dphiR = 0
    # encode to a simple CBOR array
    cbormsg = np.zeros((1,11))
    cbormsg[0] = 130
    cbormsg[1] = 250
    # Convert to bytes
    dphiL_bytes = struct.pack('f', dphiL)
    # Extract the first byte (8-bit unsigned integer)
    dphiL_uint8 = dphiL_bytes[0]
    cbormsg[2:5] = np.fliplr(dphiL_uint8)
    cbormsg[6] = 250
    dphiR_bytes = struct.pack('f', dphiR)
    # Extract the first byte (8-bit unsigned integer)
    dphiR_uint8 = dphiR_bytes[0]
    cbormsg[7:10] = np.fliplr(dphiR_uint8)
    
    tcp_obj.send(robot.tcpsock, cbormsg)

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


x_test = [[10,20]]
y_test = [[30,40]]
theta_test = [[50,60]]

# Prepare data as the animation window expects it (list of lists for each x, y, theta for each robot) according to how its received from the server (list of x, y, orientation)
def get_and_process_data():
    for pose_data in get_pose_continuous(robotat, [11], 'eulxyz', max_attempts=5):
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
        
        # animation_window.start_animation(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
        # time.sleep(0.5)
        break
    
    return x_vals_real_time, y_vals_real_time, theta_vals_real_time

def map_data(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
    x_vals_display_robot = []
    y_vals_display_robot = []
    theta_vals_display_robot = []
    # this part makes the mapping to display in the complete animation window 
    for x, y, theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
        # for x_val, y_val, theta_val in zip(x, y, theta):
        x_raw, y_raw = x, y
        x_new_val, y_new_val = inverse_change_coordinates(x_raw*100, y_raw*100, 960, 760)
            
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

# animation_window.animate(x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot)

def real_time_data_generator(num_robots):
    while True:
        x_values = [[random.randint(0, 100) for _ in range(num_robots)]]
        y_values = [[random.randint(0, 100) for _ in range(num_robots)]]
        theta_values = [[random.uniform(0, 2 * 3.14159265359) for _ in range(num_robots)]]
        yield x_values, y_values, theta_values




# MAIN TEST LOOP
run_animation = True

x_values = [1]
y_values = [1]
theta_values = [1]
# Initialize animation window child class

def get_data():
    
    # time.sleep(0.3)
    # x_values[0] += 1
    # y_values[0] += 1
    # theta_values[0] += 1
    # map_data(x_values, y_values, theta_values)
    x_vals_real_time, y_vals_real_time, theta_vals_real_time = get_and_process_data()
    x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = map_data(x_vals_real_time, y_vals_real_time, theta_vals_real_time)
    
    return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot

data_source = lambda: get_data()
animation_window = py_game_monitoring(850, 960, xtemp, ytemp, get_data)
animation_window.add_robot_character(*character)
animation_window.initialize()
while True:
    # x_values, y_values, theta_values = get_data()
    animation_window.start_animation()
    # print(x_values, y_values, theta_values)


# MAIN TEST LOOP
# if __name__ == "__main__":
#     run_animation = True


#     while run_animation == True:
#         print(x_values, y_values, theta_values)
#         animation_window.start_animation([x_values], [y_values], [theta_values])

        # # Update robot positions based on received data
        # for i in range(len(animation_window.robot_characters)):
        #     x_robot = x_values[0][i]
        #     y_robot = y_values[0][i]
        #     theta_robot = theta_values[0][i]
        #     animation_window.robot_characters[i].update(theta_robot, x_robot, y_robot)
        #     animation_window.robot_characters[i].rotate_move()

        # Update the data for the next iteration
        

        
        # run_animation = False
# Uso
# Uso
# robotat = robotat_connect()
# robotat.recv(2048)

# while(1): 
#     for pose_data in get_pose_continuous(robotat, [11], 'eulxyz', max_attempts=5):
#         if pose_data is not None:
#             print(pose_data)
#         else:
#             break
#     time.sleep(1)

# def get_and_process_data(marker):
#     while(1):
#         for pose_data in get_pose_continuous(robotat, [marker], 'quat', max_attempts=5):
#             if pose_data is not None:
#                 print(f"Marker {marker}: {pose_data[0][0]}")
#             else:
#                 break
#         time.sleep(0.5)

# Example usage:
# robot = robotat_3pi_connect(robotat, [6])  # Change the agent_id as needed