import pygame
import os
import ctypes
from typing import *
import numpy
import math
import csv

# Get the directory path of the current script, abspath because of the tree structure
# that everything is on different folders
script_dir = os.path.dirname(os.path.abspath(__file__))
pictures_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pictures"
)


# This solves scaling issues for the independent pygame window
ctypes.windll.user32.SetProcessDPIAware()


# Button class for handling actions as 'Play' for the animation
class button_pygame:
    """
    This class handles interaction with a button when it's clicked.
    For this version it's used to represent a 'play' button.
    """

    def __init__(self, x: int, y: int, image: str, screen: pygame.Surface):
        """
        Attributes:
        ------------
        x : int
        y : int
            Position (x, y) of the image representing the button.
        image : str
            Image path in the pictures folder to represent the button.
        screen : pygame.Surface
            Pygame screen object where the button will be placed
        """
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.action = None
        self.pos = None

    def draw(self):
        """
        This will constantly draw the button on the screen and handle its actions.

        Returns:
        -------------
        self.action : bool
            It returns true if the button was pressed so other action
            can occur based on this response.
        """
        self.action = False
        # get mouse position
        self.pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(self.pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        return self.action


# class for handling position and orientation on the animation window
# also collision because is related with the rect it occupates
class robot_character:
    """
    Class to handle position and orientation update (image)
    based on simulation or other input.
    """

    def __init__(
        self,
        img_path: str,
        x: float,
        y: float,
        degree: float,
        screen: pygame.Surface,
        size: list,
    ):
        """
        Attributes:
        ------------
        img_path : str
            It is used to create the pygame object to represent the robot.
        x : float
        y : float
        degree : float
            Initial (x, y, theta) position for the img based on simulation input.
        screen : pygame.Surface
            Pygame screen where the robot img will be displayed and updated.
        size : list
            [x, y] screen size
        """
        self.img_path = img_path
        self.screen = screen
        self.x = x
        self.y = y
        self.degree = degree
        self.size = size
        self.radius = 10  # radius it occupates in the animation window

        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (40, 40))

        # Resize the image if needed
        self.rot_img = self.img
        self.rot_rect = self.img.get_rect(center=(x, y))

        self.background_color = (255, 255, 255)
        self.grid = pygame.image.load(
            os.path.join(pictures_dir, "grid_back_coord.png")
        ).convert_alpha()

    # box based on the radius defined before
    def draw_hitbox(self):
        """
        Area that surrounds the robot and defines the collision evaluation area.
        """
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), self.radius, 2)

    def check_collision(robot1, robot2):
        """
        Distance formula to check if the distance between the centers of two robots is less
        than the sum of their radii

        Attributes:
        ------------
        robot n : robot character class object
        """
        distance = ((robot1.x - robot2.x) ** 2 + (robot1.y - robot2.y) ** 2) ** 0.5
        return distance < robot1.radius + robot2.radius

    def update(self, degree: numpy.float64, x: numpy.float64, y: numpy.float64):
        """
        degree, x, and y are state attributes of the robot class
        when this method is called the attributes are updated and so
        in the rotate move method they are already updated without the need of
        passing them the value
        """
        self.degree = degree
        self.x = x
        self.y = y

    def rotate_move(self):
        """
        This updates both position and orientation of the robot img.
        """
        rotated_img = pygame.transform.rotate(self.img, self.degree)
        rotated_rect = rotated_img.get_rect(center=(self.x, self.y))

        # Blit the rotated robot image
        self.screen.blit(rotated_img, rotated_rect)


