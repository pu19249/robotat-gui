import socket
import json
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
import warnings
import struct
from typing import *


class Robotat:
    """
    A class used to establish Robotat's methods to connect with server
    from compupter (client). When instanced automatically tries to
    establish the connection.

    Attributes
    ----------
    sock : sock
        socket object of type TCP
    server_address : tuple
        IP address of server and preestablished port
    robot : dict
        It holds the connection properties for the Pololu.
    """

    def __init__(self) -> None:
        self.robot = {}
        """ Attemps socket creation and connection with server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ("192.168.50.200", 1883)

        self.sock.connect(self.server_address)
        self.sock.settimeout(1)
        print("Connecting to %s port %s" % self.server_address)
        try:
            self.sock.connect(self.server_address)
            self.sock.settimeout(1)
            self.sock.recv(2048)
        except:
            print("No response from server")
            quit()

    def robotat_disconnect(self):
        """Sends command to server to close the connection."""
        self.sock.sendall(self.sock, b"EXIT")
        print("Disconnected from Robotat Server.")

    def get_pose_continuous(self, agents_ids: list[int], rotrep: str, max_attempts: int = 10):
        """Yields marker's pose.

        Args:
        ----------
        agents_id : int
            Receives the marker ID placed on the Pololu physically.
        rotrep : str
            Specifies the type of orientation to work with.
        max_attemps : int
            Specify a different number of maximum attempts to fetch marker's pose
            default is 10 attempts
        """
        for attempt in range(max_attempts):
            try:
                if min(agents_ids) > 0 and max(agents_ids) <= 100:
                    s = {"dst": 1, "cmd": 1, "pld": agents_ids}

                    self.sock.send(json.dumps(s).encode())
                    data_str = self.sock.recv(2048)
                    mocap_data = json.loads(data_str)

                    mocap_data = np.array(mocap_data)
                    num_agents = len(agents_ids)
                    mocap_data = mocap_data.reshape(num_agents, 7)

                    if rotrep != "quat":
                        quat_columns = mocap_data[:, 3:]
                        euler_angles = R.from_quat(quat_columns).as_euler(
                            "xyz", degrees=True
                        )
                        mocap_data[:, 3:] = np.rad2deg(euler_angles)
                        mocap_data = mocap_data[:, :-1]

                    yield mocap_data
                    break

                else:
                    print("ERROR: Invalid ID(s).")

            except socket.timeout:
                print("Timeout count:", attempt + 1)
                time.sleep(0.1)

        yield None

    def robotat_3pi_connect(self, agent_id: int):
        """Establishes TCP connection with Pololu's ESP32.

        Args:
        ----------
        agent_id : int
            Receives the marker ID placed on the Pololu physically.
        """

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
            robot_connection = self.sock.connect((ip, port))
        except Exception as e:
            print(f"ERROR: Could not connect to the robot. {e}")

        self.robot = {"ip": ip, "id": id, "port": port, "tcpsock": robot_connection}

    def robotat_3pi_disconnect(self):
        """Deletes robot connection."""
        del self.robot
        print("Disconnected from robot.")

    def robotat_3pi_set_wheel_velocities(self, dphiL: float, dphiR: float):
        """
        Sends left wheel velocity and right wheel velocity to Pololu's ESP32.

        Attributes:
        -------------
        dphil : float
        dphiR : float
            Right and left wheel velocities in rpm.

        Raises:
        ------------
        Warning when any of the wheels velocities is over max accepted (+/- 850 rpm).
        """
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

        self.sock.send(self.robot.tcpsock, cbormsg)

    def robotat_3pi_force_stop(self):
        """
        Sets left wheel velocity and right wheel velocity to 0.
        """
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

        self.sock.send(self.robot.tcpsock, cbormsg)

    def get_and_process_data(self, marker: int):
        """
        It calls the generator method 'get_pose_continuous' and
        iterates over the object to get the data and be able to extract
        position and orientation results.
        """
        while 1:
            for pose_data in self.get_pose_continuous([marker], "quat", max_attempts=5):
                if pose_data is not None:
                    print(f"Marker {marker}: {pose_data[0][0]}")
                else:
                    break
            time.sleep(0.5)


# Uso
# robotat = robotat_connect()
# robotat.recv(2048)

# while(1):
#     for pose_data in get_pose_continuous(robotat, [1], 'quat', max_attempts=5):
#         if pose_data is not None:
#             print(pose_data)
#         else:
#             break
#     time.sleep(0.5)

# Create threads for each marker
# marker1_thread = threading.Thread(target=get_and_process_data, args=(1,))
# marker2_thread = threading.Thread(target=get_and_process_data, args=(17,))

# # Start the threads
# marker1_thread.start()
# marker2_thread.start()


# Example usage:
# robot = robotat_3pi_connect(robotat, [6])  # Change the agent_id as needed
