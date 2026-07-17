# ==========================================================================
# Project 21 — PID–LQR Batch Comparison
# ==========================================================================
#
# Purpose:
# Evaluate PID and LQR repeatedly across a set of plant and disturbance conditions.
#
# Why This Matters:
# Batch analysis exposes brittle tuning that may look acceptable in a single hand-picked scenario.
#
# Key Concepts:
# - Batch simulation
# - Controller benchmarking
# - Scenario matrices
# - Statistical comparison
#
# Mathematical Foundation:
# - Batch statistics reveal mean, spread, and worst-case behavior
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



# Classical PID controller used as a benchmark against state-feedback methods.
class PID:

    # Execute this portion of the controller design or analysis workflow.
    def __init__(self, kp, ki, kd):
        """Execute this portion of the controller design or analysis workflow."""
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev = 0


    # Advance the controller by one sample using the current error and timestep.
    def update(self, error, dt):
        """Advance the controller by one sample using the current error and timestep."""
        self.integral += error * dt
        d = (error - self.prev) / dt
        self.prev = error
        return self.kp * error + self.ki * self.integral + self.kd * d



# Execute this portion of the controller design or analysis workflow.
def evaluate(kind, stiffness, damping, disturbance):
    """Execute this portion of the controller design or analysis workflow."""

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    target = 1.0
    x = 0.0
    v = 0.0
    errors = []
    efforts = []

    if kind == "PID":
        controller = PID(8.0, 1.2, 3.0)
    else:
        A_nom = np.array([[0.0, 1.0], [-2.0, -0.5]])
        B_nom = np.array([[0.0], [1.0]])
        # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
        P = solve_continuous_are(A_nom, B_nom, np.diag([20.0, 2.0]), np.array([[0.5]]))
        K = np.linalg.inv(np.array([[0.5]])) @ B_nom.T @ P

    # Step through the simulation or design cases one sample at a time.
    for k in range(1000):
        time = k * dt
        d = disturbance if 4 <= time <= 5 else 0.0

        if kind == "PID":
            u = controller.update(target - x, dt)
        else:
            u = float((-K @ np.array([[x-target], [v]]))[0, 0] + 2.0 * target)

        a = u + d - damping * v - stiffness * x
        v += a * dt
        x += v * dt

        errors.append(abs(target - x))
        efforts.append(abs(u))

    return np.mean(errors), np.mean(efforts)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    scenarios = [
        (1.7, 0.4, -1.0),
        (2.0, 0.5, -2.0),
        (2.4, 0.8, -1.5),
        (1.5, 0.3, -2.5),
    ]

    # Step through the simulation or design cases one sample at a time.
    for kind in ["PID", "LQR"]:
        metrics = [evaluate(kind, *scenario) for scenario in scenarios]
        mean_error = np.mean([m[0] for m in metrics])
        mean_effort = np.mean([m[1] for m in metrics])
        print(f"{kind}: mean error={mean_error:.4f}, mean effort={mean_effort:.4f}")



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
