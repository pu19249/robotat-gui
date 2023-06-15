import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QWidget, QTextBrowser, QLabel, QGridLayout, QRadioButton, QComboBox, QSpinBox, QPushButton, QTableView, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import uic, QtCore
import sys
from robots.robot_pololu import Pololu
import os
import matplotlib
from PyQt5.QtGui import QPixmap
matplotlib.use('Qt5Agg')

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # load the ui file
        uic.loadUi("main_window.ui", self)

        # define the widgets for the simulation tab
        self.sim_canvas = self.findChild(QGraphicsView, "visualization_canvas")
        img_file = "pololu_img.png"
        img_item = QPixmap(img_file)
        img = QGraphicsPixmapItem(img_item)
        self.ctrl_dropdown = self.findChild(QComboBox, "config_ctrl_box")
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_img_pos)
        self.timer.start()
        # define the widgets for the OTA tab

        # define the widgets for the RTD tab

        # methods used in the simulation tab widgets

        # def simulation_graphics():
        self.scene = QGraphicsScene()
        # self.graphWidget = pg.PlotWidget(scene)
        # self.setCentralWidget(self.graphWidget)
        self.pololu_rep = pololu_robot.img
        self.text_item = self.scene.addPixmap(self.pololu_rep)
        self.sim_canvas.setScene(self.scene)

        # img.setOffset(100, 100)
        # call the simulation_graphics method
        # simulation_graphics()
        # update_plot_data(img)
        # show the app
        self.show()

        # methods used in the the OTA tab widgets

        # methods used in the rtd tab widgets

        # methods used in multiple tab widgets
    def update_img_pos(self):
        current_pos = self.scene.items()[0].pos()
        # Calculate the new position (example: move by 10 pixels in x and y direction)
        new_pos = current_pos + QtCore.QPointF(1, 1)

        # Set the new position of the image item
        self.scene.items()[0].setPos(new_pos)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


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
