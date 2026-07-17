# ==========================================================================
# Project 12 — Monte Carlo Controller Robustness
# ==========================================================================
#
# Purpose:
# Run many randomized plant cases to estimate the distribution of controller performance under uncertainty.
#
# Why This Matters:
# Monte Carlo testing is standard for evaluating dispersed trajectories, navigation errors, and flight-control robustness.
#
# Key Concepts:
# - Monte Carlo analysis
# - Randomized parameters
# - Performance distributions
# - Probabilistic verification
#
# Mathematical Foundation:
# - Performance is summarized as a distribution, not a single value
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
def run_trial(rng, K):
    """Execute this portion of the controller design or analysis workflow."""
    stiffness = rng.uniform(1.4, 2.6)
    damping = rng.uniform(0.25, 0.9)
    input_gain = rng.uniform(0.7, 1.3)


    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-stiffness, -damping]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [input_gain]])


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 8, dt)
    x = np.array([[1.0], [0.0]])
    positions = []
    efforts = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        u = -K @ x
        # Integrate the state forward with the explicit Euler method.
        x = x + (A @ x + B @ u) * dt
        positions.append(x[0, 0])
        efforts.append(abs(float(u[0, 0])))

    positions = np.array(positions)
    settling_error = abs(positions[-1])
    max_error = np.max(abs(positions))
    effort = np.mean(efforts)
    success = settling_error < 0.02 and np.all(np.isfinite(positions))

    return settling_error, max_error, effort, success



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    rng = np.random.default_rng(12)

    A_nom = np.array([[0.0, 1.0], [-2.0, -0.5]])
    B_nom = np.array([[0.0], [1.0]])
    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([20.0, 2.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A_nom, B_nom, Q, R)
    K = np.linalg.inv(R) @ B_nom.T @ P

    results = np.array([run_trial(rng, K) for _ in range(400)], dtype=object)
    settling = results[:, 0].astype(float)
    effort = results[:, 2].astype(float)
    success = results[:, 3].astype(bool)

    print(f"Success rate: {100*np.mean(success):.1f}%")
    print(f"Mean final error: {np.mean(settling):.4f}")
    print(f"Mean control effort: {np.mean(effort):.4f}")


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    plt.hist(settling, bins=30)
    plt.title("Monte Carlo Final Error")
    plt.xlabel("Final absolute error")
    plt.ylabel("Count")
    plt.grid(True)
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
