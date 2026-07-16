"""
Project: Waypoint Following Vehicle
Purpose:
This script demonstrates how to implement a **waypoint following algorithm** for a vehicle using multiple PID loops. The vehicle follows a sequence of waypoints by simultaneously controlling its speed and heading. This project explores:
- **Waypoint Navigation**: Tracking and transitioning between multiple waypoints.
- **Heading Control**: Adjusting the steering to align the vehicle's heading with the target waypoint.
- **Speed Control**: Regulating the speed of the vehicle based on a target speed.
- **PID Controllers**: Using tuned PID loops for heading and speed regulation.

Applications:
- **Autonomous Vehicles**: Path following for cars, drones, or robots.
- **Industrial Robotics**: Precision positioning and movement of automated guided vehicles (AGVs) along predefined paths.
- **Autonomous Maritime Systems**: Maritime navigation using waypoints for route planning.

Key Learning:
- The script introduces **multiple PID control loops** where one loop manages the heading (steering) and another adjusts speed, simulating complex control systems encountered in real-world scenarios.
"""

import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization of vehicle path and waypoints

# PID control class for heading and speed regulation
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes a PID controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Output limits (default: no limits).
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Clamps for the output value
        self.integral = 0.0  # Integral accumulator
        self.prev_error = 0.0  # Stores the previous error for derivative term calculation

    def update(self, error, dt):
        """
        Computes the control output based on the error using the PID algorithm.

        Parameters:
            error (float): The difference between the desired and actual value (setpoint - measurement).
            dt (float): Time step for integrating and differentiating.

        Returns:
            float: PID output (clamped within `output_limits`).
        """
        # Update the integral and derivative components
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        # Compute the PID control signal
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Clamp the control signal to the allowed range
        self.prev_error = error
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Function to wrap angles into the range [-π, π]
def wrap_angle(a):
    """
    Wraps an angle to the range [-π, π].

    Parameters:
        a (float): Angle in radians.

    Returns:
        float: Wrapped angle in radians.
    """
    return (a + np.pi) % (2 * np.pi) - np.pi

# Main function to execute waypoint following simulation
def main():
    """
    Simulates a vehicle navigating through a series of waypoints using PID loops for heading and speed control.
    Visualizes the vehicle's calculated path and its ability to track waypoints effectively.
    """

    # Simulation parameters
    dt = 0.05  # Time step (seconds)
    t = np.arange(0, 180, dt)  # Simulation runtime (0 to 180 seconds)

    # Define a series of waypoints the vehicle should follow
    waypoints = np.array([[0, 0], [30, 0], [30, 30], [0, 30], [0, 0]], dtype=float)  # Square path
    wp = 1  # Start by targeting the second waypoint

    # Vehicle's initial state
    x, y = 0.0, 0.0  # Initial position (m)
    heading, speed = 0.0, 0.0  # Initial heading (rad) and speed (m/s)
    wheelbase = 2.5  # Distance between front and rear axles (in meters)

    # Instantiate two PID controllers: one for heading and another for speed
    heading_pid = PID(2.5, 0.0, 0.4, output_limits=(-0.5, 0.5))  # Heading control PID
    speed_pid = PID(1.2, 0.2, 0.0, output_limits=(-2, 2))  # Speed control PID

    # Logs for vehicle path
    xs, ys = [], []  # Lists to store vehicle's position over time

    # Simulation loop
    for _ in t:
        # Target waypoint
        target = waypoints[wp]
        dx, dy = target[0] - x, target[1] - y

        # Check if the vehicle has reached the current waypoint
        if np.hypot(dx, dy) < 1.5 and wp < len(waypoints) - 1:
            wp += 1  # Move to the next waypoint
            target = waypoints[wp]
            dx, dy = target[0] - x, target[1] - y

        # Compute desired heading toward the target waypoint
        desired_heading = np.arctan2(dy, dx)

        # Compute control signals using PID controllers
        steering = heading_pid.update(wrap_angle(desired_heading - heading), dt)  # Steering control
        accel = speed_pid.update(5.0 - speed, dt)  # Speed control (target speed = 5.0 m/s)

        # Update the vehicle's speed and ensure it is non-negative
        speed = max(0, speed + accel * dt)

        # Update the heading using bicycle model steering dynamics (simplified)
        heading += (speed / wheelbase) * np.tan(steering) * dt

        # Update position using current speed and heading, with added noise for realism
        x += speed * np.cos(heading) * dt + 0.15 * dt  # Forward movement
        y += speed * np.sin(heading) * dt - 0.05 * dt  # Lateral deviation

        # Log current position
        xs.append(x)
        ys.append(y)

    # Visualization: Vehicle's path and waypoint tracking
    plt.figure()
    plt.plot(xs, ys, label="Path")  # Plot the vehicle's calculated path
    plt.scatter(waypoints[:, 0], waypoints[:, 1], marker="x", label="Waypoints")  # Mark waypoints
    plt.title("Waypoint Following Vehicle")  # Add title
    plt.xlabel("X [m]")  # Label for the x-axis
    plt.ylabel("Y [m]")  # Label for the y-axis
    plt.axis("equal")  # Ensure equal scaling for x and y axes
    plt.grid(True)  # Add gridlines for readability
    plt.legend()  # Add legend to differentiate path and waypoints
    plt.show()

# Entry point: Execute the waypoint following simulation
if __name__ == "__main__":
    main()
