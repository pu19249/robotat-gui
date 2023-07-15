from robots.robot_pololu import Pololu
from controllers.pid_exponential import pid_exponential
import os

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


# Define the image file name
img_file = "pololu_img.png"

# Create the complete file path
img_path = os.path.join(script_dir, img_file)
state_0 = [0, 0, 0]  # Example state values
physical_params = [1, 1, 10, 10]  # Example physical parameters
ID = 1  # Example ID
IP = "192.168.1.1"  # Example IP
# img_path = "pololu_img.png"  # Replace with the actual path to your PNG image file

goal = [100, 100]
N = 3000
init_u = [0, 0]
def controller(state): return pid_exponential(goal, state)


u = 0

pololu_robot = Pololu(state_0, physical_params, ID, IP,
                      img_path, lambda state, goal=goal: pid_exponential(state, goal), u)

print(pololu_robot.state)
print(pololu_robot.physical_params)
print(pololu_robot.ID)
print(pololu_robot.IP)
print(pololu_robot.img)
print(pololu_robot.controller)
print(pololu_robot.Theta)

pololu_robot.simulate_robot(0.01, 0, 30, goal)
