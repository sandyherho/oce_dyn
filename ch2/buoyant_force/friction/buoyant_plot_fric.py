#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib

# Ensure that the appropriate writer is available
matplotlib.use("Agg")
plt.style.use('bmh')

def animate():
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)

    data = np.loadtxt("./output_fortran.txt")  # Load data

    ax.set_xlim(0, 60)  # Set time range in minutes
    ax.set_ylim(-100, 0)
    ax.set_xticks(np.linspace(0, 60, 13))
    ax.set_yticks(np.linspace(-100, 0, 11))
    ax.axhline(y=-50, color='k', linewidth=2)
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Depth (meters)")

    title_text = ax.text(15, -10, '', fontsize=14, color='red', horizontalalignment='center')
    time_text = ax.text(0.5, -90, '', fontsize=12, color='black')

    def init():
        title_text.set_text('')
        time_text.set_text('')
        return title_text, time_text

    def update(frame):
        if frame == 0:
            return []

        # Previous frame data
        prev_time = data[frame - 1, 0] / 60
        prev_depth = data[frame - 1, 1]
        # Current frame data
        time = data[frame, 0] / 60
        depth = data[frame, 1]
        color = 'blue' if prev_depth > -50 else 'red'
        
        ax.plot([prev_time, time], [prev_depth, depth], color=color, linewidth=2)
        
        title_text.set_text("Too light" if depth > -50 else "Too heavy")
        title_text.set_color('blue' if depth > -50 else 'red')
        time_text.set_text(f"Time: {time:.2f} minutes")

        return title_text, time_text

    ani = FuncAnimation(fig, update, frames=len(data), init_func=init, blit=False, repeat=False)

    # Save the animation
    ani.save('./oscillation_animation.gif', writer='imagemagick', fps=10)

if __name__ == '__main__':
    animate()

