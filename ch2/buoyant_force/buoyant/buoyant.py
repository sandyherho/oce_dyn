#!/usr/bin/env python

import numpy as np

# Define the density function to calculate ambient density
def density(zin, N2in):
    rhos = 1025.0
    g = 9.81
    return rhos * (1 - N2in / g * zin)

def main():
    # Initialization of variables and parameters
    z = -80.0       # initial location is 80 m below sea surface
    w = 0.0         # no vertical speed at time zero
    dt = 1.0        # value of time step; dt = 1 second here
    rho = 1025.5    # density of your object
    g = 9.81        # gravity
    N2 = 1.0e-4     # stability frequency squared of ambient ocean
    r = 0.0         # friction parameter
    ntot = int(3600 / dt)  # total number of iterations

    # File handling
    with open('output_python.txt', 'w') as file:
        # Write initial conditions to file
        file.write(f"{0:12.4f}{z:12.4f}{w:12.4f}{rho-1000:12.4f}\n")

        # Start of iteration
        for n in range(1, ntot + 1):
            rhosea = density(z, N2)      # determine ambient density at current location
            bf = -g * (rho - rhosea) / rho  # calculate buoyancy force
            wn = (w + dt * bf) / (1 + r * dt)  # predict new vertical speed
            zn = z + dt * wn              # predict new location
            zn = min(zn, 0.0)             # location constrained by sea surface
            zn = max(zn, -100.0)          # location constrained by seafloor

            # Update Z and W for next time step
            w = wn
            z = zn
            time = n * dt

            # Write to file every 10 time steps
            if n % 10 == 0:
                file.write(f"{time:12.4f}{z:12.4f}{w:12.4f}{rho-1000:12.4f}\n")

    # End of program
    print(" *** Simulation completed *** ")

if __name__ == "__main__":
    main()

