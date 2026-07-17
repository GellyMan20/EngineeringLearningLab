# Project 19 — Residual-Based Anomaly Detection
# Purpose:
# This script detects abnormal system behavior by monitoring the difference between measured output and model prediction.
#
# Key Concepts:
# - Residual monitoring
# - Threshold detection
# - Fault detection
# - Model-based anomaly detection
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
    rng = np.random.default_rng(19)
    n = 1200
    u = rng.normal(0,1,n)
    y = np.zeros(n)

    for k in range(1,n):
        y[k] = 0.9*y[k-1] + 0.25*u[k-1] + rng.normal(0,0.03)

    # Inject changed dynamics.
    for k in range(700,850):
        y[k] += 0.4

    Phi = np.column_stack((y[:599],u[:599]))
    target = y[1:600]
# Solve for the parameter values that minimize the total squared prediction error.
    theta = np.linalg.lstsq(Phi,target,rcond=None)[0]

    prediction = theta[0]*y[:-1] + theta[1]*u[:-1]
    residual = y[1:] - prediction

    baseline_std = np.std(residual[:500],ddof=1)
    threshold = 4*baseline_std
    flags = np.abs(residual) > threshold

    print(f"Anomaly samples detected: {flags.sum()}")


# Create a new figure for this result.
    plt.figure()
    plt.plot(residual,label="Residual")
    plt.axhline(threshold,linestyle="--",label="Threshold")
    plt.axhline(-threshold,linestyle="--")
    plt.scatter(np.where(flags)[0],residual[flags],marker="x",label="Anomaly")
    plt.title("Residual-Based Anomaly Detection")
    plt.xlabel("Sample")
    plt.ylabel("Residual")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
