# from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFileDialog
from PyQt5 import uic
import sys
import os
from main_for_gui import *
import json
from windows.animation_window import py_game_animation, robot_character
from robots.robot_pololu import Pololu
from controllers.exponential_pid import exponential_pid
from controllers.pid_controller import pd_controller
from controllers.lqi import lqi_controller
from windows.map_coordinates import inverse_change_coordinates
import numpy as np
import pygame
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import random
from PyQt5.QtWidgets import *


# define Worlds directory
# Get the directory path of the current script, abspath because of the tree structure that everything is on different folders
script_dir = os.path.dirname(os.path.abspath(__file__))
worlds_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src/worlds')
print(worlds_dir)

# Define a dictionary to map controller names to controller functions
controller_map = {
    'exponential_pid': exponential_pid,
    'pd_controller': pd_controller,
    'lqi_controller': lqi_controller
}

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load uic file
        # uic.loadUi("main_gui.ui", self)
        # Create and add tabs
        # Set the size of the main window
        self.resize(1121, 741)
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
        self.y_results_plt  = None
        self.theta_vals_display = None
        self.selected_robot = None
        # Load uic file
        uic.loadUi("simulator_tab.ui ", self)
        
        # Define our widgets
        self.console_label = self.findChild(QLabel, "message_sim")
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
        self.state_display.toggled.connect(lambda:self.btnstate(self.state_display))
        

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
        self.fname = QFileDialog.getOpenFileName(self, "Choose world", worlds_dir, "JSON files (*.json)")
        if self.fname:
            self.world = load_world(self.fname[0])  # Extract the file path from the tuple
        self.no_robots = self.world['no_robots']
        print(self.no_robots)
        # Clear existing items in the ComboBox
        self.robot_graph_selection.clear()
        
        # Add items to the ComboBox based on the number of robots
        for i in range(self.no_robots):
            self.robot_graph_selection.addItem(f'Robot {i+1}')

    def update_plot(self):
        self.selected_robot = self.robot_graph_selection.currentIndex()  # Get the selected index
        self.plot_simulation()

    def plot_simulation(self):
        t0 = self.world['t0']
        tf = self.world['tf']
        dt = self.world['dt']

        if any(var is None for var in (self.x_results_plt, self.y_results_plt, self.theta_vals_display)):
            # Data is not available, return without plotting
            return
        self.MplWidget.canvas.axes.clear()  # Clear the previous plot
        self.MplWidget.canvas.axes.grid()
        num_results = self.x_results_plt.shape[0]  # Assuming all robots have the same number of results
        t = np.linspace(t0, tf, num_results)
        if (self.variables_to_display == "State"):
            # Plot the selected robot's state variables
            self.MplWidget.canvas.axes.plot(t, self.x_results_plt[:, self.selected_robot], label=f'Robot {self.selected_robot+1} - x')
            self.MplWidget.canvas.axes.plot(t, self.y_results_plt[:, self.selected_robot], label=f'Robot {self.selected_robot+1} - y')
            self.MplWidget.canvas.axes.plot(t, self.theta_vals_display[:, self.selected_robot], label=f'Robot {self.selected_robot+1} - theta')

            self.MplWidget.canvas.axes.legend(loc='upper right')
            self.MplWidget.canvas.axes.set_title(f'Variables de estado para Robot {self.selected_robot+1}')
            self.MplWidget.canvas.draw()

        elif (self.variables_to_display == "Velocities"):
            # Plot the selected robot's velocities
            self.MplWidget.canvas.axes.plot(t, self.x_results_plt[:, self.selected_robot], label=f'Robot {self.selected_robot+1} - linear velocity')
            self.MplWidget.canvas.axes.plot(t, self.y_results_plt[:, self.selected_robot], label=f'Robot {self.selected_robot+1} - angular velocity')
            

            self.MplWidget.canvas.axes.legend(loc='upper right')
            self.MplWidget.canvas.axes.set_title(f'Velocidades para Robot {self.selected_robot+1}')
            self.MplWidget.canvas.draw()



    def save_sim_data(self):
        pass

    def play_animation_window(self):
        # Show the animation window
        self.animation_window = initialize_animation(self.world)
        # Create objects
        self.robots, self.pololu = create_objects(self.world, self.animation_window)
        self.x_vals_display, self.y_vals_display, self.theta_vals_display, self.x_results_plt, self.y_results_plt = calculate_simulation(self.world, self.robots, self.pololu)
        run_animation(self.animation_window, self.x_vals_display, self.y_vals_display, self.theta_vals_display)

    # def hide_show(self):


class ota_tab(QWidget):
    def __init__(self):
        super(ota_tab, self).__init__()
        # Load uic file
        uic.loadUi("simulator_tab.ui ", self)

class monitoring_tab(QWidget):
    def __init__(self):
        super(monitoring_tab, self).__init__()
        # Load uic file
        uic.loadUi("simulator_tab.ui ", self)

# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()

