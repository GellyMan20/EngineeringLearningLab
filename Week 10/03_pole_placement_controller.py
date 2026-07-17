# ==========================================================================
# Project 03 — Pole-Placement Controller
# ==========================================================================
#
# Purpose:
# Design state feedback by selecting desired closed-loop pole locations and verify the resulting transient response.
#
# Why This Matters:
# Pole placement is useful when engineers have explicit damping and response-speed requirements.
#
# Key Concepts:
# - Closed-loop eigenvalues
# - State feedback
# - Pole placement
# - Transient-response shaping
#
# Mathematical Foundation:
# - u = -Kx
# - A_cl = A - BK
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
# Import SciPy signal-processing utilities for state-space and sampled-data calculations.
from scipy.signal import place_poles



# Execute this portion of the controller design or analysis workflow.
def simulate(A, B, K, x0, dt=0.01, t_end=8.0):
    """Execute this portion of the controller design or analysis workflow."""
    # Build the simulation time vector.
    t = np.arange(0, t_end, dt)
    x = x0.copy()
    history = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        u = -K @ x
        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B @ u) * dt
        history.append(x.ravel().copy())

    return t, np.array(history)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])

    # Calculate a feedback gain that places the closed-loop poles at the selected locations.
    slow_K = place_poles(A, B, [-1.0, -1.5]).gain_matrix
    # Calculate a feedback gain that places the closed-loop poles at the selected locations.
    fast_K = place_poles(A, B, [-3.0, -4.0]).gain_matrix

    x0 = np.array([[1.0], [0.0]])

    t, slow = simulate(A, B, slow_K, x0)
    _, fast = simulate(A, B, fast_K, x0)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, slow[:, 0], label="Slow poles")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, fast[:, 0], label="Fast poles")
    plt.title("Pole Placement Comparison")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
