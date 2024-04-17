#!/usr/bin/env python

"""
waveInterference.py

Sandy Herho, 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Constants for Wave 1
lambda1 = 100.0
T1 = 60.0
amp = 1.0
xrange = 10 * lambda1
x = np.linspace(0, xrange, 500)

# Scenarios for Wave 2
scenarios = [
    {"lambda2": 100, "T2": 50, "label": "Scenario 1"},
    {"lambda2": 90, "T2": 60, "label": "Scenario 2"},
    {"lambda2": 90, "T2": 50, "label": "Scenario 3"},
    {"lambda2": 100, "T2": -60, "label": "Scenario 4"},
    {"lambda2": 50, "T2": -30, "label": "Scenario 5"},
    {"lambda2": 95, "T2": -30, "label": "Scenario 6"}
]

def create_animation(scenario):
    lambda2 = scenario["lambda2"]
    T2 = scenario["T2"]
    label = scenario["label"]
    
    plt.style.use('bmh')
    trange = 10 * T1
    dt = trange / 200
    ntot = int(trange / dt)
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    for ax in axes:
        ax.set_xlim(0, xrange)
        ax.set_ylim(-2, 2)
        ax.grid(True)
    
    axes[0].set_title(f"Wave 1: λ={lambda1}, T={T1}")
    axes[1].set_title(f"Wave 2: λ={lambda2}, T={T2}")
    axes[2].set_title("Superposition of Wave 1 and 2")

    # Custom colors for each line
    colors = ['blue', 'green', 'red']
    lines = [axes[i].plot([], [], lw=2, color=colors[i])[0] for i in range(3)]
    
    def update(frame):
        t = frame * dt
        f1 = amp * np.sin(2 * np.pi * (x / lambda1 - t / T1))
        f2 = amp * np.sin(2 * np.pi * (x / lambda2 - t / T2))
        f3 = f1 + f2

        lines[0].set_data(x, f1)
        lines[1].set_data(x, f2)
        lines[2].set_data(x, f3)
        return lines
    
    ani = FuncAnimation(fig, update, frames=ntot, blit=True, interval=50)
    gif_filename = f'waves_{label.replace(" ", "_").lower()}.gif'
    ani.save(gif_filename, writer=PillowWriter(fps=15))
    plt.close(fig)  # Close the figure to free memory

if __name__ == '__main__':
    # Run the animation creation for each scenario
    for scenario in scenarios:
        create_animation(scenario)

