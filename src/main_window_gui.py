import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
from matplotlib.figure import Figure
import pygame
import numpy as np
from map_coordinates import change_coordinate_y, change_coordinate_x

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QWidget, QTextBrowser, QLabel, QGridLayout, QRadioButton, QComboBox, QSpinBox, QPushButton, QTableView, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtBoundSignal
import sys
from robots.robot_pololu import Pololu
import controllers as ctrl
from controllers.pid_exponential import pid_exponential
import os

from PyQt5.QtGui import QPixmap, QTransform
matplotlib.use('Qt5Agg')

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


class py_game_animation():
    def __init__(self, img_path):
        self.img_path = img_path
        self.screen_x = 760
        self.screen_y = 960
        self.screen = pygame.display.set_mode([self.screen_x, self.screen_y])
        self.clock = None
        self.img = None
        self.img_rect = None
        self.degree = 0
        self.counter = 30
        self.background_color = (255, 255, 255)
        self.run = True

    def initialize(self):
        pygame.init()
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img_rect = self.img.get_rect(center=self.screen.get_rect().center)
        self.degree = 0
        self.screen.fill(self.background_color)

        self.x_0 = 0
        self.y_0 = 0

    def rotate_move(self, degree, x, y):
        self.rot_img = pygame.transform.rotate(self.img, degree)
        self.rot_rect = self.rot_img.get_rect(center=(x, y))
        self.screen.fill(self.background_color)
        # self.screen.blit(self.rot_img, self.img_rect.topleft)
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
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False

            dt = 0.01
            t0 = 0
            tf = 30

            xi0, u0, xi, XI, U, kpO, kiO, kdO, EO, eO_1, v0, alpha = initial_parameters(
                dt, t0, tf)
            xg = 100
            yg = 200
            goal = [380, 480]
            xg = change_coordinate_x(xg, self.screen_x)
            yg = change_coordinate_y(yg, self.screen_y)
            print(xg, yg)
            thetag = 0
            seltraj = 0
            traj = 0
            XI, U, x, y, theta, X, Y, Theta = simulate_robot(
                dt, t0, tf, xi0, u0, xg, yg, thetag, seltraj, traj, kpO, kiO, kdO, EO, eO_1, v0, alpha, pololu_robot)

            self.clock.tick(60)

            for i, (x, y, theta) in enumerate(zip(X, Y, Theta)):
                x_coord = change_coordinate_x(x, self.screen_x)
                y_coord = change_coordinate_y(y, self.screen_y)
                print(x_coord, y_coord)
                # x_coord = change_coordinate_x(0, self.screen_x)
                # y_coord = change_coordinate_y(0, self.screen_y)
                theta_val = np.degrees(theta)
                # print(theta_val)
                # theta_val = 0
                self.rotate_move(theta_val, x_coord, y_coord)
            pygame.display.flip()
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
        sim_game_animation = py_game_animation("pololu_img.png")
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


def initial_parameters(dt, t0, tf):
    N = int((tf - t0) / dt)
    # initial conditions
    xi0 = np.array([0, 0, 0])
    u0 = np.array([0, 0])
    xi = xi0  # state vector
    u = u0  # input vector

    # Arrays to store state, inputs, and outputs
    XI = np.zeros((len(xi), N + 1))
    U = np.zeros((len(u), N + 1))

    # initialize arrays
    XI[:, 0] = xi0
    U[:, 0] = u0

    # PID position
    kpP = 1
    kiP = 0.0001
    kdP = 0.5
    EP = 0
    eP_1 = 0

    # PID orientation
    kpO = 10
    kiO = 0.0001
    kdO = 0
    EO = 0
    eO_1 = 0

    # exponential approach
    v0 = 10
    alpha = 1

    return xi0, u0, xi, XI, U, kpO, kiO, kdO, EO, eO_1, v0, alpha


def runge_kutta(dt, XI, U, n, xi, u, robot):
    k1 = robot.dynamics(xi, u)
    k2 = robot.dynamics(xi + np.multiply(dt / 2, k1), u)
    k3 = robot.dynamics(xi + np.multiply(dt / 2, k2), u)
    k4 = robot.dynamics(xi + np.multiply(dt, k3), u)

    k1 = np.reshape(k1, xi.shape)
    k2 = np.reshape(k2, xi.shape)
    k3 = np.reshape(k3, xi.shape)
    k4 = np.reshape(k4, xi.shape)

    xi = xi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    x = xi[0]
    y = xi[1]
    theta = xi[2]
    XI[:, n + 1] = xi
    U[:, n + 1] = u
    q = XI[:, n]
    x = q[0]
    y = q[1]
    theta = q[2]
    return x, y, theta, xi


def pid_exponential(init_cond, goal, kpO, kdO, kiO, EO, eO_1, v0, alpha):

    # controller (this must run repeteadly with the numerical method)
    x = init_cond[0]
    y = init_cond[1]
    theta = init_cond[2]
    e = np.array([goal[0] - x, goal[1] - y])
    thetag = np.arctan2(e[1], e[0])

    eP = np.linalg.norm(e)
    eO = thetag - theta
    eO = np.arctan2(np.sin(eO), np.cos(eO))

    kP = v0 * (1 - np.exp(-alpha * eP ** 2)) / eP
    v = kP * eP

    eO_D = eO - eO_1
    EO = EO + eO
    w = kpO * eO + kiO * EO + kdO * eO_D
    eO_1 = eO

    u = np.array([v, w])

    return u


def simulate_robot(dt, t0, tf, xi0, u0, xg, yg, thetag, seltraj, traj, kpO, kiO, kdO, EO, eO_1, v0, alpha, robot):
    N = int((tf - t0) / dt)

    xi = xi0  # state vector
    u = u0  # input vector

    XI = np.zeros((len(xi), N + 1))
    U = np.zeros((len(u), N + 1))

    XI[:, 0] = xi0
    U[:, 0] = u0
    X = np.zeros(N + 1)
    Y = np.zeros(N + 1)
    Theta = np.zeros(N + 1)

    for n in range(N):
        if seltraj:
            xg = traj[0, n + 1]
            yg = traj[1, n + 1]

        u = pid_exponential(xi, [xg, yg], kpO, kdO, kiO, EO, eO_1, v0, alpha)

        x, y, theta, xi = runge_kutta(dt, XI, U, n, xi, u, robot)
        thetag = theta
        XI[:, n + 1] = xi
        U[:, n + 1] = u
        X[n + 1] = x
        Y[n + 1] = y
        Theta[n + 1] = theta

    return XI, U, x, y, theta, X, Y, Theta


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
