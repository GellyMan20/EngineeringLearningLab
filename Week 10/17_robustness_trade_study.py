# ==========================================================================
# Project 17 — Robustness Trade Study
# ==========================================================================
#
# Purpose:
# Compare candidate controllers across several uncertainty and disturbance cases using common performance metrics.
#
# Why This Matters:
# A controller must be judged across the mission envelope rather than on a single nominal plot.
#
# Key Concepts:
# - Trade-space analysis
# - Multi-scenario evaluation
# - Performance metrics
# - Design decisions
#
# Mathematical Foundation:
# - Evaluate the same metrics for every controller and scenario
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
# Import SciPy linear-algebra solvers used for Riccati equations, pole placement, or matrix operations.
from scipy.linalg import solve_continuous_are



# Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices.
def lqr_gain(A, B, q_scale, r_scale):
    """Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices."""
    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([20.0, 2.0]) * q_scale
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5 * r_scale]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    return np.linalg.inv(R) @ B.T @ P



# Execute this portion of the controller design or analysis workflow.
def evaluate(K, rng, trials=100):
    """Execute this portion of the controller design or analysis workflow."""
    final_errors = []
    efforts = []

    # Step through the simulation or design cases one sample at a time.
    for _ in range(trials):
        stiffness = rng.uniform(1.5, 2.5)
        damping = rng.uniform(0.25, 0.9)
        gain = rng.uniform(0.8, 1.2)


        # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
        A = np.array([[0.0, 1.0], [-stiffness, -damping]])
        # Define the input matrix B. It maps the commanded control input into the state derivatives.
        B = np.array([[0.0], [gain]])

        x = np.array([[1.0], [0.0]])

        # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
        dt = 0.01

        trial_effort = []

        # Step through the simulation or design cases one sample at a time.
        for _ in range(800):
            u = -K @ x
            # Integrate the state forward with the explicit Euler method.
            x = x + (A @ x + B @ u) * dt
            trial_effort.append(abs(float(u[0, 0])))

        final_errors.append(abs(x[0, 0]))
        efforts.append(np.mean(trial_effort))

    return np.mean(final_errors), np.mean(efforts)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    rng = np.random.default_rng(17)

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])

    candidates = [
        ("Conservative", 0.5, 2.0),
        ("Balanced", 1.0, 1.0),
        ("Aggressive", 2.0, 0.5),
    ]

    # Step through the simulation or design cases one sample at a time.
    for name, q, r in candidates:
        K = lqr_gain(A, B, q, r)
        error, effort = evaluate(K, rng)
        print(f"{name:>12}: mean final error={error:.5f}, mean effort={effort:.4f}")



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
