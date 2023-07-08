from typing import *
import math
import numpy as np
from PyQt5.QtGui import QPixmap
# Define Pololyu 3Pi + robot class


class Pololu:
    # Function to initialize attrs
    def __init__(self, state: List[float], physical_params:
                 List[float], ID: float, IP: float, img: str, controller: str, u):
        self.state = state
        self.physical_params = physical_params
        self.ID = ID
        self.IP = IP
        self.img = QPixmap(img) if img else None
        self.controller = controller

    '''
    List of state receives x, y, bearing
    List of physical parameters receives: l, r, vel_left max, vel_right max
    '''
    # Methods definition

    def dynamics(self, state, u):
        return [u[0]*np.cos(state[2]), u[0]*np.sin(state[2]), u[1]]

    def set_controller(self, controller):
        # Update the controller attribute
        self.controller = controller
