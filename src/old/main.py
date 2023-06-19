'''
frontend
'''
import tkinter as tk
from tkinter import ttk
from windows.simulation_tab import Window, Simulation

# Main window definition
main_window = tk.Tk()
main_window.title("Robotat GUI")
main_window.geometry("800x600") # (x y)

# main_window.resizable(0, 0)

# Tabs definition
notebook = ttk.Notebook(main_window)

sim_tab = Simulation(notebook)
dictionary_sim = {
    "er1" : "Test",
    "er2" : "Test2"
}
sim_tab.set_error_list(dictionary_sim)
sim_tab.display_error("er1")
notebook.add(sim_tab, text="Simulator")

ota_tab = Window(notebook)
notebook.add(ota_tab, text="OTA")

rtd_tab = Window(notebook)
notebook.add(rtd_tab, text="RTD")

notebook.grid()
notebook.pack(expand=True, fill="both")

main_window.mainloop()