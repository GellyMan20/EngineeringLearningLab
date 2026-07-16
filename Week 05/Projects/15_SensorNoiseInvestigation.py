"""
Project: Sensor Noise Investigation
Purpose:
This script investigates the effect of sensor noise on the performance of a **PID (Proportional-Integral-Derivative) controller**.
The main focus is on illustrating how **derivative sensitivity** can cause noisy or unstable control commands when noisy sensor measurements are used. The project demonstrates:
- How sensor noise affects the derivative term in PID control.
- The impact of noisy control commands on system stability and output accuracy.
- The limitations of derivative action in systems where measurement noise is present.

Applications:
- **Control Systems**: Evaluating PID performance under noisy sensor conditions.
- **Real-World Robotics**: Mitigating the impact of sensor noise on precise robotic control.
- **System Identification**: Understanding how noise affects feedback-based systems.

Key Learning:
- The derivative term in PID control amplifies noise, which can lead to oscillatory or erratic control commands.
- Filtering or tuning \( K_d \) is crucial to minimize the impact of noisy feedback.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualizing system response and control signals

# PID Controller class for feedback control
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes the PID controller with specified gains and output limits.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Minimum and maximum limits for the control signal.
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Limits to clamp the control output
        self.integral = 0.0  # Integral accumulator
        self.prev_error = 0.0  # Stores the previous error for derivative calculation

    def update(self, error, dt):
        """
        Updates the PID controller output based on the current error and time step.

        Parameters:
            error (float): Difference between the desired and measured output.
            dt (float): Time step since the last update.

        Returns:
            float: Control output, clamped to the defined limits.
        """
        # Update the integral component
        self.integral += error * dt

        # Calculate the derivative
        derivative = (error - self.prev_error) / dt

        # Save the current error for the next update
        self.prev_error = error

        # Compute the PID output
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Limit the output to the defined range
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Main function to simulate the system and visualize results
def main():
    """
    Simulates a PID-controlled system under the influence of sensor noise.
    Visualizes the true and noisy responses, as well as the derivative-induced noise in the control commands.
    """

    # Time and simulation parameters
    dt = 0.01  # Time step (seconds)
    t = np.arange(0, 20, dt)  # Time vector from 0 to 20 seconds

    # System initial conditions
    x, v, r = 0.0, 0.0, 1.0  # Initial position, velocity, and desired setpoint

    # Instantiate the PID controller
    pid = PID(kp=3.0, ki=0.0, kd=2.0, output_limits=(-20, 20))  # PID tuning with high derivative gain

    # Logs for visualization
    xs = []  # Store true system output (x)
    meas = []  # Store noisy measurements
    us = []  # Store control outputs (u)

    # Random number generator for noise
    rng = np.random.default_rng(2)

    # Simulation loop
    for _ in t:
        # Add noise to the measured position
        y = x + rng.normal(0, 0.05)  # Noisy measurement with Gaussian noise (std = 0.05)

        # Control input from PID controller
        u = pid.update(r - y, dt)  # Use noisy measurement (y) as feedback

        # System dynamics
        a = u - 0.7 * v - x  # Acceleration (based on control output)
        v += a * dt  # Update velocity
        x += v * dt  # Update position

        # Log data for visualization
        xs.append(x)  # True position
        meas.append(y)  # Noisy measurement
        us.append(u)  # Control command

    # Visualization: System outputs
    plt.figure()
    plt.plot(t, xs, label="True output")  # True output (x)
    plt.plot(t, meas, alpha=0.5, label="Noisy measurement")  # Noisy measurements
    plt.axhline(r, linestyle="--", label="Command")  # Command/reference setpoint
    plt.title("Sensor Noise Investigation")  # Add plot title
    plt.xlabel("Time [s]")  # Label for x-axis (time)
    plt.ylabel("Output")  # Label for y-axis (output position)
    plt.grid(True)  # Add grid for better readability
    plt.legend()  # Add legend
    plt.show()

    # Visualization: Control signals over time
    plt.figure()
    plt.plot(t, us, label="Control Command")  # Plot control outputs
    plt.title("Derivative Noise in Control Command")  # Title for plot
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Control")  # Label for control signals
    plt.grid(True)  # Add grid
    plt.show()

# Entry point: Run the simulation
if __name__ == "__main__":
    main()
