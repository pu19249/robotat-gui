# from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFileDialog
from PyQt5 import uic
import sys
import os
from main_for_gui import *
import json
from windows.animation_window import py_game_animation, robot_character
from robots.robot_pololu import Pololu
from controllers.exponential_pid import exponential_pid
from controllers.pid_controller import pid_controller
from controllers.lqi import lqi_controller
from windows.map_coordinates import inverse_change_coordinates
import numpy as np
import pygame
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
from PyQt5.QtWidgets import *
from ota.ota_main import *
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QThreadPool, QRunnable
from PyQt5 import QtGui
import subprocess
from pathlib import Path
import chardet

# define Worlds directory
# Get the directory path of the current script, abspath because of the tree structure that everything is on different folders
script_dir = os.path.dirname(os.path.abspath(__file__))
worlds_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src/worlds"
)
# print(worlds_dir)

IP_sim = [] 
controller_sim = []
TAG_sim = []
goal_x = []
goal_y = []


# Define a dictionary to map controller names to controller functions
controller_map = {
    "exponential_pid": exponential_pid,
    "pid_controller": pid_controller,
    "lqi_controller": lqi_controller,
}

# Define a dictionary to handle possible errors in try except blocks
error_dict = {
    1: "Seleccionar el mundo JSON a cargar antes de ejecutar otras acciones.",
    2: "Error: Another specific error message",
    3: "Hubo colisión entre los robots o con el borde la de la plataforma.",
    4: "No hay parámetros que guardar aún. Por favor seguir el orden recomendado de pasos."
    # Add more error codes and messages as needed
}



class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load uic file
        # uic.loadUi("main_gui.ui", self)
        # Create and add tabs
        # Set the size of the main window
        self.setFixedSize(1121, 741)
        self.setWindowIcon(QtGui.QIcon("pictures/Logo UVG-06.png"))
        self.setWindowTitle("ROBOTAT")
        self.tab_widget = QTabWidget()

        self.tab1_simulation = simulator_tab()
        self.tab2_ota = ota_tab()
        self.tab3_monitoring = monitoring_tab()
        self.tab_widget.addTab(self.tab1_simulation, "Simulador")
        self.tab_widget.addTab(self.tab2_ota, "Programador")
        self.tab_widget.addTab(self.tab3_monitoring, "Monitoreo")
        self.setCentralWidget(self.tab_widget)
        self.show()


