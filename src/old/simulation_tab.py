# Class definition for each of the tabs in the GUI
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime 
'''
Each window shall have:
- a CLOSE btn
- date and other basic information in the upper part
- message console
'''

class Window(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # window geometry
        # rows = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # for i in rows:
        #     self.grid_rowconfigure(i, minsize=60)

        # self.grid_columnconfigure(0, weight=4, minsize=25)
        # self.grid_columnconfigure(1, weight=1, minsize=25)
        # self.grid_columnconfigure(2, weight=1, minsize=25)
        # self.grid_columnconfigure(3, weight=1, minsize=25)
        
        # close
        self.btn = ttk.Button(self, text="Close", command=self.close_window)
        self.btn.pack()
        # self.btn.grid(row=10, column=4)

        # date
        self.today_info = tk.StringVar()
        self.update_date()
        self.today_info_disp = ttk.Label(self, textvariable=self.today_info)
        # self.today_info_disp.grid(row=0, column=2)
        self.today_info_disp.pack(side=tk.TOP)

        # console
        self.console = tk.Text(self, height=4)
        # self.console.grid(row=8, column=0)
        self.console.pack(fill="x", side=BOTTOM)
        # initial message
        self.console.insert("end", "Robotat GUI console")
        # disable input option
        self.console.config(state=DISABLED) 

        # dictionary will change (with method set_error_list) depending on the tab
        self.error_dictionary = {
            "error1":"Error 1"
        }

        # canvas for drawing
        self.visualization = tk.Canvas(self, width=380, height=480, bg="white", highlightthickness=1, highlightbackground="black")
        # self.visualization.grid(row = 1, column = 0, sticky=W)
        self.visualization.pack(side=LEFT)
        # self.grid()
        self.pack(expand=True, fill="both")

    def close_window(self):
        self.master.master.destroy()

    def update_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.today_info.set(current_date)
        self.after(1000, self.update_date)

    def display_error(self, error_type):
        # enable before displaying the next message
        self.console.config(state=NORMAL)
        self.console.insert("end", self.error_dictionary[error_type])
        self.console.config(state=DISABLED)

    def set_error_list(self, error_list):
        self.error_dictionary = error_list


class Simulation(Window):
    def increase_number():
        None
        
    Window.no_robots = ttk.Spinbox(from_=0, command=increase_number, 
                                   increment=1)
    Window.no_robots.pack()

    