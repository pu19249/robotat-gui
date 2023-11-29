from sympy import symbols, sin, cos, atan2
from sympy.utilities.codegen import codegen
import chardet

def exp_pid():
    # Define symbols
    x0, y0, theta0, goal_x, goal_y = symbols('x0 y0 theta0 goal_x goal_y')

    kpO = 15.0
    kiO = 0.01
    kdO = 0.01
    EO = 0.0
    eO_1 = 0.0

    v0 = 20.0
    alpha = 9

    x = x0
    y = y0
    theta = theta0

    goal_diff_x = goal_x - x
    goal_diff_y = goal_y - y

    thetag = atan2(goal_diff_y, goal_diff_x)
    eP = (goal_diff_x**2 + goal_diff_y**2)**0.5
    eO = thetag - theta
    eO = atan2(sin(eO), cos(eO))

    # linear velocity
    v = v0 * (1 - 2.718281828459045 ** (-alpha * eP ** 2))
    # v = kP

    # angular velocity
    eO_D = eO - eO_1
    EO = EO + eO
    w = kpO * eO + kiO * EO + kdO * eO_D
    eO_1 = eO


    # Codegen
    [(c_name, c_code), (h_name, c_header)] = codegen(('v', v), "C99", "test", header=False, empty=False)
    codigo_c = c_code

    [(c_name, c_code), (h_name, c_header)] = codegen(('w', w), "C99", "test", header=False, empty=False)
    codigo_c += '\n' + c_code

    # Whole generated expression
    # Split the code into lines
    code_lines = codigo_c.split('\n')

    # Filter lines containing assignments for v_result and w_result
    v_lines = [line for line in code_lines if "v_result =" in line]
    w_lines = [line for line in code_lines if "w_result =" in line]

    return v_lines[0], w_lines[0]


def control_file_pid_exp():
    print('se va a modificar para pid exp')
    v_result, w_result = exp_pid()
    with open("ota/esp32ota_sim/src/codegen.c", 'rb') as file:
        result1 = chardet.detect(file.read())
        file_encoding = result1['encoding']
        with open("ota/esp32ota_sim/src/codegen.c", 'r', encoding=file_encoding) as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if "v_result =" in line:
                # based on this TAG the angle should be added (in radians)
                lines[i] = f"{v_result}\n"
            elif "w_result =" in line:
                lines[i] = f"{w_result}\n"
            
        with open("ota/esp32ota_sim/src/codegen.c", 'w', encoding=file_encoding) as file:
            file.writelines(lines)