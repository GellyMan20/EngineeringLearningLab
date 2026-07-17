# ==========================================================================
# Project 11 — Model-Uncertainty Robustness
# ==========================================================================
#
# Purpose:
# Evaluate a fixed controller against plants whose physical parameters differ from the nominal design model.
#
# Why This Matters:
# Mass, inertia, aerodynamic derivatives, and center-of-gravity location vary throughout aerospace missions.
#
# Key Concepts:
# - Parametric uncertainty
# - Nominal versus off-nominal response
# - Robustness
# - Sensitivity
#
# Mathematical Foundation:
# - A_actual = A_nominal + Delta_A
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
    A_nom = np.array([[0.0, 1.0], [-2.0, -0.5]])
    B_nom = np.array([[0.0], [1.0]])

    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([20.0, 2.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A_nom, B_nom, Q, R)
    K = np.linalg.inv(R) @ B_nom.T @ P

    perturbations = [
        (1.0, 1.0),
        (0.8, 1.0),
        (1.2, 1.0),
        (1.0, 0.7),
        (1.0, 1.3),
    ]


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()

    # Step through the simulation or design cases one sample at a time.
    for stiffness_scale, damping_scale in perturbations:

        # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
        A = np.array([
            [0.0, 1.0],
            [-2.0 * stiffness_scale, -0.5 * damping_scale]
        ])
        B = B_nom.copy()
        x = np.array([[1.0], [0.0]])
        xs = []

        # Step through the simulation or design cases one sample at a time.
        for _ in t:
            u = -K @ x
            # Integrate the state forward with the explicit Euler method.
            x = x + (A @ x + B @ u) * dt
            xs.append(x[0, 0])

        # Plot the relevant response history for visual comparison.
        plt.plot(t, xs, label=f"k×{stiffness_scale}, c×{damping_scale}")

    plt.title("LQR Robustness to Model Uncertainty")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
