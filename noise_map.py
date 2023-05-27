import tkinter as tk
from tkinter import PhotoImage
import numpy as np
import threading
import random

class NoiseMapGenerator:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.canvas_width = 800
        self.canvas_height = 600

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(padx=10, pady=10)

        self.noise_map = None
        self.colors = []
        self.generating = False
        self.generator_thread = None

    def generate_noise_map(self, width, height):
        noise_map = np.zeros((height, width, 3), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                color = random.choice(self.colors)
                r, g, b = self.hex_to_rgb(color)
                noise_map[y, x] = [r, g, b]

        return noise_map

    def hex_to_rgb(self, color):
        color = color.strip("#")
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        return r, g, b

    def update_colors(self, colors):
        self.colors = colors
        self.render_map()

    def render_map(self):
        if not self.generating:
            self.clear_map()
            if len(self.colors) > 0:
                self.generating = True
                self.generator_thread = threading.Thread(target=self.render_map_thread)
                self.generator_thread.start()

    def render_map_thread(self):
        try:
            noise_map = self.generate_noise_map(self.canvas_width, self.canvas_height)
            self.display_noise_map(noise_map)
        except Exception as e:
            print(f"Failed to generate map: {e}")
        finally:
            self.generating = False

    def display_noise_map(self, noise_map):
        height, width, _ = noise_map.shape
        photo_image = PhotoImage(width=width, height=height)

        # Flatten the noise map and convert RGB values to hexadecimal strings
        flattened_map = noise_map.reshape(-1, 3)
        hex_colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in flattened_map]

        # Put the colors onto the PhotoImage
        photo_image.put(hex_colors, to=(0, 0, width - 1, height - 1))

        self.noise_map = photo_image
        self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.noise_map)
        self.canvas.image = self.noise_map

    def clear_map(self):
        self.canvas.delete("all")
