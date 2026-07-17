# ==========================================================================
# Project 01 — State-Space Basics
# ==========================================================================
#
# Purpose:
# Simulate a dynamic system in state-space form and connect the A, B, and C matrices to state evolution and measured output.
#
# Why This Matters:
# Aircraft short-period motion, spacecraft attitude dynamics, and actuator models are commonly represented in state-space form.
#
# Key Concepts:
# - State vectors and first-order dynamics
# - A, B, and C matrix interpretation
# - Euler integration
# - Time-domain simulation
#
# Mathematical Foundation:
# - x_dot = A x + B u
# - y = C x + D u
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



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)


    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.7]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Define the output matrix C. It selects or combines states to form the measured output.
    C = np.array([[1.0, 0.0]])

    x = np.array([[1.0], [0.0]])
    xs = []
    ys = []

    # Step through the simulation or design cases one sample at a time.
    for time in t:
        u = 1.0 if time >= 1.0 else 0.0
        # Evaluate the continuous-time state equation using the current state and control input.
        x_dot = A @ x + B * u
        # Integrate the state forward with the explicit Euler method.
        x = x + x_dot * dt
        y = C @ x

        xs.append(x.ravel().copy())
        ys.append(float(y[0, 0]))

    xs = np.array(xs)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, xs[:, 0], label="Position state")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, xs[:, 1], label="Velocity state")
    plt.title("State-Space Simulation")
    plt.xlabel("Time [s]")
    plt.ylabel("State")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
