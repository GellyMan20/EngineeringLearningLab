"""
Project: Mass-Spring-Damper Simulator
Purpose:
This script simulates the dynamics of a **mass-spring-damper system**, which is a classic second-order system. The primary objective is to explore:
- **Second-order dynamics**, such as oscillations in physical systems like a mass attached to a spring with damping.
- **Damping effects**: Understanding underdamped, critically damped, and overdamped conditions.
- **Free response behavior**, illustrating how the system evolves over time without external forces.

Key Concepts:
- Models the physical dynamics of real-world systems (e.g., car suspensions, building oscillations, robotic actuators, etc.).
- Demonstrates how damping affects oscillatory behavior and energy dissipation.
- Visualizes the step response for different damping coefficients.

Applications:
- **Understanding dynamics**: Modeling oscillatory systems in physics and engineering.
- **Control systems**: Provides insights for designing stable systems in robotics, mechanical, and aerospace engineering.
- **Vibration analysis**: Helps analyze vibration in mechanical and structural systems.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Function to simulate the behavior of a mass-spring-damper system
def simulate(m, c, k, x0, v0, t_end=10, dt=0.001):
    """
    Simulates the free response of a mass-spring-damper system.

    Parameters:
        m (float): Mass (kg).
        c (float): Damping coefficient (N·s/m).
        k (float): Spring constant or stiffness (N/m).
        x0 (float): Initial position (m).
        v0 (float): Initial velocity (m/s).
        t_end (float): Total simulation time (seconds).
        dt (float): Time step for integration (seconds).

    Returns:
        t (ndarray): Array of simulation time points (seconds).
        x (ndarray): Array of positions of the mass over time (meters).
    """
    # Create a time vector from 0 to t_end
    t = np.arange(0, t_end, dt)

    # Initialize arrays for position (x) and velocity (v)
    x = np.zeros_like(t)  # Position array
    v = np.zeros_like(t)  # Velocity array

    # Set initial conditions
    x[0], v[0] = x0, v0

    # Time-stepping loop to compute position and velocity using numerical integration
    for i in range(1, len(t)):
        # Compute acceleration using the second-order ODE for a mass-spring-damper system
        a = -(c / m) * v[i - 1] - (k / m) * x[i - 1]  # Acceleration = -(c/m)v - (k/m)x

        # Update velocity using Euler's method
        v[i] = v[i - 1] + a * dt

        # Update position using Euler's method
        x[i] = x[i - 1] + v[i] * dt

    # Return the time vector and the position over time
    return t, x

# Main function to visualize the mass-spring-damper system's response
def main():
    """
    Simulates and visualizes the free response of a mass-spring-damper system 
    for various damping coefficients (\( c \)). Highlights the effect of damping 
    on the system's oscillations and settling time.
    """

    # Simulate and plot responses for different damping coefficients
    for c in [0.0, 0.5, 2.0, 6.5]:  # Damping coefficients to test
        t, x = simulate(m=1.0, c=c, k=10.0, x0=1.0, v0=0.0)  # Use a unit mass and spring constant of 10 N/m
        plt.plot(t, x, label=f"c={c}")  # Plot position against time for each damping coefficient

    # Add titles, labels, grid, and legend for visualization
    plt.title("Mass-Spring-Damper Free Response")  # Title of the plot
    plt.xlabel("Time [s]")  # Label for the x-axis (time in seconds)
    plt.ylabel("Position [m]")  # Label for the y-axis (position in meters)
    plt.grid(True)  # Add gridlines for easier reading
    plt.legend()  # Add legend to distinguish damping scenarios
    plt.show()  # Display the plot

# Entry point: Execute the simulation
if __name__ == "__main__":
    main()
