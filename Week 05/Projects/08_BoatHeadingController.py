"""
Project: Boat Heading Controller
Purpose:
This script implements a **PID (Proportional-Integral-Derivative) controller** to regulate the heading of a boat. 
The controller adjusts the rudder angle to maintain a desired heading despite constant disturbances (e.g., wind or current). 
The simulation highlights how PID feedback can maintain stability and minimize heading errors.

Key Concepts:
- **Heading Control**: The control system ensures the boat aligns with the desired heading.
- **Integral Action**: Eliminates steady-state errors caused by constant disturbances.
- **Constant Disturbances**: Simulates real-world environmental forces acting on the boat.

Applications:
- **Marine Navigation**: Autonomous boats and vessels maintaining courses despite environmental disturbances.
- **Aerospace and Robotics**: Heading or yaw control for drones and ground vehicles.
- **Education**: Demonstrating PID control in practical, navigational tasks.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# PID controller class
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes the PID controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Minimum and maximum output limits for the rudder angle.
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Rudder angle limits
        self.integral = 0.0  # Integral accumulator
        self.prev_error = 0.0  # Stores the previous error for derivative calculation
