"""
Project: Inverted Pendulum
Purpose:
This script simulates the stabilization of an **inverted pendulum**, a classic control systems problem. It demonstrates the dynamics of an unstable system and the use of proportional-derivative (PD) feedback control to stabilize it. The goal is to stabilize the pendulum in an upright position by applying a correction torque.

Key Concepts:
- **Unstable Systems**: The inverted pendulum is inherently unstable and tends to fall without control.
- **Stabilizing Feedback**: Uses a proportional-derivative (PD) controller to apply corrective torque.
- **Control Theory**: Tests how proportional and derivative gains affect stability and response.

Applications:
- **Robotics**: Balancing robots such as self-balancing two-wheelers or humanoid robots.
- **Aerospace Systems**: Stability control of rockets and spacecraft.
- **Control Systems Education**: Demonstrating feedback-based stabilization of unstable dynamics.
"""

# Import necessary libraries
import numpy as np  # For numerical calculations
import matplotlib.pyplot as plt  # For plotting and visualization

# Main function to simulate and visualize the inverted pendulum stabilization
def main():
    """
    Simulates the stabilization of an inverted pendulum using a PD controller. 
    Visualizes the pendulum's angular response and control effort over time.
    """

    # Simulation parameters
    dt = 0.001  # Time step (seconds)
    t = np.arange(0, 10, dt)  # Simulation time (0 to 10 seconds)

    # Inverted pendulum parameters
    g = 9.81  # Gravitational acceleration (m/s²)
    length = 1.0  # Length of the pendulum (meters)
    theta, theta_dot = np.deg2rad(8), 0.0  # Initial angular displacement and velocity (in radians)

    # PD controller gains
    kp = 45.0  # Proportional gain
    kd = 10.0  # Derivative gain

    # Logs for visualization
    angles = []  # Log of angular displacement (converted to degrees)
    controls = []  # Log of control inputs (torque)

    # Simulation loop
    for _ in t:
        # Compute control input using a PD controller
        u = np.clip(-kp * theta - kd * theta_dot, -80, 80)  # Torque command (limited between -80 and 80)

        # Update angular velocity and angle using the differential equation of motion
        theta_dot += ((g / length) * theta + u) * dt  # Angular velocity update
        theta += theta_dot * dt  # Angular displacement update

        # Log data for plotting
        angles.append(np.rad2deg(theta))  # Convert angle to degrees for visualization
        controls.append(u)  # Log the control input

    # Visualization: Angular response over time
    plt.figure()
    plt.plot(t, angles, label="Angle [deg]")  # Plot the pendulum's angular response
    plt.axhline(0, linestyle="--", color="gray", label="Upright Position")  # Reference for upright position
    plt.title("Inverted Pendulum Stabilization")  # Add title
    plt.xlabel("Time [s]")  # Label for the x-axis
    plt.ylabel("Angle from upright [deg]")  # Label for the y-axis
    plt.grid(True)  # Add grid for better visualization
    plt.legend()  # Add legend to identify the plots
    plt.show()

# Entry point: Run the inverted pendulum simulation
if __name__ == "__main__":
    main()
