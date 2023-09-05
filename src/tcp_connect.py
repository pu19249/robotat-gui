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


    # s = {
    #     "dst": 1,  # DST robotat
    #     "cmd": 1,  # cmd get pose
    #     }
    # json_str = json.dumps(s) # Python equivalent to MATLAB's write(tcp_obj...)
    # byte_value = json_str.encode('utf-8')
        
    # sock.sendall(byte_value)
        
    # Receive and decode data from the server
    # received_data = sock.recv(2048)  # Adjust buffer size as needed
    # print(received_data) #connection verification

        # Close the socket connection
    # if sock.close() == True:
    #     print('Connection closed')

    return sock


def get_pose(tcp_obj, agents_ids, rotrep):
    timeout_count = 0
    timeout_in100ms = 1 / 0.1
    tcp_obj.recv(2048)
    print(min(agents_ids))
    
    if ((min(agents_ids) > 0) and (max(agents_ids) <= 100)):
        s = {
            "dst": 1,  # DST robotat
            "cmd": 1,  # cmd get pose
            "pld": agents_ids
        }

        tcp_obj.send(json.dumps(s).encode())
        
        data_str = tcp_obj.recv(2048)
        print(data_str)
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
    else:
        print('ERROR: Invalid ID(s).')

    return mocap_data

# Assuming you have a valid 'robotat_connect' function
robotat = robotat_connect()
print(type(robotat))
pose1 = get_pose(robotat, [2], 'quat')

print(pose1)