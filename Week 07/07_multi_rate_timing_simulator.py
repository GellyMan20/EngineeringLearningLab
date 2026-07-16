# Purpose:
# This script visualizes the timing events of multiple sensors operating at different sampling rates.
# Each sensor stream has a distinct timing frequency, and the data is plotted to show when events occur, using an event plot.
# The y-axis represents different sensors (e.g., "Altimeter," "Magnetometer," "GPS," and "IMU"), 
# while the x-axis represents time. This visualization is useful for analyzing the timing differences between sensors with varying rates.

# Import necessary libraries
import numpy as np  # For numerical computations and array manipulations
import matplotlib.pyplot as plt  # For creating plots

# Main function
def main():
    # Define a time array from 0 to 10 seconds, with a resolution of 0.001 seconds
    t = np.arange(0, 10, 0.001)

    # Create streams of events with different sampling rates
    streams = [t[::10], t[::200], t[::50], t[::25]]  # Subsample the time array at different intervals

    # Create an event plot for the different sampling streams
    plt.figure()  # Create a new figure
    plt.eventplot(
        streams,  # The input streams
        lineoffsets=[4, 3, 2, 1],  # Y-offset for each stream to distinguish them
        linelengths=0.8  # Length of each event line
    )

    # Set the y-axis ticks to correspond to sensor names
    plt.yticks(
        [1, 2, 3, 4],  # Y-tick positions
        ['Altimeter', 'Magnetometer', 'GPS', 'IMU']  # Sensor names corresponding to the streams
    )

    # Add a title and axis labels
    plt.title('Multi-Rate Sensor Timing')  # Title of the plot
    plt.xlabel('Time [s]')  # x-axis label indicating time in seconds

    # Add a grid for the x-axis for better visualization
    plt.grid(True, axis='x')

    # Display the plot
    plt.show()

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