class simulator_tab(QWidget):
    def __init__(self):
        super(simulator_tab, self).__init__()
        self.fname = None
        self.world = None
        self.robots = None
        self.pololu = None
        self.animation_window = None
        self.x_results_plt = None
        self.y_results_plt = None
        self.theta_vals_display = None
        self.selected_robot = None
        self.v = None
        self.w = None
        # Load uic file
        uic.loadUi("simulator_tab.ui ", self)

        # Define our widgets
        self.console_label = self.findChild(QLabel, "message_sim")
        self.console_label.setWordWrap(True)
        self.select_world = self.findChild(QPushButton, "select_world")
        self.plot = self.findChild(QPushButton, "plot")
        self.save_data = self.findChild(QPushButton, "save_data")
        self.play_animation = self.findChild(QPushButton, "play_animation")
        self.robot_graph_selection = self.findChild(QComboBox, "robot_graph_selection")
        self.state_display = self.findChild(QRadioButton, "state")
        self.velocities_display = self.findChild(QRadioButton, "velocities")

        # Define clicking actions for each of the buttons
        self.select_world.clicked.connect(self.open_world_windows)
        self.plot.clicked.connect(self.plot_simulation)
        self.save_data.clicked.connect(self.save_sim_data)
        self.play_animation.clicked.connect(self.play_animation_window)
        self.robot_graph_selection.currentIndexChanged.connect(self.update_plot)
        self.state_display.setChecked(True)
        self.state_display.toggled.connect(lambda: self.btnstate(self.state_display))

        # Define global flags
        self.variables_to_display = "State"
        # Show the App
        # self.show()

    # Methods for handling clicking actions
    def btnstate(self, b):
        if b.isChecked():
            self.variables_to_display = "State"
        else:
            self.variables_to_display = "Velocities"

    def open_world_windows(self):
        try:

            self.fname = QFileDialog.getOpenFileName(
                self, "Choose world", worlds_dir, "JSON files (*.json)"
            )
            if self.fname:
                self.world = load_world(
                    self.fname[0]
                )  # Extract the file path from the tuple
            self.no_robots = self.world["no_robots"]
            # print(self.no_robots)
            # Clear existing items in the ComboBox
            self.robot_graph_selection.clear()

            # Add items to the ComboBox based on the number of robots
            for i in range(self.no_robots):
                self.robot_graph_selection.addItem(f"Robot {i+1}")

        except:
            error_code = 1  # You can determine the error code based on the exception
            error_message = error_dict.get(error_code, "Unknown error")
            self.console_label.setText(error_message)

    def update_plot(self):
        self.selected_robot = (
            self.robot_graph_selection.currentIndex()
        )  # Get the selected index
        self.plot_simulation()

    def plot_simulation(self):
        t0 = self.world["t0"]
        tf = self.world["tf"]
        dt = self.world["dt"]
        


        if any(
            var is None
            for var in (self.x_results_plt, self.y_results_plt, self.theta_vals_display)
        ):
            # Data is not available, return without plotting
            return
        self.MplWidget.canvas.axes.clear()  # Clear the previous plot
        self.MplWidget.canvas.axes.grid()
        num_results = self.x_results_plt.shape[
            0
        ]  # Assuming all robots have the same number of results
        t = np.linspace(t0, tf, num_results)
        if self.variables_to_display == "State":
            # Plot the selected robot's state variables
            self.MplWidget.canvas.axes.plot(
                t,
                self.x_results_plt[:, self.selected_robot],
                label=f"Robot {self.selected_robot+1} - x",
            )
            self.MplWidget.canvas.axes.plot(
                t,
                self.y_results_plt[:, self.selected_robot],
                label=f"Robot {self.selected_robot+1} - y",
            )
            self.MplWidget.canvas.axes.plot(
                t,
                self.theta_vals_display[:, self.selected_robot],
                label=f"Robot {self.selected_robot+1} - theta",
            )

            self.MplWidget.canvas.axes.legend(loc="upper right")
            self.MplWidget.canvas.axes.set_title(
                f"Variables de estado para Robot {self.selected_robot+1}"
            )
            self.MplWidget.canvas.draw()

        elif self.variables_to_display == "Velocities":
            # Plot the selected robot's velocities
            self.MplWidget.canvas.axes.plot(
                t,
                self.v[:, self.selected_robot],
                label=f"Robot {self.selected_robot+1} - linear velocity",
            )
            self.MplWidget.canvas.axes.plot(
                t,
                self.w[:, self.selected_robot],
                label=f"Robot {self.selected_robot+1} - angular velocity",
            )

            self.MplWidget.canvas.axes.legend(loc="upper right")
            self.MplWidget.canvas.axes.set_title(
                f"Velocidades para Robot {self.selected_robot+1}"
            )
            self.MplWidget.canvas.draw()

    def save_sim_data(self):
        try:
            robots = self.world["robots"]

            for i in range(len(robots)):
                IP_sim.append(robots[i].get('IP'))
                TAG_sim.append(robots[i].get('TAG'))
                controller_sim.append(robots[i].get('controller'))
                goal_x.append(robots[i].get('goal_x'))
                goal_y.append(robots[i].get('goal_y'))
        except:
            error_code = 4  # You can determine the error code based on the exception
            error_message = error_dict.get(error_code, "Unknown error")
            self.console_label.setText(error_message)

    def play_animation_window(self):
        # Show the animation window
        try:
            self.animation_window = initialize_animation(self.world)
            # Create objects
            self.robots, self.pololu = create_objects(self.world, self.animation_window)
            (
                self.x_vals_display,
                self.y_vals_display,
                self.theta_vals_display,
                self.x_results_plt,
                self.y_results_plt,
                self.v,
                self.w,
            ) = calculate_simulation(self.world, self.robots, self.pololu)
            run_animation(
                self.animation_window,
                self.x_vals_display,
                self.y_vals_display,
                self.theta_vals_display,
            )
            if self.animation_window.index_error == 3:
                error_code = (
                    self.animation_window.index_error
                )  # You can determine the error code based on the exception
                error_message = error_dict.get(error_code, "Unknown error")
                self.console_label.setText(error_message)
        except:
            self.console_label.setText(
                "Seleccionar el mundo JSON de simulación primero."
            )

    # def hide_show(self):


