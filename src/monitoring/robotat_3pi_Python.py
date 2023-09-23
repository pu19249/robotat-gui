import socket
import json
import time
import numpy as np
from scipy.spatial.transform import Rotation as R

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
                    quat_columns = mocap_data[:, 3:]
                    euler_angles = R.from_quat(quat_columns).as_euler('xyz', degrees=True)
                    mocap_data[:, 3:] = np.rad2deg(euler_angles)
                    mocap_data = mocap_data[:, :-1]

                yield mocap_data
                break

            else:
                print('ERROR: Invalid ID(s).')
                

        except socket.timeout:
            print("Timeout count:", attempt + 1)
            time.sleep(0.1)
            

    print("Reached maximum number of attempts. Exiting.")
    yield None

# Uso
robotat = robotat_connect()
robotat.recv(2048)

while(1): 
    for pose_data in get_pose_continuous(robotat, [7], 'quat', max_attempts=5):
        if pose_data is not None:
            print(pose_data)
        else:
            break
    time.sleep(0.5)
