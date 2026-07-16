# Purpose:
# This script demonstrates a basic **fault detection** system using a simple residual-based anomaly detection approach.
# A simulated position (`truth`) is corrupted by noise and faults such as step changes and spikes.
# An estimate of the position is generated, and the residual (difference between the measurement and estimate) is computed.
# Residuals exceeding a threshold value are flagged as anomalies. 
# The results, including detected anomalies, are visualized.

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Main function
def main():
    """
    Simulates a position estimation problem with injected faults and noise.
    Implements fault detection by calculating the residual and identifying anomalies where 
    residuals exceed a threshold.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(21)

    # Define time settings and true motion
    dt = 0.1  # Time step in seconds
    t = np.arange(0, 50, dt)  # Time vector from 0 to 50 seconds with increments of 0.1
    truth = 0.5 * t  # True position (linear motion)

    # Simulate noisy sensor measurements with faults
    s = truth + rng.normal(0, 0.8, len(t))  # Add Gaussian noise to the true position
    s[(t >= 18) & (t <= 28)] += 5  # Introduce a step fault between t=18 and t=28
    s[np.argmin(abs(t - 38))] += 18  # Introduce a spike fault near t=38

    # Initialize estimation variables
    est = np.zeros_like(t)  # Initialize the estimate array
    alpha = 0.15  # Smoothing factor for recursive estimation

    # Update estimate iteratively based on measurements
    for k in range(1, len(t)):
        est[k] = est[k - 1] + 0.5 * dt  # Predict new position
        est[k] += alpha * (s[k] - est[k])  # Correct based on the measurement error

    # Calculate residuals and detect faults
    r = s - est  # Compute residual (measurement - estimate)
    th = 3.0  # Threshold for fault detection
    flags = np.abs(r) > th  # Flag residuals that exceed the threshold

    # Print number of detected faults
    print(f'Detected fault samples: {flags.sum()}')

    # Visualization of residuals and detected anomalies
    plt.figure()
    plt.plot(t, r, label='Residual')  # Plot residuals over time
    plt.axhline(th, linestyle='--', label=f'Threshold ({th})')  # Upper threshold line
    plt.axhline(-th, linestyle='--', label=f'-Threshold (-{th})')  # Lower threshold line
    plt.scatter(t[flags], r[flags], marker='x', label='Anomalies')  # Mark anomalies
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add legend for clarity in the plot
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
