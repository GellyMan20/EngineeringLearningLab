# ==========================================================================
# Project 08 — LQR with Integral Action
# ==========================================================================
#
# Purpose:
# Augment the plant with an integrated tracking error so LQR can reject constant disturbances and eliminate steady-state offset.
#
# Why This Matters:
# Integral augmentation is common when model mismatch or persistent loads would otherwise create tracking bias.
#
# Key Concepts:
# - State augmentation
# - Integral control
# - Steady-state accuracy
# - LQI architecture
#
# Mathematical Foundation:
# - z_dot = r - y
# - x_aug = [x; z]
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
    # Define the output matrix C. It selects or combines states to form the measured output.
    C = np.array([[1.0, 0.0]])

    A_aug = np.block([
        [A, np.zeros((2, 1))],
        [-C, np.zeros((1, 1))]
    ])
    B_aug = np.vstack((B, [[0.0]]))

    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([20.0, 2.0, 15.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5]])

    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A_aug, B_aug, Q, R)
    K = np.linalg.inv(R) @ B_aug.T @ P


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 12, dt)
    state = np.zeros((2, 1))
    integral = 0.0
    target = 1.0

    xs = []
    us = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        error = target - state[0, 0]
        integral += error * dt

        aug_state = np.vstack((state, [[integral]]))
        u = -K @ aug_state

        # Integrate the state forward with the explicit Euler method.
        state = state + (A @ state + B @ u) * dt

        xs.append(state[0, 0])
        us.append(float(u[0, 0]))


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, xs, label="Output")
    plt.axhline(target, linestyle="--", label="Target")
    plt.title("LQR with Integral Action")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
