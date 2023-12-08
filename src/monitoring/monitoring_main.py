import ctypes
import sys
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the sys.path
sys.path.append(parent_dir)

from windows.animation_window import *
from .robotat_3pi_Python import *
from windows.map_coordinates import inverse_change_coordinates

################ END OF IMPORTS ##############################

# # This solves scaling issues for the independent pygame window
# ctypes.windll.user32.SetProcessDPIAware()


# pictures_dir = os.path.join(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures"
# )


# robotat = robotat_connect()
# robotat.recv(2048)

# # Initialize arrays to display and save data
# x_data = []
# y_data = []
# theta_data = []
# x_vals_display_robot = []
# y_vals_display_robot = []
# theta_vals_display_robot = []
# x_results_raw = []
# y_results_raw = []


# # First we need to create the object that represents and updates the position and rotation of the Pololu img (first one robot only)
# characters = [(os.path.join(pictures_dir, "pololu_img_x.png"), 0, 0, 0), (os.path.join(pictures_dir, "pololu_img_x.png"), 100, 100, 0)]


# # Prepare data as the animation window expects it (list of lists for each x, y, theta for each robot) according to how its received from the server (list of x, y, orientation)
# # Get and process data for more than one marker (in development)
# def get_and_process_data_multiple(robotat, marker, representation):
#     x_data = []
#     y_data = []
#     theta_data = []

#     for pose_data_list in get_pose_continuous_multiple(robotat, marker, representation, max_attempts=5):
#         if pose_data_list is not None:
#             for marker_data in pose_data_list:
#                 x_vals_real_time = [marker_data[0]]
#                 y_vals_real_time = [marker_data[1]]
#                 theta_vals_real_time = [marker_data[5]]

#                 x_data.append(x_vals_real_time)
#                 y_data.append(y_vals_real_time)
#                 theta_data.append(theta_vals_real_time)

#                 # Additional processing or printing can be done here

#     return x_data, y_data, theta_data

# # Get and process data for one marker only
# def get_and_process_data(marker):
#     try:
#         for pose_data in get_pose_continuous(robotat, [marker], "eulxyz", max_attempts=5):

#             x_vals_real_time = [pose_data[0][0]]
#             y_vals_real_time = [pose_data[0][1]]
#             theta_vals_real_time = [pose_data[0][5]]
#             # print(theta_vals_real_time)
#             x_data.append(x_vals_real_time)
#             y_data.append(y_vals_real_time)
#             theta_data.append(theta_vals_real_time)
#             break
#     except Exception as e:
#         print(f"ERROR: {e}")

#     return x_vals_real_time, y_vals_real_time, theta_vals_real_time

# # Map data for multiple markers
# def map_data_multiple(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
#     x_vals_display_robot = []
#     y_vals_display_robot = []
#     theta_vals_display_robot = []
    
#     for marker_x, marker_y, marker_theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
#         x_mapped = []
#         y_mapped = []
#         theta_mapped = []

#         for x, y, theta in zip(marker_x, marker_y, marker_theta):
#             x_raw, y_raw = x, y
#             x_new_val, y_new_val = inverse_change_coordinates(x_raw * 100, y_raw * 100, 960, 760)
#             theta_new_val = theta + 180

#             x_mapped.append(x_new_val)
#             y_mapped.append(y_new_val)
#             theta_mapped.append(theta_new_val)

#         x_vals_display_robot.append(x_mapped)
#         y_vals_display_robot.append(y_mapped)
#         theta_vals_display_robot.append(theta_mapped)

#     return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot

# # Map data function for one marker
# def map_data(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
#     x_vals_display_robot = []
#     y_vals_display_robot = []
#     theta_vals_display_robot = []
#     # this part makes the mapping to display in the complete animation window
#     for x, y, theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
#         # for x_val, y_val, theta_val in zip(x, y, theta):
#         x_raw, y_raw = x, y
#         x_new_val, y_new_val = inverse_change_coordinates(
#             x_raw * 100, y_raw * 100, 960, 760
#         )

#         theta_new_val = theta  # theta_val, not just theta

#         x_vals_display_robot.append(x_new_val)
#         y_vals_display_robot.append(y_new_val)
#         theta_vals_display_robot.append(theta_new_val)
#         x_results_raw.append(x_raw)
#         y_results_raw.append(y_raw)
#         # Print statement for debugging
#         # print(f"x: {x_val}, y: {y_val} => x_new: {x_new_val}, y_new: {y_new_val}")

