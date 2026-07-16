"""
Project 05 — Proportional Navigation Intercept
Purpose:
This script demonstrates the implementation of Proportional Navigation (PN) to intercept a moving target. The PN algorithm is a 
widely-used guidance law in missile systems and autonomous vehicles designed to achieve interception by adjusting the pursuer's 
heading based on the **line-of-sight (LOS) rate**, **closing velocity**, and **navigation constant (N)**. Concepts include:
- LOS rate calculation to track the target's angular velocity.
- Closing velocity computation to assess target approach rate.
- Adjusting the pursuer's turn rate based on the navigation constant to minimize the miss distance.
The simulation includes plotting the pursuer's path, the target's path, and visually confirming successful interception.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Function to wrap angles into the range [-π, π]
def wrap_angle(angle):
    """
    Wrap an angle to the range [-π, π].

    Parameters:
        angle (float): Angle in radians.

    Returns:
        float: Wrapped angle in radians.
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

# Main function to simulate proportional navigation
def main():
    """
    Simulates a pursuer attempting to intercept a moving target using the Proportional Navigation (PN) algorithm. 
    The pursuer adjusts its heading based on the line-of-sight rate, closing velocity, and a navigation constant. 
    Visualization includes the pursuer's path towards the target and the target's trajectory.
    """

    # Simulation time and timestep
    dt = 0.02  # Simulation time step (seconds)
    t = np.arange(0, 80, dt)  # Time vector

    # Initialize pursuer's state
    pursuer_pos = np.array([0.0, 0.0])  # Initial position of the pursuer (x, y)
    pursuer_heading = np.deg2rad(20)  # Initial heading of the pursuer in radians
    pursuer_speed = 12.0  # Constant speed of the pursuer in m/s

    # Initialize target's state
    target_pos = np.array([120.0, 40.0])  # Initial position of the target (x, y)
    target_vel = np.array([-2.0, 1.0])  # Constant velocity of the target in m/s (x, y)

    # Proportional navigation parameters
    N = 3.0  # Navigation constant
    max_turn_rate = np.deg2rad(60)  # Maximum allowable turn rate (in radians per second)

    # Logs for the pursuer's and target's paths
    pursuer_path, target_path = [], []

    # Previous LOS angle (None initially)
    prev_los = None

    # Simulation loop
    for _ in t:
        # Compute relative position and range to the target
        rel_pos = target_pos - pursuer_pos  # Vector from pursuer to target
        rng = np.linalg.norm(rel_pos)  # Distance (range) to the target

        # Check if the pursuer is close enough to the target (interception success)
        if rng < 1.0:
            print('Intercept achieved.')
            break

        # Calculate the current LOS angle
        los = np.arctan2(rel_pos[1], rel_pos[0])

        # Compute the LOS rate (rate of change of LOS angle)
        los_rate = 0.0 if prev_los is None else wrap_angle(los - prev_los) / dt
        prev_los = los  # Update the previous LOS angle

        # Compute the velocity of the pursuer
        pursuer_vel = pursuer_speed * np.array([np.cos(pursuer_heading), np.sin(pursuer_heading)])

        # Compute the relative velocity (target velocity - pursuer velocity)
        rel_vel = target_vel - pursuer_vel

        # Calculate the closing velocity (rate of range reduction)
        closing_velocity = -np.dot(rel_pos, rel_vel) / rng

        # Calculate the turn rate using the Proportional Navigation law
        turn_rate = np.clip(N * closing_velocity * los_rate / pursuer_speed, -max_turn_rate, max_turn_rate)

        # Update the pursuer's heading based on the turn rate
        pursuer_heading = wrap_angle(pursuer_heading + turn_rate * dt)

        # Update the pursuer's position
        pursuer_pos += pursuer_speed * np.array([np.cos(pursuer_heading), np.sin(pursuer_heading)]) * dt

        # Update the target's position
        target_pos += target_vel * dt

        # Log the paths of both the pursuer and the target
        pursuer_path.append(pursuer_pos.copy())
        target_path.append(target_pos.copy())

    # Convert the logged paths to numpy arrays for plotting
    pursuer_path = np.array(pursuer_path)
    target_path = np.array(target_path)

    # Visualization: Plot the paths of both the pursuer and the target
    plt.figure()
    plt.plot(pursuer_path[:, 0], pursuer_path[:, 1], label='Pursuer')  # Plot pursuer's path
    plt.plot(target_path[:, 0], target_path[:, 1], label='Target')  # Plot target's path
    plt.title('Proportional Navigation Intercept')  # Add title
    plt.xlabel('X [m]')  # X-axis label
    plt.ylabel('Y [m]')  # Y-axis label
    plt.axis('equal')  # Set equal scaling for x and y axes
    plt.grid(True)  # Add a grid for clarity
    plt.legend()  # Add a legend
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
