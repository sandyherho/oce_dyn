#!/usr/bin/env python

"""
waveInterference.py

Sandy Herho, 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Activate the 'bmh' style
plt.style.use('bmh')

# Define constants
len1 = 100.0  # wavelength of wave 1
per1 = 60.0  # period of wave 1
len2 = 95.0  # wavelength of wave 2
per2 = -30.0  # period of wave 2
amp = 1.0  # amplitude of both waves
xrange = 10 * len1
x = np.linspace(0, xrange, 500)  # x-axis

# Time settings
t = 0
trange = 10 * per1
dt = trange / 200
ntot = int(trange / dt)

# Ensure proper backend for animation is used
plt.rc('animation', html='html5')

# Figure and Subplots
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# Set up the subplots
for ax in axes:
    ax.set_xlim(0, 1000)
    ax.set_ylim(-2, 2)
    ax.set_xticks([0, 200, 400, 600, 800, 1000])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.grid(True)

# Titles for each subplot
axes[0].set_title("Wave 1")
axes[1].set_title("Wave 2")
axes[2].set_title("Wave 1+2")

# Define colors for each wave
colors = ['blue', 'green', 'red']

# Plot lines with specified colors
lines = [axes[i].plot([], [], lw=2, color=colors[i])[0] for i in range(3)]

# Animation update function
def update(frame):
    t = frame * dt
    f1 = amp * np.sin(2 * np.pi * (x / len1 - t / per1))
    f2 = amp * np.sin(2 * np.pi * (x / len2 - t / per2))
    f3 = f1 + f2

    lines[0].set_data(x, f1)
    lines[1].set_data(x, f2)
    lines[2].set_data(x, f3)
    return lines

# Creating the animation
ani = FuncAnimation(fig, update, frames=ntot, blit=True, interval=50)

# Save the animation as a GIF using PillowWriter
ani.save('waves.gif', writer=PillowWriter(fps=15))

plt.show()

