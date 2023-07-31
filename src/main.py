import json
from animation_window import py_game_animation, robot_character
from robots.robot_pololu import Pololu
from controllers.exponential_pid import exponential_pid
from controllers.lqi import lqi
from map_coordinates import inverse_change_coordinates

# load json file
f = open('world_definition.json')
# returns a json object as a dictionary
world = json.load(f)

# --- create objects arrays ---
# robots
pololu = []
traj = []
X_sim = []
Y_sim = []
Theta_sim = []

goal1 = [100, 100]
goal2 = [200, 200]
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
    pololu.append(Pololu(robots[i].get('state'),
                         robots[i].get('physical_params'),
                         robots[i].get('ID_robot'),
                         robots[i].get('IP'),
                         robots[i].get('img'),
                         lambda state, goal=goal1,
                         ctrl_func=controller_function:
                         ctrl_func(state, goal),
                         animation_window.screen))


dt = world['dt']
t0 = world['t0']
tf = world['tf']

# this list needs to depend directly of the creation of the robots objects
# and also map the positions first
characters = [
    ('pictures/pololu_img.png', 100, 100, 45),
    ('pictures/pololu_img.png', 300, 200, 90),
    ('pictures/pololu_img.png', 300, 50, 90),
]

# Add robot characters to the animation
for character in characters:
    animation_window.add_robot_character(*character)

# for character in animation_window.robot_characters:
#     character.rotate_move()

# animation_window.animate()


# obstacles


# landmarks


'''
Beyond this point, the animation should occur when the play button is pressed (is a while loop needed? cause the simulation method already occurs in the indicated interval, but at the same time the animation should have a duration of the time specified...)
'''

# THIS PART ALMOST WORKS BUT FIRST OTHER TESTS WILL BE DONE TO SEE
# WHAT VALUES AND HOW NEED TO BE PASSED TO ANIMATE THE ROBOTS
# x_vals_display = []
# y_vals_display = []
# for i in range(len(robots)):
#     # pololu[i].initialize_image()

#     traj.append(pololu[i].simulate_robot(dt, t0, tf, goal1))
#     x_results, y_results, theta_results = pololu[i].get_simulation_results()
#     print(x_results)

#     # Append the X simulation results for the current robot
#     X_sim.append(x_results)
#     # Append the Y simulation results for the current robot
#     Y_sim.append(y_results)
#     # Append the Theta simulation results for the current robot
#     Theta_sim.append(theta_results)

# for x, y in zip(x_results, y_results):
#     x_new_val, y_new_val = inverse_change_coordinates(x, y, 480, 380)
#     print(x, y, "->", x_new_val, y_new_val)
#     x_vals_display.append(x_new_val)
#     y_vals_display.append(y_new_val)


animation_window.animate()
# while loop
