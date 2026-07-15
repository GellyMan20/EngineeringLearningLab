"""
Project: PID Auto-Tuner  
Purpose:
This script designs and simulates a **PID (Proportional-Integral-Derivative) controller auto-tuner** using grid search and an objective scoring function. It automatically determines the optimal set of PID gains (\( K_p \), \( K_i \), \( K_d \)) that minimize the error between the desired and actual output while penalizing overshoot and control effort.

Key Concepts:
- **Automatic PID Tuning**: Finds suitable gains for a PID controller to achieve robust and efficient system performance.
- **Grid Search**: Iterates through combinations of PID gains within specified ranges to find the best-performing configuration.
- **Objective Function**: Quantifies control quality based on output error, overshoot, and control effort.
- **Simulation-Based Tuning**: Evaluates PID gains by simulating system dynamics for each gain set.

Applications:
- **Control Systems Optimization**: Eliminates the manual trial-and-error process for tuning PID controllers.
- **Robotics and Automation**: Translates to autonomous tuning of motor and actuator controllers.
- **Engineering Education**: Provides a practical demonstration of automated controller design.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For plotting simulation results

# Define the PID controller class
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes the PID controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Output limits for the control signal (default: unlimited).
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Clamp control output within defined limits
        self.integral = 0.0  # Accumulator for integral term
        self.prev_error = 0.0  # Tracks previous error for derivative calculation

    def update(self, error, dt):
        """
        Updates the PID control output based on the current error and time step.

        Parameters:
            error (float): The difference between target and actual system state.
            dt (float): Time step for integration and differentiation.

        Returns:
            float: Control output (clamped within output limits).
        """
        # Update integral term
        self.integral += error * dt

        # Compute derivative term
        derivative = (error - self.prev_error) / dt

        # Update previous error for the next step
        self.prev_error = error

        # Calculate PID output
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Clamp output within limits
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Function to simulate system performance for given PID gains
def simulate(kp, ki, kd, return_series=False):
    """
    Simulates the dynamics of a system controlled by PID under given gains.

    Parameters:
        kp (float): Proportional gain.
        ki (float): Integral gain.
        kd (float): Derivative gain.
        return_series (bool): If True, returns full time series data (default: False).

    Returns:
        score (float): Performance score based on objective function.
        t (ndarray): Time series (if `return_series` is True).
        xs (ndarray): Output values (if `return_series` is True).
        us (ndarray): Control signals (if `return_series` is True).
    """
    # Simulation parameters
    dt =
