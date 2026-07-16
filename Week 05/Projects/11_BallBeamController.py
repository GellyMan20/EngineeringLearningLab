"""
Project: Ball-on-Beam Controller
Purpose:
This script simulates the dynamics of a **ball-on-beam system**, a classic control problem often used in control systems education. 
The objective is to control the angle of the beam to stabilize the ball at a target position. This system demonstrates:
- **Stability**: Controlling an inherently unstable system to achieve a steady balance.
- **Sensitivity**: Highlighting how small deviations in the beam's angle affect the ball's position.
- **Balancing Dynamics**: Understanding how proportional-derivative (PD) control stabilizes the system.

Applications:
- **Control Systems Education**: Demonstrating PD control principles for stabilizing inherently unstable systems.
- **Robotics**: Applicable to control tasks where balance and delicate adjustments are required.
- **Dynamic Systems Testing**: Examining responsiveness and robustness of control algorithms.

Key Concepts:
- The system is **unstable** without proper feedback control.
- The **PD controller** stabilizes the ball by continuously adjusting the beam angle to minimize position error.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualizations

# Define a PD control class for balancing dynamics
class PD:
    def __init__(self, kp, kd, output_limits=(-0.25, 0.25)):
        """
        Initializes the PD controller.

        Parameters:
            kp (float): Proportional gain.
            kd (float): Derivative gain.
            output_limits (tuple): Minimum and maximum output limits for the beam angle.
        """
        self.kp = kp  # Proportional gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Limit for the beam angle to prevent saturation
        self.prev_error = 0.0  # Tracks the error from the previous update

    def update(self, error, dt):
        """
        Computes the control signal (beam angle) based on the error and time step.

        Parameters:
            error (float): Difference between the target and current ball position (setpoint - actual).
            dt (float): Time step since the last update.

        Returns:
            float: Control signal (beam angle in radians), clamped within `output_limits`.
        """
        # Compute the derivative of the error
        derivative = (error - self.prev_error) / dt

        # Save the current error for the next iteration
        self.prev_error = error

        # Compute the control signal based on the PD formula
        u = self.kp * error + self.kd * derivative

        # Clamp the signal to prevent the beam angle from exceeding limits
        return float(np.clip(u, *self.output_limits))

# Main function to simulate the ball-on-beam system
def main():
    """
    Simulates the behavior of the ball-on-beam system under PD control. 
    Visualizes the ball's position over time and the required beam angle to stabilize it.
    """

    # Simulation parameters
    dt = 0.001  # Time step (seconds)
    t = np.arange(0, 12, dt)  # Time vector (0 to 12 seconds)

    # Ball-on-beam system parameters
    g = 9.81  # Gravitational acceleration (m/s²)
    length = 1.0  # Length of the beam (meter)

    # Initial conditions
    x = 0.4  # Initial ball position (0.4 m from center)
    v = 0.0  # Initial ball velocity (m/s)
    target = 0.0  # Target position (center of the beam)

    # Initialize the PD controller for beam angle adjustment
    controller = PD(kp=1.8, kd=1.0)  # Proportional and derivative gains

    # Logs for plotting
    xs = []  # Ball position over time
    angles = []  # Beam angles applied over time (in degrees)

    # Simulation loop
    for _ in t:
        # Calculate the control signal (beam angle) using the PD controller
        beam_angle = controller.update(target - x, dt)

        # Compute the acceleration of the ball due to the beam angle
        a = (5/7) * g * np.sin(beam_angle)  # Accounts for rolling motion (5/7 factor)

        # Update the ball's velocity and position
        v += a * dt  # Velocity update
        x += v * dt  # Position update

        # Log the ball position and beam angle for visualization
        xs.append(x)
        angles.append(np.rad2deg(beam_angle))  # Convert angle to degrees for readability

    # Visualization: Ball position over time
    plt.figure()
    plt.plot(t, xs, label="Ball Position [m]")  # Plot the ball's position
    plt.axhline(0, linestyle="--", color="gray", label="Target Position")  # Reference line for target position
    plt.title("Ball-on-Beam Control")  # Add title
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Ball Position [m]")  # Label for y-axis
    plt.grid(True)  # Add gridlines for better readability
    plt.legend()  # Add legend
    plt.show()

# Entry point: Execute the simulation
if __name__ == "__main__":
    main()
