# Purpose:
# This script simulates the effects of latency and dropout on measurements. 
# The "true" signal is a sine wave, and the measurements are affected by noise, latency (time delay), and dropout (random missing data points).
# It visually compares the true signal with measurements under different latency and dropout conditions, demonstrating the impact of these imperfections on data quality.

# Import necessary libraries
import numpy as np  # For numerical operations, including random number generation
import matplotlib.pyplot as plt  # For visualization of the signals

# Subroutine to simulate latency and dropout effects on a signal
def run(latency, dropout, rng):
    # Purpose:
    # Applies latency and dropout to a sine wave signal with added Gaussian noise.
    # Returns the time array, true signal, and affected noisy signal.

    dt = 0.05  # Time step (sampling interval)
    t = np.arange(0, 40, dt)  # Create a time array from 0 to 40 seconds with intervals of 0.05
    truth = np.sin(0.3 * t)  # Generate the "true" sine wave signal with frequency 0.3 Hz
    m = truth + rng.normal(0, 0.08, len(t))  # Add Gaussian noise to the true signal
    
    # Apply latency: shift the signal forward in time by the latency amount
    s = int(latency / dt)  # Convert latency in seconds to number of samples
    m = np.roll(m, s)  # Shift the noisy signal forward
    m[:s] = np.nan  # Make the initial shifted samples invalid (NaN)

    # Apply dropout: randomly remove data points with a certain probability
    m[rng.random(len(t)) < dropout] = np.nan  # Set dropped samples to NaN based on dropout probability
    
    return t, truth, m  # Return the time array, true signal, and noisy signal with effects

# Main function
def main():
    # Purpose:
    # Generates and visualizes the "true" signal alongside measurements with varying levels of latency and dropout.
    
    rng = np.random.default_rng(8)  # Initialize a random number generator with a fixed seed for reproducibility
    
    # Create a figure for plotting
    plt.figure()

    # Simulate and plot signals for different latency and dropout parameters
    for latency, dropout in [(0, 0), (0.2, 0.05), (0.5, 0.15)]:  # Test cases with varying latency and dropout values
        t, truth, m = run(latency, dropout, rng)  # Generate the simulated data
        plt.plot(t, m, label=f'{latency}s latency, {100 * dropout:.0f}% dropout')  # Plot the noisy signal with a descriptive label
    
    # Plot the "true" signal with higher line width for emphasis
    plt.plot(t, truth, linewidth=2, label='Truth')  # Add the true signal to the plot

    # Add plot title, grid, legend, and display the plot
    plt.title('Latency and Dropout')  # Title of the plot
    plt.grid(True)  # Add a grid for better readability
    plt.legend()  # Add a legend to distinguish signals
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
