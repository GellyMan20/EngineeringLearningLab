# ==========================================================================
# Project 07 — PID vs LQR Disturbance Rejection
# ==========================================================================
#
# Purpose:
# Compare how PID and LQR respond when an external disturbance acts on the plant.
#
# Why This Matters:
# Aircraft gust rejection and spacecraft disturbance-torque rejection are representative applications.
#
# Key Concepts:
# - Disturbance rejection
# - Recovery time
# - Transient error
# - Controller comparison
#
# Mathematical Foundation:
# - Disturbance enters the state dynamics as an additional forcing term
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



# Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices.
def lqr_gain(A, B, Q, R):
    """Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices."""
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    return np.linalg.inv(R) @ B.T @ P



# Execute this portion of the controller design or analysis workflow.
def simulate(kind):
    """Execute this portion of the controller design or analysis workflow."""

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 12, dt)
    x = 0.0
    v = 0.0
    target = 1.0

    if kind == "PID":
        controller = PID(8.0, 1.2, 3.0)
    else:

        # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
        A = np.array([[0.0, 1.0], [-2.0, -0.5]])
        # Define the input matrix B. It maps the commanded control input into the state derivatives.
        B = np.array([[0.0], [1.0]])
        K = lqr_gain(A, B, np.diag([20.0, 2.0]), np.array([[0.5]]))

    xs = []

    # Step through the simulation or design cases one sample at a time.
    for time in t:
        disturbance = -2.0 if 5 <= time <= 6.5 else 0.0

        if kind == "PID":
            u = controller.update(target - x, dt)
        else:
            state_error = np.array([[x - target], [v]])
            u = float((-K @ state_error)[0, 0] + 2.0 * target)

        a = u + disturbance - 0.5 * v - 2.0 * x
        v += a * dt
        x += v * dt
        xs.append(x)

    return t, np.array(xs)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    t, pid = simulate("PID")
    _, lqr = simulate("LQR")


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, pid, label="PID")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, lqr, label="LQR")
    plt.axhline(1.0, linestyle="--", label="Target")
    plt.axvspan(5, 6.5, alpha=0.2, label="Disturbance")
    plt.title("PID vs LQR Disturbance Rejection")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
