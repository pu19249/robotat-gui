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
        # 15 pixels to get the center not in the limit but considering the width of the picture (robot)
        self.x = 380
        self.y = 480

        self.counter = 10
        self.background_color = (255, 255, 255)
        self.run = True

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode([760, 960])
        self.x = change_coordinate_x(self.x, 760)
        self.y = change_coordinate_y(self.y, 960)
        pygame.display.set_caption('Live simulation')
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load(self.img_path).convert_alpha()
        self.img_rect = self.img.get_rect(center=self.screen.get_rect().center)
        self.degree = 0
        self.screen.fill(self.background_color)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

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

    def x_y_movement(self, x, y):
        self.screen.fill(self.background_color)
        self.screen.blit(self.img, (self.x, self.y))
        pygame.display.flip()

    def animate(self):
        self.initialize()  # Initialize pygame
        self.start_animation()  # Start the animation loop

    def start_animation(self):
        while self.run:
            for e in pygame.event.get():
                if e.type == pygame.USEREVENT:
                    self.counter -= 1
                    print(self.counter)
                    if self.counter == 0:
                        self.run = False
                if e.type == pygame.QUIT:
                    self.run = False

            # pygame.display.flip()
            '''
            The convert_alpha() method is used when loading the image to preserve transparency.
            The rotation center is correctly set by obtaining the rect of the rotated image and setting its
            center to self.img_rect.center.
            The image is blitted onto the screen using the top-left corner of the rect (self.img_rect.topleft).
            '''
            # self.x_y_movement(self.x, self.y)
            self.rotate_move(self.degree, self.x, self.y)
            self.clock.tick(60)
            self.x += 0  # update with values from ctrl
            self.y += 0  # update with values from ctrl
            self.degree += 1
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
