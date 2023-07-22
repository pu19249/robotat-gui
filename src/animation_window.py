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


class py_game_animation():
    def __init__(self, img_path, x_size, y_size):
        # Define the image file name
        grid_file = "pictures/grid_back_coord.png"

        # Create the complete file path
        grid_path = os.path.join(script_dir, grid_file)
        self.img_path = img_path
        self.screen_x = x_size
        self.screen_y = y_size
        self.screen = pygame.display.set_mode([self.screen_x, self.screen_y])
        self.clock = None
        self.img = None
        self.img_rect = None
        self.degree = 0
        self.counter = 30
        self.background_color = (255, 255, 255)
        self.run = True
        self.grid = pygame.image.load(grid_path).convert_alpha()
        self.play = None

    def initialize(self):
        pygame.init()
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load(self.img_path).convert_alpha()
        play_icon = pygame.image.load('pictures/play_icon.png').convert_alpha()
        play_icon = pygame.transform.scale(play_icon, (50, 50))
        self.play = button_pygame(780, 480, play_icon, self.screen)
        self.play.draw()
        self.img_rect = self.img.get_rect(center=self.screen.get_rect().center)
        self.degree = 0
        self.screen.fill(self.background_color)
        self.screen.blit(self.grid, (0, 0))

        self.x_0 = 0
        self.y_0 = 0

    def rotate_move(self, degree, x, y):
        self.rot_img = pygame.transform.rotate(self.img, degree)
        self.rot_rect = self.rot_img.get_rect(center=(x, y))
        self.screen.fill(self.background_color)
        self.screen.blit(self.grid, (0, 0))
        self.screen.blit(self.rot_img, self.rot_rect)
        pygame.display.flip()
        '''
        Pass the degree argument directly to pygame.transform.rotate() without using self.degree, as degree is already the parameter for rotation angle.
        Create a new rot_rect variable to store the rect (position and size) of the rotated image.
        Set the center of the rot_rect to (x, y), which will make the rotation occur around this point.
        Blit the rotated image onto the screen using self.rot_img and self.rot_rect.
        '''

    def animate(self):
        self.initialize()  # Initialize pygame
        self.start_animation()  # Start the animation loop

    def start_animation(self):
        while self.run:

            self.clock.tick(60)
            # print(traj[0], traj[1], traj[2])
            # for n in pololu_robot.X:
            #     print(n)
            self.play.draw()  # Update the play button

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False

            # x = change_coordinate_x(760, self.screen_x)
            # y = change_coordinate_y(960, self.screen_y)
            # the user gives the goal in quadrants, so the code
            # maps it back to the original system
            # for e.g. the user gives (-120, 140) the pygame coordinate system would expect a (500, 620) so the -120, 140 are the parameters for the inverse_change_coordinates func.

            if self.play.action:
                print('START')
                # for x, y, theta in zip(X_sim, Y_sim, Theta_sim):
                #     # x, y, theta = pololu_robot.X[-1], pololu_robot.Y[-1], pololu_robot.Theta[-1]
                #     x_new, y_new = inverse_change_coordinates(
                #         x, y, self.screen_y, self.screen_x)
                #     theta_val = np.degrees(theta)
                #     self.rotate_move(0, x_new, y_new)
                #     print(x_new, y_new)
            pygame.display.flip()
            time.sleep(0.1)  # Add a small delay to reduce computation load

        pygame.quit()
