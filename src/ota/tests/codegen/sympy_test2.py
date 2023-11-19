from sympy import symbols, sin, cos, atan2
from sympy.utilities.codegen import codegen

# Definir los símbolos
x0, y0, theta0, goal_x, goal_y = symbols('x0 y0 theta0 goal_x goal_y')

# Definir la función pd_controller_sim
kp = 10.0
ki = 0.01
kd = 0.01

x = x0
y = y0
theta = theta0

goal_diff_x = goal_x - x
goal_diff_y = goal_y - y

thetag = goal_diff_y / goal_diff_x

eP = (goal_diff_x**2 + goal_diff_y**2)**0.5

eO = thetag - theta
eO = atan2(sin(eO), cos(eO))

v = kp * eP + ki * eP + kd * eO
w = kp * eO + ki * eO + kd * eO
print(v)
print(w)

# Convertir las expresiones a código C
[(c_name, c_code), (h_name, c_header)] = codegen(('v', v), "C99", "test", header=False, empty=False)
codigo_c = c_code

[(c_name, c_code), (h_name, c_header)] = codegen(('w', w), "C99", "test", header=False, empty=False)
codigo_c += '\n' + c_code

# Imprimir el código C completo
print(codigo_c)