class py_game_animation:
    """
    This class handles every funtion and action related to the animation window
    of the simulation (precalculated data) using pygame module.
    """

    def __init__(self, x_size: int, y_size: int):
        """
        Attributes:
        ------------
        x_size : int
        y_size : int
            (x, y) size of the animation window (in this value the actual size of the
            Robotat platform and scaling needs to be taken into account).

        """
        grid_file = os.path.join(pictures_dir, "grid_back_coord.png")

        # Create the complete file path
        grid_path = os.path.join(script_dir, grid_file)

        self.screen_x = x_size
        self.screen_y = y_size
        self.original_size = (self.screen_x, self.screen_y)
        self.screen = pygame.display.set_mode(
            [self.screen_x, self.screen_y], pygame.RESIZABLE
        )
        self.background_color = (255, 255, 255)
        self.run = True
        self.grid_img = pygame.image.load(grid_path).convert_alpha()
        self.grid = pygame.transform.scale(
            self.grid_img, (self.screen_x - 90, self.screen_y)
        )
        self.play = None
        self.bounding_box = pygame.Rect(
            0, 0, 760, 960
        )  # Create a rectangle around the grid

        # the list size will be defined by the number of robots indicated
        self.robot_characters = []

    def add_robot_character(self, img_path: str, x: int, y: int, degree: int):
        """
        This method will create as many robots need to be created inside
        this animation window
        """
        robot = robot_character(
            img_path, x, y, degree, self.screen, [self.screen_x, self.screen_y]
        )
        self.robot_characters.append(robot)

    def update_robot_characters(
        self, x_vals_display, y_vals_display, theta_vals_display
    ):
        """
        This method takes the set of values for x, y, theta and updates
        each robot in robot_characters list calling .update method from robot_character
        class.
        """
        for robot_character, x, y, theta in zip(
            self.robot_characters, x_vals_display, y_vals_display, theta_vals_display
        ):
            robot_character.update(theta, x, y)

    def initialize(self):
        """
        Initiates pygame object, including the play button from the button class.
        """
        pygame.init()
        pygame.display.set_caption("Live simulation")
        self.clock = pygame.time.Clock()
        play_icon = pygame.image.load(
            os.path.join(pictures_dir, "play_icon.png")
        ).convert_alpha()
        play_icon = pygame.transform.scale(
            play_icon, (self.screen_x * 0.05, self.screen_x * 0.05)
        )
        self.play = button_pygame(
            self.screen_x - 50, self.screen_y / 2, play_icon, self.screen
        )
        self.play.draw()

        self.screen.fill(self.background_color)
        self.screen.blit(self.grid, (0, 0))

    def display_initial_positions(self):
        """
        Displays each robot in their initial position (in the main script it's defined
        by the JSON values).
        """
        for robot in self.robot_characters:
            robot.rotate_move()
        pygame.display.flip()

    def animate(
        self,
        x_values: numpy.ndarray,
        y_values: numpy.ndarray,
        theta_values: numpy.ndarray,
    ):
        """
        Initializes the window and starts the animation passing the arrays to the animation method.
        """
        self.initialize()  # Initialize pygame
        self.start_animation(x_values, y_values, theta_values)

    def start_animation(
        self,
        x_values: numpy.ndarray,
        y_values: numpy.ndarray,
        theta_values: numpy.ndarray,
    ):
        """
        It takes the arrays to animate the robots based on simulation data,
        it also handles the pygame events to start and stop the animation. The basic flow of this is
        that it iterates over the robot_characters added previously, and for each index it looks for the
        corresponding data on the numpy arrays, to assign the corresponding x, y, theta data for each robot.
        Then with the robot_character methods, it updates the picture position and orientation, deleting the
        previous one until it reaches the final data.

        """
        index = (
            0  # Initialize the index for accessing x_values, y_values and theta_values
        )
        animation_running = False
        index_error = 0
        for robot_index in range(len(self.robot_characters)):
            x_robot = x_values[0][robot_index]  # Initial x position
            y_robot = y_values[0][robot_index]  # Initial y position
            theta_robot = theta_values[0][robot_index]  # Initial theta value
            self.robot_characters[robot_index].update(theta_robot, x_robot, y_robot)
            self.robot_characters[robot_index].rotate_move()

        pygame.display.flip()
        pygame.time.delay(10)

        while self.run:
            self.clock.tick(60)
            self.play.draw()  # Update the play button

            # Flag to terminate window correctly without crashing all Python execution
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False
                    break

            self.screen.fill(self.background_color)
            self.screen.blit(self.grid, (0, 0))
            self.play.draw()
            self.display_initial_positions()  # this keeps the robots at their final position even when the time has finished :D

            if self.play.action and not animation_running:
                print("START")
                animation_running = True  # Start the animation
                index = 0  # Reset the index

            for i in range(len(self.robot_characters)):
                for j in range(i + 1, len(self.robot_characters)):
                    if robot_character.check_collision(
                        self.robot_characters[i], self.robot_characters[j]
                    ):
                        # Handle collision here (e.g., change color, stop movement, etc.)
                        print("Collision")
                        animation_running = False  # Stop the animation
                        pygame.time.delay(1000)  # Wait until pygame window closes
                        self.run = False
                        self.index_error = 3

            for robot in self.robot_characters:
                if not self.bounding_box.collidepoint(robot.x, robot.y):
                    # Handle collision with bounding box (e.g., stop movement, change direction, etc.)
                    print("Collision")
                    animation_running = False  # Stop the animation
                    pygame.time.delay(1000)
                    self.run = False
                    self.index_error = 3

            if animation_running and index < len(x_values):
                for i in range(len(self.robot_characters)):
                    x_robot = x_values[index][i]  # x-value for the i-th robot
                    y_robot = y_values[index][
                        i
                    ]  # corresponding y-value for the i-th robot
                    theta_robot = theta_values[index][
                        i
                    ]  # corresponding theta-value for the i-th robot

                    robot = self.robot_characters[i]

                    # Update character attributes and animations
                    robot.update(theta_robot, x_robot, y_robot)
                    robot.rotate_move()

                pygame.display.flip()
                pygame.time.delay(10)
                index += 1

            pygame.display.flip()

            if animation_running and index >= len(x_values):
                animation_running = False  # Stop the animation

        pygame.quit()  # Quit Pygame after the loop finishes


