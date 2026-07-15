# Purpose:
# This script simulates the phenomenon of dead reckoning drift.
# It calculates the position of an object based on a given acceleration profile,
# and compares the true position (calculated without noise) with an estimated position
# (derived from noisy sensor data).
# The script demonstrates how measurement noise and bias can accumulate over time,
# leading to drift in the estimated position.

import numpy as np  # Numerical operations and random number generation
import matplotlib.pyplot as plt  # Visualization of results using plots
  
# Main function
def main():
    # Purpose:
    # Simulates true and measured acceleration, velocity, and position
    # over time. Visualizes the impact of dead reckoning drift caused
    # by noise and bias in the measurements.
    
    # Initialize a random number generator for reproducibility
    rng = np.random.default_rng(4)

    # Define time array and step
    dt = 0.01
    t = np.arange(0, 60, dt)

    # True acceleration profile
    a = np.zeros_like(t)
    a[(t >= 3) & (t < 12)] = 0.7
    a[(t >= 30) & (t < 38)] = -0.5

    # Integration to calculate true velocity and position
    v = np.cumsum(a) * dt
    x = np.cumsum(v) * dt

    # Simulated noisy acceleration
    am = a + 0.025 + rng.normal(0, 0.04, len(t))

    # Integration to calculate estimated velocity and position from measurements
    ve = np.cumsum(am) * dt
    xe = np.cumsum(ve) * dt

    # Visualization of dead reckoning drift
    plt.figure()
    plt.plot(t, x, label='Truth')
    plt.plot(t, xe, label='Dead reckoning')
    plt.title('Dead Reckoning Drift')
    plt.grid(True)
    plt.legend()
    plt.show()

# Entry point for the script
if __name__ == '__main__':
    main()
