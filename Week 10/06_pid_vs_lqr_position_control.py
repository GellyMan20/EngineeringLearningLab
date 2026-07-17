# ==========================================================================
# Project 06 — PID vs LQR Position Control
# ==========================================================================
#
# Purpose:
# Compare classical PID control with optimal state feedback for reference tracking and control effort.
#
# Why This Matters:
# Controller selection should be based on architecture, available state estimates, certification burden, and mission performance—not fashion.
#
# Key Concepts:
# - PID control
# - LQR control
# - Tracking error
# - Control-effort comparison
#
# Mathematical Foundation:
# - PID: u = Kp e + Ki integral(e) + Kd de/dt
# - LQR: u = -K(x - x_ref) + feedforward
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
    def __init__(self, kp, ki, kd, limits=(-20, 20)):
        """Execute this portion of the controller design or analysis workflow."""
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.limits = limits
        self.integral = 0.0
        self.prev_error = 0.0


    # Advance the controller by one sample using the current error and timestep.
    def update(self, error, dt):
        """Advance the controller by one sample using the current error and timestep."""
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        # Enforce the physical command limits before the control input reaches the plant.
        return float(np.clip(
            self.kp * error + self.ki * self.integral + self.kd * derivative,
            *self.limits
        ))



# Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices.
def lqr_gain(A, B, Q, R):
    """Compute the continuous-time LQR state-feedback gain for the supplied plant and weighting matrices."""
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, Q, R)
    return np.linalg.inv(R) @ B.T @ P



# Simulate the plant using the selected PID controller and return time, response, and control histories.
def simulate_pid():
    """Simulate the plant using the selected PID controller and return time, response, and control histories."""

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)
    x = 0.0
    v = 0.0
    target = 1.0
    pid = PID(8.0, 1.5, 3.0)
    xs = []
    us = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        u = pid.update(target - x, dt)
        a = u - 0.5 * v - 2.0 * x
        v += a * dt
        x += v * dt
        xs.append(x)
        us.append(u)

    return t, np.array(xs), np.array(us)



# Simulate the plant using the selected LQR controller and return time, response, and control histories.
def simulate_lqr():
    """Simulate the plant using the selected LQR controller and return time, response, and control histories."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Set state penalties. Larger entries demand tighter regulation of the corresponding states.
    Q = np.diag([20.0, 2.0])
    # Set the control penalty. Larger values reduce actuator use but usually slow the response.
    R = np.array([[0.5]])
    K = lqr_gain(A, B, Q, R)


    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)
    target = 1.0
    state = np.array([[0.0], [0.0]])
    reference = np.array([[target], [0.0]])
    xs = []
    us = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        error_state = state - reference
        u = -K @ error_state + 2.0 * target
        # Integrate the state forward with the explicit Euler method.
        state = state + (A @ state + B @ u) * dt
        xs.append(state[0, 0])
        us.append(float(u[0, 0]))

    return t, np.array(xs), np.array(us)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    t, pid_x, pid_u = simulate_pid()
    _, lqr_x, lqr_u = simulate_lqr()


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, pid_x, label="PID")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, lqr_x, label="LQR")
    plt.axhline(1.0, linestyle="--", label="Target")
    plt.title("PID vs LQR Position Tracking")
    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, pid_u, label="PID effort")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, lqr_u, label="LQR effort")
    plt.title("PID vs LQR Control Effort")
    plt.xlabel("Time [s]")
    plt.ylabel("u")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
