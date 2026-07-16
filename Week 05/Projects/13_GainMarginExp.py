"""
Project: Gain Margin Experiment
Purpose:
This script simulates and visualizes the effects of varying proportional gain (\( K_p \)) on a second-order system. 
The **gain margin** is a critical concept in control systems, indicating the stability of the system under higher feedback gain values. 
The experiment explores:
- **Excessive Gain**: Observing how large feedback gains can destabilize the system.
- **Oscillation**: Identifying gain values that result in oscillatory behavior.
- **Instability**: Showing how improper gains lead the system to diverge rather than stabilize.

Applications:
- **Control Systems Design**: Evaluating the stability of controllers and tuning gain values for stable operation.
- **Mechanical Systems**: Understanding resonance and oscillation in feedback-controlled dynamic systems.
- **Educational Purposes**: Demonstrating the relationship between gain and system stability.

Key Concepts:
- Stability is defined as the system's ability to converge to a desired setpoint (\( r \)).
- High \( K_p \) gains amplify corrective action, potentially causing oscillations or destabilization.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Function to simulate the system dynamics with a given proportional gain (Kp)
def simulate(kp, dt=0.001, t_end=10):
    """
    Simulates the response of a second-order system controlled by proportional feedback.

    Parameters:
        kp (float): The proportional gain.
        dt (float): Time step size (default: 0.001 seconds).
        t_end (float): Simulation duration in seconds (default: 10 seconds).

    Returns:
        tuple: Time vector and system response (array of output values).
    """
    t = np.arange(0, t_end, dt)  # Generate time vector
    x, v, r = 0.0, 0.0, 1.0  # Initial conditions: position, velocity, and reference setpoint
    xs = []  # Storage for output values

    # Simulation loop to compute system response over time
    for _ in t:
        u = kp * (r - x)  # Controller output (proportional to error)
        a = u - 0.5 * v - x  # Acceleration based on second-order dynamics
        v += a * dt  # Update velocity
        x += v * dt  # Update position
        xs.append(x)  # Store current position (output)

    return t, np.array(xs)

# Main function to visualize the effect of gain on system stability
def main():
    """
    Visualizes the response of a second-order system with different proportional gain values.
    Highlights the transition from stability to oscillations and instability based on gain margin.
    """
    plt.figure()

    # Simulate and plot the system response for various proportional gains
    for kp in [0.5, 1, 2, 5, 10, 20]:  # Test gains ranging from small to large
        t, y = simulate(kp)  # Generate system response
        plt.plot(t, y, label=f"Kp={kp}")  # Plot output for each gain

    # Add reference line (desired setpoint) and annotations
    plt.axhline(1, linestyle="--", color="gray", label="Command")  # Desired setpoint at y=1
    plt.title("Gain Margin Experiment")  # Title of the plot
    plt.xlabel("Time [s]")  # Label for x-axis
    plt.ylabel("Output")  # Label for y-axis
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add legend to differentiate gains
    plt.show()

# Entry point: Execute the experiment
if __name__ == "__main__":
    main()
