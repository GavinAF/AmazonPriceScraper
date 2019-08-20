import tkinter as tk
import pygubu # tkinter ui builder

# Set main window
main = tk.Tk()
main.title("[APS] Amazon Price Scraper")

# Quit Button
button = tk.Button(main, text='Quit', width=15, command=main.destroy) 
button.pack() 


# Initialize & load main window
main.mainloop()