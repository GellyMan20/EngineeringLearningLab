# Import the necessary libraries
import numpy as np  # For numerical operations and random number generation
import matplotlib.pyplot as plt  # For plotting graphs

# Define the main function
def main():
    # Initialize a random number generator with a seed for reproducibility
    rng = np.random.default_rng(1)
    
    # Define the time step and time array
    dt = 0.01  # Time step (sampling interval)
    t = np.arange(0, 30, dt)  # Generate a time array from 0 to 30 seconds in increments of 0.01
    
    # Create the "true" signal which is a sine wave
    truth = np.sin(0.7 * t)  # Sine wave with a specific frequency (0.7 rad/s)
    
    # Simulate different types of sensor errors and add them to the true signal
    series = {
        'White noise': truth + rng.normal(0, 0.08, len(t)),  # Add random Gaussian noise
        'Bias': truth + 0.25,  # Add a constant bias of 0.25 to the signal
        'Random walk': truth + np.cumsum(rng.normal(0, 0.0015, len(t))),  # Simulate a random walk
        'Drift': truth + 0.01 * t,  # Add a slow linear drift over time
        'Quantized': np.round(truth / 0.1) * 0.1,  # Quantize the signal (round to nearest 0.1)
    }
    
    # Initialize a plot
    plt.figure()  # Create a new figure for plotting
    
    # Plot the "true" signal
    plt.plot(t, truth, label='Truth')  # Add the true signal to the plot with a label
    
    # Loop through each sensor error type and plot it
    for name, y in series.items():
        plt.plot(t, y, alpha=0.75, label=name)  # Plot the signal and set transparency (alpha)
    
    # Add chart title and axis labels
    plt.title('Common Sensor Error Types')  # Set the title of the plot
    plt.xlabel('Time [s]')  # Label the x-axis as time
    plt.ylabel('Measurement')  # Label the y-axis as measurement/signal

    # Add a grid to the plot for better readability
    plt.grid(True)

    # Add a legend to differentiate between signals
    plt.legend()
    
    # Display the plot
    plt.show()

# Entry point for the program: Run the main function if this script is executed directly
if __name__ == '__main__':
    main()
