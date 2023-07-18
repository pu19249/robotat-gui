import numpy as np
import control as ct


def lqr_init():
    xi_0 = [0, 0, 0]
    u_0 = [0, 0]
    array1 = np.array([[1, 0], [0, 1/0.01]])
    array2 = np.array([[np.cos(xi_0[2]), -np.sin(xi_0[2])],
                       [np.sin(xi_0[2]), np.cos(xi_0[2])]])
    array2 = np.transpose(array2)
    array3 = np.array([u_0[0], u_0[1]])
    finv = np.dot(array1, np.dot(array2, array3))
    A = np.zeros((2, 2))
    B = np.eye(2)
    Q = np.eye(2)
    R = np.eye(2)
    Klqr = 2*ct.lqr(A, B, Q, R)
    return Klqr, finv


def lqr_pp(xi, goal):
    Klqr, finv = lqr_init()
    x = xi[0]
    y = xi[1]
    e = [x - goal[0], y - goal[1]]
    mu = -1*Klqr*e
    u = finv(xi, mu)

    return u

# % LQR
# Q = eye(2);
# R = eye(2);
# Klqr = 2*lqr(A,B,Q,R);

# % LQR + Integradores (LQI)
# Cr = eye(2);
# Dr = zeros(2);
# AA = [A, zeros(size(Cr')); Cr, zeros(size(Cr,1))];
# BB = [B; Dr];
# QQ = eye(size(A,1) + size(Cr,1)); QQ(3,3) = 10; QQ(4,4) = 10;
# Klqi = lqr(AA, BB, QQ, R);
# ref = [xg; yg];
# sigma = 0;


# x = xi(1); y = xi(2);
#             e = [x - xg; y - yg];
#             mu = -Klqi.*e;
#             u = finv(xi, mu);
