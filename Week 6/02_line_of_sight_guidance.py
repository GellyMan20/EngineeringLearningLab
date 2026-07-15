"""
Project 02 — Line-of-Sight Guidance Simulator
Purpose:
This script demonstrates a Line-of-Sight (LOS) guidance simulator that models how a vehicle navigates 
towards a target point using proportional heading control. The goal is to learn key concepts such as:
- LOS angle computation.
- Heading command generation based on LOS angle error.
- The distinction between a guidance law (path planning) and a control law (path execution).
The performance of the navigation is evaluated, and results are visualized using the vehicle's path 
and heading error over time.
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
        float: Angle wrapped to [-π, π].
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

# Main function to simulate line-of-sight guidance
def main():
    """
    Simulates a vehicle navigating toward a target using Line-of-Sight (LOS) guidance, 
    a key guidance algorithm where the vehicle turns to reduce the angular error 
    between its current heading and the LOS angle to the target.

    Visualization includes:
    1. The vehicle's path toward the target.
    2. The heading error over time.
    """

    # Simulation parameters
    dt = 0.05  # Simulation time step (seconds)
    t = np.arange(0, 80, dt)  # Time vector

    # Vehicle initial conditions
    x, y = 0.0, -20.0  # Initial position (x, y)
    heading = np.deg2rad(30)  # Initial heading in radians (30 degrees)
    speed = 4.0  # Constant vehicle speed (m/s)

    # Define target position
    target = np.array([60.0, 20.0])  # Target coordinates

    # Control parameters
    heading_gain = 1.8  # Proportional gain for heading control
    max_turn_rate = np.deg2rad(35)  # Maximum turn rate (in radians/second)

    # Lists for plotting results
    xs, ys = [], []  # Logs for the vehicle's path
    heading_errors = []  # Logs for heading error over time

    # Simulation loop
    for _ in t:
        # Compute the vector to the target
        dx, dy = target[0] - x, target[1] - y
        rng = np.hypot(dx, dy)  # Range (distance) to the target

        # Calculate the line-of-sight (LOS) angle
        los_angle = np.arctan2(dy, dx)

        # Compute heading error between current heading and LOS angle
        err = wrap_angle(los_angle - heading)

        # Compute the turn rate using proportional control
        turn_rate = np.clip(heading_gain * err, -max_turn_rate, max_turn_rate)

        # Update heading based on turn rate
        heading = wrap_angle(heading + turn_rate * dt)

        # Update position using the updated heading
        x += speed * np.cos(heading) * dt  # Update x-position
        y += speed * np.sin(heading) * dt  # Update y-position

        # Log data for plotting
        xs.append(x)
        ys.append(y)
        heading_errors.append(np.rad2deg(err))  # Log the heading error (in degrees)

        # Stop the loop if the vehicle reaches the target
        if rng < 1.0:  # Check if the vehicle is within 1
