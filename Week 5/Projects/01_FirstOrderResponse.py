"""
Project: First-Order Step Response Explorer
Purpose:
This script demonstrates the behavior of a **first-order system** in response to a step input. First-order systems are common in control systems, electrical circuits, and thermal systems. The goals of this project include:
- Understanding the **time constant** (\( \tau \)), which characterizes how quickly the system responds.
- Observing the system's **rise time**, indicating how fast the system approaches its steady-state value.
- Exploring the system's **settling behavior**, specifically when the output stabilizes near its final value.
The script visualizes step responses for different time constants to help users draw insights on system dynamics.
"""

# Importing necessary libraries
import numpy as np  # Numerical library for computations
import matplotlib.pyplot as plt  # Library for creating plots and visualizations

# Function to calculate the first-order system's step response
def first_order_step(t, tau, gain=1.0):
    """
    Computes the step response of a first-order system.

    Parameters:
        t (ndarray): Time vector (in seconds).
        tau (float): Time constant of the system (seconds). Determines the speed of response.
        gain (float): System output scaling factor (default is 1.0 for unity gain).

    Returns:
        ndarray: The output response of the first-order system at each point in time.
    """
    return gain * (1.0 - np.exp(-t / tau))  # Exponential response for a first-order system

# Main function to compute and plot the first-order step responses
def main():
    """
    Simulates and visualizes the step responses of a first-order system for various time constants.
    Each time constant (\( \tau \)) is plotted to compare the speed of response across settings.
    """
    # Generate a time vector from 0 to 10 seconds, with 1000 evenly spaced points
    t = np.linspace(0, 10, 1000)

    # Loop through different time constants to explore their effects on the system's response
    for tau in [0.25, 0.5, 1.0, 2.0, 4.0]:  # Time constants in seconds
        plt.plot(t, first_order_step(t, tau), label=f"tau={tau}")  # Plot the step response for each tau

    # Plot reference lines for 63.2% response (1 time constant) and 95% response (approximately 3 time constants)
    plt.axhline(0.632, linestyle="--", color="gray", label="63.2% (1 time constant)")  # 63.2% line
    plt.axhline(0.95, linestyle=":", color="gray", label="95% (settling value)")  # 95% (nearly steady-state)

    # Add titles, labels, grid, and legend for better visualization
    plt.title("First-Order Step Response")  # Title for the plot
    plt.xlabel("Time [s]")  # Label for the x-axis (time in seconds)
    plt.ylabel("Output")  # Label for the y-axis (output value)
    plt.grid(True)  # Add gridlines for better readability
    plt.legend()  # Add a legend to identify each curve

    # Display the plot
    plt.show()

# Entry point: Run the script
if __name__ == "__main__":
    main()
