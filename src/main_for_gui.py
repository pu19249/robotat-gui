import json
from windows.animation_window import py_game_animation, robot_character
from robots.robot_pololu import Pololu
from controllers.exponential_pid import exponential_pid
from controllers.pid_controller import pd_controller
from controllers.lqi import lqi_controller
from windows.map_coordinates import inverse_change_coordinates
import numpy as np
import pygame

# Define a dictionary to map controller names to controller functions
controller_map = {
    'exponential_pid': exponential_pid,
    'pd_controller': pd_controller,
    'lqi_controller': lqi_controller
}

def load_world(file_path):
    with open(file_path) as f:
        world = json.load(f)
        return world

def initialize_animation(world):
    # define the animation dimensions based on the json information - initialize animation window
    animation_window = py_game_animation(
        world.get('x_dimension_arena'),
        world.get('y_dimension_arena')) 

    #   animation_window.initialize()
    return animation_window


def create_objects(world, animation_window):
    pololu = []
    characters = []
    traj = []
    X_sim = []
    Y_sim = []
    Theta_sim = []

    robots = world['robots']  # this takes the robot object from the json file
    goals = world['landmarks']

    # Create the objects based on the json data
    for i in range(len(robots)):
        controller_name = robots[i].get('controller')
        controller_function = controller_map.get(controller_name, None)
        landmark_id = robots[i].get('ID_robot')
        
        # match landmarks id with robots id order
        closest_landmark = next((lm for lm in world['landmarks'] if lm['id'] == landmark_id), None)
        if closest_landmark is not None:
            current_goal = closest_landmark['pos']
        else:
            # Handle case where no matching landmark is found
            current_goal = [0, 0]

        pololu.append(Pololu(robots[i].get('state'),
                            robots[i].get('physical_params'),
                            robots[i].get('ID_robot'),
                            robots[i].get('IP'),
                            robots[i].get('img'),
                            lambda state, goal=current_goal,
                            ctrl_func=controller_function:
                            ctrl_func(state, goal)
                            ))
        
        characters.append((robots[i].get('img'),
                                robots[i].get('state')[0],
                                robots[i].get('state')[1],
                                robots[i].get('state')[2]))
    
    # Add robot characters to the animation
    for character in characters:
        animation_window.add_robot_character(*character)

    return robots, pololu

def calculate_simulation(world, robots, pololu):
    # Simulation params based on json
    dt = world['dt']
    t0 = world['t0']
    tf = world['tf']

    # this part of the code simulates each robot based on the landmark set for each robot and the controller
    x_vals_display = []
    y_vals_display = []
    theta_vals_display = []
    x_results_plt = []
    y_results_plt = []
    theta_results_plt = []
    
    for i in range(len(robots)):
        landmark_id = robots[i].get('ID_robot')
        closest_landmark = next((lm for lm in world['landmarks'] if lm['id'] == landmark_id), None)
        if closest_landmark is not None:
            current_goal = closest_landmark['pos']
        else:
            current_goal = [0, 0]
            
        traj = pololu[i].simulate_robot(dt, t0, tf, current_goal)
        x_results, y_results, theta_results = pololu[i].get_simulation_results()

        x_vals_display_robot = []
        y_vals_display_robot = []
        theta_vals_display_robot = []
        x_results_raw = []
        y_results_raw = []

        # this part makes the mapping to display in the commplete animation window 
        for x, y, theta in zip(x_results, y_results, theta_results):
            # Get raw data
            x_raw, y_raw = x, y
            x_new_val, y_new_val = inverse_change_coordinates(x, y, 960, 760) #(in this case we know its doubled, so 760x960)
            theta_new_val = np.rad2deg(theta)
            x_vals_display_robot.append(x_new_val)
            y_vals_display_robot.append(y_new_val)
            theta_vals_display_robot.append(theta_new_val)
            x_results_raw.append(x_raw)
            y_results_raw.append(y_raw)
            # Print statement for debugging
            # print(f"x: {x}, y: {y} => x_new: {x_new_val}, y_new: {y_new_val}")
        
        x_vals_display.append(x_vals_display_robot)
        y_vals_display.append(y_vals_display_robot)
        theta_vals_display.append(theta_vals_display_robot)
        x_results_plt.append(x_results_raw)
        y_results_plt.append(y_results_raw)
    # Remove the first value from each list
    
    x_vals_display = np.array(list(zip(*x_vals_display)))
    x_vals_display = x_vals_display[1:]
    y_vals_display = np.array(list(zip(*y_vals_display)))
    y_vals_display = y_vals_display[1:]
    theta_vals_display = np.array(list(zip(*theta_vals_display)))
    theta_vals_display = theta_vals_display[:-1]

    x_results_plt = np.array(list(zip(*x_results_plt)))
    x_results_plt = x_results_plt[1:]
    y_results_plt = np.array(list(zip(*y_results_plt)))
    y_results_plt = y_results_plt[1:]
    
    return x_vals_display, y_vals_display, theta_vals_display, x_results_plt, y_results_plt

def run_animation(animation_window, x_vals_display, y_vals_display, theta_vals_display):
    # run the animation with the results for each robot
    animation_window.animate(x_vals_display, y_vals_display, theta_vals_display)
