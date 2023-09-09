import json
from windows.animation_window import py_game_animation, robot_character
from robots.robot_pololu import Pololu
from controllers.exponential_pid import exponential_pid
from controllers.lqi import lqi
from windows.map_coordinates import inverse_change_coordinates
import numpy as np

# load json file
f = open('worlds/world_definition.json')
# returns a json object as a dictionary
world = json.load(f)

# --- create objects arrays ---
# robots
pololu = []
traj = []
X_sim = []
Y_sim = []
Theta_sim = []
characters = []

goal1 = [100, 100]
goal2 = [-100, -150]
robots = world['robots']  # this takes the robot object from the json file

# Define a dictionary to map controller names to controller functions
controller_map = {
    'exponential_pid': exponential_pid,
    'lqi': lqi,
}

# define the animation dimensions based on the json information
animation_window = py_game_animation(
    world.get('x_dimension_arena'),
    world.get('y_dimension_arena'))  # , pololu[0].img,
# world.get('no_robots'))

animation_window.initialize()

# animation_window.animate()
for i in range(len(robots)):
    controller_name = robots[i].get('controller')
    controller_function = controller_map.get(controller_name, None)
     # Define the goal based on robot's index
    if i == 0:
        current_goal = goal1
    elif i == 1:
        current_goal = goal2
    else:
        # You can define additional goals here if needed
        current_goal = [0, 0]  # Default goal

    pololu.append(Pololu(robots[i].get('state'),
                         robots[i].get('physical_params'),
                         robots[i].get('ID_robot'),
                         robots[i].get('IP'),
                         robots[i].get('img'),
                         lambda state, goal=current_goal,
                         ctrl_func=controller_function:
                         ctrl_func(state, goal),
                         animation_window.screen))
    characters.append((robots[i].get('img'),
                             robots[i].get('state')[0],
                             robots[i].get('state')[1],
                             robots[i].get('state')[2]))
    
print(characters)

dt = world['dt']
t0 = world['t0']
tf = world['tf']

# this list needs to depend directly of the creation of the robots objects
# and also map the positions first
# characters = [
#     ('pictures/pololu_img.png', 100, 100, 45)
# ]

# Add robot characters to the animation
for character in characters:
    animation_window.add_robot_character(*character)

# animation_window.animate()

# obstacles

# landmarks


'''
Beyond this point, the animation should occur when the play button is pressed (is a while loop needed? cause the simulation method already occurs in the indicated interval, but at the same time the animation should have a duration of the time specified...)
'''

# THIS PART ALMOST WORKS BUT FIRST OTHER TESTS WILL BE DONE TO SEE
# WHAT VALUES AND HOW NEED TO BE PASSED TO ANIMATE THE ROBOTS
x_vals_display = []
y_vals_display = []
theta_vals_display = []
for i in range(len(robots)):
    # pololu[i].initialize_image()
    if i == 0:
        current_goal = goal1
    elif i == 1:
        current_goal = goal2
    else:
        # You can define additional goals here if needed
        current_goal = [0, 0]  # Default goal
    traj.append(pololu[i].simulate_robot(dt, t0, tf, current_goal))
    x_results, y_results, theta_results = pololu[i].get_simulation_results()
    # print(x_results)

    # Append the X simulation results for the current robot
    X_sim.append(x_results)
    # Append the Y simulation results for the current robot
    Y_sim.append(y_results)
    # Append the Theta simulation results for the current robot
    Theta_sim.append(theta_results)


# for x, y in zip(x_results, y_results):
#     x_new_val, y_new_val = inverse_change_coordinates(x, y, 960, 760)
#     # print(x, y, "->", x_new_val, y_new_val)
#     x_vals_display.append(x_new_val)
#     y_vals_display.append(y_new_val)
#     # print(x_new_val)


for i in range(len(robots)):
    x_results = X_sim[i]
    y_results = Y_sim[i]
    theta_results = Theta_sim[i]
    
    x_vals_display_robot = []
    y_vals_display_robot = []
    theta_vals_display_robot = []
    
    for x, y, theta in zip(x_results, y_results, theta_results):
        x_new_val, y_new_val = inverse_change_coordinates(x, y, 960, 760)
        theta_new_val = np.rad2deg(theta)
        x_vals_display_robot.append(x_new_val)
        y_vals_display_robot.append(y_new_val)
        theta_vals_display_robot.append(theta_new_val)
        # print(x, y, "->", x_new_val, y_new_val)
    
    x_vals_display.append(x_vals_display_robot)
    y_vals_display.append(y_vals_display_robot)
    theta_vals_display.append(theta_vals_display_robot)


x_vals_display = np.array(list(zip(x_vals_display[0], x_vals_display[1])))
y_vals_display = np.array(list(zip(y_vals_display[0], y_vals_display[1])))
theta_vals_display = np.array(list(zip(theta_vals_display[0], theta_vals_display[1])))
# print(x_vals_display)
# print(x_vals_display)
## WILL TEST TO PASS JUST ONE MOVEMENT FOR NOW TO A ROBOT IN THE ANIMATION WINDOW

# Iterate through the robot characters and update their attributes
# Update robot characters within the animation window
# animation_window.update_robot_characters(x_vals_display, y_vals_display)
animation_window.animate(x_vals_display, y_vals_display, theta_vals_display)

# while loop