#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation, PillowWriter

def main():
    # Constants and parameters
    T = 24 * 3600  # period in seconds
    fre = 2 * np.pi / T  # rotation rate
    radius = 20
    dt = T / 200  # time step
    factor = 0.9
    fac2 = factor * radius

    # Initial position and velocity
    xp, yp = 0, 5
    up, vp = 0.5, 0.5

    # Plot setup
    plt.style.use('bmh')
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_title("Fixed Frame of Reference")

    # Initial ellipse
    ellipse = Ellipse((0, 0), 2 * fac2, 2 * fac2, angle=0, edgecolor='blue', facecolor='none', lw=2)
    ax.add_patch(ellipse)

    # Trajectory data storage
    x_positions, y_positions = [], []

    # Update function for animation
    def update(frame):
        nonlocal xp, yp, up, vp, ellipse
        # Time calculation
        time = frame * dt

        # Calculate new positions based on Coriolis effect
        alpha = np.cos(dt * 2 * fre)
        beta = np.sin(dt * 2 * fre)

        upn = alpha * (up - dt * 2 * fre * vp) - beta * dt * 2 * fre * up
        vpn = alpha * (vp + dt * 2 * fre * up) + beta * dt * 2 * fre * vp

        xp += dt * upn / 1000
        yp += dt * vpn / 1000

        xpn = xp * np.cos(fre * time) + yp * np.sin(fre * time)
        ypn = yp * np.cos(fre * time) - xp * np.sin(fre * time)

        x_positions.append(xpn)
        y_positions.append(ypn)

        up, vp = upn, vpn

        ax.clear()
        ax.set_xlim(-radius, radius)
        ax.set_ylim(-radius, radius)
        ax.plot(x_positions, y_positions, 'r-')

        # Update and redraw the rotating ellipse
        angle = np.degrees(fre * time) % 360
        ellipse = Ellipse((0, 0), 2 * fac2, 2 * fac2, angle=angle, edgecolor='blue', facecolor='none', lw=2)
        ax.add_patch(ellipse)

        return ellipse,

    # Create animation
    ani = FuncAnimation(fig, update, frames=200, blit=True, interval=50)

    # Save animation as GIF
    writer = PillowWriter(fps=20)
    ani.save('Traject.gif', writer=writer)

if __name__ == "__main__":
    main()

