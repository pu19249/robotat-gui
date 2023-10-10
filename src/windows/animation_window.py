import pygame
import os
import ctypes

# Get the directory path of the current script, abspath because of the tree structure that everything is on different folders
script_dir = os.path.dirname(os.path.abspath(__file__))
pictures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pictures')
# this solves scaling issues for the independent pygame window
ctypes.windll.user32.SetProcessDPIAware()

# Button class for handling actions as 'Play' for the animation
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

# class for handling position and orientation on the animation window
# also collision because is related with the rect it occupates
class robot_character():
    def __init__(self, img_path, x, y, degree, screen, size):
        self.img_path = img_path
        self.screen = screen
        self.x = x
        self.y = y
        self.degree = degree
        self.size = size
        self.radius = 10 # radius it occupates in the animation window

        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img = pygame.transform.scale(
            self.img, (40, 40))  # Resize the image if needed
        self.rot_img = self.img
        self.rot_rect = self.img.get_rect(center=(x, y))
        
        self.background_color = (255, 255, 255)
        self.grid = pygame.image.load(os.path.join(pictures_dir, "grid_back_coord.png")).convert_alpha()

    # box based on the radius defined before
    def draw_hitbox(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), self.radius, 2)

    #  distance formula to check if the distance between the centers of two robots is less than the sum of their radii
    def check_collision(robot1, robot2):
        distance = ((robot1.x - robot2.x)**2 + (robot1.y - robot2.y)**2)**0.5
        return distance < robot1.radius + robot2.radius

    # degree, x, and y are state attributes of the robot class
    # when this method is called the attributes are updated and so
    # in the rotate move method they are already updated without the need of
    # passing them the value
    def update(self, degree, x, y):
        self.degree = degree
        self.x = x
        self.y = y

    def rotate_move(self):
        rotated_img = pygame.transform.rotate(self.img, self.degree)
        rotated_rect = rotated_img.get_rect(center=(self.x, self.y))

        # Blit the rotated robot image
        self.screen.blit(rotated_img, rotated_rect)


class py_game_animation():
    def __init__(self, x_size, y_size):

        # self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        grid_file = os.path.join(pictures_dir, "grid_back_coord.png")

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
        self.bounding_box = pygame.Rect(0, 0, 760, 960)  # Create a rectangle around the grid

        # the list size will be defined by the number of robots indicated
        self.robot_characters = []

    # this method will create as many robots need to be created inside
    # this animation window
    def add_robot_character(self, img_path, x, y, degree):
        robot = robot_character(img_path, x, y, degree,
                                self.screen, [self.screen_x, self.screen_y])
        self.robot_characters.append(robot)

    def update_robot_characters(self, x_vals_display, y_vals_display, theta_vals_display):
            for robot_character, x, y, theta in zip(self.robot_characters, x_vals_display, y_vals_display, theta_vals_display):
                robot_character.update(theta, x, y)
    
    def initialize(self):
        pygame.init()
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        play_icon = pygame.image.load(os.path.join(pictures_dir, "play_icon.png")).convert_alpha()
        play_icon = pygame.transform.scale(play_icon, (self.screen_x*0.05, self.screen_x*0.05))
        self.play = button_pygame(self.screen_x - 50, self.screen_y/2, play_icon, self.screen)
        self.play.draw()
        
        self.screen.fill(self.background_color)
        self.screen.blit(self.grid, (0, 0))
        
    def display_initial_positions(self):
        for robot in self.robot_characters:
            robot.rotate_move()
        pygame.display.flip()


    def animate(self, x_values, y_values, theta_values):
        self.initialize()  # Initialize pygame
        self.start_animation(x_values, y_values, theta_values)


    def start_animation(self, x_values, y_values, theta_values):
        index = 0  # Initialize the index for accessing x_values and y_values
        animation_running = False
        
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
            self.display_initial_positions() # this keeps the robots at their final position even when the time has finished :D
            
            if self.play.action and not animation_running:
                print('START')
                animation_running = True  # Start the animation
                index = 0  # Reset the index
            
            for i in range(len(self.robot_characters)):
                    for j in range(i + 1, len(self.robot_characters)):
                        if robot_character.check_collision(self.robot_characters[i], self.robot_characters[j]):
                            # Handle collision here (e.g., change color, stop movement, etc.)
                            print('collision')
                            animation_running = False  # Stop the animation
                            pygame.time.delay(1000)
                            self.run = False

            for robot in self.robot_characters:
                if not self.bounding_box.collidepoint(robot.x, robot.y):
                    # Handle collision with bounding box (e.g., stop movement, change direction, etc.)
                    print('collision')
                    animation_running = False  # Stop the animation
                    pygame.time.delay(1000)
                    self.run = False
                    

            if animation_running and index < len(x_values):
                
                for i in range(len(self.robot_characters)):
                    x_robot = x_values[index][i]  # x-value for the i-th robot
                    y_robot = y_values[index][i]  # corresponding y-value for the i-th robot
                    theta_robot = theta_values[index][i]  # corresponding theta-value for the i-th robot

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
    def start_animation(self, x_values, y_values, theta_values):
        index = 0  # Initialize the index for accessing x_values and y_values
        animation_running = False
        
        for robot_index in range(len(self.robot_characters)):
            x_robot, y_robot, theta_robot = next(real_time_data_generator)  # Get real-time data
            self.robot_characters[robot_index].update(theta_robot, x_robot, y_robot)
            self.robot_characters[robot_index].rotate_move()


        pygame.display.flip()
        pygame.time.delay(10)

        while self.run:
            
            self.clock.tick(60)
            self.play.draw()  # Update the play button

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False
                    break

            self.screen.fill(self.background_color)
            self.screen.blit(self.grid, (0, 0))
            self.play.draw()
            self.display_initial_positions() # this keeps the robots at their final position even when the time has finished :D
            
            if self.play.action and not animation_running:
                print('START')
                animation_running = True  # Start the animation
                index = 0  # Reset the index
            
            for i in range(len(self.robot_characters)):
                    for j in range(i + 1, len(self.robot_characters)):
                        if robot_character.check_collision(self.robot_characters[i], self.robot_characters[j]):
                            # Handle collision here (e.g., change color, stop movement, etc.)
                            print('collision')
                            animation_running = False  # Stop the animation
                            pygame.time.delay(1000)
                            self.run = False

            for robot in self.robot_characters:
                if not self.bounding_box.collidepoint(robot.x, robot.y):
                    # Handle collision with bounding box (e.g., stop movement, change direction, etc.)
                    print('collision')
                    animation_running = False  # Stop the animation
                    pygame.time.delay(1000)
                    self.run = False
                    

            if animation_running and index < len(x_values):
                
                for i in range(len(self.robot_characters)):
                    x_robot = x_values[index][i]  # x-value for the i-th robot
                    y_robot = y_values[index][i]  # corresponding y-value for the i-th robot
                    theta_robot = theta_values[index][i]  # corresponding theta-value for the i-th robot

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