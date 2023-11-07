from typing import *
import numpy as np
import pygame

# Define Pololu 3Pi+ robot class


class Pololu:
    """
    Pololu class handles the attrs related to control and simulation.
    NOTE: No img update is handled in this class, refer to windows/animation_window
    """

    # Function to initialize attrs
    def __init__(
        self,
        state: List[float],
        physical_params: List[float],
        ID: int,
        IP: str,
        img_path: str,
        controller: str,
    ):
        """
        Attributes:
        ---------------
        state : list[float]
            The list consists of x, y, theta (also referred as xi = xi(1), xi(2), xi(3)).
        physical_params : list[float]
            distance between wheels, wheel radius, max speed left, max speed right
        ID : int
            Actual Pololu's ID (physically pasted on the robot).
        IP : str
            Actual ESP32's IP (can be found on the robot, run an Arduino code to find it,
            or build it from ID). In the case of Robotat, is statically defined.
        img_path : str
            Picture used to represent the Pololu (pictures directory).
        controller : str
            Controller name that will be used in the lambda function.
        """
        self.state = state
        self.physical_params = physical_params
        self.ID = ID
        self.IP = IP
        self.img_path = img_path
        self.img = None
        self.img_rect = None
        self.controller = controller

        # Initialize arrays to store simulation values
        self.N = None
        self.XI = None
        self.U = None
        self.X = None
        self.Y = None
        self.Theta = None

        self.steps = None  # To store the number of steps taken during the simulation
        self.simulated = (
            False  # To indicate if the simulation has been performed or not
        )
        # To store the simulation results (X, Y, Theta)
        self.simulation_results = None
        self.velocities_simulation_results = None

    def dynamics(self, state: list[float], u: list[float]):
        """
        Function to define the systems dynamics (unicycle model).

        Attributes:
        ---------------
        state : list[float]
            x, y, theta
        u : list[float]
            Receives a list of type [v, w]

        Returns:
        ---------------
        f : list
            Function to evaluate state and input to make simulation
        """
        f = [u[0] * np.cos(state[2]), u[0] * np.sin(state[2]), u[1]]
        return f

    def control(self, goal: list[float], state: list[float]):
        """
        Function 'prototype' to receive control function
        and the pass it to the lambda handler.

        Attributes:
        ------------
        goal: list[float]
            Expects a list specifying x goal and y goal

        Returns:
        -------------
        u: numpy.ndarray
            [v, w]
        v, w
        """
        u = self.controller(state, goal)

        return u

    def initialize_image(self):
        """
        It gets img_path and loads it using pygame funcionts.
        """
        # Load the img and make the background transparent
        self.img = pygame.image.load(self.img_path).convert_alpha()
        # Resize the image to a suitable size
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.img_rect = self.img.get_rect()

    def update_state(self, dt, f, u):
        """
        The state of the system is updated by means of a discretization by the Runge-Kutta method (RK4).
        """
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
        # Transforms it back to the expected value type for the other methods.
        self.state = xi.tolist()

    # goal should be defined as [xg, yg]
    def simulate_robot(self, dt: float, t0: int, tf: int, goal: list[float]):
        """
        Takes simulation parameters to get position and orientation data for the
        cllass.
        Attributes:
        ------------
        dt: float
            Sampling period.
        t0: int
        tf: int
            Initial and ending time for the simulation.

        Returns:
        -------------
        self.X, self.Y, self.Theta: numpy.ndarray
            It's necessary to access this values with return
            to grab data in another script running this method directly.x
        """
        # simulation params
        N = int((tf - t0) / dt)

        # arrays to store state variables trajectories, inputs, and system outputs
        self.XI = np.zeros((len(self.state), N + 1))
        self.U = np.zeros((2, N + 1))

        # initialize trajectory arrays
        self.X = np.zeros(N + 1)
        self.Y = np.zeros(N + 1)
        self.Theta = np.zeros(N + 1)
        self.V = np.zeros(N + 1)
        self.W = np.zeros(N + 1)
        # arrays initialization
        self.XI[:, 0] = self.state

        self.initialize_image()  # Load the robot's image

        for n in range(N):
            u = self.control(goal, self.state)
            self.update_state(dt, self.dynamics, u)
            # used to check in individual test
            # print(f"Step {n}: State = {self.state}")

            # store the state variables trajectories and inputs
            self.XI[:, n + 1] = self.state
            u1 = u.tolist()
            self.U[:, n + 1] = u1
            # Store the values of position and orientation
            self.V[n + 1] = u1[0]
            self.W[n + 1] = u1[1]
            self.X[n + 1] = self.state[0]
            self.Y[n + 1] = self.state[1]
            self.Theta[n + 1] = self.state[2]

        self.steps = N + 1  # Store the number of steps taken during the simulation
        self.simulated = True  # Mark the simulation as completed
        # Store the simulation results
        self.simulation_results = (self.X, self.Y, self.Theta)
        self.velocities_simulation_results = (self.V, self.W)
        # Return the state and input arrays
        return self.X, self.Y, self.Theta

    def get_simulation_results(self):
        """
        Function definition to get self.X, self.Y, self.Theta in a
        tuple all at once.
        """
        if not self.simulated:
            raise ValueError("Simulation not performed yet.")
        return self.simulation_results
    
    def get_velocities_results(self):
        return self.velocities_simulation_results
    
    def get_number_of_steps(self):
        if not self.simulated:
            raise ValueError("Simulation not performed yet.")
        return self.steps

    # Add a method to update the robot's position in the animation loop
    def update_position(self, x, y, theta):
        self.state = [x, y, theta]
