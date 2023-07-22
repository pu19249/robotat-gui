import json
from animation_window import py_game_animation
from robots.robot_pololu import Pololu
from controllers.exponential_pid import exponential_pid

# load json file
f = open('world_definition.json')
# returns a json object as a dictionary
world = json.load(f)

# --- create objects arrays ---
# robots
pololu = []
goal = [100, 100]
robots = world['robot']


# Define a dictionary to map controller names to controller functions
controller_map = {
    'exponential_pid': exponential_pid,
    # Add more controllers here if needed
}

for i in range(len(robots)):
    controller_name = robots[i].get('controller')
    controller_function = controller_map.get(controller_name, None)
    pololu.append(Pololu(robots[i].get('state'),
                         robots[i].get('physical_params'),
                         robots[i].get('ID_robot'),
                         robots[i].get('IP'),
                         robots[i].get('img'),
                         lambda state, goal=goal,
                         ctrl_func=controller_function:
                         ctrl_func(state, goal)))

dt = 0.1
t0 = 0
tf = 100

traj = pololu[0].simulate_robot(dt, t0, tf, goal)
# Access the simulation results
X_sim, Y_sim, Theta_sim = pololu[0].get_simulation_results()

# initialize pygame animation

animation_window = py_game_animation(
    world.get('x_dimension_arena'),
    world.get('y_dimension_arena'), pololu[0].img,
    world.get('no_robots'))
animation_window.initialize()
animation_window.animate()

# Access the number of steps taken during the simulation
# num_steps = pololu[0].get_number_of_steps()
# obstacles
# landmarks

# while loop
