# ==========================================================================
# Project 10 — LQR Tracking Prefilter
# ==========================================================================
#
# Purpose:
# Compute a reference prefilter that converts a regulator into a command-following controller with correct steady-state gain.
#
# Why This Matters:
# Command shaping and prefiltering help separate desired response behavior from disturbance regulation.
#
# Key Concepts:
# - Reference tracking
# - Steady-state gain
# - Prefilter design
# - Regulation versus tracking
#
# Mathematical Foundation:
# - u = -Kx + Nbar r
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

    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([15.0, 2.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.linalg.inv(R) @ B.T @ P

    Nbar = -1.0 / (C @ np.linalg.inv(A - B @ K) @ B)
    Nbar = float(Nbar[0, 0])


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)
    x = np.zeros((2, 1))
    target = 1.0
    output = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        u = -K @ x + Nbar * target
        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B @ u) * dt
        output.append(float((C @ x)[0, 0]))

    print(f"Nbar = {Nbar:.4f}")


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, output, label="Output")
    plt.axhline(target, linestyle="--", label="Target")
    plt.title("LQR Reference Tracking with Prefilter")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
