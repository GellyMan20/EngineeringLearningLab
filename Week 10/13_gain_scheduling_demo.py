# ==========================================================================
# Project 13 — Gain Scheduling
# ==========================================================================
#
# Purpose:
# Use different controller gains in different operating regions and compare scheduled behavior with a fixed-gain design.
#
# Why This Matters:
# Aircraft dynamics change with airspeed, altitude, Mach number, fuel state, and configuration.
#
# Key Concepts:
# - Operating points
# - Scheduled gains
# - Interpolation or switching
# - Nonlinear envelopes
#
# Mathematical Foundation:
# - K = K(rho), where rho is a scheduling variable
#
# Learning Objectives:
# - Explain the controller or analysis method in engineering terms.
# - Connect the governing equations to their implementation in Python.
# - Interpret the plots and calculated performance metrics.
# - Identify assumptions, implementation limits, and useful extensions.
#
# Suggested Experiments:
# - Change the plant parameters and observe the effect on stability and response.
# - Change controller gains or LQR weights and compare tracking versus effort.
# - Add disturbances, sensor noise, or actuator limits where appropriate.
# - Replace Euler integration with a higher-order numerical method.
# ==========================================================================
# Import NumPy for vectors, matrices, numerical integration, and performance calculations.
import numpy as np
# Import Matplotlib for state histories, control histories, and trade-study plots.
import matplotlib.pyplot as plt



# Execute this portion of the controller design or analysis workflow.
def gain_schedule(speed):
    """Execute this portion of the controller design or analysis workflow."""
    if speed < 5:
        return 2.0
    if speed < 15:
        return 1.2
    return 0.7



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 30, dt)

    heading = 0.5
    desired_heading = 0.0
    speed = 0.0

    headings = []
    gains = []
    speeds = []

    # Step through the simulation or design cases one sample at a time.
    for time in t:
        speed = min(20.0, 0.8 * time)
        gain = gain_schedule(speed)

        heading_error = desired_heading - heading
        turn_rate = gain * heading_error
        heading += turn_rate * dt

        headings.append(heading)
        gains.append(gain)
        speeds.append(speed)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, headings)
    plt.title("Gain-Scheduled Heading Response")
    plt.xlabel("Time [s]")
    plt.ylabel("Heading Error [rad]")
    plt.grid(True)
    # Display all completed figures.
    plt.show()


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, gains, label="Scheduled gain")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, speeds, label="Speed")
    plt.title("Gain Schedule")
    plt.xlabel("Time [s]")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
