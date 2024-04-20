#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation, PillowWriter

def main():
    # Constants and initial conditions
    T = 24 * 3600  # Period in seconds
    fre = 2 * np.pi / T  # Rotation rate
    radius = 20
    dt = T / 200  # Time step
    factor = 0.9
    fac2 = factor * radius

    # Initial position and velocity
    xp, yp = 0, 5
    up, vp = 0.5, 0.5

    # Setup the plot
    plt.style.use('bmh')
    fig, ax = plt.subplots()
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_aspect('equal')
    ax.set_title("Rotating Frame of Reference")

    # Data storage for trajectory
    x_positions, y_positions = [], []

    # Update function for the animation
    def update(frame):
        nonlocal xp, yp, up, vp

        # Update time
        time = frame * dt

        # Calculate new ball position
        alpha = np.cos(dt * 2 * fre)
        beta = np.sin(dt * 2 * fre)

        upn = alpha * (up - dt * 2 * fre * vp) - beta * dt * 2 * fre * up
        vpn = alpha * (vp + dt * 2 * fre * up) + beta * dt * 2 * fre * vp

        xp += dt * upn / 1000
        yp += dt * vpn / 1000

        x_positions.append(xp)
        y_positions.append(yp)

        up, vp = upn, vpn

        ax.clear()
        ax.set_xlim(-radius, radius)
        ax.set_ylim(-radius, radius)
        ax.plot(x_positions, y_positions, 'r-', linewidth=4)  # Plot the trajectory

        # Draw all rotating lines and ellipses
        angles = np.linspace(0, 2 * np.pi, 5)
        for angle in angles:
            xx = radius * np.sin(-fre * time + angle)
            yy = radius * np.cos(-fre * time + angle)
            ax.plot([0, factor * xx], [0, factor * yy], 'k-', lw=6)

        # Plotting the ellipse representing boundaries
        ellipse = Ellipse((0, 0), 2 * fac2, 2 * fac2, angle=0, color='blue', fill=False, linewidth=6)
        ax.add_patch(ellipse)

    # Create animation
    ani = FuncAnimation(fig, update, frames=200, repeat=False)

    # Save to GIF
    ani.save('CoriolisForceRevealed.gif', writer=PillowWriter(fps=20))

if __name__ == "__main__":
    main()

