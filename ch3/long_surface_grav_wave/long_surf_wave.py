#!/usr/bin/env python

"""
long_surf_wave.py

1D Shalow-Water Simulation: Long Surface Gravity Wave

Sandy Herho <sh001@ucr.edu>
04/21/2024
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

class WaveAnimation:
    def __init__(self):
        """
        Initialize the wave animation with physical constants and settings.
        """
        self.len_wave = 500.0  # Wavelength of the wave in meters.
        self.eta0 = 1.0        # Amplitude of the wave in meters.
        self.g = 9.81          # Acceleration due to gravity in m/s^2.
        self.h = 20.0          # Water depth in meters.
        self.c = np.sqrt(self.g * self.h)  # Phase speed calculated with wave equation in m/s.
        self.per = self.len_wave / self.c  # Period of the wave in seconds.
        self.u0 = self.eta0 * np.sqrt(self.g / self.h)  # Horizontal velocity amplitude in m/s.

        self.xrange = 2 * self.len_wave  # Horizontal range to cover in the plot in meters.
        self.x = np.linspace(0, self.xrange, 100)  # X-coordinates for plotting.
        self.t = 0.0  # Start time of the simulation.
        self.trange = 2 * self.per  # Total time range to simulate in seconds.
        self.dt = self.trange / 100.  # Time step in seconds.
        self.ntot = int(self.trange / self.dt)  # Total number of time steps.

        # Initial z-positions for different fluid parcels
        self.zpos1 = np.ones_like(self.x)
        self.zpos2 = 6.0 * np.ones_like(self.x)
        self.zpos3 = 11.0 * np.ones_like(self.x)
        self.zpos4 = 16.0 * np.ones_like(self.x)

        # Set up matplotlib plot aesthetics
        plt.style.use('bmh')
        self.fig, self.ax = plt.subplots()
        self.setup_plot()

        # Initialize the animation
        self.ani = FuncAnimation(self.fig, self.animate, frames=self.ntot, init_func=self.init, blit=True, interval=50)

    def setup_plot(self):
        """
        Configure plot axes, labels, and horizontal sea level line.
        Also sets the legend and initial plot configuration.
        """
        self.ax.set_xlim(0, self.xrange)
        self.ax.set_ylim(-20, 2)
        self.ax.set_xlabel('Distance [meters]', fontsize=14)
        self.ax.set_ylabel('Depth [meters]', fontsize=14)
        self.ax.axhline(0, color='black', linewidth=1)  # Horizontal line representing sea level.

        # Define labels and colors for the plot lines, reversing the order
        labels = ['Surface Wave', 'Fluid Parcel at 16m Depth', 'Fluid Parcel at 11m Depth', 'Fluid Parcel at 6m Depth', 'Fluid Parcel at 1m Depth']
        colors = ['#2eaaf2', '#03263b', '#074d75', '#08679e', '#0a88d1']
        self.lines = [self.ax.plot([], [], lw=2, label=label, color=color)[0] for label, color in reversed(list(zip(labels, colors)))]
        
        self.ax.legend()  # Add a legend to the plot

        # Time annotation in the plot
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, color='black')

    def init(self):
        """
        Initialize the plot lines to empty for the animation's start.
        """
        for line in self.lines:
            line.set_data([], [])
        self.time_text.set_text('')
        return self.lines + [self.time_text]

    def animate(self, i):
        """
        Update plot lines for each frame of the animation based on wave properties.
        """
        eta = self.eta0 * np.sin(2 * np.pi * (self.x / self.len_wave - self.t / self.per))  # Wave surface displacement
        u = self.u0 * np.sin(2 * np.pi * (self.x / self.len_wave - self.t / self.per))  # Horizontal velocity
        dwdz = -2 * np.pi * self.u0 / self.len_wave * np.cos(2 * np.pi * (self.x / self.len_wave - self.t / self.per))  # Vertical velocity gradient

        for j, zpos in enumerate([self.zpos4, self.zpos3, self.zpos2, self.zpos1]):
            xpos = self.x + self.dt * u  # Calculate new positions based on horizontal velocity
            w = dwdz * zpos
            zpos += self.dt * w  # Update z positions based on vertical velocity
            self.lines[j].set_data(xpos, -self.h + zpos)  # Set new data for each line
        self.lines[-1].set_data(self.x, eta)  # Update surface wave position
        self.time_text.set_text(f'Time: {self.t:.2f} s')  # Update time annotation
        self.t += self.dt
        return self.lines + [self.time_text]

    def save_gif(self):
        """
        Save the animation as a GIF file.
        """
        self.ani.save('long_surf_grav_wav.gif', writer=PillowWriter(fps=20))

if __name__ == "__main__":
    wave_anim = WaveAnimation()
    wave_anim.save_gif()  # Save the animation as a GIF
    plt.show()  # Display the animation

