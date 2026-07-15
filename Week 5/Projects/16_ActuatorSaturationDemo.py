"""
Project: Actuator Saturation Demo
Purpose:
This script simulates and demonstrates the phenomenon of **integral windup** in a proportional-integral (PI) controller and shows how including an **anti-windup mechanism** can mitigate its effects. The key objectives of this project are:
- Understanding how actuator saturation leads to integral windup.
- Learning how anti-windup techniques improve control performance and prevent instability.
- Observing system output and control signals with and without anti-windup.

Applications:
- **Control Systems Design**: Tuning controllers for systems with actuators that have limited output ranges.
- **Robotics and Automation**: Ensures robust control in systems with constrained actuators like motors or valves.
- **Model Development**: Incorporating anti-windup strategies for improved controller performance.

Key Concepts:
- **Integral Windup**: When the integral term in a controller accumulates excessively large errors due to actuator saturation, leading to instability or sluggish recovery.
- **Anti-Windup**: A method to prevent the integral term from growing unbounded when the controller's output is saturated.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualizations

# Define a PI controller class
class PI:
    def __init__(self, kp, ki, limits=(-1, 1), anti_windup=False):
        """
        Initializes the PI controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            limits (tuple): Minimum and maximum actuator output range (default: (-1, 1)).
            anti_windup (bool): Enables or disables anti-windup logic (default: False).
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.limits = limits  # Actuator output limits
        self.anti_windup = anti_windup  # Anti-windup mode
        self.integral = 0.0  # Integral accumulator

    def update(self, error, dt):
        """
        Updates the PI control output with or without anti-windup measures.

        Parameters:
            error (float): Error between the target setpoint and current system state.
            dt (float): Simulation time step (seconds).

        Returns:
            float: Control output (clipped to the actuator limits).
        """
        # Update integral term (proposed integral if no anti-windup)
        proposed = self.integral + error * dt

        # Compute raw control output
        raw = self.kp * error + self.ki * proposed

        # Saturate the output to the predefined limits
        sat = float(np.clip(raw, *self.limits))

        # Anti-windup: Prevent integral term from growing when output is saturated
        if not self.anti_windup or raw == sat:  # Update only if output is not limited or anti-windup is off
            self.integral = proposed

        return sat  # Return the saturated control signal

# Function to run the simulation with and without anti-windup
def run(anti_windup):
    """
    Runs the simulation for the PI controller with or without anti-windup.

    Parameters:
        anti_windup (bool): Determines whether anti-windup is enabled.

    Returns:
        tuple: Time vector, system output, and control signal.
    """
    dt = 0.01  # Time step
    t = np.arange(0, 30, dt)  # Time duration (30 seconds)

    x = 0.0  # Initial system state
    c = PI(0.8, 0.5, anti_windup=anti_windup)  # Instantiate the PI controller

    xs, us = [], []  # Logs for output and control signals

    # Simulation loop
    for time in t:
        # Define the target setpoint: 10.0 until 15s, then switch to 0.0
        target = 10.0 if time <= 15 else 0.0

        # Compute control output (u) using the PI controller
        u = c.update(target - x, dt)

        # Update system state: simple linear dynamics with saturation
        x += (-0.4 * x + u) * dt

        # Log output state and control signal
        xs.append(x)
        us.append(u)

    return t, np.array(xs), np.array(us)  # Return time, system output, and control signal

# Main function to compare system behavior with and without anti-windup
def main():
    """
    Compares system performance with and without anti-windup enabled.
    Visualizes outputs and highlights the problems caused by integral windup.
    """

    # Run the simulation without anti-windup
    t, x1, u1 = run(False)

    # Run the simulation with anti-windup
    _, x2, u2 = run(True)

    # Visualization: System outputs over time
    plt.figure()
    plt.plot(t, x1, label="No anti-windup")  # Without anti-windup
    plt.plot(t, x2, label="With anti-windup")  # With anti-windup
    plt.title("Integral Windup")  # Add title
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Output")  # Label for y-axis
    plt.grid(True)  # Add grid for better readability
    plt.legend()  # Add legend to identify the two systems
    plt.show()

    # You can extend this with additional visualizations as needed

# Entry point: Run the simulation
if __name__ == "__main__":
    main()
