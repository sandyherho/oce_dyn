#!/usr/bin/env python

"""
winethief.py

Sandy Herho, 2024
"""

import numpy as np

def main():
    print("Select the numerical scheme for the decay simulation:")
    print("1: Explicit scheme")
    print("2: Implicit scheme")
    mode = int(input("Enter your choice (1 or 2): "))

    # Constants and Initialization
    CZERO = 100.0   # Initial concentration
    kappa = 0.0001  # Decay constant
    dt = 3600.0     # Time step (seconds)
    ntot = int(24.0 * 3600 / dt)  # Total number of iterations for 24 hours
    nout = int(3600.0 / dt)       # Output every hour

    # Factor used in the scheme
    if mode == 1:
        fac = 1.0 - dt * kappa
        if fac <= 0.0:
            print('STABILITY CRITERION ALERT: REDUCE TIME STEP')
    elif mode == 2:
        fac = 1.0 / (1.0 + dt * kappa)

    # Initialize variables
    C = CZERO
    time = 0

    # File handling
    output_file = 'output1_py.txt' if mode == 1 else 'output2_py.txt'
    with open(output_file, 'w') as file:
        file.write(f"{0},{100.0},{100.0}\n")  # Write initial values

        # Iteration loop
        for n in range(1, ntot + 1):
            CN = C * fac  # prediction for the next time step
            time = n * dt
            CTRUE = CZERO * np.exp(-kappa * time)  # exact analytical solution
            C = CN  # updating for upcoming time step

            # Output data if the current iteration is a multiple of nout
            if n % nout == 0:
                file.write(f"{time/3600.0},{C},{CTRUE}\n")  # Write to file
                print(f"Data output at time = {time/3600.0} hours")  # Print to screen

if __name__ == "__main__":
    main()
