# Project 06 — ARX Model Identification
# Purpose:
# This script identifies an Auto-Regressive model with eXogenous inputs using past outputs and inputs to predict the next output sample.
#
# Key Concepts:
# - ARX models
# - Lagged regressors
# - Input/output identification
# - Prediction validation
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
    rng = np.random.default_rng(6)
    n = 1500
    u = rng.normal(0, 1.0, n)
    y = np.zeros(n)

    true_theta = np.array([1.4, -0.52, 0.25, 0.08])

    for k in range(2, n):
        phi = np.array([y[k-1], y[k-2], u[k-1], u[k-2]])
        y[k] = phi @ true_theta + rng.normal(0, 0.03)

    Phi = []
    Y = []
    for k in range(2, n):
        Phi.append([y[k-1], y[k-2], u[k-1], u[k-2]])
        Y.append(y[k])

    Phi = np.asarray(Phi)
    Y = np.asarray(Y)
# Solve for the parameter values that minimize the total squared prediction error.
    theta_est = np.linalg.lstsq(Phi, Y, rcond=None)[0]

    y_hat = Phi @ theta_est

    print("True parameters:", true_theta)
    print("Estimated parameters:", theta_est)


# Create a new figure for this result.
    plt.figure()
    plt.plot(Y[:300], label="Measured output")
    plt.plot(y_hat[:300], label="ARX prediction")
    plt.title("ARX Model Identification")
    plt.xlabel("Sample")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
