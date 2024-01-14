from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk


class ImageEditor:
    def __init__(self):
        self.root = tk.Tk()

        # Create menu bar
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_command(label="Save", command=self.save_image)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Create buttons
        self.flood_fill_button = tk.Button(
            self.root, text="Flood Fill", command=self.start_flood_fill
        )
        self.flood_fill_button.pack()

        self.original_image = None
        self.current_image = None
        self.undo_stack = []

        self.root.mainloop()

    def mouse_click_handler(self, event):
        start_x, start_y = int(event.x), int(event.y)
        target_color = self.current_image.getpixel((start_x, start_y))
        replacement_color = (255, 0, 0)  # Replace with your desired replacement color
        self.flood_fill(start_x, start_y, target_color, replacement_color)
        self.canvas.unbind("<Button-1>")

    def start_flood_fill(self):
        if self.current_image:
            messagebox.showinfo(
                "Image Editor", "Click on the canvas to start flood fill."
            )
            self.canvas.bind("<Button-1>", self.mouse_click_handler)

    # Rest of the code...

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            self.current_image = self.original_image.copy()
            self.display_image()

    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg")],
            )
            if file_path:
                self.current_image.save(file_path)
                messagebox.showinfo("Image Editor", "Image saved successfully.")

    def display_image(self):
        if self.current_image:
            self.canvas.delete("all")
            image_width, image_height = self.current_image.size
            if image_width > 800 or image_height > 600:
                scale_factor = min(800 / image_width, 600 / image_height)
                new_width = int(image_width * scale_factor)
                new_height = int(image_height * scale_factor)
                self.current_image = self.current_image.resize(
                    (new_width, new_height), Image.ANTIALIAS
                )
            self.photo_image = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def flood_fill(self, x, y, target_color, replacement_color):
        if self.current_image:
            # Create a mask for visited pixels
            mask = np.zeros(
                (self.current_image.height, self.current_image.width), dtype=bool
            )

            def dfs(x, y):
                # Check if the coordinates are within the bounds of the image
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Check if the pixel at the current coordinates is of the target color
                    if (
                        mask[y, x]
                        and self.current_image.getpixel((x, y)) == target_color
                    ):
                        # Change the color of the pixel to the replacement color
                        self.current_image.putpixel((x, y), replacement_color)

                        # Recursively call dfs for neighboring pixels
                        dfs(x + 1, y)
                        dfs(x - 1, y)
                        dfs(x, y + 1)
                        dfs(x, y - 1)

            dfs(x, y)
            self.display_image()

    def cut_image(self, x1, y1, x2, y2):
        if self.current_image:
            self.undo_stack.append(self.current_image.copy())
            self.current_image = self.current_image.crop((x1, y1, x2, y2))
            self.display_image()

    def undo(self):
        if self.undo_stack:
            self.current_image = self.undo_stack.pop()
            self.display_image()


# Usage example
editor = ImageEditor()
