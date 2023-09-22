from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFileDialog
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
        self.fname = None
        # Load uic file
        uic.loadUi("main_gui.ui", self)

        # Define our widgets
        self.console_label = self.findChild(QLabel, "message_sim")
        self.select_world = self.findChild(QPushButton, "select_world")
        self.calculate = self.findChild(QPushButton, "calculate")
        self.save_data = self.findChild(QPushButton, "save_data")
        self.play_animation = self.findChild(QPushButton, "play_animation")

        # Define clicking actions for each of the buttons
        self.select_world.clicked.connect(self.open_world_windows)
        self.calculate.clicked.connect(self.calculate_simulation)
        self.save_data.clicked.connect(self.save_sim_data)
        self.play_animation.clicked.connect(self.play_animation_window)

        # Show the App
        self.show()

    # Methods for handling clicking actions
    def open_world_windows(self):
        self.fname = QFileDialog.getOpenFileName(self, "Choose world", worlds_dir, "JSON files (*.json)")

    def calculate_simulation(self):
        pass

    def save_sim_data(self):
        pass

    def play_animation_window(self):
        run_animation(animation_window, x_vals_display, y_vals_display, theta_vals_display)

        

# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()

