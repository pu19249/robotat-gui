import numpy as np
cimport numpy as np

def pd_controller(np.ndarray[np.float64_t, ndim=1] xi, np.ndarray[np.float64_t, ndim=1] goal):
    cdef np.float64_t kp = 0.10  # Ajusta según tus preferencias
    cdef np.float64_t ki = 0.01  # Ajusta según tus preferencias
    cdef np.float64_t kd = 0.1  # Ajusta según tus preferencias

    cdef np.float64_t x = xi[0]
    cdef np.float64_t y = xi[1]
    cdef np.float64_t theta = xi[2]

    cdef np.ndarray[np.float64_t, ndim=1] e = np.array([goal[0] - x, goal[1] - y])
    cdef np.float64_t thetag = np.arctan2(e[1], e[0])

    cdef np.float64_t eP = np.linalg.norm(e)
    cdef np.float64_t eO = thetag - theta
    eO = np.arctan2(np.sin(eO), np.cos(eO))

    cdef np.float64_t v = kp * eP + ki * eP + kd * eO
    cdef np.float64_t w = kp * eO + ki * eO + kd * eO

    cdef np.ndarray[np.float64_t, ndim=1] u = np.array([v, w])
    return u
