import numpy as np

def pid_controller(xi, goal):
    kp = 0.10  # Ajusta según tus preferencias
    ki = 0.01  # Ajusta según tus preferencias
    kd = 0.1  # Ajusta según tus preferencias

    x = xi[0]
    y = xi[1]
    theta = xi[2]

    e = np.array([goal[0] - x, goal[1] - y])
    thetag = np.arctan2(e[1], e[0])

    eP = np.linalg.norm(e)
    eO = thetag - theta
    eO = np.arctan2(np.sin(eO), np.cos(eO))

    v = kp * eP + ki * eP + kd * eO
    w = kp * eO + ki * eO + kd * eO

    u = np.array([v, w])
    # print(u)
    return u
