# Project 13 — Recursive Least Squares
# Purpose:
# This script estimates parameters online as new telemetry arrives and uses a forgetting factor to track changing dynamics.
#
# Key Concepts:
# - Online identification
# - Recursive estimation
# - Forgetting factors
# - Time-varying systems
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np
# Import Matplotlib to visualize telemetry, model predictions, residuals, and trade studies.
import matplotlib.pyplot as plt



# Main project workflow
def main():
    rng = np.random.default_rng(13)
    n = 1200
    u = rng.normal(0, 1, n)
    y = np.zeros(n)

    a_true = np.where(np.arange(n) < 600, 0.92, 0.82)
    b_true = 0.25

    for k in range(1, n):
        y[k] = a_true[k]*y[k-1] + b_true*u[k-1] + rng.normal(0, 0.03)

    theta = np.zeros(2)
    P = np.eye(2)*1000
    lam = 0.995
    history = []

    for k in range(1, n):
        phi = np.array([y[k-1], u[k-1]])
        gain = P @ phi / (lam + phi.T @ P @ phi)
        prediction_error = y[k] - phi.T @ theta
        theta = theta + gain*prediction_error
        P = (P - np.outer(gain, phi.T @ P)) / lam
        history.append(theta.copy())

    history = np.array(history)


# Create a new figure for this result.
    plt.figure()
    plt.plot(a_true[1:], label="True a")
    plt.plot(history[:,0], label="Estimated a")
    plt.title("Recursive Least Squares")
    plt.xlabel("Sample")
    plt.ylabel("Parameter")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
