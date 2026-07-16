# Purpose:
# This script simulates the effects of GPS noise, outliers, and dropouts on object trajectory data. 
# It generates a true trajectory for an object moving in two dimensions and introduces simulated errors 
# (random noise, outliers, and dropouts) to mimic real-world GPS measurement imperfections. 
# The script illustrates how these errors impact the accuracy of the estimated trajectory 
# compared to the true trajectory. The results are visualized using plots to highlight the differences.

# Import necessary libraries
import numpy as np  # For numerical operations and random data generation
import matplotlib.pyplot as plt  # For data visualization (plotting graphs)

# Main function
def main():
    # Purpose:
    # Generates and visualizes a simulated "true" trajectory of an object and contrasts it
    # with noisy and error-prone GPS data, including the effects of noise, outliers, and dropouts.
    
    # Initialize a random number generator with seed 2 for reproducibility
    rng = np.random.default_rng(2)
    
    # Configure parameters for time and signal generation
    dt = 0.2  # Time step (sampling period)
    t = np.arange(0, 100, dt)  # Create an array of time values from 0 to 100 seconds in increments of 0.2
    
    # Compute the "true" trajectory (ground truth for comparison)
    tx = 0.8 * t  # X-coordinate (linear progression scaled by factor of 0.8)
    ty = 12 * np.sin(t / 15)  # Y-coordinate (sine wave scaled and stretched)

    # Generate simulated noisy GPS data based on the true trajectory
    gx = tx + 1.5 + rng.normal(0, 1.8, len(t))  # Add random Gaussian noise to X data
    gy = ty - 0.8 + rng.normal(0, 1.8, len(t))  # Add random Gaussian noise to Y data
    
    # Introduce GPS outliers
    out = rng.choice(len(t), 8, replace=False)  # Select 8 random indices for outliers
    gx[out] += rng.normal(0, 20, len(out))  # Add exaggerated noise to X data for outliers
    gy[out] += rng.normal(0, 20, len(out))  # Add exaggerated noise to Y data for outliers

    # Simulate GPS dropouts (missing data)
    drop = rng.random(len(t)) < 0.06  # Generate random dropouts based on a 6% probability
    gx[drop] = np.nan  # Replace dropped X data with NaN
    gy[drop] = np.nan  # Replace dropped Y data with NaN

    # Calculate error between true signal and noisy GPS data
    err = np.hypot(gx - tx, gy - ty)  # Compute Euclidean distance error at each time step

    # Print statistics for the error and dropouts
    print(f'Mean error: {np.nanmean(err):.2f} m')  # Average error, ignoring NaN values
    print(f'95th percentile: {np.nanpercentile(err, 95):.2f} m')  # 95th percentile of errors
    print(f'Dropout rate: {100 * np.mean(drop):.1f}%')  # Dropout rate as a percentage

    # Plot the true trajectory and the simulated noisy GPS data
    plt.figure()  # Create a new plot
    plt.plot(tx, ty, label='Truth')  # Plot the true trajectory (ground truth)
    plt.scatter(gx, gy, s=10, label='GPS')  # Scatter plot for noisy GPS data points
    plt.title('GPS Noise, Outliers, Dropouts')  # Set the plot title
    plt.axis('equal')  # Equalize axis scaling for better visualization
    plt.grid(True)  # Add a grid to the plot for clarity
    plt.legend()  # Display plot legend to differentiate signals
    plt.show()  # Show the plot

# Entry point: Execute main() if the script is run directly
if __name__ == '__main__':
    main()
