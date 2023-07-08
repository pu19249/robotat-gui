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
        f = [u[0]*np.cos(state[2]), u[0]*np.sin(state[2]), u[1]]
        return f

    def control(self):
        u = self(params)
        return u

    def update_state(self, dt, f, u, ini_cond, n):
        XI = ini_cond[0]
        U = ini_cond[1]
        k1 = f(xi, u)
        k2 = f(xi + np.multiply(dt / 2, k1), u)
        k3 = f(xi + np.multiply(dt / 2, k2), u)
        k4 = f(xi + np.multiply(dt, k3), u)

        k1 = np.reshape(k1, xi.shape)
        k2 = np.reshape(k2, xi.shape)
        k3 = np.reshape(k3, xi.shape)
        k4 = np.reshape(k4, xi.shape)

        xi = xi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x = xi[0]
        y = xi[1]
        theta = xi[2]
        XI[:, n + 1] = xi
        U[:, n + 1] = u
        q = XI[:, n]
        x = q[0]
        y = q[1]
        theta = q[2]

        return x, y, theta, xi

    def simulate_robot(self):
        
