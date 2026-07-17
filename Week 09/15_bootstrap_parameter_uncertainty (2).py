# Project 15 — Bootstrap Parameter Uncertainty
# Purpose:
# This script uses bootstrap resampling to estimate parameter uncertainty and a confidence interval.
#
# Key Concepts:
# - Bootstrap resampling
# - Confidence intervals
# - Parameter uncertainty
# - Statistical robustness
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np



# Main project workflow
def main():
    rng = np.random.default_rng(15)
    n = 1000
    x = rng.uniform(0, 10, n)
    true_slope = 2.5
    y = true_slope*x + rng.normal(0, 2.0, n)

    estimates = []
    for _ in range(500):
        idx = rng.integers(0, n, n)
# Solve for the parameter values that minimize the total squared prediction error.
        slope = np.linalg.lstsq(x[idx].reshape(-1,1), y[idx], rcond=None)[0][0]
        estimates.append(slope)

    estimates = np.asarray(estimates)
    print(f"Mean estimate: {np.mean(estimates):.4f}")
    print(f"95% CI: [{np.percentile(estimates,2.5):.4f}, {np.percentile(estimates,97.5):.4f}]")



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
