#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation, PillowWriter

def update(frame, fac2, factor, fre, dt, lines, small_circle):
    time = frame * dt

    # Calculate new positions using the simplified dynamics
    xp = fac2 * np.cos(fre * time)
    yp = fac2 * np.sin(fre * time)

    # Update trajectory
    x_vals, y_vals = lines.get_data()
    x_vals = np.append(x_vals, xp)
    y_vals = np.append(y_vals, yp)
    lines.set_data(x_vals, y_vals)

    # Update small circle for ball position
    small_circle.center = (xp, yp)

    return lines, small_circle

def main():
    # Constants
    T = 24 * 3600  # Period in seconds
    fre = 2 * np.pi / T  # Rotation rate
    radius = 20
    dt = T / 200  # Time step
    factor = 0.9
    fac2 = factor * radius

    # Set the style
    plt.style.use('bmh')

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)

    # Drawing initial circle and lines
    circle = Circle((0, 0), fac2, edgecolor='black', facecolor='none')
    ax.add_patch(circle)
    lines, = ax.plot([], [], 'r-')

    # Initialize small circle for ball position
    small_circle = Circle((0, 0), 1, color='red')
    ax.add_patch(small_circle)

    # Creating the animation
    ani = FuncAnimation(fig, update, frames=np.arange(0, 200), fargs=(fac2, factor, fre, dt, lines, small_circle),
                        blit=True, interval=50)

    # Save to GIF using Pillow
    writer = PillowWriter(fps=20)
    ani.save('CentripetalForce.gif', writer=writer)

if __name__ == "__main__":
    main()

