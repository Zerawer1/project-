import tkinter as tk

class CircleApp:
    def __init__(self, root):
        self.root = root

        self.width=500
        self.height=500
        self.root.geometry(f"{self.width}x{self.height}")

        self.radius=100

        self.cx=self.width//2
        self.cy=self.height//2

        self.canvas=tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.draw_circle()

        self.root.bind("<Left>", self.decrease_radius)
        self.root.bind("<Right>", self.increase_radius)

    def draw_circle(self):
        self.canvas.delete("all")

        x1=self.cx-self.radius
        y1=self.cy-self.radius
        x2=self.cx+self.radius
        y2=self.cy+self.radius

        self.canvas.create_oval(x1, y1, x2, y2, fill="pink")
        self.canvas.create_text(self.cx, self.cy + self.radius+20, text=f"r = {self.radius}")

    def increase_radius(self, event):
        max_r=self.width/2
        if self.radius<max_r:
            self.radius+= 1
            self.draw_circle()

    def decrease_radius(self, event):
        if self.radius>1:
            self.radius-=1
            self.draw_circle()


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleApp(root)
    root.mainloop()
