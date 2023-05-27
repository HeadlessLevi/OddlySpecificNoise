from tkinter import filedialog
import tkinter as tk


class ImageExporter:
    def __init__(self, master, noise_map_generator, *args, **kwargs):
        self.master = master
        self.noise_map_generator = noise_map_generator

        self.export_button = tk.Button(self.master, text="Export Image", command=self.export_image)
        self.export_button.pack(pady=5)

    def export_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path and self.noise_map_generator.noise_map:
            self.noise_map_generator.noise_map.write(file_path, format="png")
