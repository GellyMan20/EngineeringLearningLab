"""
Project 06 — Dubins Path Generator
Purpose:
This script demonstrates the approximation of generating a Dubins-style path, which is a type of 
path planning method for vehicles with a constrained turning radius. The primary objective is to 
educate users on the concepts of minimum turning radius and heading-constrained path planning.
This implementation provides an approximate solution and is not a full Dubins solver.

Concepts learned:
- Constrained turning radius for vehicles.
- Heading-constrained maneuvers.
- Approximation of Dubins paths using arc-line-arc maneuvers.
- Path planning for vehicles like airplanes and ground vehicles with limited maneuverability.

The output visualizes the vehicle's path as it moves between a starting pose and a goal pose under 
turning constraints.
"""

# Import necessary libraries
import numpy as np  # For numerical operations
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

# Function to simulate an approximate Dubins-style path using arc-line-arc segments
def simulate_arc_line_arc(start, goal, turn_radius=8.0, ds=0.2):
    """
    Simulates an approximate Dubins-style path from a start pose to a goal pose. The 
    generated path consists of arc and line segments that respect the vehicle's 
    minimum turning radius.

    Parameters:
        start (tuple): The starting pose (x, y, heading) in meters and radians.
        goal (tuple): The goal pose (x, y, heading) in meters and radians.
        turn_radius (float): Minimum turning radius of the vehicle in meters.
        ds (float): Step size for simulation in meters.

    Returns:
        xs (ndarray): X-coordinates of the path.
        ys (ndarray): Y-coordinates of the path.
    """
    x, y, heading = start  # Starting pose of the vehicle
    gx, gy, gheading = goal  # Goal pose of the vehicle (position and heading)
    xs, ys = [x], [y]  # Initialize path with starting point
    goal_line_heading = np.arctan2(gy - y, gx - x)  # Heading direction to the goal

    # Phase 1: Turn towards the direct line to the goal
    for _ in range(400):
        err = wrap_angle(goal_line_heading - heading)  # Heading error
        if abs(err) < np.deg2rad(2):  # Stop turning if heading error is small
            break
        heading = wrap_angle(heading + np.sign(err) * ds / turn_radius)  # Turn towards the goal
        x += ds * np.cos(heading)  # Move forward in x-direction
        y += ds * np.sin(heading)  # Move forward in y-direction
        xs.append(x)
        ys.append(y)

    # Phase 2: Travel along a straight line towards the goal
    for _ in range(1000):
        dx, dy = gx - x, gy - y  # Difference between current position and goal
        if np.hypot(dx, dy) < turn_radius:  # Stop when close to goal turning radius
            break
        heading = np.arctan2(dy, dx)  # Point directly towards the goal along a straight line
        x += ds * np.cos(heading)  # Move forward in x-direction
        y += ds * np.sin(heading)  # Move forward in y-direction
        xs.append(x)
        ys.append(y)

    # Phase 3: Adjust heading to align with the goal's target heading
    for _ in range(500):
        err = wrap_angle(gheading - heading)  # Error between current and desired heading
        if abs(err) < np.deg2rad(2) and np.hypot(gx - x, gy - y) < 2.0:  # Stop if orientation and distance are within tolerance
            break
        turn = np.sign(err) if abs(err) > np.deg2rad(2) else 0  # Determine turn direction
        heading = wrap_angle(heading + turn * ds / turn_radius)  # Adjust heading
        desired = np.arctan2(gy - y, gx - x)  # Desired direction toward the target
        heading = wrap_angle(0.85 * heading + 0.15 * desired)  # Blend current and desired heading
        x += ds * np.cos(heading)  # Move forward in x-direction
        y += ds * np.sin(heading)  # Move forward in y-direction
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)  # Return the path coordinates

# Main function for running the Dubins path generator
def main():
    """
    Simulates a vehicle moving from a starting pose to a goal pose while respecting 
    a minimum turning radius. The path is generated using an arc-line-arc strategy 
    and visualized through a 2D path plot.
    """

    # Define the start and goal poses (x, y, heading in radians)
    start = (0.0, 0.0, np.deg2rad(0))  # Starting pose
    goal = (60.0, 35.0, np.deg2rad(90))  # Goal pose

    # Generate the approximate Dubins-style path
    xs, ys = simulate_arc_line_arc(start, goal)

    # Visualization: Plot the generated path and start/goal points
    plt.figure()
    plt.plot(xs, ys, label='Approximate Dubins-style path')  # Plot the path
    plt.scatter([start[0], goal[0]], [start[1], goal[1]], marker='x', label='Start / Goal')  # Mark start/goal points
    plt.title('Dubins Path Generator — Teaching Approximation')  # Add title
    plt.xlabel('X [m]')  # X-axis label
    plt.ylabel('Y [m]')  # Y-axis label
    plt.axis('equal')  # Equal scaling for x and y axes
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add legend
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
