import numpy as np
import control as ct
from scipy.linalg import solve_discrete_are


# A = np.array([[1],[0]]) this creates a 2x1 matrix
# while A = np.array([1,0]) creates a 1x2 matrix


# def finv(xi_0, u_0):
#     # xi_0 = [0, 0, 0]
#     # u_0 = [0, 0]
#     array1 = np.array([[1, 0], [0, 1/0.01]])
#     array2 = np.array([[np.cos(xi_0[2]), -np.sin(xi_0[2])],
#                        [np.sin(xi_0[2]), np.cos(xi_0[2])]])
#     array2 = np.transpose(array2)
#     array3 = np.array([u_0[0], u_0[1]])
#     finv = np.dot(array1, np.dot(array2, array3))
#     return finv


# def lqr(A, B, Q, R):  # byMark Wilfried Mueller
#     """Solve the continuous time lqr controller.

#     dx/dt = A x + B u

#     cost = integral x.T*Q*x + u.T*R*u
#     """
#     # ref Bertsekas, p.151

#     # first, try to solve the ricatti equation
#     X = np.matrix(scipy.linalg.solve_continuous_are(A, B, Q, R))

#     # compute the LQR gain
#     K = np.matrix(scipy.linalg.inv(R)*(B.T*X))

#     eigVals, eigVecs = scipy.linalg.eig(A-B*K)

#     return K, X, eigVals


# def lqr_init():
#     A = np.zeros((2, 2))
#     B = np.eye(2)
#     Q = np.array([[1000, 0], [0, 1000]])
#     R = np.eye(2)
#     Klqr, Xlqr, eigValslqr = ct.lqr(A, B, Q, R)
#     # LQR + Integrators (LQI)
#     Cr = np.eye(2)
#     Dr = np.zeros((2, 2))
#     Cr_trans = np.transpose(Cr)
#     AA = np.block([[A, np.zeros(Cr_trans.shape)],
#                   [Cr, np.zeros((Cr.shape[0], Cr.shape[0]))]])
#     BB = np.block([[B], [Dr]])  # np.block([[A], [B]]) # vstack([A, B])
#     QQ = np.eye(A.shape[0]+Cr.shape[0])
#     QQ[2, 2] = 100
#     QQ[3, 3] = 100
#     Klqi, d1, d2 = ct.lqr(AA, BB, QQ, R)
#     sigma = 50

#     return Klqr, sigma, Klqi, Cr


# def lqi(xi, goal):
#     Klqr, sigma, Klqi, Cr = lqr_init()
#     dt = 0.1
#     x = (xi[0:2])
#     x = np.array([[x[0]], [x[1]]])

#     ref = np.array([[goal[0]], [goal[1]]])

#     sigma = sigma + (Cr@x - ref)*dt
#     e = np.concatenate((x, sigma))  # concatenate rows
#     mu = np.dot(-Klqi, e)

#     u = finv(xi, mu)
#     u = np.concatenate((u[0], u[1]))
#     return u

def dynamics(state, u):
    x, y, theta = state
    v, w = u

    A = np.array([[0, 0, -v * np.sin(theta)],
                  [0, 0, v * np.cos(theta)],
                  [0, 0, 0]])

    B = np.array([[np.cos(theta), 0],
                  [np.sin(theta), 0],
                  [0, 1]])

    return A, B

def lqi_controller(xi, goal):
    A, B = dynamics(xi, [0, 0])  # Obtén las matrices A y B
    # Definir las matrices de peso Q y R
    Q = np.diag([1, 1, 1])  # Ajusta según tus preferencias
    R = np.array([[1, 0],
              [0, 1]])
          # Ajusta según tus preferencias

    x = xi[0]
    y = xi[1]
    theta = xi[2]

    # Construye el vector de estado x
    x_state = np.array([x, y, theta])

    # Calcula la entrada de control u
    P = solve_discrete_are(A, B, Q, R)
    K = np.linalg.inv(B.T @ P @ B + R) @ B.T @ P @ A

    u = -K @ x_state
    print(u)
    return u
