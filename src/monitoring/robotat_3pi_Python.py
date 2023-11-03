import socket
import json
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
import warnings
import struct
import math
from squaternion import Quaternion
def robotat_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.50.200", 1883)

    print("Connecting to %s port %s" % server_address)
    try:
        sock.connect(server_address)
        sock.settimeout(1)
    except:
        print("No response from server")
        quit()
    return sock


def robotat_disconnect(tcp_obj):
    tcp_obj.sendall(tcp_obj, b"EXIT")
    print("Disconnected from Robotat Server.")

def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

def get_pose_continuous(tcp_obj, agents_ids, rotrep, max_attempts=10):
    # tcp_obj.settimeout(1)
    # tcp_obj.recv(2048)
    for attempt in range(max_attempts):
        try:
            # print("DEB1")
            # print(len(tcp_obj.recv(2048)))

            if min(agents_ids) > 0 and max(agents_ids) <= 100:
                s = {"dst": 1, "cmd": 1, "pld": agents_ids}

                tcp_obj.send(json.dumps(s).encode())
                data_str = tcp_obj.recv(2048)
                mocap_data = json.loads(data_str)

                mocap_data = np.array(mocap_data)
                num_agents = len(agents_ids)
                mocap_data = mocap_data.reshape(num_agents, 7)

                if rotrep != "quat":
                    try:
                        euler = mocap_data[:, 3:]
                        # print('euler1', euler)
                        # print('euler2', euler[0][0], euler[0][1], euler[0][2], euler[0][3])
                        q = Quaternion(euler[0][0], euler[0][1], euler[0][2], euler[0][3])
                        eu = q.to_euler(degrees=True)
                        # roll, pitch, yaw = euler_from_quaternion(euler[0][0], euler[0][1], euler[0][2], euler[0][3])

                        # print(roll, pitch, yaw)
                        # print(eu)
                        mocap_data[:, 3:6] = eu
                        mocap_data =  mocap_data[:, :-1]
                        # print(mocap_data)
                    except ValueError as e:
                        print("Invalid Euler angle sequence:", e)
                        

                yield mocap_data
                break

            else:
                print("ERROR: Invalid ID(s).")

        except socket.timeout:
            print("Timeout count:", attempt + 1)
            time.sleep(0.1)

    # print("Reached maximum number of attempts. Exiting.")
    yield None



def robotat_3pi_connect(tcp_obj, agent_id):
    if len(agent_id) != 1:
        raise ValueError("Can only pair with a single 3Pi agent.")

    agent_id = agent_id[0]
    if (agent_id < 0) or (agent_id > 19):
        raise ValueError("Invalid agent ID. Allowed IDs: 0 - 19.")

    id = agent_id

    if agent_id > 9:
        ip = "192.168.50.1"
    else:
        ip = "192.168.50.10"

    ip = f"{ip}{agent_id}"
    port = 8888

    try:
        robot_connection = tcp_obj.connect((ip, port))
    except Exception as e:
        print(f"ERROR: Could not connect to the robot. {e}")

    robot = {"ip": ip, "id": id, "port": port, "tcpsock": robot_connection}
    return robot


def robotat_3pi_disconnect(robot):
    del robot
    print("Disconnected from robot.")


def robotat_3pi_set_wheel_velocities(tcp_obj, robot, dphiL, dphiR):
    wheel_maxvel_rpm = 850
    wheel_minvel_rpm = -850

    if dphiL > wheel_maxvel_rpm:
        message = f"Left wheel speed saturated to  {wheel_maxvel_rpm} rpm"
        warnings.warn(message)
        dphiL = wheel_maxvel_rpm

    if dphiR > wheel_maxvel_rpm:
        message = f"Right wheel speed saturated to  {wheel_maxvel_rpm} rpm"
        warnings.warn(message)
        dphiR = wheel_maxvel_rpm

    if dphiL < wheel_minvel_rpm:
        message = f"Left wheel speed saturated to  {wheel_minvel_rpm} rpm"
        warnings.warn(message)
        dphiL = wheel_minvel_rpm

    if dphiR < wheel_minvel_rpm:
        message = f"Right wheel speed saturated to  {wheel_minvel_rpm} rpm"
        warnings.warn(message)
        dphiR = wheel_minvel_rpm

    # encode to a simple CBOR array
    cbormsg = np.zeros((1, 11))
    cbormsg[0] = 130
    cbormsg[1] = 250
    # Convert to bytes
    dphiL_bytes = struct.pack("f", dphiL)
    # Extract the first byte (8-bit unsigned integer)
    dphiL_uint8 = dphiL_bytes[0]
    cbormsg[2:5] = np.fliplr(dphiL_uint8)
    cbormsg[6] = 250
    dphiR_bytes = struct.pack("f", dphiR)
    # Extract the first byte (8-bit unsigned integer)
    dphiR_uint8 = dphiR_bytes[0]
    cbormsg[7:10] = np.fliplr(dphiR_uint8)

    tcp_obj.send(robot.tcpsock, cbormsg)


def robotat_3pi_force_stop(tcp_obj, robot):
    dphiL = 0
    dphiR = 0
    # encode to a simple CBOR array
    cbormsg = np.zeros((1, 11))
    cbormsg[0] = 130
    cbormsg[1] = 250
    # Convert to bytes
    dphiL_bytes = struct.pack("f", dphiL)
    # Extract the first byte (8-bit unsigned integer)
    dphiL_uint8 = dphiL_bytes[0]
    cbormsg[2:5] = np.fliplr(dphiL_uint8)
    cbormsg[6] = 250
    dphiR_bytes = struct.pack("f", dphiR)
    # Extract the first byte (8-bit unsigned integer)
    dphiR_uint8 = dphiR_bytes[0]
    cbormsg[7:10] = np.fliplr(dphiR_uint8)

    tcp_obj.send(robot.tcpsock, cbormsg)





# Uso
# Uso
# robotat = robotat_connect()
# robotat.recv(2048)

# while(1):
#     for pose_data in get_pose_continuous(robotat, [19], 'eulxyz', max_attempts=5):
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
