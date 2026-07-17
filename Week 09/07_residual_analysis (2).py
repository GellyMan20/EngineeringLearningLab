# Project 07 — Residual Analysis
# Purpose:
# This script checks whether model prediction errors are unbiased and approximately uncorrelated, helping reveal missing dynamics.
#
# Key Concepts:
# - Residual statistics
# - Autocorrelation
# - Model adequacy
# - Underfitting detection
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


def autocorrelation(x, max_lag):
    x = x - np.mean(x)
    result = []
    denom = np.dot(x, x)
    for lag in range(max_lag + 1):
        result.append(np.dot(x[:len(x)-lag], x[lag:]) / denom)
    return np.array(result)



# Main project workflow
def main():
    rng = np.random.default_rng(7)
    n = 1000
    u = rng.normal(0, 1.0, n)
    y = np.zeros(n)

    for k in range(2, n):
        y[k] = 1.2*y[k-1] - 0.4*y[k-2] + 0.3*u[k-1] + rng.normal(0, 0.05)

    # Intentionally underfit with first-order model.
    Phi = np.column_stack((y[1:-1], u[1:-1]))
    target = y[2:]
# Solve for the parameter values that minimize the total squared prediction error.
    theta = np.linalg.lstsq(Phi, target, rcond=None)[0]
    prediction = Phi @ theta
    residual = target - prediction

    print(f"Residual mean: {np.mean(residual):.5f}")
    print(f"Residual std:  {np.std(residual, ddof=1):.5f}")

    acf = autocorrelation(residual, 40)


# Create a new figure for this result.
    plt.figure()
    plt.plot(residual)
    plt.title("Residual Sequence")
    plt.xlabel("Sample")
    plt.ylabel("Residual")
    plt.grid(True)
# Display the completed visualization.
    plt.show()


# Create a new figure for this result.
    plt.figure()
    plt.stem(np.arange(len(acf)), acf)
    plt.title("Residual Autocorrelation")
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation")
    plt.grid(True)
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
