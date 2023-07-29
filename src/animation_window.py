import pygame
import os
import time
import ctypes

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

        self.screen = pygame.display.set_mode([self.size[0], self.size[1]])
        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img_rect = self.img.get_rect(center=screen.get_rect().center)

    def rotate_move(self, degree, x, y):
        self.rot_img = pygame.transform.rotate(self.img, degree)
        self.rot_rect = self.rot_img.get_rect(center=(x, y))
        self.screen.fill(self.background_color)  # background color
        self.screen.blit(self.grid, (0, 0))
        self.screen.blit(self.rot_img, self.rot_rect)
        pygame.display.flip()


class py_game_animation():
    def __init__(self, x_size, y_size):
        # Define the image file name
        grid_file = "pictures/grid_back_coord.png"

        # Create the complete file path
        grid_path = os.path.join(script_dir, grid_file)
        self.screen_x = x_size
        self.screen_y = y_size
        self.screen = pygame.display.set_mode([self.screen_x, self.screen_y])
        self.background_color = (255, 255, 255)
        self.run = True
        self.grid = pygame.image.load(grid_path).convert_alpha()
        self.play = None
        # the list size will be defined by the number of robots indicated
        self.robot_characters = []

    def add_robot_character(self, img_path, x, y, degree):
        robot = robot_character(img_path, x, y, degree,
                                self.screen, [self.screen_x, self.screen_y])
        self.robot_characters.append(robot)

    def initialize(self):
        pygame.init()
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        play_icon = pygame.image.load('pictures/play_icon.png').convert_alpha()
        play_icon = pygame.transform.scale(play_icon, (50, 50))
        self.play = button_pygame(780, 480, play_icon, self.screen)
        self.play.draw()
        self.screen.fill(self.background_color)
        self.screen.blit(self.grid, (0, 0))

        for robot in self.robot_characters:
            robot.initialize()

    def animate(self):
        self.initialize()  # Initialize pygame
        self.start_animation()  # Start the animation loop

    def start_animation(self):
        while self.run:

            self.clock.tick(60)
            self.play.draw()  # Update the play button

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    break

            if self.play.action:
                print('START')

                # Move and rotate each robot character
                for robot in self.robot_characters:
                    robot.rotate_move(robot.degree, robot.x,
                                      robot.y)

            pygame.display.flip()
            time.sleep(0.1)  # Add a small delay to reduce computation load
        pygame.quit()
