from sympy.utilities.codegen import codegen
from sympy import *
from sympy.utilities.lambdify import lambdify
from sympy import symbols, cos, sin
import numpy as np
import re
import inspect

# def convert_function_to_individual_args(func):
#     args = inspect.getfullargspec(func).args
#     if len(args) != 2:
#         raise ValueError("La función debe tener exactamente dos argumentos.")

#     def new_func(*args):
#         if len(args) != 5:
#             raise ValueError("La nueva función debe recibir exactamente cinco argumentos.")
#         return func([args[0], args[1], args[2]], [args[3], args[4]])

#     return new_func

def pd_controller_sim(x0, y0, theta0, goal_x, goal_y):
    kp = 0.10
    ki = 0.01
    kd = 0.1

    x = x0
    y = y0
    theta = theta0

    goal_diff_x = goal_x - x
    goal_diff_y = goal_y - y

    thetag = goal_diff_y / goal_diff_x

    eP = (goal_diff_x**2 + goal_diff_y**2)**0.5

    eO = thetag - theta
    eO = (sin(eO) / cos(eO))

    v = kp * eP + ki * eP + kd * eO
    w = kp * eO + ki * eO + kd * eO

    return [v, w]

# def pd_controller_lambda(xi, goal):
#     return lambdify((xi, goal), pd_controller(xi, goal))

# # Convertir la función
# new_pd_controller = convert_function_to_individual_args(pd_controller)
# print(inspect.getsource(new_pd_controller))

# def pid_controller(x, y, theta, goal_x, goal_y):
#     kp = 0.10  # Ajusta según tus preferencias
#     ki = 0.01  # Ajusta según tus preferencias
#     kd = 0.1   # Ajusta según tus preferencias

#     e = np.array([goal_x - x, goal_y - y])
#     thetag = atan2(e[1], e[0])

#     eP = np.linalg.norm(e)
#     eO = thetag - theta
#     eO = atan2(np.sin(eO), np.cos(eO))

#     v = kp * eP + ki * eP + kd * eO
#     w = kp * eO + ki * eO + kd * eO

#     u = np.array([v, w])
#     return u
# x, y, theta, x_d, y_d, kp, eP, ki, kd, eO = symbols('x, y, theta, x_d, y_d, kp, eP, ki, kd, eO')
# v = kp * eP + ki * eP + kd * eO

[(c_name, c_code), (h_name, c_header)] = \
    codegen(('v', expresion), "C99", "test", header=False, empty=False)
# print(c_name)
print(c_code)

print(h_name)
print(c_header)

# [(c_name, c_code), (h_name, c_header)] = \
#     codegen(('volume', lambdify((xi, goal), pd_controller(xi, goal))), "C99", "test",
#         header=False, empty=False)
# print(c_name)
# print(c_code)
# print(h_name)
# print(c_header)
# from sympy import symbols, ccode
# from sympy import atan2, sqrt, sin, cos
# from sympy.utilities.codegen import codegen
# from sympy import *
# from sympy.utilities.lambdify import lambdify
# def pid_controller(x, y, theta, goal_x, goal_y):
#     kp = 0.10  # Ajusta según tus preferencias
#     ki = 0.01  # Ajusta según tus preferencias
#     kd = 0.1   # Ajusta según tus preferencias

#     e_x = goal_x - x
#     e_y = goal_y - y
#     thetag = atan2(e_y, e_x)

#     eP = sqrt(e_x**2 + e_y**2)
#     eO = thetag - theta
#     eO = atan2(sin(eO), cos(eO))

#     v = kp * eP + ki * eP + kd * eO
#     w = kp * eO + ki * eO + kd * eO

#     u = [v, w]
#     return u
# x, y, theta, goal_x, goal_y = symbols('x y theta goal_x goal_y')

# def suma(x, y):
#     result = x + y
#     return result

# expresion = pid_controller(x, y, theta, goal_x, goal_y)

# # codigo_c = ccode(expresion, standard='C89', contract = True)

# print(codigo_c)
# [(c_name, c_code)] = \
#     codegen(('volume', expresion), "C99", "test",
#             header=False, empty=False)