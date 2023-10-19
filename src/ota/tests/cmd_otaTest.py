import sys
import os
import subprocess
import time
from pathlib import Path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from wifi_connect import NetworkManager

NetWork = NetworkManager()

Robotat_SSID = 'Robotat'
Robotat_Password = 'iemtbmcit116'
NetWork.define_network_parameters(Robotat_SSID, Robotat_Password)
retries_connection = 0
retries_update = 0
max_retries_connection = 3
max_retries_update = 3

if not NetWork.is_connected_to_network():
    print('Not connected to Robotat')
    print('Connecting ...')
    NetWork.create_new_connection(Robotat_SSID)
    NetWork.connect(Robotat_SSID)
    connected = True
    print('Connected to ', Robotat_SSID)
    while connected == False and retries_connection != max_retries_connection:
        print('Retrying connection')
        time.sleep(3)
        NetWork.connect(Robotat_SSID)
        retries_connection += 1
        connected = True
        print('Connected to ', Robotat_SSID)



# Replace this with the path to your sketch directory
sketch_directory = os.path.join(str(Path(__file__).parent), "esp32ota_ota_update")
print(sketch_directory)
# Replace "esp32doit-devkit-v1" with the correct environment name
compile_result = subprocess.run(["platformio", "run", "--target", "upload", "--environment", "esp32ota"], cwd=sketch_directory, capture_output=True, text=True)

# Manages the error retrying 3 times before giving it up
if compile_result.returncode != 0:
    # this indicates the error ocurred in the .cpp file, it must be debugged manually if the script is proven to be working
    print("Compilation failed:", compile_result.stderr) 
    exit(1)


print("OTA update completed.")
