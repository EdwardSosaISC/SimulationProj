import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

def getParabolic(v0, angle, y0=0, dt=0.01):
    g = 9.81
    angle_rad = np.radians(angle)
    v0x = v0 * np.cos(angle_rad)
    v0y = v0 * np.sin(angle_rad)

    a = -0.5 * g
    b = v0y
    c = y0
    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        return None, None, None

    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)
    flight_time = max(t1, t2)

    t = np.arange(0, flight_time + dt, dt)
    x = v0x * t
    y = y0 + v0y * t - 0.5 * g * t**2

    return x, y, flight_time

def animate(i):
    if i < len(x_data):
        point.set_data([x_data[i]], [y_data[i]])
        line.set_data(x_data[:i+1], y_data[:i+1])
        
        if i < 5:
            cannon.set_data([cannon_x + i * 0.2], [cannon_y])
    return point, line, cannon

def simulate():
    global x_data, y_data, point, line, cannon, cannon_x, cannon_y
    v0 = v0_scale.get()
    angle = angle_scale.get()
    y0 = y0_scale.get()

    x_data, y_data, flight_time = getParabolic(v0, angle, y0)

    if x_data is not None:
        for widget in sim_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlabel("Distancia (m)")
        ax.set_ylabel("Altura (m)")
        ax.set_title("Movimiento parabólico")
        ax.grid()
        ax.set_xlim(0, max(x_data) * 1.1)
        ax.set_ylim(0, max(y_data) * 1.1)

        cannon_x = 0
        cannon_y = y0
        cannon, = ax.plot([cannon_x], [cannon_y], 'ks', markersize=10)
        point, = ax.plot([], [], 'ro', markersize=8)
        line, = ax.plot([], [], 'b-', lw=2)

        canvas = FigureCanvasTkAgg(fig, master=sim_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        anim = FuncAnimation(fig, animate, frames=len(x_data), interval=30, blit=True)
        canvas.draw()

root = tk.Tk()
root.title("Simulación de Movimiento Parabólico")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

control_frame = ttk.Frame(root, padding=10)
control_frame.pack(side=tk.TOP, fill=tk.X)

ttk.Label(control_frame, text="Velocidad inicial (m/s):").pack(side=tk.LEFT)
v0_scale = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL)
v0_scale.pack(side=tk.LEFT)
v0_scale.set(20)

ttk.Label(control_frame, text="Ángulo de lanzamiento (°):").pack(side=tk.LEFT)
angle_scale = tk.Scale(control_frame, from_=0, to=90, orient=tk.HORIZONTAL)
angle_scale.pack(side=tk.LEFT)
angle_scale.set(45)

ttk.Label(control_frame, text="Altura inicial (m):").pack(side=tk.LEFT)
y0_scale = tk.Scale(control_frame, from_=0, to=50, orient=tk.HORIZONTAL)
y0_scale.pack(side=tk.LEFT)
y0_scale.set(0)

ttk.Button(control_frame, text="Simular", command=simulate).pack(side=tk.LEFT)

sim_frame = ttk.Frame(root, padding=10)
sim_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root.mainloop()
