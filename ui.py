import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import PhotoImage
from tkinter import filedialog
import random

class UI:
    def __init__(self, master):
        self.master = master
        self.canvas_width = tk.IntVar(value=800)
        self.canvas_height = tk.IntVar(value=600)
        self.aspect_ratio = tk.StringVar(value="1:1")

        self.colors = []
        self.color_frames = []
        self.noise_map = None

        self.master.configure(bg="#222222")  # Set the background color

        self.create_canvas()
        self.create_color_picker_frame()
        self.create_resolution_frame()
        self.create_buttons()

        # Configure grid weights for responsive scaling
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_columnconfigure(0, weight=1)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.master, bg="#111111", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def create_color_picker_frame(self):
        self.color_frame_container = tk.Frame(self.master, bg="#222222", bd=1, relief=tk.RAISED)
        self.color_frame_container.grid(row=1, column=0, pady=20, padx=20, sticky="ew")

    def create_resolution_frame(self):
        resolution_frame = tk.Frame(self.master, bg="#222222")
        resolution_frame.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        width_label = ttk.Label(resolution_frame, text="Width:", style="TButton")
        width_label.grid(row=0, column=0, padx=(0, 5))

        width_entry = ttk.Entry(resolution_frame, textvariable=self.canvas_width, width=10)
        width_entry.grid(row=0, column=1, padx=(0, 10))

        height_label = ttk.Label(resolution_frame, text="Height:", style="TButton")
        height_label.grid(row=0, column=2, padx=(0, 5))

        height_entry = ttk.Entry(resolution_frame, textvariable=self.canvas_height, width=10)
        height_entry.grid(row=0, column=3, padx=(0, 10))

        aspect_ratio_label = ttk.Label(resolution_frame, text="Aspect Ratio:", style="TButton")
        aspect_ratio_label.grid(row=0, column=4, padx=(0, 5))

        aspect_ratio_combobox = ttk.Combobox(
            resolution_frame,
            textvariable=self.aspect_ratio,
            values=["1:1", "3:2", "4:3", "16:9"],
            state="readonly",
            width=5,
            style="TButton"
        )
        aspect_ratio_combobox.grid(row=0, column=5, padx=(0, 10))

    def create_buttons(self):
        button_frame = tk.Frame(self.master, bg="#222222")
        button_frame.grid(row=3, column=0, pady=20, padx=20, sticky="ew")

        style = ttk.Style()
        style.configure("TButton", relief=tk.RAISED, foreground="#222222", font=("Arial", 10, "bold"),
                        background="#555555", borderwidth=0)  # Adjust the styles as desired

        add_button = ttk.Button(button_frame, text="Add Color", command=self.add_color, style="TButton")
        add_button.grid(row=0, column=0, padx=10)

        random_color_button = ttk.Button(button_frame, text="Random Color", command=self.add_random_color, style="TButton")
        random_color_button.grid(row=0, column=1, padx=10)

        generate_button = ttk.Button(button_frame, text="Generate Map", command=self.generate_map, style="TButton")
        generate_button.grid(row=0, column=2, padx=10)

        export_button = ttk.Button(button_frame, text="Export Image", command=self.export_image, style="TButton")
        export_button.grid(row=0, column=3, padx=10)

        # Configure column weights for responsive scaling
        button_frame.grid_columnconfigure(4, weight=1)

    def generate_noise_map(self, width, height, colors):
        noise_map = PhotoImage(width=width, height=height)

        for x in range(width):
            for y in range(height):
                color = random.choice(colors)
                noise_map.put(color, (x, y))

        return noise_map

    def add_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.colors.append(color)
            self.update_color_pickers()

    def add_random_color(self):
        random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.colors.append(random_color)
        self.update_color_pickers()

    def update_color_pickers(self):
        for color_frame in self.color_frames:
            color_frame.destroy()
        self.color_frames.clear()

        for i, color in enumerate(self.colors):
            color_frame = tk.Frame(self.color_frame_container, bg=color, bd=1, relief=tk.RAISED)
            color_frame.grid(row=0, column=i, padx=5, pady=5)

            color_label = tk.Label(color_frame, text="Color {}".format(i + 1), bg=color, fg="#222222")
            color_label.pack()

            self.color_frames.append(color_frame)

    def generate_map(self):
        width = self.canvas_width.get()
        height = self.canvas_height.get()
        aspect_ratio = self.aspect_ratio.get()
        aspect_width, aspect_height = map(int, aspect_ratio.split(":"))

        if width > 0 and height > 0 and aspect_width > 0 and aspect_height > 0:
            adjusted_width = width
            adjusted_height = height

            if width * aspect_height < height * aspect_width:
                adjusted_width = height * aspect_width // aspect_height
            else:
                adjusted_height = width * aspect_height // aspect_width

            self.canvas_width.set(adjusted_width)
            self.canvas_height.set(adjusted_height)

            self.noise_map = self.generate_noise_map(adjusted_width, adjusted_height, self.colors)
            self.canvas.config(width=adjusted_width, height=adjusted_height)
            self.canvas.create_image(adjusted_width // 2, adjusted_height // 2, image=self.noise_map)
            self.canvas.image = self.noise_map

    def export_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path and self.noise_map:
            self.noise_map.write(file_path, format="png")

# Create the GUI window
window = tk.Tk()
window.title("Noise Map Generator")

# Create the UI
ui = UI(window)

# Start the GUI event loop
window.mainloop()
