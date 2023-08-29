import socket
import sys
import json
import time
import numpy as np

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.50.200', 1883)

print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    
    # Send data
    message = b'Example'
    print(sys.stderr, 'sending "%s"' % message)
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print(sys.stderr, 'received "%s"' % data)

finally:
    print(sys.stderr, 'closing socket')
    # sock.close()

# time.sleep(1)
# sock.connect(server_address)
agents_ids = [1]
timeout_count = 0
timeout_in_100ms = 1 / 0.1
mocap_data = None
rotrep = 'quat'
if 0 < min(agents_ids) <= 100:
    s = {
        "dst": 1,  # DST robotat
        "cmd": 1,  # cmd get pose
        "pld": round(agents_ids[0])
    }
    json_str = json.dumps(s)
    byte_value = json_str.encode('utf-8')
    
    # byte_value = int(json_str, 16).to_bytes((len(json_str)+1)//2,byteorder='big')
    # byte_value = json_str.encode('utf-8')
    sock.sendall(byte_value)
    
# Receive and decode data from the server
    received_data = sock.recv(1024)  # Adjust buffer size as needed
    # received_data = np.reshape(received_data, (7, len(agents_ids))).transpose

    # mocap_data = json.loads(received_data.decode('utf-8'))

    # Close the socket connection
    sock.close()

    print(received_data)



# function tcp_obj = robotat_connect(ip)
# %UNTITLED2 Summary of this function goes here
# %   Detailed explanation goes here
#     port = 1883;
#     try
#         tcp_obj = tcpclient(ip, port);
#     catch
#         disp('ERROR: Could not connect to Robotat server.');
#     end
# end