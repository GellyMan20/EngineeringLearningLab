# Purpose:
# This script simulates the effects of noise and drift on accelerometer and gyroscope signals.
# It generates "true" signals for an accelerometer (based on a sine wave) and a gyroscope (based on a cosine wave),
# then introduces simulated measurement errors such as random noise and cumulative drift to model real-world sensor behavior.
# The script visualizes and compares the true signals with the noisy, drift-affected measured signals to highlight the impact 
# of errors in sensor-based motion tracking systems.

# Import necessary libraries
import numpy as np  # For numerical operations, including random number generation
import matplotlib.pyplot as plt  # For visualization through plotting graphs

# Main function
def main():
    # Purpose:
    # Simulates both 'true' and noisy accelerometer and gyroscope signals, introducing drift and noise.
    # Compares and visualizes these signals to demonstrate how sensor imperfections affect measurements.
    
    # Initialize a random number generator with a fixed seed for reproducibility
    rng = np.random.default_rng(3)  # Seed ensures consistent random values across runs
    
    # Configure time parameters
    dt = 0.01  # Time step (interval of sampling)
    t = np.arange(0, 40, dt)  # Create an array of time values from 0 to 40 seconds in increments of 0.01
    
    # Define the 'true' accelerometer and gyroscope signal (ground truth)
    ta = 0.8 * np.sin(0.4 * t)  # True accelerometer signal as a sine wave
    tg = 0.15 * np.cos(0.25 * t)  # True gyroscope signal as a cosine wave
    
    # Simulate measured accelerometer signal with noise and drift
    a = (
        ta  # Start with the true accelerometer signal
        + 0.08  # Add a constant offset
        + np.cumsum(rng.normal(0, 0.0004, len(t)))  # Add random cumulative drift over time
        + rng.normal(0, 0.06, len(t))  # Add random Gaussian noise
    )
    
    # Simulate measured gyroscope signal with noise and drift
    g = (
        tg  # Start with the true gyroscope signal
        + np.deg2rad(0.4)  # Add a constant offset (converted to radians)
        + np.cumsum(rng.normal(0, np.deg2rad(0.002), len(t)))  # Add random cumulative drift in radians
        + rng.normal(0, np.deg2rad(0.08), len(t))  # Add random Gaussian noise in radians
    )

    # Plot the accelerometer signals (comparison of true and measured)
    plt.figure()  # Create a new figure
    plt.plot(t, ta, label='True accel')  # Plot the true accelerometer signal
    plt.plot(t, a, alpha=0.7, label='Measured accel')  # Plot the measured accelerometer signal (with transparency)
    plt.grid(True)  # Add a grid to improve readability
    plt.legend()  # Display a legend to differentiate the signals
    plt.show()  # Show the accelerometer plot

    # Plot the gyroscope signals (comparison of true and measured)
    plt.figure()  # Create another figure
    plt.plot(t, np.rad2deg(tg), label='True gyro')  # Convert true gyroscope signal to degrees and plot
    plt.plot(t, np.rad2deg(g), alpha=0.7, label='Measured gyro')  # Convert measured gyroscope signal to degrees and plot
    plt.grid(True)  # Add a grid for better readability
    plt.legend()  # Display a legend to differentiate the signals
    plt.show()  # Show the gyroscope plot

# Entry point: Execute main() if the script is run directly
if __name__ == '__main__':
    main()
