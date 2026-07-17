# ==========================================================================
# Project 09 — Discrete LQR
# ==========================================================================
#
# Purpose:
# Design an LQR controller directly for a sampled-data system using the discrete Riccati equation.
#
# Why This Matters:
# Real flight computers execute controllers at finite rates, so sampling and discretization must be treated explicitly.
#
# Key Concepts:
# - Sampled-data control
# - Discrete state-space models
# - Discrete Riccati equation
# - Digital implementation
#
# Mathematical Foundation:
# - x[k+1] = A_d x[k] + B_d u[k]
# - K = (R + B^T P B)^-1 B^T P A
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
from scipy.linalg import solve_discrete_are



# Execute this portion of the controller design or analysis workflow.
def dlqr(A, B, Q, R):
    """Execute this portion of the controller design or analysis workflow."""
    # Solve the discrete algebraic Riccati equation for the sampled-data controller.
    P = solve_discrete_are(A, B, Q, R)
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.linalg.inv(B.T @ P @ B + R) @ (B.T @ P @ A)
    return K



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.1

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[1.0, dt], [0.0, 1.0]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.5 * dt**2], [dt]])

    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([10.0, 1.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.2]])
    K = dlqr(A, B, Q, R)

    x = np.array([[5.0], [0.0]])
    history = []
    controls = []

    # Step through the simulation or design cases one sample at a time.
    for _ in range(120):
        u = -K @ x
        x = A @ x + B @ u
        history.append(x.ravel().copy())
        controls.append(float(u[0, 0]))

    history = np.array(history)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(history[:, 0], label="Position")
    # Plot the relevant response history for visual comparison.
    plt.plot(history[:, 1], label="Velocity")
    plt.title("Discrete LQR")
    plt.xlabel("Step")
    plt.ylabel("State")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
