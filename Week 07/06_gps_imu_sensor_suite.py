# Purpose:
# This script simulates data from an Inertial Measurement Unit (IMU) and a GPS system, demonstrating how GPS characteristics 
# such as sampling rate, latency, measurement noise, and dropouts affect position estimation. 
# It calculates the "true" position of an object based on acceleration data and compares it with noisy and delay-affected 
# GPS-derived positions, highlighting discrepancies caused by these imperfections. The results are visualized as plots 
# and exported as tabular data for further analysis.

# Import necessary libraries
from dataclasses import dataclass  # For concise data structure definition to store configurations
import numpy as np  # For numerical and random operations
import pandas as pd  # For creating and handling structured tabular data
import matplotlib.pyplot as plt  # For visualization of the data

# Define a configuration class to store simulation parameters
@dataclass
class Config:
    imu_rate_hz: float = 100.0  # IMU data sampling rate in Hz
    gps_rate_hz: float = 5.0  # GPS data sampling rate in Hz
    gps_latency_s: float = 0.4  # GPS measurement latency in seconds
    gps_dropout_probability: float = 0.05  # Probability of GPS dropout at each sample

# Main function
def main():
    # Purpose:
    # Simulates IMU-derived and GPS-derived position data based on acceleration inputs, incorporating realistic 
    # imperfections like noise, dropout, and latency in GPS data. Outputs the data and visualizes the results.

    # Set up random number generator for reproducibility
    rng = np.random.default_rng(6)  # Seed ensures consistent results
    c = Config()  # Create a configuration object with default values

    # Define simulation time array and sampling interval
    dt = 1 / c.imu_rate_hz  # Time increment for IMU based on sampling rate
    t = np.arange(0, 60, dt)  # Time array from 0 to 60 seconds at 'dt' intervals

    # Calculate true acceleration, velocity, and position in both x and y dimensions
    ax = 0.3 * np.sin(0.3 * t)  # True x-acceleration as a sine wave pattern
    ay = 0.2 * np.cos(0.2 * t)  # True y-acceleration as a cosine wave pattern
    vx = np.cumsum(ax) * dt  # Integrate acceleration to compute x-velocity
    vy = np.cumsum(ay) * dt  # Integrate acceleration to compute y-velocity
    x = np.cumsum(vx) * dt  # Integrate x-velocity to compute x-position
    y = np.cumsum(vy) * dt  # Integrate y-velocity to compute y-position

    # Add noise and biases to the accelerometer signals to simulate IMU sensor imperfections
    iax = ax + 0.03 + rng.normal(0, 0.05, len(t))  # Simulate biased and noisy x-acceleration
    iay = ay - 0.02 + rng.normal(0, 0.05, len(t))  # Simulate biased and noisy y-acceleration

    # Simulate noisy GPS measurements
    stride = int(c.imu_rate_hz / c.gps_rate_hz)  # Convert IMU rate to GPS rate (downsampling factor)
    gx = np.full(len(t), np.nan)  # Initialize GPS x-position with NaN
    gy = np.full(len(t), np.nan)  # Initialize GPS y-position with NaN
    gx[::stride] = x[::stride] + rng.normal(0, 1.5, len(x[::stride]))  # Add noise to GPS x-position
    gy[::stride] = y[::stride] + rng.normal(0, 1.5, len(y[::stride]))  # Add noise to GPS y-position

    # Simulate GPS dropout based on a probability
    idx = np.where(~np.isnan(gx))[0]  # Get indices for available GPS samples (non-NaN values)
    drop = rng.random(len(idx)) < c.gps_dropout_probability  # Generate random dropouts
    gx[idx[drop]] = np.nan  # Apply dropout to GPS x-position
    gy[idx[drop]] = np.nan  # Apply dropout to GPS y-position

    # Simulate GPS latency by shifting the GPS signals by a fixed time delay
    d = int(c.gps_latency_s / dt)  # Convert the latency in seconds to number of samples
    gx = np.roll(gx, d)  # Shift GPS x-position by the latency
    gy = np.roll(gy, d)  # Shift GPS y-position by the latency
    gx[:d] = np.nan  # Set invalid shifted values to NaN
    gy[:d] = np.nan  # Set invalid shifted values to NaN

    # Create a Pandas DataFrame to store the simulated data for analysis
    df = pd.DataFrame({
        'time_s': t,  # Time array (seconds)
        'true_x_m': x,  # True x-position
        'true_y_m': y,  # True y-position
        'imu_ax_mps2': iax,  # IMU x-acceleration (noisy and biased)
        'imu_ay_mps2': iay,  # IMU y-acceleration (noisy and biased)
        'gps_x_m': gx,  # Simulated GPS x-position
        'gps_y_m': gy,  # Simulated GPS y-position
    })

    # Print the first few rows and descriptive statistics of the DataFrame
    print(df.head())  # Display the first 5 rows
    print(df.describe())  # Display summary statistics for the DataFrame

    # Visualize the true position and GPS-derived position
    plt.figure()  # Create a new figure for plotting
    plt.plot(x, y, label='Truth')  # Plot the true trajectory
    plt.scatter(gx, gy, s=12, label='GPS')  # Scatter plot for GPS data points
    plt.axis('equal')  # Set equal scaling for both x and y axes
    plt.grid(True)  # Add a grid to the plot for better readability
    plt.legend()  # Add a legend to distinguish between true and GPS signals
    plt.show()  # Display the plot

# Entry point: Execute main() if the script is run directly
if __name__ == '__main__':
    main()
