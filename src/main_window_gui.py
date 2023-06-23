import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
from matplotlib.figure import Figure
import pygame
import numpy as np
from map_coordinates import change_coordinate

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QWidget, QTextBrowser, QLabel, QGridLayout, QRadioButton, QComboBox, QSpinBox, QPushButton, QTableView, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtBoundSignal
import sys
from robots.robot_pololu import Pololu
import controllers as ctrl
import os

from PyQt5.QtGui import QPixmap, QTransform
matplotlib.use('Qt5Agg')

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


class py_game_animation():
    def __init__(self, img_path):
        self.img_path = img_path
        self.screen = None
        self.clock = None
        self.img = None
        self.img_rect = None
        self.degree = 0
        self.x = 0
        self.y = 0
        self.counter = 10
        self.background_color = (255, 255, 255)
        # Simulation parameters
        self.dt = 0.1  # sample period
        self.t0 = 0  # initial time
        self.tf = 30  # final time
        # iteration number, convert to integer
        self.N = int((self.tf - self.t0) / self.dt)
        self.run = True
        # Initial conditions
        self.xi0 = np.array([380, 480, 0])
        self.u0 = np.array([0, 0])
        self.xi = self.xi0  # state vector
        self.u = self.u0  # input vector

        # Arrays to store state, inputs, and outputs
        self.XI = np.zeros((len(self.xi), self.N + 1))
        self.U = np.zeros((len(self.u), self.N + 1))

        # Initialize arrays
        self.XI[:, 0] = self.xi0
        self.U[:, 0] = self.u0

        # Target coordinates
        self.xg = 0  # in m
        self.yg = 0  # in m
        self.yg = change_coordinate(self.yg, 960)
        self.thetag = 0  # in rad
        # PID position
        self.kpP = 1
        self.kiP = 0.0001
        self.kdP = 0.5
        self.EP = 0
        self.eP_1 = 0

        # PID orientation
        self.kpO = 2 * 5
        self.kiO = 0.0001
        self.kdO = 0
        self.EO = 0
        self.eO_1 = 0

        # Exponential approach
        self.v0 = 10
        self.alpha = 1

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode([760, 960])
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img_rect = self.img.get_rect(center=self.screen.get_rect().center)
        self.degree = 0
        self.screen.fill(self.background_color)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def rotate_move(self, degree, x, y):
        self.rot_img = pygame.transform.rotate(self.img, self.degree)
        self.img_rect = self.rot_img.get_rect(center=self.img_rect.center)
        self.screen.fill(self.background_color)
        # self.screen.blit(self.rot_img, self.img_rect.topleft)
        self.screen.blit(self.rot_img, (self.x, self.y))
        pygame.display.flip()

    def x_y_movement(self, x, y):
        self.screen.fill(self.background_color)
        self.screen.blit(self.img, (self.x, self.y))
        pygame.display.flip()

    def animate(self):
        self.initialize()  # Initialize pygame
        self.start_animation()  # Start the animation loop

    def start_animation(self):
        self.clock = pygame.time.Clock()
        for n in range(self.N):
            self.x = self.xi[0]
            self.y = self.xi[1]
            self.theta = self.xi[2]
            self.e = np.array([self.xg - self.x, self.yg - self.y])
            self.thetag = np.arctan2(self.e[1], self.e[0])

            self.eP = np.linalg.norm(self.e)
            self.eO = self.thetag - self.theta
            self.eO = np.arctan2(np.sin(self.eO), np.cos(self.eO))

            self.kP = self.v0 * \
                (1 - np.exp(-self.alpha * self.eP ** 2)) / self.eP
            self.v = self.kP * self.eP

            self.eO_D = self.eO - self.eO_1
            self.EO = self.EO + self.eO
            self.w = self.kpO * self.eO + self.kiO * self.EO + self.kdO * self.eO_D
            self.eO_1 = self.eO

            self.u = np.array([self.v, self.w])

            self.k1 = pololu_robot.dynamics(self.xi, self.u)
            self.k2 = pololu_robot.dynamics(
                self.xi + np.multiply(self.dt / 2, self.k1), self.u)
            self.k3 = pololu_robot.dynamics(
                self.xi + np.multiply(self.dt / 2, self.k2), self.u)
            self.k4 = pololu_robot.dynamics(
                self.xi + np.multiply(self.dt, self.k3), self.u)

            self.k1 = np.reshape(self.k1, self.xi.shape)
            self.k2 = np.reshape(self.k2, self.xi.shape)
            self.k3 = np.reshape(self.k3, self.xi.shape)
            self.k4 = np.reshape(self.k4, self.xi.shape)

            self.xi = self.xi + (self.dt / 6) * \
                (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)

            self.XI[:, n + 1] = self.xi
            self.U[:, n + 1] = self.u

            # Update the state variables
            self.q = self.XI[:, n]
            self.x = self.q[0]
            self.y = self.q[1]
            # Update angular velocity based on control inputs or desired behavior
            # Example: Use the second element of self.u as angular velocity
            self.angular_velocity = self.u[1]

            # Update the rotation angle
            self.degree += np.degrees(self.angular_velocity)
            # self.degree = np.degrees(self.q[2])

            # Rotate and move the image
            self.rotate_move(self.degree, self.x, self.y)

            # Check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.clock.tick(60)  # Limit the frame rate

        pygame.quit()

    # def start_animation(self):
    #     for n in range(self.N):
    #         self.x = self.xi[0]
    #         self.y = self.xi[1]
    #         self.theta = self.xi[2]
    #         self.e = np.array([self.xg - self.x, self.yg - self.y])
    #         self.thetag = np.arctan2(self.e[1], self.e[0])

    #         self.eP = np.linalg.norm(self.e)
    #         self.eO = self.thetag - self.theta
    #         self.eO = np.arctan2(np.sin(self.eO), np.cos(self.eO))

    #         self.kP = self.v0 * \
    #             (1 - np.exp(-self.alpha * self.eP ** 2)) / self.eP
    #         self.v = self.kP * self.eP

    #         self.eO_D = self.eO - self.eO_1
    #         self.EO = self.EO + self.eO
    #         self.w = self.kpO * self.eO + self.kiO * self.EO + self.kdO * self.eO_D
    #         self.eO_1 = self.eO

    #         self.u = np.array([self.v, self.w])

    #         self.k1 = pololu_robot.dynamics(self.xi, self.u)
    #         self.k2 = pololu_robot.dynamics(
    #             self.xi + np.multiply(self.dt / 2, self.k1), self.u)
    #         self.k3 = pololu_robot.dynamics(
    #             self.xi + np.multiply(self.dt / 2, self.k2), self.u)
    #         self.k4 = pololu_robot.dynamics(
    #             self.xi + np.multiply(self.dt, self.k3), self.u)

    #         self.k1 = np.reshape(self.k1, self.xi.shape)
    #         self.k2 = np.reshape(self.k2, self.xi.shape)
    #         self.k3 = np.reshape(self.k3, self.xi.shape)
    #         self.k4 = np.reshape(self.k4, self.xi.shape)

    #         self.xi = self.xi + (self.dt / 6) * \
    #             (self.k1 + 2 * self.k2 + 2 * self.k3 + self.k4)

    #         self.XI[:, n + 1] = self.xi
    #         self.U[:, n + 1] = self.u
    #     # while self.run:
    #     #     for e in pygame.event.get():
    #     #         if e.type == pygame.USEREVENT:
    #     #             self.tf -= 1
    #     #             print(self.counter)
    #     #             if self.tf == 0:
    #     #                 self.run = False
    #     #         if e.type == pygame.QUIT:
    #     #             self.run = False

    #     #     # pygame.display.flip()
    #     #     '''
    #     #     The convert_alpha() method is used when loading the image to preserve transparency.
    #     #     The rotation center is correctly set by obtaining the rect of the rotated image and setting its
    #     #     center to self.img_rect.center.
    #     #     The image is blitted onto the screen using the top-left corner of the rect (self.img_rect.topleft).
    #     #     '''
    #     #     # self.x_y_movement(self.x, self.y)
    #     #     self.rotate_move(self.degree, self.x, self.y)
    #     #     self.clock.tick(60)
    #     #     self.x += 1  # update with values from ctrl
    #     #     self.y += 1  # update with values from ctrl
    #     #     self.degree += 1
    #         self.q = self.XI[:, n]
    #         self.x = self.q[0]
    #         self.y = self.q[1]
    #         self.degree = self.q[2]
    #         self.rotate_move(self.degree, self.x, self.y)
    #     pygame.quit()


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
        sim_game_animation = py_game_animation("pololu_img.png")
        sim_game_animation.animate()
        # sim_game_animation.initialize()
        # sim_game_animation.start_animation()

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
img_file = "pololu_img.png"

# Create the complete file path
img_path = os.path.join(script_dir, img_file)
state = [0, 0, 0]  # Example state values
physical_params = [1, 1, 10, 10]  # Example physical parameters
ID = 1  # Example ID
IP = "192.168.1.1"  # Example IP
# img_path = "pololu_img.png"  # Replace with the actual path to your PNG image file
controller = 0
u = 0

pololu_robot = Pololu(state, physical_params, ID, IP, img_path, controller, u)

main_window = Window()
app.exec_()
