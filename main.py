import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk


class PainterApp:
    def __init__(self, root):
        self.root = root
        self.current_image = None
        self.original_image = None
        self.undo_stack = []
        # self.canvas.delete("all")

        self.root.title("Painter App")
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        # self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.pack()

        # Create menu bar
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_canvas)
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_command(label="Save", command=self.save_image)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Color", command=self.choose_color)
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.root.config(menu=menubar)

        self.color = "black"
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        # self.canvas.bind("<B1-Motion>", self.paint)
        # self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.bucket_fill_button = tk.Button(
            root, text="Bucket Fill", command=self.start_bucket_fill
        )
        self.bucket_fill_button.pack()

        self.is_bucket_fill_active = False

    """ def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, width=2)
        self.draw.line([x1, y1, x2, y2], fill=self.color, width=2)
"""

    def reset(self, event):
        self.draw.line([event.x, event.y, event.x, event.y], fill=self.color, width=2)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    def new_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = Image.open(file_path)

            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(
                0, 0, anchor=tk.NW, image=ImageTk.PhotoImage(self.image)
            )
            self.current_image = self.original_image.copy()

            self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Painter App", "Image saved successfully.")

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

    def start_bucket_fill(self):
        self.is_bucket_fill_active = True
        if self.is_bucket_fill_active:
            messagebox.showinfo(
                "Painter App", "Click on the canvas to start bucket fill."
            )
            self.canvas.bind("<Button-1>", self.bucket_fill_handler)
        else:
            self.canvas.unbind("<Button-1>")

    def bucket_fill_handler(self, event):
        x, y = event.x, event.y
        target_color = self.image.getpixel((x, y))
        replacement_color = self.color
        self.bucket_fill(x, y, target_color, replacement_color)
        self.canvas.unbind("<Button-1>")

    def bucket_fill(self, x, y, target_color, replacement_color):
        if self.image:
            width, height = self.image.size
            visited = set()
            replacement_color_rgb = self.get_rgb_from_color(replacement_color)

            def is_valid(x, y):
                return 0 <= x < width and 0 <= y < height

            def dfs(x, y):
                if (
                    not (0 <= x < width)
                    or not (0 <= y < height)
                    or (x, y) in visited
                    or self.image.getpixel((x, y)) == (0, 0, 0)
                ):
                    return

                visited.add((x, y))

                if self.image.getpixel((x, y)) == target_color:
                    self.image.putpixel((x, y), replacement_color_rgb)
                    self.draw.point((x, y), fill=replacement_color_rgb)

                    # Recursively call dfs for neighboring pixels
                    dfs(x + 1, y)
                    dfs(x - 1, y)
                    dfs(x, y + 1)
                    dfs(x, y - 1)

            dfs(x, y)

            self.canvas.delete("all")
            self.canvas.create_image(
                0, 0, anchor=tk.NW, image=ImageTk.PhotoImage(self.image)
            )

    def get_rgb_from_color(self, color):
        if isinstance(color, tuple) and len(color) == 3:
            return color
        elif isinstance(color, str):
            rgb_color = colorchooser.askcolor()
            rgb_color = rgb_color[0]
            if rgb_color:
                return rgb_color
        return (0, 0, 0)  # Default to black if conversion fails


if __name__ == "__main__":
    root = tk.Tk()
    app = PainterApp(root)
    root.mainloop()