class ota_tab(QWidget):
    def __init__(self):
        super(ota_tab, self).__init__()
        # Load uic file
        uic.loadUi("ota_tab.ui ", self)
        self.fname = None
        # self.thread1 = prepare_esp_for_update()
        # self.thread2 = load_sketch(self.fname)
        # Define our widgets
        self.status_label = self.findChild(QLabel, "status_mssg")
        self.status_label.setWordWrap(True)
        self.from_simulator = self.findChild(QRadioButton, "from_simulator")
        self.from_new_sketch = self.findChild(QRadioButton, "from_new_sketch")
        self.code_preview = self.findChild(QTextBrowser, "code_preview")
        # SIMULATOR GROUP
        self.simulator_group = self.findChild(QGroupBox, "simulator_group")
        self.data_from_sim = self.findChild(QPushButton, "data_from_sim")
        self.prepare_esp_sim = self.findChild(QPushButton, "prepare_esp_sim")
        self.update_from_sim = self.findChild(QPushButton, "update_from_sim")
        self.number_robot = self.findChild(QComboBox, "number_robot")
        # NEW SKETCH GROUP
        self.new_sketch_group = self.findChild(QGroupBox, "new_sketch_group")
        self.ip_list = self.findChild(QComboBox, "ip_list")
        self.tag_list = self.findChild(QComboBox, "tag_list")
        self.load_new_sketch = self.findChild(QPushButton, "load_new_sketch")
        self.prepare_esp32 = self.findChild(QPushButton, "prepare_esp32")
        self.search_new_sketch = self.findChild(QPushButton, "search_new_sketch")

        #
        self.progress_bar_group = self.findChild(QGroupBox, "progress_bar_group")

        # Define clicking actions for each of the buttons
        self.new_sketch_group.setVisible(False)
        self.from_simulator.setChecked(True)
        self.from_simulator.toggled.connect(lambda: self.btnstate(self.from_simulator))
        self.search_new_sketch.clicked.connect(self.sketch_browser)
        self.prepare_esp32.clicked.connect(self.prepare_esp32_funct)
        self.load_new_sketch.clicked.connect(self.upload_esp32_funct)
        self.data_from_sim.clicked.connect(self.data_from_sim_params)

        # geek list
        ip_list = [
            "192.168.50.101",
            "192.168.50.102",
            "192.168.50.103",
            "192.168.50.104",
            "192.168.50.105",
            "192.168.50.106",
            "192.168.50.107",
            "192.168.50.108",
            "192.168.50.109",
        ]

        tag_list = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ]

        # adding list of items to combo box
        self.ip_list.addItems(ip_list)
        self.tag_list.addItems(tag_list)

    # Methods for handling clicking actions
    def btnstate(self, b):
        if b.isChecked():
            self.status_label.setText("Se cargará data del JSON de simulación.")
            self.simulator_group.setVisible(True)
            self.new_sketch_group.setVisible(False)
            # Add robots number according to simulation data
            self.number_robot.clear()
            for number in enumerate(IP_sim):
                self.number_robot.addItem(f"{number[0]}")

        else:
            self.status_label.setText(
                "Recordar presionar el botón de Boot del ESP32 durante el proceso de preparación. \nData de un nuevo sketch \nRevisar los requisitos del nuevo sketch."
            )
            # self.status_label.setText('Revisar los requisitos del nuevo sketch.')
            self.new_sketch_group.setVisible(True)
            self.simulator_group.setVisible(False)

    def sketch_browser(self):
        self.fname = QFileDialog.getExistingDirectory(self, "Choose platformio project")
        if self.fname:  # Check if a folder was selected
            print(f"Selected folder: {self.fname}")
        # IP and TAG value is also loaded (goal x, goal y and other controller no because it's supposed to be
        # specified in the intended sketch) - based on that TAG selection the angle should be added


    def prepare_esp32_funct(self):
        self.thread = QThread()
        self.worker = Worker_prepare_esp_for_update()
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateLabel)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.prepare_esp32.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.prepare_esp32.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.status_label.setText("Ejecutando proceso de carga serial.")
        )



    def updateLabel(self, output):
        self.code_preview.clearHistory()
        self.code_preview.append(output)

    def upload_esp32_funct(self):
        self.thread = QThread()
        self.worker = Worker_load_sketch(self.fname)
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateLabel)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.load_new_sketch.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.load_new_sketch.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.status_label.setText("Ejecutando proceso de carga OTA.")
        )

    def data_from_sim_params(self):

        self.selected_robot_sim = (
        self.number_robot.currentIndex()
    )  # Get the selected index
        print(self.selected_robot_sim)
        print(TAG_sim[self.selected_robot_sim])
        # Now based on the current index that value from the lists will be gotten to update the .c files
        self.modify_ota_update_file()
    
    def modify_ota_update_file(self):
        with open("ota/esp32ota_sim/src/main.cpp", 'rb') as file:
            result1 = chardet.detect(file.read())
        file_encoding = result1['encoding']
        with open("ota/esp32ota_sim/src/main.cpp", 'r', encoding=file_encoding) as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if "const unsigned robot_id =" in line:
                # based on this TAG the angle should be added (in radians)
                lines[i] = f" const unsigned robot_id = {TAG_sim[self.selected_robot_sim]};\n"
            elif "float goal_x = " in line:
                lines[i] = f" float goal_x = {goal_x[self.selected_robot_sim]};\n"
            elif "float goal_y = " in line:
                lines[i] = f" float goal_y = {goal_y[self.selected_robot_sim]};\n"
        with open("ota/esp32ota_sim/src/main.cpp", 'w', encoding=file_encoding) as file:
            file.writelines(lines)

        with open("ota/esp32ota_sim/platformio.ini", 'rb') as file:
            result2 = chardet.detect(file.read())
        file_encoding = result2['encoding']
        with open("ota/esp32ota_sim/platformio.ini", 'rb') as file:
            result = chardet.detect(file.read())
        file_encoding = result['encoding']
        with open("ota/esp32ota_sim/platformio.ini", 'r', encoding=file_encoding) as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if "upload_port = " in line:
                lines[i] = f"upload_port = {IP_sim[self.selected_robot_sim]} \n"
            
        with open("ota/esp32ota_sim/platformio.ini", 'w', encoding=file_encoding) as file:
            file.writelines(lines)

class monitoring_tab(QWidget):
    def __init__(self):
        super(monitoring_tab, self).__init__()
        # Load uic file
        uic.loadUi("monitoring_tab.ui ", self)


# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
UIWindow.show()

app.exec_()
