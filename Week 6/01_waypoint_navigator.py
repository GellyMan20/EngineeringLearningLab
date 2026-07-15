# Project 01 — Waypoint Navigator
# Purpose:
# This script simulates a basic waypoint navigator for a vehicle. The goal is for the vehicle to 
# follow a sequence of waypoints using simple heading control. The vehicle adjusts its heading 
# towards a target waypoint based on its current position and orientation. Key concepts include:
# - Waypoint navigation
# - Desired heading calculation
# - Distance-to-go computation
# - Simple heading control using proportional gain and turn-rate limits
# The performance of the navigation is visualized through the vehicle's path and the distance 
# to the current waypoint.

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
        float: Angle wrapped to [-π, π].
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

# Main function for waypoint navigation simulation
def main():
    """
    Simulates a vehicle navigating through a set of waypoints using simple proportional 
    heading control. The vehicle adjusts its turn rate based on the heading error to stay on 
    course towards each waypoint.

    The simulation results are visualized, showing the vehicle's path and the distance to the 
    next waypoint over time.
    """

    # Simulation parameters
    dt = 0.05  # Simulation time step (seconds)
    t = np.arange(0, 140, dt)  # Time vector

    # Define waypoints (2D positions for the vehicle to reach)
    waypoints = np.array([[0, 0], [30, 0], [45, 25], [20, 45], [0, 20]], dtype=float)

    # Initialize vehicle state
    x, y = waypoints[0]  # Initial position at the first waypoint
    heading = np.deg2rad(20)  # Initial heading in radians (20 degrees)
    speed = 3.0  # Constant vehicle speed in m/s
    waypoint_index = 1  # Start navigating to the second waypoint
    heading_gain = 2.0  # Proportional gain for heading adjustment
    max_turn_rate = np.deg2rad(45)  # Maximum turn rate in radians/second

    # Logs for path and distance to waypoints
    xs, ys, dists = [], [], []

    # Simulation loop
    for _ in t:
        # Get the target waypoint coordinates
        target = waypoints[waypoint_index]
        dx, dy = target[0] - x, target[1] - y  # Compute relative x, y distances
        distance = np.hypot(dx, dy)  # Compute Euclidean distance to the target

        # Check if the vehicle has reached the current waypoint
        if distance < 1.0 and waypoint_index < len(waypoints) - 1:
            waypoint_index += 1  # Move to the next waypoint
            target = waypoints[waypoint_index]  # Update target waypoint
            dx, dy = target[0] - x, target[1] - y  # Re-compute distances
            distance = np.hypot(dx, dy)

        # Compute desired heading to the target waypoint
        desired_heading = np.arctan2(dy, dx)

        # Compute the heading error between the current and desired heading
        heading_error = wrap_angle(desired_heading - heading)

        # Calculate turn rate using proportional control with limits
        turn_rate = np.clip(heading_gain * heading_error, -max_turn_rate, max_turn_rate)

        # Update the vehicle's heading by applying the turn rate
        heading = wrap_angle(heading + turn_rate * dt)

        # Update the vehicle's position based on the new heading
        x += speed * np.cos(heading) * dt  # Update x-position
        y += speed * np.sin(heading) * dt  # Update y-position

        # Log the vehicle's position and distance to the current waypoint
        xs.append(x)
        ys.append(y)
        dists.append(distance)

        # Break the loop if the last waypoint is reached
        if waypoint_index == len(waypoints) - 1 and distance < 1.0:
            break

    # Visualization: Plot the vehicle's path and the waypoints
    plt.figure()
    plt.plot(xs, ys, label='Vehicle path')  # Plot the path of the vehicle
    plt.scatter(waypoints[:, 0], waypoints[:, 1], marker='x', label='Waypoints')  # Mark the waypoints
    plt.title('Waypoint Navigator')
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.axis('equal')  # Ensure equal scaling of x and y axes
    plt.grid(True)
    plt.legend()  # Add a legend
    plt.show()

    # Visualization: Plot distance to the current waypoint over time
    plt.figure()
    plt.plot(dists)
    plt.title('Distance to Current Waypoint')
    plt.xlabel('Step')
    plt.ylabel('Distance [m]')
    plt.grid(True)
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
