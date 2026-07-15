"""
Project 03 — Pure Pursuit Path Follower
Purpose:
This script demonstrates the implementation of a Pure Pursuit path-following algorithm. The Pure Pursuit method 
is a geometric path-following algorithm that computes steering commands to guide a vehicle toward a desired 
trajectory by finding and steering toward a "lookahead point." The key concepts introduced in this project include:
- Calculating the lookahead point.
- Generating curvature commands for smooth path tracking.
- Executing smooth and reactive path-following using proportional control.

The script simulates the vehicle's trajectory along a pre-defined path and visualizes the tracking performance 
with respect to the desired path. The steering angle commands are also visualized over time.
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

# Function to compute the lookahead point along a path
def find_lookahead_point(path, position, lookahead_distance):
    """
    Finds the lookahead point on a path that is at least `lookahead_distance` away 
    from the current position.

    Parameters:
        path (ndarray): Array of 2D points representing the desired path.
        position (ndarray): Current position of the vehicle [x, y].
        lookahead_distance (float): Distance ahead of the vehicle to find the lookahead point.

    Returns:
        lookahead (ndarray): The lookahead point [x, y].
        index (int): The index of the lookahead point in the path array.
    """
    # Compute distances from the vehicle to all points in the path
    distances = np.linalg.norm(path - position, axis=1)

    # Find the first point that is at least `lookahead_distance` away
    candidates = np.where(distances >= lookahead_distance)[0]
    if len(candidates) == 0:  # If no such point exists, return the last point of the path
        return path[-1], len(path) - 1
    return path[candidates[0]], candidates[0]

# Main function to simulate the Pure Pursuit path-following algorithm
def main():
    """
    Simulates a vehicle tracking a sinusoidal path using the Pure Pursuit algorithm.
    The key outputs are the vehicle's path and the steering angle commands over time,
    both of which are visualized at the end of the simulation.
    """

    # Simulation parameters
    dt = 0.05  # Simulation time step (seconds)
    t = np.arange(0, 120, dt)  # Time vector

    # Define the desired path (sinusoidal curve)
    path_x = np.linspace(0, 100, 500)  # X-coordinates of the path
    path_y = 10 * np.sin(path_x / 12)  # Y-coordinates (sinusoidal shape)
    path = np.column_stack((path_x, path_y))  # Combine x and y into a path array

    # Vehicle initial state
    x, y = 0.0, -8.0  # Start position
    heading = 0.0  # Initial heading in radians
    speed = 4.0  # Constant vehicle speed in m/s
    wheelbase = 2.5  # Distance between front and rear axles (m)
    lookahead_distance = 8.0  # Fixed lookahead distance for path following

    # Logs for visualization
    xs, ys = [], []  # Logs for the vehicle's path
    steer = []  # Logs for steering angle commands

    # Simulation loop
    for _ in t:
        # Find the lookahead point
        lookahead, idx = find_lookahead_point(path, np.array([x, y]), lookahead_distance)

        # Compute the angle to the lookahead point relative to the vehicle's heading
        alpha = wrap_angle(np.arctan2(lookahead[1] - y, lookahead[0] - x) - heading)

        # Compute the curvature based on the lookahead point
        curvature = 2 * np.sin(alpha) / lookahead_distance

        # Calculate the steering angle from curvature
        steering = np.clip(np.arctan(wheelbase * curvature), np.deg2rad(-35), np.deg2rad(35))

        # Update the heading and position based on the steering
        heading = wrap_angle(heading + (speed / wheelbase) * np.tan(steering) * dt)
        x += speed * np.cos(heading) * dt  # Update x-position
        y += speed * np.sin(heading) * dt  # Update y-position

        # Log data for plotting
        xs.append(x)
        ys.append(y)
        steer.append(np.rad2deg(steering))  # Store steering angle in degrees for plotting

        # Stop the loop if near the end of the path
        if idx >= len(path) - 2:
            break

    # Visualization: Vehicle path and desired path
    plt.figure()
    plt.plot(path[:, 0], path[:, 1], '--', label='Desired path')  # Plot the desired path
    plt.plot(xs, ys, label='Vehicle path')  # Plot the actual vehicle path
    plt.title('Pure Pursuit Path Follower')  # Add title
    plt.xlabel('X [m]')  # X-axis label
    plt.ylabel('Y [m]')  # Y-axis label
    plt.axis('equal')  # Equal scaling for X and Y axes
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add legend
    plt.show()

    # Visualization: Steering Command over time
    plt.figure()
    plt.plot(steer)  # Plot steering commands
    plt.title('Steering Command')  # Add title
    plt.xlabel('Step')  # X-axis label
    plt.ylabel('Steering [deg]')  # Y-axis label
    plt.grid(True)  # Add grid for clarity
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
