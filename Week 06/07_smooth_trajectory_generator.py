"""
Project 07 — Smooth Trajectory Generator
Purpose:
This script demonstrates how to generate a smooth trajectory for a moving object in 2D space using a fifth-order 
polynomial smoothstep function. The smoothstep function ensures that the generated position, velocity, 
and acceleration profiles are continuous and smooth (differentiable). This is crucial for applications involving 
autonomous systems, robotics, and motion planning, where sudden changes in velocity or acceleration can cause 
instabilities or inefficiencies.

Key concepts:
- Smooth trajectory generation using a fifth-order polynomial (smoothstep).
- Creating position, velocity, and acceleration profiles.
- Plotting 2D trajectories, speed profiles, and acceleration magnitudes for visualization.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Function to generate a smooth trajectory using a fifth-order smoothstep
def smoothstep_trajectory(p0, pf, duration, dt):
    """
    Generates a smooth 2D trajectory using a fifth-order smoothstep function.

    Parameters:
        p0 (ndarray): Initial position [x, y].
        pf (ndarray): Final position [x, y].
        duration (float): Time to complete the trajectory in seconds.
        dt (float): Time step in seconds.

    Returns:
        t (ndarray): Time vector.
        pos (ndarray): Positions [N x 2] along the trajectory.
        vel (ndarray): Velocities [N x 2] along the trajectory.
        acc (ndarray): Accelerations [N x 2] along the trajectory.
    """
    # Generate time vector
    t = np.arange(0, duration + dt, dt)  # Time array from 0 to duration with increments of dt

    # Normalize time variable between [0, 1]
    a = t / duration

    # Fifth-order smoothstep function for position profile
    s = 10 * a**3 - 15 * a**4 + 6 * a**5  # Smooth transition factor (position profile)
    
    # Derivatives of the smoothstep function
    ds = 30 * a**2 - 60 * a**3 + 30 * a**4  # Velocity profile (scaled by final position and duration)
    d2s = 60 * a - 180 * a**2 + 120 * a**3  # Acceleration profile (scaled by final position and duration)

    # Compute position, velocity, and acceleration in 2D space
    pos = p0 + (pf - p0) * s[:, None]  # Interpolated position
    vel = (pf - p0) * ds[:, None] / duration  # Velocity in m/s
    acc = (pf - p0) * d2s[:, None] / duration**2  # Acceleration in m/s²

    return t, pos, vel, acc

# Main function to simulate and visualize the smooth trajectory
def main():
    """
    Simulates and visualizes a 2D trajectory generated using a fifth-order smoothstep.
    Key plots include:
    - The smooth 2D trajectory.
    - Speed profile over time.
    - Acceleration magnitude over time.
    """

    # Define the starting and final positions in 2D space
    p0 = np.array([0.0, 0.0])  # Start position [x, y]
    pf = np.array([50.0, 30.0])  # End position [x, y]

    # Generate the trajectory
    t, pos, vel, acc = smoothstep_trajectory(p0, pf, 12.0, 0.02)  # Duration: 12.0s, Time step: 0.02s

    # Visualization: Smooth 2D Trajectory
    plt.figure()
    plt.plot(pos[:, 0], pos[:, 1], label='Trajectory')  # Plot the trajectory in 2D
    plt.scatter([p0[0], pf[0]], [p0[1], pf[1]], marker='x', label='Start/End Points')  # Mark start and end points
    plt.title('Smooth 2D Trajectory')  # Add title
    plt.xlabel('X [m]')  # X-axis label
    plt.ylabel('Y [m]')  # Y-axis label
    plt.axis('equal')  # Set equal scaling for x and y axes
    plt.grid(True)  # Add grid
    plt.legend()  # Add legend
    plt.show()

    # Visualization: Speed Profile
    plt.figure()
    plt.plot(t, np.linalg.norm(vel, axis=1))  # Plot speed (magnitude of velocity)
    plt.title('Speed Profile')  # Add title
    plt.xlabel('Time [s]')  # X-axis label
    plt.ylabel('Speed [m/s]')  # Y-axis label
    plt.grid(True)  # Add grid for clarity
    plt.show()

    # Visualization: Acceleration Magnitude
    plt.figure()
    plt.plot(t, np.linalg.norm(acc, axis=1))  # Plot acceleration magnitude
    plt.title('Acceleration Magnitude')  # Add title
    plt.xlabel('Time [s]')  # X-axis label
    plt.ylabel('Acceleration [m/s²]')  # Y-axis label
    plt.grid(True)  # Add grid
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
