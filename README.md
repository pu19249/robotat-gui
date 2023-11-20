# Robotat GUI - Alpha

![Robotat Logo](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

This project aims to establish the foundation for developing a full desktop application to simulate robots on the robotics experimentation platform of Universidad del Valle de Guatemala, Robotat. The first version establishes a structure to simulate Pololu 3Pi+ mobile robots, program the ESP32 controlling various functions of the Pololu (including establishing a connection with 'Robotat's' server), and monitoring the Pololu's pose on the test table of the Robotat. The goal is to create a complete experimentation flow with the Pololu 3Pi+.

**Table of Contents**

- [Features](###features)
- [System Requirements](###system-requirements)
- [Repository Structure](###repository-structure)
- [Dependencies](###dependencies)
- [How to Run the Code](###how-to-run-the-code)

### Features

- The project sets up the structure to simulate robots (Pololu 3Pi+) using the Pygame library, JSON format to define simulation scenarios, and a GUI tab to set some user input/output options.
- It defines the structure to edit the main code of the ESP32 running control functions of the Pololu 3Pi+ using OTA updates on the Robotat's WiFi network.
- It establishes basic functions to monitor data from the server related to the Pololu; for now, the data that can be obtained is the pose based on the marker mounted over the Pololu.
- It explores some basic implementations of ROS2 and micro-ROS on the ESP32 and a computer running Ubuntu.

### System requirements
This project was developed in Windows OS (except micro-ROS module which was developed on Ubuntu Linux). The following software is needed:
- Python 3.11 (Python 3.11.4 was used for this version, if you will change Python's version, check compatibility of modules imported as some functionalities may vary - not too much but it can be a parting point to debug if some library is not working as expected).
- Visual Studio Code
- PlatformIO IDE extension for Visual Studio Code
### Repository Structure

Here's an overview of the project's file structure:

- **`docs`**: This folder contains documentation related to the project, including video demos showcasing the GUI functionality. The content is organized into subfolders:

  - **`recordings`**: Video recordings demonstrating the usage and features of the GUI, Pololu's movement on Robotat's platform, and screen recordings of a display updating based on the movement of Optitrack's markers on the testbed.
  - **`screenshots`**: Screenshots capturing different aspects of the GUI for reference.
  - **`robotat_3pi_MATLAB`**: Source code from which the functions to connect to Robotat's server were ported. They work as a reference and also to debug changes that want to be made to Python's functions.
  - **`images`**: These images are not used directly in the code but were used to generate some of them in draw.io, such as the background image and Pololu image.
  - **`guidelines`**: This folder contains some guides generated relevant to the project, such as the usage of the GUI, implementation of OTA on ESP32. Keep all the guidelines generated in the future in this folder.
  - *Other Files*: Additional documentation or files relevant to the project.

- **`microros`**: This directory holds all the source files required for working with ROS2 and micro-ROS on an ESP32. It's designed for development on the Ubuntu operating system.

  - **`esp32_ros_test`**: It contains the PlatformIO project for the ESP32 with micro-ROS functions.
  - **`listener_node_ros.py`**: It contains the source file to run the listener node on Python (refer to the explanation in the Thesis document to understand the usage, requirements, and implementation of this folder).

- **`src`**: This directory is dedicated to the source code of the project, housing implementations for the three main features. Within this folder, you'll find the following subdirectories:
  - **`pictures`**: This contains the pictures that are referenced in some part of the code, if you want to include new pictures please keep them in this folder as the code will navigate to this file to look for the pictures' imports.
  - **`robots`**: For now, the only robot defined is the Pololu on it's own class, future robots would be placed here.
  - **`controllers`**: Here are the .py files with the controllers' definitions for the robots, all the code in which the name of the controller is used will look for the controller in this folder.
  - **`monitoring`**: It contains the Python functions to establish the connection from the computer to the server, and obtain the pose from the marker. It contains a .py to run individual monitoring without running the GUI.
  - **`ota`**: It contains functions to establish connection with the WiFi network, and classes to run OTA functions from the GUI. It has some other subfolders:
    - **`tests`**: It contains .py to run OTA updates without the GUI, Arduino OTA tests, and PlatformIO projects to run OTA tests.
	- **`esp32dev_ota_prepare`**: This is the base file to prepare the ESP32 to receive OTA updates serially.
	- **`esp32ota_ota_update`**:  This is the base file for the new code for the ESP32 running OTA updates, control, and Optitrack connection from the ESP32.
  - **`windows`**: It has the class for the animation window used both in simulation and monitoring. It also has some other useful functions for the correct display of the animation.
  - **`worlds`**: Please write all the JSON scenarios for simulation in this folder.
  - **`tests_py`**: It has some basic tests on of two simulations.
  - **`ui_files`**: It has the .ui files generated from PyQt5 drag and drop designer for each tab.
  - *Other Files*: Additional source files, utilities, or configurations relevant to the main features.

### Dependencies
The project depends on multiple Python modules, please follow these steps to clone the repository:
1. Clone the repository on your local computer.
2. Create a Python virtual environment.
3. Run the following command after activating the venv:

```bash
python -m pip install -r requirements.txt
```
### How to run the code
One of the main cores of this project and using Python was to keep everything as modular, maintainable and replicable as possible, you should not encounter problems on the imports nor in the references to images and submodules as each script in which it was needed, relative imports were used. If you still encounter issues on an image or module not found, please check the structure of folders and that you are running the code on the virtual environment and from the Windows cmd (it's not recommended to run the main code from VSCode built-in terminal as some libraries are not recognized correctly). This version of the code is not yet an executable file so to run the main script (GUI) please follow the following commands on the terminal:
```bash
cd <env_name>/Scripts && activate.bat && cd ../../src
python maingui.py
```
