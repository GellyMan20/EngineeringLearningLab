# Project 12 — Nonlinear Parameter Estimation
# Purpose:
# This script uses SciPy nonlinear least squares to estimate mass, linear drag, and quadratic drag.
#
# Key Concepts:
# - Nonlinear least squares
# - SciPy optimization
# - Quadratic drag
# - Bounded estimation
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np
# Import SciPy tools for optimization or numerical system analysis.
from scipy.optimize import least_squares


def simulate(params, force, dt):
    mass, c1, c2 = params
    v = np.zeros(len(force))
    for k in range(1, len(force)):
        drag = c1*v[k-1] + c2*v[k-1]*abs(v[k-1])
        a = (force[k-1] - drag) / mass
        v[k] = v[k-1] + a*dt
    return v



# Main project workflow
def main():
    rng = np.random.default_rng(12)
    dt = 0.05
    t = np.arange(0, 50, dt)
    force = 2200 + 900*np.sin(0.2*t) + 500*np.sin(0.9*t)

    true_params = np.array([1100.0, 50.0, 2.0])
    measured = simulate(true_params, force, dt) + rng.normal(0, 0.04, len(t))

    def residual(params):
        return simulate(params, force, dt) - measured

# Run bounded nonlinear optimization to minimize the model-to-telemetry mismatch.
    result = least_squares(
        residual,
        x0=np.array([900.0, 30.0, 1.0]),
        bounds=([500, 0, 0], [2000, 200, 10]),
    )

    print("True parameters:     ", true_params)
    print("Estimated parameters:", result.x)
    print("Cost:", result.cost)



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
