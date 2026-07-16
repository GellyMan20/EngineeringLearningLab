"""
Project: Drone Altitude Hold
Purpose:
This script simulates a **PID (Proportional-Integral-Derivative) controller** designed to maintain the altitude of a drone at a desired target level. 
The PID controller dynamically adjusts the thrust to stabilize altitude and compensates for external disturbances, such as wind acting on the drone. 

Key Concepts:
- **PID Altitude Control**: Uses feedback from the current altitude to adjust thrust.
- **Wind Disturbance**: Models external forces acting downward to test the robustness of the controller.
- **Actuator Limits**: Defines constraints on thrust output to ensure realistic simulation.

Applications:
- **Drone Navigation and Stability**: Maintaining consistent altitude for autonomous drones.
- **Aerospace Systems**: Regulating vertical position in aircraft and UAVs.
- **Robotics**: Controlling the height of aerial robots during flight or hovering tasks.
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
            output_limits (tuple): Limits for the output thrust (default: no limits).
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Output limits for thrust
        self.integral = 0.0  # Sum of past errors (used for integral term)
        self.prev_error = 0.0  # Previous error to compute derivative

    def update(self, error, dt):
        """
        Updates the PID controller's output thrust based on the error.

        Parameters:
            error (float): Difference between target altitude and current altitude.
            dt (float): Simulation time step.

        Returns:
            float: Control signal (thrust), limited by output limits.
        """
        # Update the integral term (sum of errors over time)
        self.integral += error * dt

        # Compute the derivative term (rate of change of error)
        derivative = (error - self.prev_error) / dt

        # Calculate the control signal using the PID formula
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Apply output limits and store the current error for the next step
        self.prev_error = error
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Main function to simulate drone altitude hold
def main():
    """
    Simulates a PID-controlled drone to maintain a target altitude. Incorporates disturbances (e.g., wind) 
    and thrust constraints. Visualizes the altitude response and thrust commands.
    """

    # Simulation parameters
    dt = 0.01  # Time step
    t = np.arange(0, 30, dt)  # Time vector (30 seconds simulation)

    # Drone parameters
    mass = 1.5  # Drone mass in kg
    g = 9.81  # Gravitational acceleration in m/s²
    target = 20.0  # Desired target altitude in meters

    # Initial conditions
    z = 0.0  # Initial altitude
    vz = 0.0  # Initial vertical velocity

    # Instantiate the PID controller
    pid = PID(kp=4.0, ki=0.8, kd=3.0, output_limits=(0, 35))  # Tuning for altitude control

    # Logs for visualization
    zs = []  # Altitude over time
    thrusts = []  # Thrust commands over time

    # Simulation loop
    for time in t:
        # Introduce wind disturbance (downward force active between 12s and 18s)
        wind_down = 3.0 if 12 <= time <= 18 else 0.0

        # Compute thrust using the PID controller
        thrust = pid.update(target - z, dt)

        # Update vertical velocity based on thrust, gravitational pull, and wind disturbance
        vz += ((thrust - mass * g - wind_down) / mass) * dt

        # Update altitude based on vertical velocity
        z += vz * dt

        # Prevent the drone from going below ground level
        if z < 0:
            z, vz = 0, max(0, vz)

        # Log altitude and thrust for visualization
        zs.append(z)
        thrusts.append(thrust)

    # Visualization: Altitude over time
    plt.figure()
    plt.plot(t, zs, label="Altitude")  # Plot altitude response
    plt.axhline(target, linestyle="--", label="Target")  # Plot target altitude
    plt.title("Drone Altitude Hold")  # Title of the plot
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Altitude [m]")  # Label for y-axis
    plt.grid(True)  # Add gridlines for better readability
    plt.legend()  # Add legend to identify plots
    plt.show()

    # Visualization: Thrust commands over time
    plt.figure()
    plt.plot(t, thrusts, label="Thrust")  # Plot thrust commands
    plt.title("Thrust Command")  # Title for the thrust graph
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Thrust [N]")  # Label for y-axis
    plt.grid(True)  # Add gridlines for clarity
    plt.legend()  # Add legend
    plt.show()

# Entry point: Run the simulation
if __name__ == "__main__":
    main()
