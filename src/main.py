import json


# load json file
f = open('world_definition.json')
# returns a json object as a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['pololu_robot']:
    print(i)


# initialize pygame animation

# create objects arrays
# robots
# obstacles
# landmarks

# while loop
