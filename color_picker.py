import tkinter as tk
from tkinter import colorchooser
import random


class ColorPickerFrame(tk.Frame):
    def __init__(self, master, noise_map_generator, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.colors = []
        self.color_frames = []
        self.noise_map_generator = noise_map_generator


    def add_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.colors.append(color)
            self.update_color_pickers()
            self.noise_map_generator.update_colors(self.colors)

    def add_random_color(self):
        random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.colors.append(random_color)
        self.update_color_pickers()
        self.noise_map_generator.update_colors(self.colors)
