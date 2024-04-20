#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Ellipse, Arc
from matplotlib.animation import FuncAnimation, PillowWriter

def read_data(filename):
    """ Reads data from the specified file, handling multiple spaces as delimiters. """
    return pd.read_csv(filename, delim_whitespace=True, header=None)

def setup_plot(radius, factor, fac2):
    """ Set up the initial plot settings. """
    fig, ax = plt.subplots()
    plt.style.use('bmh')
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_aspect('equal')
    ax.set_title("Rotating Frame of Reference", fontsize=14, fontstyle='italic')
    
    # Draw stationary arcs
    inner_ticks = Ellipse((0, 0), 2 * fac2, 2 * fac2, color='black', fill=False, linewidth=6)
    ax.add_patch(inner_ticks)

    return fig, ax

def update(frame, data, radius, fact, fre, ax):
    """ Update function for animation. """
    time = data.iloc[frame, 2]
    xr = data.iloc[frame, 0]
    yr = data.iloc[frame, 1]

    ax.clear()
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)

    # Draw rotating arcs to visualize relative rotation of the tank
    angles = np.linspace(0, 2 * np.pi, 5)
    for angle in angles:
        xx = radius * np.sin(fre * time + angle)
        yy = radius * np.cos(fre * time + angle)
        ax.plot([0, fact * xx], [0, fact * yy], 'k-', lw=6)

    # Draw trajectory
    ax.plot(data.iloc[1:frame+1, 0], data.iloc[1:frame+1, 1], 'r-', linewidth=4)

    # Draw location
    ax.add_patch(Ellipse((xr, yr), 2, 2, color='red', fill=True))
    ax.add_patch(Ellipse((xr, yr), 1.6, 1.6, color='yellow', fill=True))

def main():
    filename = './output1.txt'
    data = read_data(filename)

    fre = data.iloc[0, 0]
    dt = data.iloc[0, 1]
    ntot = int(data.iloc[0, 2])
    radius = 20
    fact = 0.9
    fac2 = fact * radius

    fig, ax = setup_plot(radius, fact, fac2)

    ani = FuncAnimation(fig, update, frames=ntot-1, fargs=(data, radius, fact, fre, ax), repeat=False)

    ani.save('CoriolisEffectSimulation.gif', writer='pillow', fps=10)

if __name__ == "__main__":
    main()

