#!/usr/bin/env python

import numpy as np

def main():
    # Constants
    pi = np.pi
    freq = -2 * pi / (24 * 3600)
    f = 2 * freq
    dt = 6 * 24 * 3600 / 120
    alpha = f * dt
    beta = 0.25 * alpha * alpha
    ntot = 120

    # Initial conditions
    uzero = 0.05
    vzero = 0.05
    u = 0.1
    v = 0.0
    x = 0.0
    y = 0.0

    # Initialize mode 2 variables
    u2, v2, x2, y2 = u, v, x, y

    # Open files
    with open('output1_pyv1.txt', 'w') as file1, open('output2_pyv1.txt', 'w') as file2:
        # Write headers
        file1.write(f"{freq} {dt} {ntot}\n")
        file2.write(f"{freq} {dt} {ntot}\n")

        # Iteration loop
        for n in range(1, ntot + 1):
            time = n * dt
            du = 0.0
            dv = 0.0

            if n == 40:
                dv = -0.3
            elif n == 80:
                dv = 0.1

            # Mode 1 calculations
            ustar = u + du
            vstar = v + dv

            un = (ustar * (1 - beta) + alpha * vstar) / (1 + beta)
            vn = (vstar * (1 - beta) - alpha * ustar) / (1 + beta)

            xn = x + dt * (un + uzero) / 1000
            yn = y + dt * (vn + vzero) / 1000

            u, v, x, y = un, vn, xn, yn

            file1.write(f"{x} {y} {time}\n")

            # Mode 2 calculations
            ustar = u2 + du
            vstar = v2 + dv

            un2 = np.cos(alpha) * ustar + np.sin(alpha) * vstar
            vn2 = np.cos(alpha) * vstar - np.sin(alpha) * ustar

            xn2 = x2 + dt * (un2 + uzero) / 1000
            yn2 = y2 + dt * (vn2 + vzero) / 1000

            u2, v2, x2, y2 = un2, vn2, xn2, yn2

            file2.write(f"{x2} {y2} {time}\n")

if __name__ == "__main__":
    main()