#     # Wrap the final arrays in a list
#     x_vals_display_robot = [x_vals_display_robot]
#     y_vals_display_robot = [y_vals_display_robot]
#     theta_vals_display_robot = [theta_vals_display_robot]

#     # print(f"X: {x_vals_display_robot}, Y: {y_vals_display_robot}, THETA: {theta_vals_display_robot}")
#     return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot

# # Multiple markers get_data function
# def get_data_multiple():
#     x_vals_real_time, y_vals_real_time, theta_vals_real_time = get_and_process_data_multiple(robotat, [2, 1], 'eulxyz')

#     x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = map_data_multiple(
#         x_vals_real_time, y_vals_real_time, theta_vals_real_time
#     )

#     return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot, \
#         x_vals_real_time, y_vals_real_time, theta_vals_real_time

# # One marker get_data function
# def get_data():
#     x_vals_real_time, y_vals_real_time, theta_vals_real_time = get_and_process_data()
#     x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = map_data(
#         x_vals_real_time, y_vals_real_time, theta_vals_real_time
#     )
#     # print(theta_vals_display_robot)
#     return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot, \
#         x_vals_real_time, y_vals_real_time, theta_vals_real_time


# data_source = lambda: get_data()
# animation_window = py_game_monitoring(850, 960, get_data, filename)
# for character in characters:
#     # print(character)
#     animation_window.add_robot_character(*character)
# animation_window.initialize()
# # Open the file in append mode once, outside the loop



# def animation_function(flag):
#     while flag:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 flag = False  # Set the flag to False to exit the loop

#         animation_window.start_animation()

#     # Cleanup or perform any necessary actions before exiting the function
#     pygame.quit()


# import ctypes
# import sys
# import os

# # Get the current script's directory
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Get the parent directory
# parent_dir = os.path.dirname(current_dir)

# # Add the parent directory to the sys.path
# sys.path.append(parent_dir)

# from windows.animation_window import *
# from windows.map_coordinates import inverse_change_coordinates
# from robotat_3pi_Python import *
# ################ END OF IMPORTS ##############################

# This solves scaling issues for the independent pygame window
ctypes.windll.user32.SetProcessDPIAware()


pictures_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures"
)