class py_game_monitoring(py_game_animation):
    """
    Child class of the pygame animation window for simulated (pre-calculated) data.
    What changes here is the start_animation method, instead of iteration over data, it receives
    constantly new data as it's intended for real time display of the motion of the robots.
    The data is obtained by an external system (OptiTrack).
    #"""

    def __init__(self, width, height, data_src_funct):
        super().__init__(width, height)
        self.data_src_funct = data_src_funct

    def start_animation(self):
        """
        It takes the arrays to animate the robots based on simulation data,
        it also handles the pygame events to start and stop the animation. The basic flow of this is
        that it iterates over the robot_characters added previously, and for each index it looks for the
        corresponding data on the numpy arrays, to assign the corresponding x, y, theta data for each robot.
        Then with the robot_character methods, it updates the picture position and orientation, deleting the
        previous one until it reaches the final data.

        """

        index = (
            0  # Initialize the index for accessing x_values, y_values and theta_values
        )
        animation_running = True

        # for robot_index in range(len(self.robot_characters)):
        #     x_robot = x_values[0][robot_index]  # Initial x position
        #     y_robot = y_values[0][robot_index]  # Initial y position
        #     theta_robot = theta_values[0][robot_index]  # Initial theta value
        #     self.robot_characters[robot_index].update(theta_robot, x_robot, y_robot)
        #     self.robot_characters[robot_index].rotate_move()

        #pygame.display.flip()
        pygame.time.delay(10)

        while self.run:
            self.clock.tick(60)
            self.play.draw()  # Update the play button
            x_values, y_values, theta_values, x_raw, y_raw, theta_raw = self.data_src_funct()
            # Separate data into pairs
            pairs_x = [x_values[i:i+2] for i in range(0, len(x_values), 2)]
            pairs_y = [y_values[i:i+2] for i in range(0, len(y_values), 2)]
            pairs_theta = [theta_values[i:i+2] for i in range(0, len(theta_values), 2)]
            # Print the pairs
            # for pair in pairs_x:
            #     print(pair)
            with open("cuadrante3" + ".csv", "a", newline="") as file:
                writer = csv.writer(file)
                field = [
                    "x position",
                    "y position",
                    "orientation",
                ]  # titles of the columns
                #writer.writerow(i for i in field)
                # Write the field names only once, not in every iteration
                # writer.writerow(field)
                writer.writerow([x_raw[0], y_raw[0], theta_raw[0]])
            # print(x_raw, y_raw, theta_raw)
                
            for x, y, theta in zip(pairs_x, pairs_y, pairs_theta):
                print(x, y, theta)
                for i, robot in enumerate(self.robot_characters):
                    # Use the index 'i' to get the corresponding values for the current robot
                    robot.degree = float(theta[i][0]) + 180
                    robot.x = int(x[i][0])
                    robot.y = int(y[i][0])
                    # Additional modifications to the individual robot's attributes can be added here
                    # For example, you might want to update other attributes of the robot

            # Flag to terminate window correctly without crashing all Python execution
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False

            self.screen.fill(self.background_color)
            self.screen.blit(self.grid, (0, 0))
            self.display_initial_positions()  # this keeps the robots at their final position even when the time has finished :D

            if self.play.action and not animation_running:
                print("START")
                animation_running = True  # Start the animation
                index = 0  # Reset the index

            for i in range(len(self.robot_characters)):
                for j in range(i + 1, len(self.robot_characters)):
                    if robot_character.check_collision(
                        self.robot_characters[i], self.robot_characters[j]
                    ):
                        # Handle collision here (e.g., change color, stop movement, etc.)
                        print("collision")
                        # animation_running = False  # Stop the animation
                        # pygame.time.delay(1000)  # Wait until pygame window closes
                        # self.run = False

            for robot in self.robot_characters:
                if not self.bounding_box.collidepoint(robot.x, robot.y):
                    # Handle collision with bounding box (e.g., stop movement, change direction, etc.)
                    print("collision")
                    # animation_running = False  # Stop the animation
                    # pygame.time.delay(1000)
                    # self.run = False

            # if animation_running:  # and index < len(x_values):
            #     for i in range(len(self.robot_characters)):
            #         x_robot = x_values[index][i]
            #         y_robot = y_values[index][i]
            #         theta_robot = theta_values[index][i]
            #         robot = self.robot_characters[i]
            #         print(x_robot, y_robot, theta_robot)
            #         # Update character attributes and animations
            #         robot.update(theta_robot, x_robot, y_robot)
            #         robot.rotate_move()

            #         pygame.display.flip()
            #         pygame.time.delay(10)

                pygame.display.flip()
                pygame.time.delay(10)
                index += 1

            pygame.display.flip()
            # pygame.transform.flip(self.screen, True, False)

            if animation_running and index >= len(x_values):
                animation_running = False  # Stop the animation

        pygame.quit()  # Quit Pygame after the loop finishes
