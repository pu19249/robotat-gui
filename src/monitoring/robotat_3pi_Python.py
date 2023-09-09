import socket
import sys
import json
import time
import numpy as np
from scipy.spatial.transform import Rotation as R

# Create a TCP/IP socket
def robotat_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('192.168.50.200', 1883)

    print(sys.stderr, 'connecting to %s port %s' % server_address)

    sock.connect(server_address)
    return sock # returns tcp client (socket.socket) object to be able to get info from the server as in MATLAB's tcp_obj = robotat_connect


def get_pose(tcp_obj, agents_ids, rotrep):
    timeout_count = 0
    timeout_in100ms = 1
    tcp_obj.settimeout(0.1)
    tcp_obj.recv(2048)
    print(min(agents_ids))
    
    if ((min(agents_ids) > 0) and (max(agents_ids) <= 100)):
        s = {
            "dst": 1,  # DST robotat
            "cmd": 1,  # cmd get pose
            "pld": agents_ids
        }

        tcp_obj.send(json.dumps(s).encode())

        while timeout_count < timeout_in100ms:
            try:
                data_str = tcp_obj.recv(2048)  # This will raise socket.timeout if no data is available
                mocap_data = json.loads(data_str)

                mocap_data = np.array(mocap_data)

                num_agents = len(agents_ids)
                mocap_data = mocap_data.reshape(num_agents, 7)

                if rotrep == 'quat':
                    pass
                else:
                    try:
                        quat_columns = mocap_data[:, 3:]
                        euler_angles = R.from_quat(quat_columns).as_euler('xyz', degrees=True)
                        mocap_data[:, 3:] = np.rad2deg(euler_angles)

                        mocap_data = mocap_data[:, :-1]
                    except Exception as e:
                        raise ValueError('Invalid Euler angle sequence.') from e
                break
            except socket.timeout:
                timeout_count += 1
                print("Timeout count:", timeout_count)
                # You can add additional actions or code here if needed
                time.sleep(0.1)  # Wait for the specified timeout
                print("No data available within the specified timeout.")
            
    else:
        print('ERROR: Invalid ID(s).')

    return mocap_data

# def get_pose(tcp_obj, agents_ids, rotrep):
#     timeout_count = 0
#     timeout_in100ms = 1 / 0.1
#     tcp_obj.settimeout(0.1)
#     tcp_obj.recv(2048)
#     print(min(agents_ids))
    
#     if ((min(agents_ids) > 0) and (max(agents_ids) <= 100)):
#         s = {
#             "dst": 1,  # DST robotat
#             "cmd": 1,  # cmd get pose
#             "pld": agents_ids
#         }

#         tcp_obj.send(json.dumps(s).encode())

#         while timeout_count < timeout_in100ms:
#             try:
#                 data_str = tcp_obj.recv(2048)  # This will raise socket.timeout if no data is available
#                 mocap_data = json.loads(data_str)

#                 mocap_data = np.array(mocap_data)

#                 num_agents = len(agents_ids)
#                 mocap_data = mocap_data.reshape(num_agents, 7)

#                 if rotrep == 'quat':
#                     pass
#                 else:
#                     try:
#                         quat_columns = mocap_data[:, 3:]
#                         euler_angles = R.from_quat(quat_columns).as_euler('xyz', degrees=True)
#                         mocap_data[:, 3:] = np.rad2deg(euler_angles)

#                         mocap_data = mocap_data[:, :-1]
#                     except Exception as e:
#                         raise ValueError('Invalid Euler angle sequence.') from e
#                 break
#             except socket.timeout:
#                 timeout_count += 1
#                 print("Timeout count:", timeout_count)
#                 # You can add additional actions or code here if needed
#                 time.sleep(0.1)  # Wait for the specified timeout
#                 print("No data available within the specified timeout.")
            
#     else:
#         print('ERROR: Invalid ID(s).')

#     return mocap_data

# Assuming you have a valid 'robotat_connect' function
robotat = robotat_connect()
print(type(robotat))
time_sim = 0
pose1 = get_pose(robotat, [9], 'quat') 
print(pose1)
# while time_sim < 10:
#     pose1 = get_pose(robotat, [6], 'quat') 
#     print(pose1)
#     time_sim += 0.1
#     time.sleep(0.1)
#     print(time_sim)