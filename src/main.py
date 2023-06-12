'''
frontend
'''
import tkinter as tk
from tkinter import ttk
from windows.simulation_tab import Window

# Main window definition
main_window = tk.Tk()
main_window.title("Robotat GUI")
main_window.geometry("800x500")
main_window.resizable(0, 0)

# Tabs definition
notebook = ttk.Notebook(main_window)

sim_tab = Window(notebook)
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


notebook.pack(expand=True, fill="both")

main_window.mainloop()


  
# lbl = Label(app,text = "A list of favourite countries...")  
# lbl.pack() 
# listbox = Listbox(app)  
# listbox.pack()  


# listbox.insert(1,"text 1")  
  
# listbox.insert(2, "text 2")  
  
# listbox.insert(3, "text 3")  
  
# listbox.insert(4, "text 4")  
  
 

  
# app.mainloop()  

