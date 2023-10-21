"""
This test file is not editable in terms of controller. It does not reflect
the functionality of physical parameters, IP, or any other. This script
was used to validate basic simulation flow and runge kutta simulation
and it plots using matplotlib instead of pygame that is the current use for
animation handling.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from robots.robot_pololu import Pololu

# Robot object definitions
Robot1 = Pololu([0.0, 0.0, 0.0], [0.01, 0.5, 100, 100], 1, "1.1", "path", "controller")
script_dir = os.path.dirname(os.path.abspath(__file__))
pictures_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures"
)
# Simulation parameters
dt = 0.001  # sample period
t0 = 0  # initial time
tf = 10  # final time
N = int((tf - t0) / dt)  # iteration number, convert to integer

# Initial conditions
xi0 = np.array([0, 0, 0])
u0 = np.array([0, 0])
xi = xi0  # state vector
u = u0  # input vector

# Arrays to store state, inputs, and outputs
XI = np.zeros((len(xi), N + 1))
U = np.zeros((len(u), N + 1))

# Initialize arrays
XI[:, 0] = xi0
U[:, 0] = u0

# Target coordinates
xg = -2  # in m
yg = 3  # in m
thetag = 0  # in rad

# Trajectory
seltraj = 0
t = np.arange(t0, tf + dt, dt)
traj = 2 * np.array([np.cos(0.1 * 2 * np.pi * t), np.sin(0.1 * 2 * np.pi * t)])

# PID position
kpP = 1
kiP = 0.0001
kdP = 0.5
EP = 0
eP_1 = 0

# PID orientation
kpO = 2 * 5
kiO = 0.0001
kdO = 0
EO = 0
eO_1 = 0

# Exponential approach
v0 = 10
alpha = 1

for n in range(N):
    if seltraj:
        xg = traj[0, n + 1]
        yg = traj[1, n + 1]

    x = xi[0]
    y = xi[1]
    theta = xi[2]
    e = np.array([xg - x, yg - y])
    thetag = np.arctan2(e[1], e[0])

    eP = np.linalg.norm(e)
    eO = thetag - theta
    eO = np.arctan2(np.sin(eO), np.cos(eO))

    kP = v0 * (1 - np.exp(-alpha * eP**2)) / eP
    v = kP * eP

    eO_D = eO - eO_1
    EO = EO + eO
    w = kpO * eO + kiO * EO + kdO * eO_D
    eO_1 = eO

    u = np.array([v, w])

    k1 = Robot1.dynamics(xi, u)
    k2 = Robot1.dynamics(xi + np.multiply(dt / 2, k1), u)
    k3 = Robot1.dynamics(xi + np.multiply(dt / 2, k2), u)
    k4 = Robot1.dynamics(xi + np.multiply(dt, k3), u)

    k1 = np.reshape(k1, xi.shape)
    k2 = np.reshape(k2, xi.shape)
    k3 = np.reshape(k3, xi.shape)
    k4 = np.reshape(k4, xi.shape)

    xi = xi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    XI[:, n + 1] = xi
    U[:, n + 1] = u

# Figure 1 - Plotting the state variables over time
fig1, ax1 = plt.subplots()
t = np.arange(t0, tf + dt, dt)
ax1.plot(t, XI.T, linewidth=1)
ax1.set_xlabel("$t$", fontsize=16)
ax1.set_ylabel("$\\mathbf{x}(t)$", fontsize=16)
l = ax1.legend(["$x(t)$", "$y(t)$", "$\\theta(t)$"], loc="best", prop={"size": 12})
ax1.grid(True, which="minor")
ax1.grid(True, which="major")
plt.show()

# Figure 2 - Robot animation
figure2 = plt.figure()
# Set appropriate limits for x and y axes
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
plt.grid(True, which="minor")
plt.grid(True, which="major")

# Plotting the trajectory if applicable
if seltraj:
    plt.plot(traj[0, :], traj[1, :], "k")

(trajplot,) = plt.plot([], [], "--k", linewidth=1)
# Load the robot image
robot_image = plt.imread(os.path.join(pictures_dir, "pololu_img.png"))
robotplot = plt.imshow(robot_image, extent=(-0.15, 0.15, -0.15, 0.15))


plt.xlabel("$x$", fontsize=16)
plt.ylabel("$y$", fontsize=16)


def update_plot(n):
    q = XI[:, n]
    x = q[0]
    y = q[1]
    theta = q[2]

    trajplot.set_data(
        np.append(trajplot.get_xdata(), x), np.append(trajplot.get_ydata(), y)
    )

    BV = np.array([[-0.1, 0, 0.1], [0, 0.3, 0]])
    IV = np.dot(
        [
            [np.cos(theta - np.pi / 2), -np.sin(theta - np.pi / 2)],
            [np.sin(theta - np.pi / 2), np.cos(theta - np.pi / 2)],
        ],
        BV,
    )

    # Update the vertices of the polygon
    robotplot.set_extent((x - 1, x + 1, y - 1, y + 1))

    return trajplot, robotplot


# Update the FuncAnimation call
animation_variable = animation.FuncAnimation(
    figure2, update_plot, frames=N + 1, interval=dt * 10
)

plt.show()