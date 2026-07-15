# Purpose:
# This script simulates a sensor fusion process to estimate orientation (angle) over time using data from a gyroscope 
# and an accelerometer. The gyroscope provides angular velocity, and the accelerometer provides orientation with noise. 
# The script demonstrates how integrating gyroscope and accelerometer data can create a fused signal 
# (e.g., with a complementary filter) that combines the fast response of the gyroscope with the long-term stability of the accelerometer.
# The output is a plot showing the "true" angle, raw gyroscope integration, noisy accelerometer data, and the fused angle.

# Import necessary libraries
import numpy as np  # For numerical operations and random data
import matplotlib.pyplot as plt  # For creating plots

# Main function
def main():
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(12)

    # Configure time and simulation parameters
    dt = 0.01  # Time step in seconds
    t = np.arange(0, 40, dt)  # Time vector from 0 to 40 seconds with increments of 0.01

    # Define the "true" angle as a sine wave and calculate the angular rate (derivative) of the angle
    truth = np.deg2rad(20 * np.sin(0.35 * t))  # "True" angle in radians (sine wave of 20 degrees amplitude)
    rate = np.gradient(truth, dt)  # Angular rate (derivative of angle with respect to time)

    # Simulate gyroscope readings with bias and Gaussian noise
    gyro = rate + np.deg2rad(0.35) + rng.normal(0, np.deg2rad(0.12), len(t))  # Gyro: rate + small bias + noise

    # Simulate accelerometer readings with Gaussian noise
    accel = truth + rng.normal(0, np.deg2rad(2.5), len(t))  # Accelerometer: truth + large noise

    # Initialize arrays for integrated gyro (gi) and fused estimate (fused)
    gi = np.zeros_like(t)  # Integrated angle from the gyroscope
    fused = np.zeros_like(t)  # Fused angle combining gyroscope and accelerometer data
    a = 0.98  # Complementary filter weighting factor (closer to 1 gives more weight to gyro)

    # Fuse gyroscope and accelerometer data using a complementary filter
    for k in range(1, len(t)):
        # Integrate gyroscope data to estimate angle (previous angle + rate * dt)
        gi[k] = gi[k - 1] + gyro[k] * dt
        # Complementary filter: combine short-term gyroscope data with long-term accelerometer data
        fused[k] = a * (fused[k - 1] + gyro[k] * dt) + (1 - a) * accel[k]

    # Plot the true signal, gyro-only integration, accelerometer signal, and fused signal
    plt.figure()  # Create a new plot
    plt.plot(t, np.rad2deg(truth), label='Truth')  # Convert the true angle to degrees and plot
    plt.plot(t, np.rad2deg(gi), label='Gyro')  # Plot gyro-integrated angle in degrees
    plt.plot(t, np.rad2deg(accel), alpha=0.4, label='Accel')  # Plot accelerometer data in degrees, with transparency
    plt.plot(t, np.rad2deg(fused), label='Fused')  # Plot the fused angle estimate in degrees
    plt.grid(True)  # Add a grid for better readability
    plt.legend()  # Add a legend to distinguish different signals
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
