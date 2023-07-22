from typing import *
import math
import numpy as np
from PyQt5.QtGui import QPixmap
# Define Pololyu 3Pi + robot class


class Pololu:
    # Function to initialize attrs
    def __init__(self, state: List[float], physical_params:
                 List[float], ID: float, IP: float, img: str, controller):
        self.state = state
        self.physical_params = physical_params
        self.ID = ID
        self.IP = IP
        # self.img = QPixmap(img) if img else None
        self.img = img  # to make tests in a individual script
        self.controller = controller

        # Initialize arrays
        self.N = None
        self.XI = None
        self.U = None
        self.X = None
        self.Y = None
        self.Theta = None

        self.steps = None  # To store the number of steps taken during the simulation
        self.simulated = False  # To indicate if the simulation has been performed or not
        # To store the simulation results (X, Y, Theta)
        self.simulation_results = None

    '''
    List of state receives x, y, bearing
    List of physical parameters receives: l, r, vel_left max, vel_right max
    '''
    # Methods definition

    def dynamics(self, state, u):
        f = [u[0]*np.cos(state[2]), u[0]*np.sin(state[2]), u[1]]
        return f

    def control(self, goal, state):
        u = self.controller(state, goal)
        return u

    def goal_def(self, xg, yg):
        # make the needed converesions to fit the canvas
        # define the dimension of the given value (m, mm, etc)
        return xg, yg

    def update_state(self, dt, f, u):
        # the state of the system is updated by means of a discretization by the Runge-Kutta method (RK4)
        xi = np.array(self.state)
        k1 = f(xi, u)
        k2 = f(xi + np.multiply(dt / 2, k1), u)
        k3 = f(xi + np.multiply(dt / 2, k2), u)
        k4 = f(xi + np.multiply(dt, k3), u)

        k1 = np.reshape(k1, xi.shape)
        k2 = np.reshape(k2, xi.shape)
        k3 = np.reshape(k3, xi.shape)
        k4 = np.reshape(k4, xi.shape)

        xi = xi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        self.state = xi.tolist()

    # goal should be defined as [xg, yg]
    def simulate_robot(self, dt, t0, tf, goal):
        # simulation params
        N = int((tf - t0) / dt)

        # arrays to store state variables trajectories, inputs, and system outputs
        self.XI = np.zeros((len(self.state), N + 1))
        self.U = np.zeros((2, N + 1))

        # initialize trajectory arrays
        self.X = np.zeros(N + 1)
        self.Y = np.zeros(N + 1)
        self.Theta = np.zeros(N + 1)
        # arrays initialization
        self.XI[:, 0] = self.state

        for n in range(N):
            u = self.control(goal, self.state)
            self.update_state(dt, self.dynamics, u)
            # Example: Print the state in each step
            # used to check in individual test
            # print(f"Step {n}: State = {self.state}")

            # store the state variables trajectories and inputs
            self.XI[:, n+1] = self.state
            self.U[:, n+1] = u
            # Store the values of position and orientation
            self.X[n + 1] = self.state[0]
            self.Y[n + 1] = self.state[1]
            self.Theta[n + 1] = self.state[2]

        self.steps = N + 1  # Store the number of steps taken during the simulation
        self.simulated = True  # Mark the simulation as completed
        # Store the simulation results
        self.simulation_results = (self.X, self.Y, self.Theta)
        # Return the state and input arrays
        return self.X, self.Y, self.Theta

    def get_simulation_results(self):
        if not self.simulated:
            raise ValueError("Simulation not performed yet.")
        return self.simulation_results

    def get_number_of_steps(self):
        if not self.simulated:
            raise ValueError("Simulation not performed yet.")
        return self.steps
