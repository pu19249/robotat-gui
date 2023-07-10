from typing import *
import math
import numpy as np
from PyQt5.QtGui import QPixmap
# Define Pololyu 3Pi + robot class


class Pololu:
    # Function to initialize attrs
    def __init__(self, state: List[float], physical_params:
                 List[float], ID: float, IP: float, img: str, controller, u):
        self.state = state
        self.physical_params = physical_params
        self.ID = ID
        self.IP = IP
        self.img = QPixmap(img) if img else None
        self.controller = controller

        # Initialize arrays
        self.N = None
        self.XI = None
        self.U = None
        self.X = None
        self.Y = None
        self.Theta = None

    '''
    List of state receives x, y, bearing
    List of physical parameters receives: l, r, vel_left max, vel_right max
    '''
    # Methods definition

    def dynamics(self, state, u):
        f = [u[0]*np.cos(state[2]), u[0]*np.sin(state[2]), u[1]]
        return f

    def control(self):
        u = self.controller(self.state)
        return u

    def goal_def(self, xg, yg):
        # make the needed converesions to fit the canvas
        # define the dimension of the given value (m, mm, etc)
        return xg, yg

    def update_state(self, dt, f, u):
        # the state of the system is updated by means of a discretization bythe Runge-Kutta method (RK4)
        xi = self.state
        k1 = f(xi, u)
        k2 = f(xi + np.multiply(dt / 2, k1), u)
        k3 = f(xi + np.multiply(dt / 2, k2), u)
        k4 = f(xi + np.multiply(dt, k3), u)

        k1 = np.reshape(k1, xi.shape)
        k2 = np.reshape(k2, xi.shape)
        k3 = np.reshape(k3, xi.shape)
        k4 = np.reshape(k4, xi.shape)

        xi = xi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        # return x, y, theta, xi

    def simulate_robot(self, dt, t0, tf, ini_cond):
        # simulation params
        N = int((tf - t0) / dt)

        # initial conditions and arrays initialization
        xi0 = [0, 0, 0]  # state vector
        xi = xi0
        u0 = [0, 0]  # input vector
        u = u0
        # arrays to store state variables trajectories, inputs, and system outputs
        XI = np.zeros((len(xi), N + 1))
        U = np.zeros((len(u), N + 1))
        # arrays initialization
        XI[:, 0] = xi0
        U[:, 0] = u0

        for n in range(N):
            u = self.control()
            self.update_state(dt, self.dynamics, u, ini_cond, n)
            # Example: Print the state in each step
            print(f"Step {n}: State = {self.state}")
            # Store the values of position and orientation
            self.X[n + 1] = self.XI[0, n + 1]
            self.Y[n + 1] = self.XI[1, n + 1]
            self.Theta[n + 1] = self.XI[2, n + 1]

        # Return the state and input arrays
        return self.X, self.Y, self.Theta
