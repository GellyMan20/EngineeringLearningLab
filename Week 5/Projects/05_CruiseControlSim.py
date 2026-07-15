"""
Project: Cruise Control Simulator
Purpose:
This script simulates a **PID (Proportional-Integral-Derivative)** controller applied to a vehicle's cruise control system. The system adjusts throttle commands to maintain a desired speed (setpoint) under varying road conditions and disturbances such as wind resistance and hill climbing. The simulation demonstrates:
- **Tuning PID parameters** for balancing responsiveness and stability.
- Observing the vehicle's behavior under external disturbances.
- Visualizing system outputs (speed and throttle commands) to understand PID dynamics.

Key Concepts:
- **P (Proportional)**: Responds to instantaneous speed errors.
- **I (Integral)**: Addresses accumulated errors over time to minimize steady-state error.
- **D (Derivative)**: Reacts to changes in error rate to prevent response overshoot.
- **Disturbance Rejection**: Ability of PID to maintain system stability under external forces.

Applications:
- **Autonomous Driving**: Used in cruise control systems to maintain consistent vehicle speed.
- **Robotics**: Motor control for constant linear or rotational speed in robots.
- **Industrial Automation**: Control systems for precise velocity regulation of machinery.
"""

# Import necessary libraries
import numpy as np  # For numerical operations
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
            output_limits (tuple): Limits for the control output (default: no limits).
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits
        self.integral = 0.0  # Integral term accumulator
        self.prev_error = 0.0  # Previous error for derivative term calculation

    def update(self, error, dt):
        """
        Updates the PID controller output.

        Parameters:
            error (float): Difference between the target and current value (control error).
            dt (float): Time step since the last update.

        Returns:
            float: Control output (e.g., throttle percentage).
        """
        # Update integral term to account for accumulated error
        self.integral += error * dt

        # Calculate the derivative term (rate of change of error)
        derivative = (error - self.prev_error) / dt

        # Update the previous error for the next step
        self.prev_error = error

        # Compute the control signal using PID formula
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Return the control signal, clipped to the specified output limits
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Main function to simulate PID-based cruise control
def main():
    """
    Simulates a vehicle cruise control system using PID to maintain a target speed despite external disturbances.
    Visualizes the speed response, throttle command, and disturbance effects.
    """

    # Simulation parameters
    dt = 0.05  # Time step (seconds)
    t = np.arange(0, 80, dt)  # Simulation duration (0 to 80 seconds) with a time step

    # Vehicle parameters
    mass = 1500.0  # Vehicle mass (kg)
    drag = 0.38  # Drag coefficient (proportional to speed squared)
    max_force = 4500.0  # Maximum force from throttle (N)
    target_speed = 27.0  # Desired cruising speed (m/s)
    speed = 0.0  # Initial speed (m/s)

    # Instantiate the PID controller
    pid = PID(kp=0.08, ki=0.015, kd=0.01, output_limits=(0, 1))  # PID gains and throttle limits

    # Logs for visualization
    speeds = []  # Vehicle speed over time
    throttles = []  # Throttle command over time

    # Simulation loop
    for time in t:
        # Introduce external disturbances: hill resistance and wind resistance
        hill = 1200.0 if 30 <= time <= 50 else 0.0  # Hill resistance active between 30s and 50s
        wind = 600.0 if time >= 55 else 0.0  # Wind resistance active after 55s

        # Compute throttle command based on PID output
        throttle = pid.update(target_speed - speed, dt)

        # Calculate acceleration considering throttle force, drag, hill resistance, and wind
        accel = (throttle * max_force - drag * speed**2 - hill - wind) / mass

        # Update speed based on computed acceleration
        speed += accel * dt

        # Log vehicle speed and throttle command for plotting later
        speeds.append(speed)
        throttles.append(throttle)

    # Visualization: Speed response over time
    plt.figure()
    plt.plot(t, speeds, label="Speed")  # Plot actual speed
    plt.axhline(target_speed, linestyle="--", label="Target")  # Plot target speed
    plt.title("PID Temperature Controller")
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [m/s]")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Visualization: Throttle command over time
    plt.figure()
    plt.plot(t, throttles)  # Plot throttle output
    plt.title("Throttle Command")
    plt.xlabel("Time [s]")
    plt.ylabel("Throttle [0-1]")
    plt.grid(True)
    plt.show()

# Entry point: Execute the simulation
if __name__ == "__main__":
    main()
