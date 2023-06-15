import numpy as np


def pid_exponential(init_cond, init_u, goal):
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

    # controller (this must run repeteadly with the numerical method)
    x = init_cond[0]
    y = init_cond[1]
    theta = init_cond[2]
    e = np.array([goal[0] - x, goal[1] - y])
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

    return u
