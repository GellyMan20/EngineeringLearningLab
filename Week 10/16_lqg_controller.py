# ==========================================================================
# Project 16 — LQG Controller
# ==========================================================================
#
# Purpose:
# Combine a Kalman state estimator with LQR state feedback to control a system when the full state is not measured directly.
#
# Why This Matters:
# LQG reflects a practical flight-control architecture: estimation supplies states and optimal control commands the plant.
#
# Key Concepts:
# - Separation principle
# - Kalman filtering
# - Estimated-state feedback
# - LQG
#
# Mathematical Foundation:
# - u = -K x_hat
# - x_hat_dot = A x_hat + Bu + L(y - C x_hat)
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
    rng = np.random.default_rng(16)


    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Define the output matrix C. It selects or combines states to form the measured output.
    C = np.array([[1.0, 0.0]])

    # LQR
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P_lqr = solve_continuous_are(A, B, np.diag([20.0, 2.0]), np.array([[0.5]]))
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.linalg.inv(np.array([[0.5]])) @ B.T @ P_lqr


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 12, dt)

    true_state = np.zeros((2, 1))
    est_state = np.zeros((2, 1))
    est_cov = np.diag([2.0, 2.0])

    F = np.eye(2) + A * dt
    G = B * dt
    H = C
    Qk = np.diag([0.0005, 0.01])
    Rk = np.array([[0.04]])
    I = np.eye(2)

    target = 1.0
    truth = []
    estimate = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        error_state = est_state - np.array([[target], [0.0]])
        u = -K @ error_state + 2.0 * target

        process_noise = rng.multivariate_normal([0, 0], Qk).reshape(2, 1)
        true_state = F @ true_state + G @ u + process_noise

        measurement = H @ true_state + rng.normal(0, np.sqrt(Rk[0, 0]), (1, 1))

        est_state = F @ est_state + G @ u
        est_cov = F @ est_cov @ F.T + Qk

        innovation = measurement - H @ est_state
        S = H @ est_cov @ H.T + Rk
        L = est_cov @ H.T @ np.linalg.inv(S)

        est_state = est_state + L @ innovation
        est_cov = (I - L @ H) @ est_cov

        truth.append(true_state[0, 0])
        estimate.append(est_state[0, 0])


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, truth, label="True position")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, estimate, label="Estimated position")
    plt.axhline(target, linestyle="--", label="Target")
    plt.title("LQG Control")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
