"""
Project: Disturbance Rejection Challenge
Purpose:
This script simulates the performance of a **PID (Proportional-Integral-Derivative) controller** in rejecting various types of disturbances while maintaining a target system state. The disturbances explored include:
- **Step force**: A sudden, constant force applied to the system.
- **Gust**: A time-limited burst of external force.
- **Sensor bias**: A constant offset in the feedback signal due to sensor error.

Key Concepts:
- **Disturbance Rejection**: The ability of a controller to handle external disruptions while maintaining system stability.
- **PID Control**: Ensures system stability and robustness by correcting deviations caused by disturbances.
- **Robustness Testing**: Evaluates how well the system handles different types of disruptions.

Applications:
- **Control Systems**: Engineering systems exposed to external forces, such as automotive, aerospace, and industrial control.
- **Robotics**: Maintaining precise position or speed control in robots subjected to disturbances.
- **Aerospace**: Controlling aircraft or UAVs under gust or wind disturbances.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization of system response

# PID Controller Class
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes a PID controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Minimum and maximum limits for the control signal.
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Output limits for the control signal
        self.integral = 0.0  # Integral accumulator
        self.prev_error = 0.0  # Previous error for derivative calculation

    def update(self, error, dt):
        """
        Updates the PID controller output based on the error and time step.

        Parameters:
            error (float): The difference between the target and current state.
            dt (float): The time step since the last update.

        Returns:
            float: Control output (e.g., force or throttle) clipped to the output limits.
        """
        # Update integral term
        self.integral += error * dt

        # Compute the derivative term
        derivative = (error - self.prev_error) / dt

        # Save the current error for the next step
        self.prev_error = error

        # Calculate the control output using PID formula
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Clamp the output within the specified limits
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Function to simulate the system response for a given disturbance case
def simulate(case):
    """
    Simulates the system's response to various disturbances using a PID controller.

    Parameters:
        case (str): The type of disturbance ("step_force", "gust", or "sensor_bias").

    Returns:
        tuple: Time vector and system output over time.
    """
    # Simulation parameters
    dt = 0.01  # Time step
    t = np.arange(0, 30, dt)  # Time vector (0 to 30 seconds)

    # Initial conditions
    x, v, target = 0.0, 0.0, 1.0  # Position, velocity, and target position

    # Create the PID controller
    pid = PID(4.0, 0.8, 2.5, output_limits=(-10, 10))  # PID gains and output limits

    # List to store system outputs
    xs = []

    # Simulation loop
    for time in t:
        # Initialize disturbance and sensor bias
        disturbance = 0.0
        bias = 0.0

        # Define disturbances based on the test case
        if case == "step_force" and time >= 10:
            disturbance = -1.5  # Constant external force starting at t=10s
        if case == "gust" and 10 <= time <= 14:
            disturbance = -4.0  # Time-limited gust force (10s to 14s)
        if case == "sensor_bias" and time >= 10:
            bias = 0.25  # Sensor bias introduced after t=10s

        # Update control signal using PID based on the error (input with bias)
        u = pid.update(target - (x + bias), dt)

        # Update velocity and position considering control input and disturbances
        v += (u + disturbance - 0.6 * v - x) * dt  # Update velocity
        x += v * dt  # Update position

        # Log the current position
        xs.append(x)

    return t, np.array(xs)  # Return the time vector and system output

# Main function to visualize the system's response under disturbances
def main():
    """
    Simulates three different types of disturbances and visualizes how the PID-controlled 
    system responds to maintain stability and reach the target state.
    """

    # Create the figure for plotting
    plt.figure()

    # Simulate the system for each disturbance case
    for case in ["step_force", "gust", "sensor_bias"]:
        t, x = simulate(case)  # Run simulation for the specified disturbance
        plt.plot(t, x, label=case)  # Plot the system response

    # Add reference lines and labels
    plt.axhline(1, linestyle="--", label="Target")  # Desired setpoint
    plt.title("Disturbance Rejection Challenge")  # Plot title
    plt.xlabel("Time [s]")  # Label for the x-axis
    plt.ylabel("Output")  # Label for the y-axis
    plt.grid(True)  # Add gridlines
    plt.legend()  # Add legend
    plt.show()

# Entry point: Run the disturbance simulation and visualization
if __name__ == "__main__":
    main()
