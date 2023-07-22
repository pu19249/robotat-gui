import json
from animation_window import py_game_animation

# load json file
f = open('world_definition.json')
# returns a json object as a dictionary
data = json.load(f)

# initialize pygame animation

animation_window = py_game_animation(
    data['pololu_robot'][0]['img'], data['x_dimension_arena'],
    data['y_dimension_arena'])

print(data['y_dimension_arena'])
animation_window.initialize()
animation_window.animate()

# create objects arrays
# robots
# obstacles
# landmarks

# while loop
