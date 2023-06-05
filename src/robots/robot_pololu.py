from typing import *
import math
import numpy as np

# Define Pololyu 3Pi + robot class

class Pololu:
    # Function to initialize attrs
    def __init__(self, state: List[float], physical_params: \
                 List[float], ID: float, IP: float, img, controller, u):
        self.state = state
        self.physical_params = physical_params
        self.ID = ID
        self.IP = IP
        self.img = img
        self.controller = controller
    '''
    List of state receives x, y, bearing
    List of physical parameters receives: l, r, vel_left max, vel_right max
    '''
    # Methods definition
    def dynamics(self, state, u):
        return [u[0]*np.cos(state[2]), u[0]*np.sin(state[2]), u[1]]


