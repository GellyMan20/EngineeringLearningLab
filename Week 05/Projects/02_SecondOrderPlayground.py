"""
Project: Second-Order System Playground
Purpose:
This script simulates the step response of a **second-order system**, often used to model the dynamics of systems like springs, oscillators, and robotic actuators. It explores how the **damping ratio** (\( \zeta \)), **natural frequency** (\( \omega_n \)), and overshoot affect system behavior, providing insights into system stability and performance.

Key Concepts:
- **Damping Ratio** (\( \zeta \)): Determines whether the system is underdamped, critically damped, or overdamped.
- **Natural Frequency** (\( \omega_n \)): Defines the frequency of oscillation for the system without damping.
- **Overshoot**: Measures how much the system overshoots its steady-state value before settling.

Applications:
Second-order systems are common in engineering and robotics, with applications in:
- Spring-mass-damper systems.
- Electrical circuits (e.g., RLC circuits).
- Control systems, such as PID controller design.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization of the system's response

# Function to simulate the step response of a second-order system
def simulate_second_order(zeta, omega_n, t_end=10.0, dt=0.001):
    """
    Simulates the step response of a second-order system.

    Parameters:
        zeta (float): The damping ratio (\( \zeta \)), which determines the system's damping behavior.
        omega_n (float): The natural frequency (\( \omega_n \)) in rad/s.
        t_end (float): Simulation time duration in seconds (default: 10s).
        dt (float): Simulation time step in seconds (default: 0.001s).

    Returns:
        t (ndarray): Time vector of the simulation.
        x (ndarray): System response over time (output of the system).
    """
    # Generate the time vector
    t = np.arange(0, t_end, dt)

    # Initialize output (x) and derivative (v) variables
    x = np.zeros_like(t)  # Position or output of the system
    v = np.zeros_like(t)  # Velocity of the system

    # Input step value (reference)
    r = 1.0

    # Simulate the system using Euler's method
    for k in range(1, len(t)):
        a = omega_n**2 * (r - x[k - 1]) - 2 * zeta * omega_n * v[k - 1]  # Acceleration
        v[k] = v[k - 1] + a * dt  # Update velocity
        x[k] = x[k - 1] + v[k] * dt  # Update position (output)

    return t, x

# Main function to visualize the second-order step response
def main():
    """
    Visualizes the step response of second-order systems for various damping ratios (\( \zeta \)).
    Shows how different damping characteristics affect system behavior.
    """
    # Simulate a second-order step response for various damping ratios
    for zeta in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]:  # Range of damping ratios
        t, y = simulate_second_order(zeta, omega_n=2.0)  # Use a natural frequency of 2 rad/s
        plt.plot(t, y, label=f"zeta={zeta}")  # Plot the response for each damping ratio

    # Add reference lines and annotations
    plt.axhline(1.0, linestyle="--", label="Command")  # Reference line for steady-state value
    plt.title("Second-Order Step Response")  # Add plot title
    plt.xlabel("Time [s]")  # Label for the x-axis
    plt.ylabel("Output")  # Label for the y-axis
    plt.grid(True)  # Add gridlines for clarity
    plt.legend()  # Add legend to identify damping ratios
    plt.show()  # Display the plot

# Entry point: Run the visualization
if __name__ == "__main__":
    main()
