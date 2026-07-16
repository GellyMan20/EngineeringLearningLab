# Purpose:
# This script simulates the effects of timing jitter and system latency on data delivery.
# Using a generated sine wave as the "true" signal, it adds random variations (jitter) to simulate
# irregular sampling and introduces a fixed delay (latency) before data becomes available. 
# The true signal and the delayed, jittered samples are visualized to highlight the impact of
# these phenomena on data transmission systems or processes.

# Import necessary libraries
from collections import deque  # For implementing a double-ended queue (FIFO data structure)
import numpy as np  # For numerical operations and random number generation
import matplotlib.pyplot as plt  # For creating plots to visualize the data

# Define the main function
def main():
    # Purpose:
    # Simulates timing jitter and latency in data sampling and delivery, 
    # and visualizes the impact on a known sine wave signal ("truth").
    
    # Initialize a random number generator with a seed for reproducibility
    rng = np.random.default_rng(5)  # Ensures consistent results across runs

    # Define the true signal and time parameters
    dt = 0.01  # Time step (sampling interval)
    t = np.arange(0, 30, dt)  # Create a time array from 0 to 30 seconds, step size = 0.01
    truth = np.sin(0.6 * t)  # Generate the "true" signal as a sine wave with frequency 0.6

    # Initialize simulation variables
    next_sample = 0.0  # Time for the next sample to be generated
    q = deque()  # Queue to store delayed samples (time-value pairs of data)
    td = []  # List to store the delivery times of the samples
    yd = []  # List to store the delivered (jittered) sample values

    # Simulate jitter and latency
    for time, val in zip(t, truth):
        # Generate new samples with a fixed delay (latency) and random jitter
        if time >= next_sample:  # If the next sample time is reached
            q.append((time + 0.35, val + rng.normal(0, 0.05)))  # Add delayed sample to the queue
            next_sample += max(0.01, 0.1 + rng.normal(0, 0.01))  # Schedule the next sample with some jitter

        # Deliver samples from the queue when their delay time has passed
        while q and q[0][0] <= time:
            a, b = q.popleft()  # Retrieve and remove the first sample in the queue
            td.append(a)  # Store the delivery time of the sample
            yd.append(b)  # Store the delivered sample value

    # Visualization of the true signal and the delivered signal
    plt.figure()  # Create a new figure for plotting
    plt.plot(t, truth, label='Truth')  # Plot the true signal
    plt.scatter(td, yd, s=12, label='Delivered')  # Scatter plot of delivered samples
    plt.title('Timing Jitter and Latency')  # Set the plot title
    plt.grid(True)  # Add a grid to the plot
    plt.legend()  # Add a legend to distinguish the lines and points
    plt.show()  # Display the plot

# Entry point for the program: Run the main function if this script is executed directly
if __name__ == '__main__':
    main()