class RobotAnimation:
    def __init__(self):

        self.robotat = robotat_connect()
        self.robotat.recv(2048)

        # Initialize arrays to display and save data
        self.x_data = []
        self.y_data = []
        self.theta_data = []
        self.x_results_raw = []
        self.y_results_raw = []

        # First we need to create the object that represents and updates the position and rotation of the Pololu img (first one robot only)
        self.characters_multiple = [
            (os.path.join(pictures_dir, "pololu_img_x.png"), 0, 0, 0),
            (os.path.join(pictures_dir, "pololu_img_x.png"), 100, 100, 0),
        ]

        self.character = (os.path.join(pictures_dir, "pololu_img_x.png"), 0, 0, 0)

        self.animation_window = None

    def get_and_process_data_multiple(self, marker, representation):
        x_data = []
        y_data = []
        theta_data = []

        for pose_data_list in get_pose_continuous_multiple(self.robotat, marker, representation, max_attempts=5):
            if pose_data_list is not None:
                for marker_data in pose_data_list:
                    x_vals_real_time = [marker_data[0]]
                    y_vals_real_time = [marker_data[1]]
                    theta_vals_real_time = [marker_data[5]]

                    x_data.append(x_vals_real_time)
                    y_data.append(y_vals_real_time)
                    theta_data.append(theta_vals_real_time)

                    # Additional processing or printing can be done here

        return x_data, y_data, theta_data

    def get_and_process_data(self, marker):
        try:
            for pose_data in get_pose_continuous(self.robotat, [marker], "eulxyz", max_attempts=5):
                
                x_vals_real_time = [pose_data[0][0]]
                y_vals_real_time = [pose_data[0][1]]
                theta_vals_real_time = [pose_data[0][5]]
                print(marker)
                if marker == 1:
                    theta_vals_real_time = [pose_data[0][5]] # done
                elif marker == 2:
                    theta_vals_real_time = [pose_data[0][5]-40] # done
                elif marker == 3:
                    theta_vals_real_time = [pose_data[0][5]-90]
                elif marker == 4:
                    theta_vals_real_time = [pose_data[0][5]-140]
                elif marker == 5:
                    theta_vals_real_time = [pose_data[0][5]+175]
                elif marker == 6:
                    theta_vals_real_time = [pose_data[0][5]-145]
                elif marker == 7:
                    theta_vals_real_time = [pose_data[0][5]+90] # done
                elif marker == 8:
                    theta_vals_real_time = [pose_data[0][5]-10] # done
                elif marker == 9:
                    theta_vals_real_time = [pose_data[0][5]-80] # done
                elif marker == 13:
                    theta_vals_real_time = [pose_data[0][5]+40] # done
                elif marker == 14:
                    theta_vals_real_time = [pose_data[0][5]+20] # done
                self.x_data.append(x_vals_real_time)
                self.y_data.append(y_vals_real_time)
                self.theta_data.append(theta_vals_real_time)
                break
        except Exception as e:
            print(f"ERROR: {e}")

        return x_vals_real_time, y_vals_real_time, theta_vals_real_time

    def map_data_multiple(self, x_vals_real_time, y_vals_real_time, theta_vals_real_time):
        x_vals_display_robot = []
        y_vals_display_robot = []
        theta_vals_display_robot = []
        
        for marker_x, marker_y, marker_theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
            x_mapped = []
            y_mapped = []
            theta_mapped = []

            for x, y, theta in zip(marker_x, marker_y, marker_theta):
                x_raw, y_raw = x, y
                x_new_val, y_new_val = inverse_change_coordinates(x_raw * 100, y_raw * 100, 960, 760)
                theta_new_val = theta + 180

                x_mapped.append(x_new_val)
                y_mapped.append(y_new_val)
                theta_mapped.append(theta_new_val)

            x_vals_display_robot.append(x_mapped)
            y_vals_display_robot.append(y_mapped)
            theta_vals_display_robot.append(theta_mapped)

        return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot

    def map_data(self, x_vals_real_time, y_vals_real_time, theta_vals_real_time):
        x_vals_display_robot = []
        y_vals_display_robot = []
        theta_vals_display_robot = []

        for x, y, theta in zip(x_vals_real_time, y_vals_real_time, theta_vals_real_time):
            x_raw, y_raw = x, y
            x_new_val, y_new_val = inverse_change_coordinates(
                x_raw * 100, y_raw * 100, 960, 760
            )

            theta_new_val = theta  # theta_val, not just theta

            x_vals_display_robot.append(x_new_val)
            y_vals_display_robot.append(y_new_val)
            theta_vals_display_robot.append(theta_new_val)
            self.x_results_raw.append(x_raw)
            self.y_results_raw.append(y_raw)

        # Wrap the final arrays in a list
        x_vals_display_robot = [x_vals_display_robot]
        y_vals_display_robot = [y_vals_display_robot]
        theta_vals_display_robot = [theta_vals_display_robot]

        return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot

    def get_data_multiple(self, tag1, tag2):
        x_vals_real_time, y_vals_real_time, theta_vals_real_time = self.get_and_process_data_multiple([tag1, tag2], 'eulxyz')

        x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = self.map_data_multiple(
            x_vals_real_time, y_vals_real_time, theta_vals_real_time
        )

        return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot, \
            x_vals_real_time, y_vals_real_time, theta_vals_real_time

    def get_data(self, tag):
        x_vals_real_time, y_vals_real_time, theta_vals_real_time = self.get_and_process_data(tag)
        x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot = self.map_data(
            x_vals_real_time, y_vals_real_time, theta_vals_real_time
        )
        return x_vals_display_robot, y_vals_display_robot, theta_vals_display_robot, \
            x_vals_real_time, y_vals_real_time, theta_vals_real_time

    def setup_animation_window(self, filename, tag):
        self.animation_window = py_game_monitoring(850, 960, lambda: self.get_data(tag), filename)
        self.animation_window.add_robot_character(*self.character)
        self.animation_window.initialize()
        
    def setup_animation_window_multiple(self, filename, tag1, tag2):
        self.animation_window = py_game_monitoring_multiple(850, 960, lambda: self.get_data_multiple(tag1, tag2), filename)
        for character in self.characters_multiple:
            self.animation_window.add_robot_character(*character)
        self.animation_window.initialize()

    def animation_function(self, flag):
        pygame.init()
        while flag:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    flag = False  # Set the flag to False to exit the loop
                    pygame.quit()
            self.animation_window.start_animation()

        # Cleanup or perform any necessary actions before exiting the function
        

# if __name__ == "__main__":
#     robot_animation = RobotAnimation()
#     robot_animation.setup_animation_window()
#     robot_animation.animation_function(True)
