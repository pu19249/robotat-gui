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

        # close
        self.btn = ttk.Button(self, text="Close", command=self.close_window)
        self.btn.pack(side=tk.TOP)

        # date
        self.today_info = tk.StringVar()
        self.update_date()
        self.today_info_disp = ttk.Label(self, textvariable=self.today_info)
        self.today_info_disp.pack(side=tk.TOP)

        # console
        self.console = tk.Text(self, height=4)
        self.console.pack(fill="x")
        # initial message
        self.console.insert("end", "Robotat GUI console")
        # disable input option
        self.console.config(state=DISABLED) 

        # dictionary will change (with method set_error_list) depending on the tab
        self.error_dictionary = {
            "error1":"Error 1"
        }

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
