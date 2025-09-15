import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- Physics Engine ---
def projectile_calculations(h_initial, u, ang_deg, g):
    ang_rad = math.radians(ang_deg)
    vx = u * math.cos(ang_rad)
    vy = u * math.sin(ang_rad)

    # 🔥 FIX: If angle is vertical, force vx = 0
    if abs(vx) < 1e-10:
        vx = 0.0

    a, b, c = -0.5 * g, vy, h_initial
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return [], [], 0, 0, 0

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    time_s = max(t1, t2)

    range_m = vx * time_s
    max_height = h_initial + (vy**2) / (2 * g)

    n_points = 200
    x_vals, y_vals = [], []
    for i in range(n_points + 1):
        t = i * time_s / n_points
        x = vx * t
        y = h_initial + vy * t - 0.5 * g * t**2
        if y < 0: 
            y = 0
        x_vals.append(x)
        y_vals.append(y)

    return x_vals, y_vals, time_s, range_m, max_height


# --- GUI App ---
class SpaceProjectileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Space Trajectory Simulator")
        self.root.configure(bg="#0d0d1a")  # Dark space background

        # Custom style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#0d0d1a", foreground="white", font=("Consolas", 10))
        style.configure("TEntry", fieldbackground="#1f1f2e", foreground="white")

        # FIX: Button style with hover
        style.configure("TButton",
                        background="#1f1f2e",
                        foreground="cyan",
                        font=("Consolas", 10, "bold"))
        style.map("TButton",
                  background=[("active", "#2e2e3e")],   # darker on hover
                  foreground=[("active", "cyan")])      # keep cyan text

        # Control Panel
        control = ttk.Frame(root, padding=10, style="TFrame")
        control.pack(side="left", fill="y")

        self.vel_var = tk.StringVar(value="20")
        self.ang_var = tk.StringVar(value="45")
        self.g_var = tk.StringVar(value="9.8")
        self.h_var = tk.StringVar(value="0")
        self.planet_var = tk.StringVar(value="Earth 🌍")

        self.add_input(control, "Velocity (m/s):", self.vel_var, 0)
        self.add_input(control, "Angle (°):", self.ang_var, 1)
        self.add_input(control, "Gravity (m/s²):", self.g_var, 2)
        self.add_input(control, "Height (m):", self.h_var, 3)

        ttk.Label(control, text="Planet 🌍:").grid(row=4, column=0, sticky="w")
        planets = ttk.Combobox(control, textvariable=self.planet_var,
                               values=["Earth 🌍", "Moon 🌕", "Mars ♂️"],
                               state="readonly", width=12)
        planets.grid(row=4, column=1, pady=3)

        ttk.Button(control, text="🚀 Launch", command=self.simulate).grid(row=5, column=0, pady=10, sticky="ew")
        ttk.Button(control, text="🗑 Clear", command=self.clear_plot).grid(row=5, column=1, pady=10, sticky="ew")

        # Results Panel
        self.results = tk.Label(control, text="Results will appear here...", justify="left",
                                fg="cyan", bg="#0d0d1a", font=("Consolas", 10))
        self.results.grid(row=6, column=0, columnspan=2, pady=10)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.fig.patch.set_facecolor("#0d0d1a")
        self.ax.set_facecolor("#0d0d1a")
        self.ax.tick_params(colors="white")
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")
        self.ax.title.set_color("cyan")

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def add_input(self, parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=10).grid(row=row, column=1, pady=3)

    def get_gravity(self):
        planet = self.planet_var.get()
        if "Moon" in planet: return 1.62
        if "Mars" in planet: return 3.71
        return float(self.g_var.get())

    def simulate(self):
        try:
            u = float(self.vel_var.get())
            ang = float(self.ang_var.get())
            h0 = float(self.h_var.get())
            g = self.get_gravity()
        except ValueError:
            return

        x_vals, y_vals, time_s, range_m, max_height = projectile_calculations(h0, u, ang, g)

        self.ax.clear()
        self.ax.set_facecolor("#0d0d1a")
        self.ax.plot(x_vals, y_vals, label="Trajectory", color="cyan")

        if y_vals:
            max_index = y_vals.index(max(y_vals))
            self.ax.scatter(x_vals[max_index], y_vals[max_index], color="magenta", label="Max Height")
            self.ax.scatter(x_vals[-1], y_vals[-1], color="lime", label="Landing Point")

        # FIX: Axis labels now white
        self.ax.set_title("Trajectory in Space", fontsize=12, color="cyan")
        self.ax.set_xlabel("Horizontal Distance (m)", color="white")
        self.ax.set_ylabel("Vertical Height (m)", color="white")

        self.ax.grid(color="#444444")
        self.ax.legend(facecolor="#1a1a2e", edgecolor="cyan", labelcolor="white")
        self.canvas.draw()

        self.results.config(
            text=f"🕒 Time of Flight: {time_s:.2f} s\n"
                 f"🔼 Max Height: {max_height:.2f} m\n"
                 f"➡ Range: {range_m:.2f} m"
        )

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_facecolor("#0d0d1a")
        self.canvas.draw()
        self.results.config(text="Results will appear here...")


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceProjectileApp(root)

    # 🔥 Ensure the process fully exits when window is closed
    def on_close():
        root.destroy()
        root.quit()   # stop Tkinter loop
        exit(0)       # force Python process to end

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
