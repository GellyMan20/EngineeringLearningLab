"""
Project: PID Temperature Controller
Purpose:
This script demonstrates the implementation of a **PID (Proportional-Integral-Derivative) controller** applied to a 
temperature control system. It models how PID control can be used to maintain a desired temperature 
(setpoint) for a thermal system by adjusting the heating power. 

Key Concepts:
- Understand the influence of **Proportional (P)**, **Integral (I)**, and **Derivative (D)** gains on the response.
- Observe and analyze key performance characteristics such as steady-state error, rise time, and the effect of external disturbances.
- Provide a foundation for PID tuning and system modeling.

Applications:
- **Industrial Automation**: Used to control temperature in heating systems or furnaces.
- **Robotics**: Precise movement control by tuning P, I, and D gains.
- **Home Heating Systems**: Managing thermostats and environmental control.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization of output and control commands

# Class defining a PID controller
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes a PID controller with specified gains and output limits.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Minimum and maximum output limits.
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Limit output to avoid excessive control values
        self.integral = 0.0  # Integral term accumulator
        self.prev_error = 0.0  # Previous error for derivative calculation

    def update(self, error, dt):
        """
        Updates the PID controller output based on the current error.

        Parameters:
            error (float): Error between the desired and actual value.
            dt (float): Time step since the last update.

        Returns:
            float: The control output, limited by `output_limits`.
        """
        # Update integral term
        self.integral += error * dt

        # Calculate derivative term
        derivative = (error - self.prev_error) / dt

        # Save the current error for the next step
        self.prev_error = error

        # Compute the control output
        u = self.kp * error + self.ki * self.integral + self.kd * derivative  # PID formula

        # Clamp the output within the specified limits
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Main function to simulate and visualize PID-based temperature control
def main():
    """
    Simulates a PID controller regulating the temperature of a thermal system. 
    The system adjusts its heating power to maintain a desired target temperature 
    despite external disturbances.
    """
    dt = 0.1  # Time step (seconds)
    t = np.arange(0, 300, dt)  # Time array for simulation (from 0 to 300 seconds)

    # System parameters
    ambient = 20.0  # Ambient temperature in °C
    target = 70.0  # Desired (target) temperature in °C
    temp = 20.0  # Initial temperature in °C
    thermal_mass = 50.0  # Thermal mass of the system
    loss = 0.08  # Heat loss coefficient

    # Instantiate the PID controller
    pid = PID(kp=3.0, ki=0.04, kd=8.0, output_limits=(0, 100))

    # Logs for visualization
    temps = []  # Temperature over time
    controls = []  # Heating power applied over time

    # Simulation loop
    for time in t:
        # Introduce a disturbance: Sudden cooling for a duration (from 120s to 160s)
        disturbance = -10.0 if 120 <= time <= 160 else 0.0

        # Calculate the power command from the PID controller
        power = pid.update(target - temp, dt)

        # Update the temperature based on dynamics: heating power, heat loss, and disturbance
        temp += ((power - loss * (temp - ambient) + disturbance) / thermal_mass) * dt

        # Log data for plotting
        temps.append(temp)  # Log temperature
        controls.append(power)  # Log heater power

    # Visualization: Temperature response
    plt.figure()
    plt.plot(t, temps, label="Temperature")  # Plot temperature over time
    plt.axhline(target, linestyle="--", label="Target")  # The target temperature
    plt.title("PID Temperature Controller")  # Add title
    plt.xlabel("Time [s]")  # Label for the x-axis
    plt.ylabel("Temperature [°C]")  # Label for the y-axis
    plt.grid(True)  # Add grid for better readability
    plt.legend()  # Add legend to identify plots
    plt.show()

    # Visualization: Heater command output
    plt.figure()
    plt.plot(t, controls)  # Plot heater power over time
    plt.title("Heater Command")  # Add title
    plt.xlabel("Time [s]")  # Label for the x-axis
    plt.ylabel("Power [%]")  # Label for the y-axis
    plt.grid(True)  # Add grid for clarity
    plt.show()

# Entry point: Execute the simulation
if __name__ == "__main__":
    main()
