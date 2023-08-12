import pygame
import os
import time
import ctypes
import numpy as np

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# this solves scaling issues for the independent pygame window
ctypes.windll.user32.SetProcessDPIAware()

class button_pygame():
    def __init__(self, x, y, image, screen):
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.action = None
        self.pos = None

    def draw(self):
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


class robot_character():
    def __init__(self, img_path, x, y, degree, screen, size):
        self.img_path = img_path
        self.screen = screen
        self.x = x
        self.y = y
        self.degree = degree
        self.size = size

        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img = pygame.transform.scale(
            self.img, (40, 40))  # Resize the image if needed
        self.rot_img = self.img
        self.rot_rect = self.img.get_rect(center=(x, y))

        self.background_color = (255, 255, 255)
        self.grid = pygame.image.load(
            "pictures/grid_back_coord.png").convert_alpha()

    # degree, x, and y are state attributes of the robot class
    # when this method is called the attributes are updated and so
    # in the rotate move method they are already updated without the need of
    # passing them the value
    def update(self, degree, x, y):
        self.degree = degree
        self.x = x
        self.y = y
        # print(self.x, self.y, self.degree)

    def rotate_move(self):
        rotated_img = pygame.transform.rotate(self.img, self.degree)
        rotated_rect = rotated_img.get_rect(center=(self.x, self.y))

        # Blit the rotated robot image
        self.screen.blit(rotated_img, rotated_rect)
    def __str__(self):
        return self.img_path

class py_game_animation():
    def __init__(self, x_size, y_size):

        # self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        # Define the image file name
        grid_file = "pictures/grid_back_coord.png"

        # Create the complete file path
        grid_path = os.path.join(script_dir, grid_file)
        self.screen_x = x_size
        self.screen_y = y_size
        self.original_size = (self.screen_x, self.screen_y)
        self.screen = pygame.display.set_mode([self.screen_x, self.screen_y], pygame.RESIZABLE)
        self.background_color = (255, 255, 255)
        self.run = True
        self.grid_img = pygame.image.load(grid_path).convert_alpha()
        self.grid = pygame.transform.scale(self.grid_img, (self.screen_x-90, self.screen_y))
        self.play = None
        # the list size will be defined by the number of robots indicated
        self.robot_characters = []

    # this method will create as many robots need to be created inside
    # this animation window
    def add_robot_character(self, img_path, x, y, degree):
        robot = robot_character(img_path, x, y, degree,
                                self.screen, [self.screen_x, self.screen_y])
        self.robot_characters.append(robot)

    def update_robot_characters(self, x_vals_display, y_vals_display):
            for robot_character, x, y in zip(self.robot_characters, x_vals_display, y_vals_display):
                robot_character.update(0, x, y)
                print(x, y)
    def initialize(self):
        pygame.init()
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        play_icon = pygame.image.load('pictures/play_icon.png').convert_alpha()
        play_icon = pygame.transform.scale(play_icon, (self.screen_x*0.05, self.screen_x*0.05))
        self.play = button_pygame(self.screen_x - 50, self.screen_y/2, play_icon, self.screen)
        self.play.draw()
        self.screen.fill(self.background_color)
        self.screen.blit(self.grid, (0, 0))

    def animate(self, x_values, y_values, theta_values):
        self.initialize()  # Initialize pygame
        self.start_animation(x_values, y_values, theta_values)

    def start_animation(self, x_values, y_values, theta_values):
        index = 0  # Initialize the index for accessing x_values and y_values
        animation_running = False

        while self.run:
            self.clock.tick(60)
            self.play.draw()  # Update the play button

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False
                    break
                elif e.type == pygame.VIDEORESIZE:
                    self.screen_x, self.screen_y = e.w, e.h
                    self.screen = pygame.display.set_mode((self.screen_x, self.screen_y), pygame.RESIZABLE)

                    # Calculate the aspect ratio of the original image
                    original_aspect_ratio = self.original_size[0] / self.original_size[1]

                    # Calculate the maximum width based on the height to maintain aspect ratio
                    max_width = int(self.screen_y * original_aspect_ratio)

                    # Use the smaller of max_width and screen_x to avoid exceeding the screen dimensions
                    new_width = min(max_width, self.screen_x)

                    # Calculate the corresponding height
                    new_height = int(new_width / original_aspect_ratio)

                    self.grid = pygame.transform.scale(self.grid_img, (new_width, new_height))

            self.screen.fill(self.background_color)
            self.screen.blit(self.grid, (0, 0))
            self.play.draw()
            
            if self.play.action and not animation_running:
                print('START')
                animation_running = True  # Start the animation
                index = 0  # Reset the index

            if animation_running and index < len(x_values):
                x_robot1 = x_values[index][0]  # x-value for the first robot
                x_robot2 = x_values[index][1]  # x-value for the second robot
                y_robot1 = y_values[index][0]  # corresponding y-value for the first robot
                y_robot2 = y_values[index][1]  # corresponding y-value for the second robot
                theta_robot1 = theta_values[index][0]  # corresponding y-value for the first robot
                theta_robot2 = theta_values[index][1]  # corresponding y-value for the second robot
                # self.robot_characters[0].update(theta_robot1, x_robot1, y_robot1)
                # print(self.robot_characters[0])
                # self.robot_characters[0].rotate_move()
                # self.robot_characters[1].update(theta_robot2, x_robot2, y_robot2)
                # self.robot_characters[1].rotate_move()
                # print(self.robot_characters[1])
                for robot, x, y, theta in zip(self.robot_characters, [x_robot1, x_robot2], [y_robot1, y_robot2], [theta_robot1, theta_robot2]):
                    # Update character attributes and animations if needed
                    robot.update(theta, x, y)
                    robot.rotate_move()
                
                pygame.display.flip()
                pygame.time.delay(10)
                index += 1
                # print(index)

            pygame.display.flip()

            if animation_running and index >= len(x_values):
                animation_running = False  # Stop the animation

        pygame.quit()  # Quit Pygame after the loop finishes

