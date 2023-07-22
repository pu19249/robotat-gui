import matplotlib
import pygame
import numpy as np
from map_coordinates import inverse_change_coordinates
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt5.QtWidgets import QPushButton, QGraphicsView, QGraphicsScene
from PyQt5 import uic, QtCore
import sys
from robots.robot_pololu import Pololu
from controllers.exponential_pid import pid_exponential
from controllers.lqr_pp import lqr_pp
import os

matplotlib.use('Qt5Agg')

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


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
    def __init__(self, img_path):
        # Define the image file name
        grid_file = "pictures/grid_back_coord.png"

        # Create the complete file path
        grid_path = os.path.join(script_dir, grid_file)
        self.img_path = img_path
        self.screen_x = 850
        self.screen_y = 960
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
                for x, y, theta in zip(X_sim, Y_sim, Theta_sim):
                    # x, y, theta = pololu_robot.X[-1], pololu_robot.Y[-1], pololu_robot.Theta[-1]
                    x_new, y_new = inverse_change_coordinates(
                        x, y, self.screen_y, self.screen_x)
                    theta_val = np.degrees(theta)
                    self.rotate_move(0, x_new, y_new)
                    print(x_new, y_new)
            pygame.display.flip()
            time.sleep(0.1)  # Add a small delay to reduce computation load

        pygame.quit()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # load the ui file
        uic.loadUi("main_window.ui", self)

        # define the widgets for the simulation tab
        self.sim_canvas = self.findChild(QGraphicsView, "visualization_canvas")
        self.ctrl_dropdown = self.findChild(QComboBox, "config_ctrl_box")
        self.play_btn = self.findChild(QPushButton, "sim_play_btn")

        # play btn to open the pygame animation
        self.play_btn.clicked.connect(self.play_animation)

        # combo box for ctrl choice
        ctrl_list = [("PID exponencial", "pid_exponential"),
                     ("PID punto-punto", "pid_point"), ("LQR", "lqr"), ("LQI", "lqi")]
        for x, i in enumerate(ctrl_list):
            self.ctrl_dropdown.addItem(i[0])
            self.ctrl_dropdown.setItemData(x, i[1])
        self.ctrl_dropdown.currentTextChanged.connect(self.selection_change)

        # timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        #  self.timer.timeout.connect(self.update_img_pos)
        # self.timer.timeout.connect(self.rotate_img2)
        self.timer.start()

        # define the widgets for the OTA tab

        # define the widgets for the RTD tab

        # methods used in the simulation tab widgets

        # def simulation_graphics():
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 370, 470)

        self.pololu_rep = pololu_robot.img

        self.sim_canvas.setScene(self.scene)
        self.img_item = self.scene.addPixmap(self.pololu_rep)
        self.img_item.setPos(0, 0)

        self.sim_canvas.setScene(self.scene)

        # show the app
        self.rotation_angle = 0
        self.initial_pos = self.scene.items()[0].pos()
        self.show()

        # methods used in the the OTA tab widgets

        # methods used in the rtd tab widgets

        # methods used in multiple tab widgets

    def play_animation(self):
        sim_game_animation = py_game_animation("pictures/pololu_img.png")
        sim_game_animation.initialize()
        sim_game_animation.start_animation()

    def update_img_pos(self):
        current_pos = self.scene.items()[0].pos()
        # Calculate the new position (example: move by 10 pixels in x and y direction)
        new_pos = current_pos + QtCore.QPointF(1, 1)

        # Set the new position of the image item
        self.scene.items()[0].setPos(new_pos)

    def rotate_img(self):
        print("")

    def selection_change(self, text):
        print("The choice was:", text)
        self.index = self.ctrl_dropdown.currentIndex()
        self.data = self.ctrl_dropdown.itemData(self.index)
        print(f"Data: {self.data}")

        # Update the controller of the pololu_robot instance
        self.ctrl_selected = self.data + ".py"
        pololu_robot.set_controller(self.ctrl_selected)
        print("controller:", pololu_robot.controller)
        print("IP: ", pololu_robot.IP)


# initialize the app
app = QApplication(sys.argv)

# Define the image file name
img_file = "pictures/pololu_img.png"

# Create the complete file path
img_path = os.path.join(script_dir, img_file)
state_0 = [0, 0, 0]  # Example state values
physical_params = [1, 1, 10, 10]  # Example physical parameters
ID = 1  # Example ID
IP = "192.168.1.1"  # Example IP
# Replace with the actual path to your PNG image file
img_path = "pictures/pololu_img.png"

goal = [-190, -240]
N = 3000
init_u = [0, 0]
def controller(state): return pid_exponential(goal, state)


u = 0

pololu_robot = Pololu(state_0, physical_params, ID, IP,
                      img_path, lambda state, goal=goal: lqr_pp(state, goal), u)

dt = 0.1
t0 = 0
tf = 100

xg = 100
yg = 100

goal = [xg, yg]

traj = pololu_robot.simulate_robot(dt, t0, tf, goal)
# Access the simulation results
X_sim, Y_sim, Theta_sim = pololu_robot.get_simulation_results()


# Access the number of steps taken during the simulation
num_steps = pololu_robot.get_number_of_steps()

main_window = Window()
app.exec_()
