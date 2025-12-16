import math
import tkinter as tk
from random import choice

colors = ["red", "orange", "yellow", "green", "blue", "dark blue", "purple"]

class PieChart:
    def __init__(self, root):
        self.root = root
        self.root.title("Task 2")

        self.values = [10, 20, 30, 50, 60]
        #размещ холста
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        #добавление значения
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        #кнопка
        self.add_button = tk.Button(root, text="Add value", command=self.add_value)
        self.add_button.pack(pady=5)

        #отрисовка
        self.draw_chart()

    def add_value(self):
        #добавление значения
        try:
            val = float(self.entry.get())
            if val > 0:
                self.values.append(val)
                self.draw_chart()
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def draw_chart(self):
        #рисует
        self.canvas.delete("all")  #очистка

        total = sum(self.values)
        start_angle = 0

        cx, cy, r = 250, 250, 150  #центр и радиус

        #отрисовка секторов
        for value in self.values:
            extent = (value / total) * 360
            color = choice(colors)
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_angle, extent=extent, fill=color)
            start_angle += extent

if __name__ == "__main__":
    root = tk.Tk()
    app = PieChart(root)
    root.mainloop()