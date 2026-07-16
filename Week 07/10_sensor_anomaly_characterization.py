# Purpose:
# This script simulates various types of anomalies in sensor data over time and visualizes those anomalies against
# a "true" reference signal. The anomalies modeled include bias, drift, sensor freeze (stuck), data dropout,
# and outliers. The script also categorizes and counts the occurrence of each type of anomaly, providing insights 
# into the distribution of data quality issues.

# Import necessary libraries
import numpy as np  # For numerical computations and random number generation
import matplotlib.pyplot as plt  # For data visualization

# Main function
def main():
    # Purpose:
    # Simulates a sensor signal with anomalies (bias, drift, stuck values, dropouts, outliers) compared to a linear "truth" signal.
    # Visualizes the true signal and the anomalous sensor signal, and counts the occurrences for each type of anomaly.

    # Initialize a random number generator with a fixed seed for reproducibility
    rng = np.random.default_rng(10)
    
    # Set up the time array and the true signal
    dt = 0.1  # Time step (sampling interval)
    t = np.arange(0, 60, dt)  # Time array from 0 to 60 seconds at intervals of 0.1
    truth = 0.4 * t  # Define a linear "true" signal

    # Initialize the sensor signal by adding Gaussian noise to the true signal
    s = truth + rng.normal(0, 0.5, len(t))  # Add random noise with a standard deviation of 0.5
    labels = np.array(['nominal'] * len(t), dtype=object)  # Initialize labels to mark the status of each data point

    # Apply different types of anomalies to the sensor signal

    # Inject a bias between 10 and 20 seconds
    w = (t >= 10) & (t < 20)  # Time window for the bias anomaly
    s[w] += 4  # Add a constant bias of 4
    labels[w] = 'bias'  # Update labels for this time range

    # Apply a drift anomaly between 20 and 35 seconds
    w = (t >= 20) & (t < 35)  # Time window for the drift anomaly
    s[w] += 0.4 * (t[w] - 20)  # Introduce a drift proportional to time
    labels[w] = 'drift'  # Update labels for this time range

    # Simulate a "stuck" sensor between 35 and 43 seconds
    w = (t >= 35) & (t < 43)  # Time window for the stuck anomaly
    s[w] = s[np.where(t >= 35)[0][0]]  # Keep the value constant (stuck at the value from the start of this window)
    labels[w] = 'stuck'  # Update labels for this time range

    # Introduce dropout (missing data) between 43 and 50 seconds
    w = (t >= 43) & (t < 50)  # Time window for the dropout anomaly
    s[w] = np.nan  # Replace sensor values with NaN to simulate data dropout
    labels[w] = 'dropout'  # Update labels for this time range

    # Add a single outlier at 54 seconds
    i = np.argmin(abs(t - 54))  # Find the closest index to 54 seconds
    s[i] += 15  # Add a large outlier value
    labels[i] = 'outlier'  # Update label for the outlier

    # Count and print the occurrences of each type of data label
    for label in np.unique(labels):
        print(label, np.sum(labels == label))

    # Plot the true signal and the sensor signal with anomalies
    plt.figure()  # Create a new figure
    plt.plot(t, truth, label='Truth')  # Plot the true signal
    plt.plot(t, s, label='Sensor')  # Plot the sensor signal with anomalies
    plt.title('Sensor Anomalies')  # Title of the plot
    plt.grid(True)  # Add a grid for better readability
    plt.legend()  # Add a legend to differentiate signals
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
