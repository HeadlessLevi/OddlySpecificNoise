import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import random
from noise_map import NoiseMapGenerator
from ui import UI

# Create the GUI window
window = tk.Tk()
print("test")
window.title("Noise Map Generator")

# Create the NoiseMapGenerator instance
noise_map_generator = NoiseMapGenerator()

# Create the UI
ui = UI(window)
