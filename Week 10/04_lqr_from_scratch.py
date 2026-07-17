# ==========================================================================
# Project 04 — LQR from Scratch
# ==========================================================================
#
# Purpose:
# Build a continuous-time Linear Quadratic Regulator using the algebraic Riccati equation and simulate optimal state regulation.
#
# Why This Matters:
# LQR is widely used for aircraft, launch vehicles, satellites, robotics, and other multivariable systems.
#
# Key Concepts:
# - Quadratic cost function
# - Riccati equation
# - Optimal state feedback
# - Closed-loop stability
#
# Mathematical Foundation:
# - J = integral(x^T Q x + u^T R u) dt
# - A^T P + PA - PBR^-1B^TP + Q = 0
# - K = R^-1 B^T P
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



# Solve the continuous-time Riccati equation and return the optimal feedback gain, Riccati matrix, and closed-loop eigenvalues.
def lqr(A, B, Q, R):
    """Solve the continuous-time Riccati equation and return the optimal feedback gain, Riccati matrix, and closed-loop eigenvalues."""
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.linalg.inv(R) @ B.T @ P
    eigvals = np.linalg.eigvals(A - B @ K)
    return K, P, eigvals



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.4]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])

    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([10.0, 1.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5]])

    K, P, eigvals = lqr(A, B, Q, R)

    print("LQR gain K:")
    print(K)
    print("Closed-loop eigenvalues:")
    print(eigvals)


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 8, dt)
    x = np.array([[1.0], [0.0]])
    xs = []
    us = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        u = -K @ x
        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B @ u) * dt
        xs.append(x.ravel().copy())
        us.append(float(u[0, 0]))

    xs = np.array(xs)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, xs[:, 0], label="Position")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, xs[:, 1], label="Velocity")
    plt.title("LQR State Regulation")
    plt.xlabel("Time [s]")
    plt.ylabel("State")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, us)
    plt.title("LQR Control Effort")
    plt.xlabel("Time [s]")
    plt.ylabel("u")
    plt.grid(True)
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
