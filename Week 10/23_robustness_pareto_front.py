# ==========================================================================
# Project 23 — Robustness Pareto Front
# ==========================================================================
#
# Purpose:
# Identify non-dominated controller designs when tracking, effort, and robustness objectives conflict.
#
# Why This Matters:
# Aerospace design rarely has one best answer; Pareto fronts show the cost of improving one objective at the expense of another.
#
# Key Concepts:
# - Pareto optimality
# - Multi-objective design
# - Trade fronts
# - Dominated solutions
#
# Mathematical Foundation:
# - A design is non-dominated when no objective can improve without worsening another
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



# Execute this portion of the controller design or analysis workflow.
def evaluate(q_scale, r_scale):
    """Execute this portion of the controller design or analysis workflow."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([20.0, 2.0]) * q_scale
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5 * r_scale]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.linalg.inv(R) @ B.T @ P

    x = np.array([[1.0], [0.0]])

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    errors = []
    efforts = []

    # Step through the simulation or design cases one sample at a time.
    for _ in range(800):
        u = -K @ x
        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B @ u) * dt
        errors.append(abs(x[0, 0]))
        efforts.append(abs(float(u[0, 0])))

    return np.mean(errors), np.mean(efforts)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    points = []

    # Step through the simulation or design cases one sample at a time.
    for q in np.logspace(-1, 1, 12):
        # Step through the simulation or design cases one sample at a time.
        for r in np.logspace(-1, 1, 12):
            error, effort = evaluate(q, r)
            points.append((error, effort, q, r))

    points = np.array(points)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    plt.scatter(points[:, 0], points[:, 1])
    plt.title("LQR Tracking vs Control-Effort Trade Space")
    plt.xlabel("Mean tracking error")
    plt.ylabel("Mean control effort")
    plt.grid(True)
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
