from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QWidget, QTextBrowser, QLabel, QGridLayout, QRadioButton, QComboBox, QSpinBox, QPushButton, QTableView, QGraphicsView
from PyQt5 import uic
import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # load the ui file
        uic.loadUi("main_window.ui", self)

        # define the widgets for the simulation tab
        self.sim_canvas = self.findChild(QGraphicsView, "visualization_canvas")

        # define the widgets for the OTA tab
        
        
        # define the widgets for the RTD tab


        # methods used in the simulation tab widgets

        
        # methods used in the the OTA tab widgets


        # methods used in the rtd tab widgets


        # methods used in multiple tab widgets

        # show the app
        self.show()

# initialize the app
app = QApplication(sys.argv)
main_window = Window()
app.exec_()

