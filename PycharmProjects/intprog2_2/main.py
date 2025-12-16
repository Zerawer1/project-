import tkinter as tk

class CircleAnimation:
    def __init__(self, root):
        self.root=root

        self.width=500
        self.height=500
        self.root.geometry(f"{self.width}x{self.height}")

        self.radius=100
        self.direction=1
        self.step=1

        self.cx=self.width//2
        self.cy=self.height//2

        self.canvas=tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.animation()

    def animation(self):
        self.canvas.delete("all")

        max_r=self.width/2
        min_r=10

        if self.radius>=max_r:
            self.direction=-1
        elif self.radius<=min_r:
            self.direction=1

        self.radius+=self.step*self.direction

        x1=self.cx-self.radius
        y1=self.cy-self.radius
        x2=self.cx+self.radius
        y2=self.cy+self.radius

        self.canvas.create_oval(x1, y1, x2, y2, fill="pink")
        self.canvas.create_text(self.cx, self.cy+self.radius+20, text=f"r={int(self.radius)}")

        self.root.after(50, self.animation)


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleAnimation(root)
    root.mainloop()
