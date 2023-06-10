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
# class Window(ttk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
        

#         # close
#         self.btn = ttk.Button(self, text="Close", command=self.close_window)
#         self.btn.place()

#         # date
#         self.today_info = tk.StringVar()
#         self.update_date()
#         self.today_info_disp = ttk.Label(self, textvariable=self.today_info)
#         self.today_info_disp.place()

#         self.pack()

#     def close_window(self):
#         self.master.destroy()

#     def update_date(self):
#         current_date = datetime.now().strftime("%A, %B %d, %Y")
#         self.today_info.set(current_date)
#         self.after(1000, self.update_date)  # Update the date every second (1000 milliseconds)

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

        self.pack(expand=True, fill="both")

    def close_window(self):
        self.master.destroy()

    def update_date(self):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.today_info.set(current_date)
        self.after(1000, self.update_date)