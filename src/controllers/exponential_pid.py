import numpy as np


def pid_exponential_cte():
    # PID position
    kpP = 1
    kiP = 0.0001
    kdP = 0.5
    EP = 0
    eP_1 = 0

    position_cte = [kpP, kiP, kdP, EP, eP_1]

    # PID orientation
    kpO = 10
    kiO = 0.0001
    kdO = 0
    EO = 0
    eO_1 = 0

    orientation_cte = [kpO, kiO, kdO, EO, eO_1]

    # exponential approach
    v0 = 10
    alpha = 1

    return position_cte, orientation_cte, v0, alpha


def exponential_pid(xi, goal):
    position_cte, orientation_cte, v0, alpha = pid_exponential_cte()
    kpO = orientation_cte[0]
    kiO = orientation_cte[1]
    kdO = orientation_cte[2]
    EO = orientation_cte[3]
    eO_1 = orientation_cte[4]
    # controller (this must run repeteadly with the numerical method)
    x = xi[0]
    y = xi[1]
    theta = xi[2]
    # x, y, theta = xi

    e = np.array([goal[0] - x, goal[1] - y])
    thetag = np.arctan2(e[1], e[0])

    eP = np.linalg.norm(e)
    eO = thetag - theta
    eO = np.arctan2(np.sin(eO), np.cos(eO))

    # linear velocity
    kP = v0 * (1 - np.exp(-alpha * eP ** 2)) / eP
    v = kP * eP

    # angular velocity
    eO_D = eO - eO_1
    EO = EO + eO
    w = kpO * eO + kiO * EO + kdO * eO_D
    eO_1 = eO

    u = np.array([v, w])
    return u
