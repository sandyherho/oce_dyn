#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def main():
    # Constants
    T = 24 * 3600  # period in seconds
    fre = -2 * np.pi / T  # negative rotation rate
    radius = 20
    dt = T / 200  # time step
    factor = 0.9
    fac2 = factor * radius

    # Initial position and velocity
    xp, yp = 0, 5
    xf, yf = xp, yp
    uf, vf = 0.0, 0.15  # speed in m/s

    # Create plot
    plt.style.use('bmh')
    fig, ax = plt.subplots()
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_aspect('equal')
    ax.set_title("Rotating Frame of Reference")

    # Data storage for trajectory
    x_positions, y_positions = [], []

    # Update function for animation
    def update(frame):
        nonlocal xf, yf, xp, yp

        # Time update
        time = frame * dt

        # Update fixed frame position
        xf += dt * uf / 1000
        yf += dt * vf / 1000

        # Transform to rotating frame
        xp = xf * np.cos(fre * time) + yf * np.sin(fre * time)
        yp = yf * np.cos(fre * time) - xf * np.sin(fre * time)

        x_positions.append(xp)
        y_positions.append(yp)

        ax.clear()
        ax.set_xlim(-radius, radius)
        ax.set_ylim(-radius, radius)

        # Draw lines and arcs
        angles = np.linspace(0, 2 * np.pi, 5)
        for angle in angles:
            xx = radius * np.sin(-fre * time + angle)
            yy = radius * np.cos(-fre * time + angle)
            ax.plot([0, factor * xx], [0, factor * yy], 'k-', lw=6)

        # Plot trajectory
        ax.plot(x_positions, y_positions, 'r-', lw=2)

    # Create animation
    ani = FuncAnimation(fig, update, frames=200, repeat=False)

    # Save to GIF
    ani.save('StraightPath.gif', writer='pillow', fps=20)

if __name__ == "__main__":
    main()

