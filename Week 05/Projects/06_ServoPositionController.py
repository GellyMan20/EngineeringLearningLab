"""
Project: Servo Position Controller
Purpose:
This script demonstrates the use of a **PID (Proportional-Integral-Derivative) controller** for servo position control. 
The servo aims to align with a desired target angle while dealing with overshoot and damping. 
Key concepts include the role of proportional, integral, and derivative gains in controlling position, 
minimizing overshoot, and achieving a short settling time.

Key Concepts:
- **Overshoot**: The amount by which the output exceeds the target value before settling.
- **Settling Time**: Time taken for the output to stabilize within a certain percentage (e.g., 5%) of the target.
- **Proportional-Derivative (PD)/PID Position Control**: Combines immediate error correction and damping of oscillations.

Applications:
- **Robotics**: Servo motor control for precise position tasks.
- **Industrial Applications**: Accurate positioning of actuators.
- **Aerospace**: Stabilizing control surfaces like flaps or rudders in aircraft or drones.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Define a PID controller class
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes the PID controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Minimum and maximum output limits for the control signal.
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Output limits (e.g., for actuator saturation)
        self.integral = 0.0  # Integral accumulator
        self.prev_error = 0.0  # Previous error for computing derivative term

    def update(self, error, dt):
        """
        Updates the PID controller output for the given error.

        Parameters:
            error (float): Difference between the target and current value.
            dt (float): Time step since last update.

        Returns:
            float: The calculated control signal, limited by output limits.
        """
        # Update the integral term
        self.integral += error * dt

        # Compute the derivative term
        derivative = (error - self.prev_error) / dt

        # Save current error for the next update
        self.prev_error = error

        # Compute PID output
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Limit the output signal to specified bounds
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Main function to simulate servo position control
def main():
    """
    Simulates a PID-controlled servo system to track a target angle. Evaluates:
    - System overshoot
    - Settling time
    - The effect of PID gains on the response
    """

    # Simulation parameters
    dt = 0.001  # Time step (seconds)
    t = np.arange(0, 5, dt)  # Simulation duration: 5 seconds

    # System parameters
    inertia = 0.04  # Rotational inertia [kg·m²]
    damping = 0.03  # Damping coefficient [N·m/(rad/s)]

    # Initial conditions
    target = np.deg2rad(90)  # Desired servo angle in radians (90 degrees)
    angle = 0.0  # Initial servo angle in radians
    rate = 0.0  # Initial angular velocity in radians per second

    # Configure PID controller
    pid = PID(kp=12.0, ki=0.0, kd=1.2, output_limits=(-10, 10))  # Tuning PID for position control

    # Logs for visualization
    angles = []  # Servo angle over time (degrees)
    torques = []  # Torque (control output) over time

    # Simulation loop
    for _ in t:
        # Calculate the control torque using PID controller
        torque = pid.update(target - angle, dt)

        # Update angular velocity based on dynamics
        rate += ((torque - damping * rate) / inertia) * dt

        # Update angle based on angular velocity
        angle += rate * dt

        # Log current angle and torque for visualization
        angles.append(np.rad2deg(angle))  # Convert angle to degrees for display
        torques.append(torque)

    # Visualization: Servo angle response over time
    plt.figure()
    plt.plot(t, angles, label="Angle")  # Plot the actual angle
    plt.axhline(90, linestyle="--", label="Target")  # Plot the target angle at 90 degrees
    plt.title("Servo Position Controller")  # Add title
    plt.xlabel("Time [s]")  # Label for x-axis (time in seconds)
    plt.ylabel("Angle [deg]")  # Label for y-axis (angle in degrees)
    plt.grid(True)  # Add grid for better readability
    plt.legend()  # Add legend to identify the plots
    plt.show()

    # Visualization: Torque command over time
    plt.figure()
    plt.plot(t, torques, label="Torque")  # Plot torque commands (control signals)
    plt.title("Torque Command")
    plt.xlabel("Time [s]")
    plt.ylabel("Torque [N·m]")
    plt.grid(True)
    plt.legend()
    plt.show()

# Entry point: Run the simulation
if __name__ == "__main__":
    main()
