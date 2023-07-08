import numpy as np

def pid_exponential(init_cond, init_u, goal, N):
    
    # initial conditions
    xi0 = np.array([0, 0, 0])
    u0 = np.array([0, 0])
    xi = xi0  # state vector
    u = u0  # input vector

    # Arrays to store state, inputs, and outputs
    XI = np.zeros((len(xi), N + 1))
    U = np.zeros((len(u), N + 1))

    # initialize arrays
    XI[:, 0] = xi0
    U[:, 0] = u0
    X = np.zeros(N + 1)
    Y = np.zeros(N + 1)
    Theta = np.zeros(N + 1)

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
    x = xi[0]
    y = xi[1]
    theta = xi[2]
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
