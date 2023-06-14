import numpy as np


def pid_exponential():
    # PID position
    kpP = 1
    kiP = 0.0001
    kdP = 0.5
    EP = 0
    eP_1 = 0

    # PID orientation
    kpO = 10
    kiO = 0.0001
    kdO = 0
    EO = 0
    eO_1 = 0

    # exponential approach
    v0 = 10
    alpha = 1

    # controller
    x = xi[0]
    y = xi[1]
    theta = xi[2]
    e = np.array([xg - x, yg - y])
    thetag = np.arctan2(e[1], e[0])

    eP = np.linalg.norm(e)
    eO = thetag - theta
    eO = np.arctan2(np.sin(eO), np.cos(eO))

    kP = v0 * (1 - np.exp(-alpha * eP ** 2)) / eP
    v = kP * eP

    eO_D = eO - eO_1
    EO = EO + eO
    w = kpO * eO + kiO * EO + kdO * eO_D
    eO_1 = eO

    u = np.array([v, w])
