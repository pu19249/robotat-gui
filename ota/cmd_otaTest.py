# import subprocess
# import os

# # Ruta completa al directorio del sketch "ota-blinking-firstTest"
# sketch_directory = os.path.join(os.getcwd(), "ota-blinking-firstTest")

# # Compilar y generar el binario del sketch
# subprocess.run(["arduino-cli", "compile", "--fqbn", "esp32:esp32:esp32", sketch_directory])

# # Ruta completa al binario del firmware
# firmware_binary = os.path.join(sketch_directory, "ota-blinking-firstTest.bin")

# # Dirección IP del ESP32
# esp_ip = "192.168.50.211"

# # Detectar dispositivos ESP32 en la red
# device_list = subprocess.check_output(["esptool", "--port", "auto", "--baud", "115200", "nmap"], universal_newlines=True).split("\n")
# selected_device = ""

# for device in device_list:
#     if esp_ip in device:
#         selected_device = device.split()[0]
#         break

# if selected_device:
#     # Actualizar OTA
#     subprocess.run(["esptool", "--port", "tcp://" + selected_device, "--baud", "921600", "write_flash", "--flash_size", "detect", "0", firmware_binary])
#     print("Actualización completada.")
# else:
#     print("No se encontró el dispositivo en la red.")





# import subprocess
# import os

# # Ruta completa al directorio del sketch "ota-blinking-firstTest"
# sketch_directory = os.path.join(os.getcwd(), "ota-blinking-firstTest")

# # Compilar y generar el binario del sketch
# subprocess.run(["arduino-cli", "compile", "--fqbn", "esp32:esp32:esp32", sketch_directory])

# # Ruta completa al binario del firmware
# firmware_binary = os.path.join(sketch_directory, "ota-blinking-firstTest.ino.bin")

# # Dirección IP del ESP32
# esp_ip = "192.168.0.10"

# # Actualizar OTA usando esptool.py
# subprocess.run(["esptool.py", "--chip", "esp32", "--port", "tcp://" + esp_ip, "--baud", "921600", "write_flash", "--flash_size", "detect", "0", firmware_binary])

# print("Actualización completada.")


# import subprocess
# import os

# # Ruta completa al directorio del sketch "ota-blinking-firstTest"
# sketch_directory = os.path.join(os.getcwd(), "ota-secondTest")

# # Compilar y generar el binario del sketch
# compile_result = subprocess.run(["arduino-cli", "compile", "--fqbn", "esp32:esp32:esp32", sketch_directory], capture_output=True, text=True)
# if compile_result.returncode != 0:
#     print("Compilation failed:", compile_result.stderr)
#     exit(1)

# # Search for the .ino.bin file in the sketch directory
# firmware_binary = os.path.join(sketch_directory, ".pio\\build\esp32doit-devkit-v1\\firmware.bin")
# print(firmware_binary)
# if not os.path.exists(firmware_binary):
#     print("Firmware binary not found.")
#     exit(1)

# # Dirección IP del ESP32
# esp_ip = "192.168.0.10"

# # Actualizar OTA usando esptool.py
# subprocess.run(["esptool.py", "--chip", "esp32", "--port", "tcp://" + esp_ip, "--baud", "921600", "write_flash", "--flash_size", "detect", "0", firmware_binary])

# print("Actualización completada.")


import subprocess
import os


# Replace this with the path to your sketch directory
sketch_directory = os.path.join(os.getcwd(), "ota-secondTest")

# Replace "esp32doit-devkit-v1" with the correct environment name
compile_result = subprocess.run(["platformio", "run", "--target", "upload", "--environment", "esp32dev"], cwd=sketch_directory, capture_output=True, text=True)
if compile_result.returncode != 0:
    print("Compilation failed:", compile_result.stderr)
    exit(1)

print("OTA update completed.")
