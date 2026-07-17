# ==========================================================================
# Project 05 — LQR Weight Tuning
# ==========================================================================
#
# Purpose:
# Explore how the Q and R matrices trade state regulation against actuator effort.
#
# Why This Matters:
# Flight-control tuning often balances tracking performance, structural loads, propellant use, and actuator life.
#
# Key Concepts:
# - Bryson-style tuning intuition
# - State penalties
# - Control penalty
# - Performance tradeoffs
#
# Mathematical Foundation:
# - Large Q increases state penalties
# - Large R discourages control effort
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



# Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices.
def lqr_gain(A, B, Q, R):
    """Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices."""
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    return np.linalg.inv(R) @ B.T @ P



# Execute this portion of the controller design or analysis workflow.
def run_case(q_position, r_control):
    """Execute this portion of the controller design or analysis workflow."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.4]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([q_position, 1.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[r_control]])
    K = lqr_gain(A, B, Q, R)


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 8, dt)
    x = np.array([[1.0], [0.0]])
    positions = []
    controls = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        u = -K @ x
        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B @ u) * dt
        positions.append(x[0, 0])
        controls.append(float(u[0, 0]))

    return t, np.array(positions), np.array(controls)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    cases = [(1.0, 1.0), (10.0, 1.0), (50.0, 1.0), (10.0, 5.0)]


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Step through the simulation or design cases one sample at a time.
    for q, r in cases:
        t, pos, _ = run_case(q, r)
        # Plot the relevant response history for visual comparison.
        plt.plot(t, pos, label=f"Qpos={q}, R={r}")
    plt.title("LQR Weight Tuning: State Response")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Step through the simulation or design cases one sample at a time.
    for q, r in cases:
        t, _, u = run_case(q, r)
        # Plot the relevant response history for visual comparison.
        plt.plot(t, u, label=f"Qpos={q}, R={r}")
    plt.title("LQR Weight Tuning: Control Effort")
    plt.xlabel("Time [s]")
    plt.ylabel("u")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
