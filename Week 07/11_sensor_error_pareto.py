# Purpose:
# This script generates a Pareto analysis to visualize the distribution of sensor errors.
# It simulates occurrences of different types of sensor issues (e.g., "Accel bias," "GPS dropout," etc.),
# calculates their frequencies, and then ranks them in descending order of importance.
# Two visualizations are created:
#   1. A bar chart showing the frequency of each error type.
#   2. A cumulative percentage line chart to identify the most significant contributors (Pareto principle: 80/20 rule).

# Import necessary libraries
from collections import Counter  # For counting the occurrences of categorical data
import numpy as np  # For numerical operations and random number generation
import matplotlib.pyplot as plt  # For creating visualizations

# Main function
def main():
    # Initialize a random number generator with a fixed seed for reproducibility
    rng = np.random.default_rng(11)
    
    # Simulate sensor error categories and their probabilities
    cats = rng.choice(
        ['Accel bias', 'GPS dropout', 'Latency', 'GPS outlier', 'Timing jitter', 'Gyro drift'],  # Categories
        500,  # Number of samples
        p=[0.28, 0.22, 0.18, 0.12, 0.10, 0.10]  # Probabilities for each category
    )
    
    # Count the occurrences of each error type and sort them in descending order
    ordered = Counter(cats).most_common()
    names = [x[0] for x in ordered]  # Extract the names of the error categories
    vals = [x[1] for x in ordered]  # Extract their respective counts
    
    # Calculate cumulative percentage for the Pareto chart
    cum = 100 * np.cumsum(vals) / np.sum(vals)  # Calculate cumulative percentages
    
    # Create a bar chart to show the frequency of each sensor error
    plt.figure()
    plt.bar(names, vals)  # Bar chart of error counts
    plt.xticks(rotation=35)  # Rotate x-axis labels for readability
    plt.title('Sensor Error Pareto')  # Title for the chart
    plt.tight_layout()  # Adjust layout to avoid label overlap
    plt.show()  # Display the bar chart
    
    # Create a cumulative percentage chart (Pareto chart)
    plt.figure()
    plt.plot(names, cum, marker='o')  # Line plot of cumulative percentages
    plt.axhline(80, linestyle='--')  # Horizontal line at 80% (Pareto threshold)
    plt.xticks(rotation=35)  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout
    plt.show()  # Display the Pareto chart

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
