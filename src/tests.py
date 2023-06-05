# Code to run a simulation of point-to-point PID
import numpy as np
import matplotlib.pyplot as plt
from robots.robot_pololu import Pololu


# Robot object definitions
Robot1 = Pololu([0.0,0.0,0.0], [0.01, 0.5, 100, 100], 6.0, 1.1, 0, 0, 0)

