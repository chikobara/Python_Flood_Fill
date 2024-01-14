import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk


class PainterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Painter App")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

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

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, width=2)
        self.draw.line([x1, y1, x2, y2], fill=self.color, width=2)

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
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(
                0, 0, anchor=tk.NW, image=ImageTk.PhotoImage(self.image)
            )

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Painter App", "Image saved successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PainterApp(root)
    root.mainloop()
