"""
Project: Phase Margin Experiment
Purpose:
This script simulates the dynamics of a second-order system with varying time delays to explore **delay-induced instability** and **phase lag**, concepts critical in control systems. It demonstrates how time delay in the feedback loop can destabilize a system even when other parameters are stable. The experiment visualizes:
- How increasing delay causes oscillations and instability.
- The concept of **phase lag** introduced by delay.
- The importance of phase margin to ensure system stability.

Key Concepts:
- **Phase Margin**: Determines how much phase lag the system can tolerate before becoming unstable.
- **Delay-Induced Instability**: Increasing delays in feedback loops can push the system toward instability.
- **Phase Lag**: Time delay in feedback introduces phase changes, reducing stability margins.

Applications:
- **Control Systems**: Designing controllers to handle time delays in feedback loops.
- **Signal Processing**: Studying the effect of delays on signal stability.
- **Robotics and Automation**: Mitigating delays in sensor-based system feedback loops.

"""

import numpy as np  # For numerical computation
import matplotlib.pyplot as plt  # For visualization
from collections import deque  # For implementing feedback with delays

# Function to simulate the system dynamics with a specific feedback delay
def simulate(delay_s, kp=3.0, kd=1.0, dt=0.001, t_end=10):
    """
    Simulates system behavior under varying time delays in the feedback loop.

    Parameters:
        delay_s (float): Feedback delay (in seconds).
        kp (float): Proportional gain.
        kd (float): Derivative gain.
        dt (float): Time step for numerical integration.
        t_end (float): Simulation duration in seconds.

    Returns:
        t (ndarray): Time vector.
        xs (ndarray): Output of the system over time.
    """
    t = np.arange(0, t_end, dt)  # Create time vector
    delay_steps = max(1, int(delay_s / dt))  # Compute number of integration steps corresponding to the delay
    q = deque([0.0] * delay_steps, maxlen=delay_steps)  # Delay buffer (FIFO queue)

    # Initialize system variables
    x = 0.0  # System state (position)
    v = 0.0  # Velocity
    r = 1.0  # Desired setpoint

    xs = []  # List to store the output positions

    # Simulation loop
    for _ in t:
        q.append(x)  # Append current state to delay queue
        delayed_x = q[0]  # Retrieve the delayed value

        # Control input (feedback with delay)
        u = kp * (r - delayed_x) - kd * v  # PID control (P and D terms)

        # Compute acceleration from the equation of motion
        a = u - 0.5 * v - x  # Second-order dynamics

        # Update velocity and position
        v += a * dt  # Update velocity
        x += v * dt  # Update position

        # Log the current position
        xs.append(x)

    return t, np.array(xs)  # Return the time vector and output response

# Main function to run and visualize the experiment
def main():
    """
    Simulates a second-order system with feedback delays and visualizes its response.
    Explores how delays affect system response, stability, and phase margins.
    """

    # Time delays to test in seconds
    delays = [0.0, 0.05, 0.15, 0.3, 0.5]

    plt.figure()

    # Simulate the system and generate plots for each delay
    for delay in delays:
        t, y = simulate(delay)  # Simulate system dynamics for a given delay
        plt.plot(t, y, label=f"delay={delay}s")  # Plot the system output

    # Add a horizontal line indicating the setpoint (r = 1.0)
    plt.axhline(1, linestyle="--", label="Command")  # Command (setpoint) reference line

    # Add plot titles, labels, and legend
    plt.title("Phase Margin Experiment")  # Add title
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Output")  # Label for y-axis
    plt.grid(True)  # Add grid to the plot
    plt.legend()  # Add legend for clarity
    plt.show()  # Display the plot

# Entry point: Run the simulation
if __name__ == "__main__":
    main()
