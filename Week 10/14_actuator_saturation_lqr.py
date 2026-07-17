# ==========================================================================
# Project 14 — LQR with Actuator Saturation
# ==========================================================================
#
# Purpose:
# Investigate how input limits change an otherwise linear optimal-control response.
#
# Why This Matters:
# Control surfaces, reaction wheels, thrusters, and motors all have hard position, rate, force, or torque limits.
#
# Key Concepts:
# - Actuator limits
# - Saturation nonlinearity
# - Windup-like behavior
# - Command feasibility
#
# Mathematical Foundation:
# - u_applied = clip(u_commanded, u_min, u_max)
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
# Import SciPy linear-algebra solvers used for Riccati equations, pole placement, or matrix operations.
from scipy.linalg import solve_continuous_are



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, np.diag([40.0, 3.0]), np.array([[0.2]]))
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.array([[1.0]]) @ B.T @ P / 0.2


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)
    x = np.array([[3.0], [0.0]])

    unlimited = []
    saturated = []
    xs = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        raw_u = float((-K @ x)[0, 0])
        # Enforce the physical command limits before the control input reaches the plant.
        u = np.clip(raw_u, -3.0, 3.0)

        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B * u) * dt

        unlimited.append(raw_u)
        saturated.append(u)
        xs.append(x[0, 0])


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, xs)
    plt.title("LQR Response with Saturation")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    # Display all completed figures.
    plt.show()


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, unlimited, label="Requested control")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, saturated, label="Applied control")
    plt.title("Actuator Saturation")
    plt.xlabel("Time [s]")
    plt.ylabel("u")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
