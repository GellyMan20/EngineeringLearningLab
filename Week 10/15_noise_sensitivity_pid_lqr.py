# ==========================================================================
# Project 15 — PID and LQR Noise Sensitivity
# ==========================================================================
#
# Purpose:
# Compare how measurement noise influences PID and state-feedback control signals.
#
# Why This Matters:
# No controller operates on perfect measurements; noise affects loads, actuator wear, and stability margins.
#
# Key Concepts:
# - Measurement noise
# - Derivative amplification
# - Control chatter
# - Filtering considerations
#
# Mathematical Foundation:
# - Measured state = true state + sensor noise
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
        derivative = (error - self.prev) / dt
        self.prev = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    rng = np.random.default_rng(15)

    # Choose the simulation timestep. It must be small relative to the fastest system dynamics.
    dt = 0.01
    # Build the simulation time vector.
    t = np.arange(0, 10, dt)


    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.5]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Solve the continuous algebraic Riccati equation for the optimal cost-to-go matrix P.
    P = solve_continuous_are(A, B, np.diag([20.0, 2.0]), np.array([[0.5]]))
    # Convert the Riccati solution into the optimal state-feedback gain K.
    K = np.linalg.inv(np.array([[0.5]])) @ B.T @ P

    pid = PID(8.0, 1.0, 3.0)
    pid_state = np.zeros((2, 1))
    lqr_state = np.zeros((2, 1))
    target = 1.0

    pid_u = []
    lqr_u = []

    # Step through the simulation or design cases one sample at a time.
    for _ in t:
        noisy_pos_pid = pid_state[0, 0] + rng.normal(0, 0.02)
        noisy_pos_lqr = lqr_state[0, 0] + rng.normal(0, 0.02)
        noisy_vel_lqr = lqr_state[1, 0] + rng.normal(0, 0.03)

        u_pid = pid.update(target - noisy_pos_pid, dt)
        error_state = np.array([[noisy_pos_lqr - target], [noisy_vel_lqr]])
        u_lqr = float((-K @ error_state)[0, 0] + 2.0 * target)

        pid_state = pid_state + (A @ pid_state + B * u_pid) * dt
        lqr_state = lqr_state + (A @ lqr_state + B * u_lqr) * dt

        pid_u.append(u_pid)
        lqr_u.append(u_lqr)


    # Create a separate figure so this result can be reviewed independently.
    plt.figure()
    # Plot the relevant response history for visual comparison.
    plt.plot(t, pid_u, label="PID control")
    # Plot the relevant response history for visual comparison.
    plt.plot(t, lqr_u, label="LQR control")
    plt.title("Noise Sensitivity")
    plt.xlabel("Time [s]")
    plt.ylabel("Control effort")
    plt.grid(True)
    plt.legend()
    # Display all completed figures.
    plt.show()



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
