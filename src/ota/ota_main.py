# Call the platformio project that has the initalization

# Prepare each of the ESP32 of the robots selected

# Choose whether to load data from simulation or another file to upload


import sys
import os
import subprocess
import time
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal, QRunnable

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from ota.wifi_connect import NetworkManager

class Worker_prepare_esp_for_update(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        print('subiendo!')
        sketch_directory = os.path.join(
            str(Path(__file__).parent), "esp32dev_ota_prepare"
        )
        compile_result = subprocess.Popen(
            ["platformio", "run", "--target", "upload", "--environment", "esp32dev"],
            cwd=sketch_directory,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        for line in compile_result.stdout:
            self.progress.emit(line.strip())

        compile_result.stdout.close()
        compile_result.kill()
        if compile_result.returncode != 0:
            self.progress.emit("Compilation failed")#, compile_result.stderr)
            # exit(1)
        else:
            self.progress.emit("ESP32 ready to receive")
        compile_result.kill()

        
        self.finished.emit()


class Worker_load_sketch(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, file_path, parent=None):
        super(Worker_load_sketch, self).__init__(parent)
        self.file_path = file_path

        # Initialize NetworkManager and configure network parameters
        self.NetWork = NetworkManager()
        self.Robotat_SSID = "Robotat"
        self.Robotat_Password = "iemtbmcit116"
        # self.Robotat_SSID = "TIGO-F4CD"
        # self.Robotat_Password = "4NJ667300826"
        self.NetWork.define_network_parameters(self.Robotat_SSID, self.Robotat_Password)
    def init_connection(self):
        if not self.NetWork.is_connected_to_network():
            print("Not connected to Robotat")
            print("Connecting ...")
            self.NetWork.create_new_connection(self.Robotat_SSID)
            self.NetWork.connect(self.Robotat_SSID)
            connected = True
            print("Connected to ", self.Robotat_SSID)
            retries_connection = 0
            retries_update = 0
            max_retries_connection = 3
            max_retries_update = 3
            while connected == False and retries_connection != max_retries_connection:
                print("Retrying connection")
                time.sleep(3)
                self.NetWork.connect(self.Robotat_SSID)
                retries_connection += 1
                connected = True
                print("Connected to ", self.Robotat_SSID)
    
    def run(self):
        self.init_connection()
        sketch_directory = os.path.join(
            str(Path(__file__).parent), self.file_path
        )
        print(sketch_directory)
        compile_result = subprocess.Popen(
            ["platformio", "run", "--target", "upload", "--environment", "esp32ota"],
            cwd=sketch_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        
        for line in compile_result.stdout:
            self.progress.emit(line.strip())

        compile_result.stdout.close()
        compile_result.kill()
        if compile_result.returncode != 0:
            self.progress.emit("Compilation failed")#, compile_result.stderr)
            # exit(1)
        else:
            self.progress.emit("ESP32 ready to receive")
        compile_result.kill()

        
        self.finished.emit()

