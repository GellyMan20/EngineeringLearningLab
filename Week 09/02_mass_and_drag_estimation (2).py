# Project 02 — Mass and Drag Estimation
# Purpose:
# This script estimates both vehicle mass and linear drag from input and velocity telemetry by rewriting the physical dynamics as a multi-parameter regression problem.
#
# Key Concepts:
# - Multi-parameter estimation
# - Regression matrices
# - Physical parameter recovery
# - Identifiability
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
    rng = np.random.default_rng(2)
    dt = 0.05
    t = np.arange(0, 60, dt)

    true_mass = 1200.0
    true_drag = 90.0
    force = 2500 + 1200 * np.sin(0.18 * t) + 400 * np.sin(0.7 * t)

    velocity = np.zeros_like(t)
    for k in range(1, len(t)):
        acceleration = (force[k - 1] - true_drag * velocity[k - 1]) / true_mass
        velocity[k] = velocity[k - 1] + acceleration * dt

    measured_v = velocity + rng.normal(0, 0.08, len(t))
# Estimate acceleration numerically from the measured velocity history.
    measured_a = np.gradient(measured_v, dt)

    # a = alpha*u + beta*v, where alpha=1/m, beta=-c/m
    phi = np.column_stack((force, measured_v))
# Solve for the parameter values that minimize the total squared prediction error.
    theta = np.linalg.lstsq(phi, measured_a, rcond=None)[0]

    alpha, beta = theta
    estimated_mass = 1.0 / alpha
    estimated_drag = -beta * estimated_mass

    print(f"True mass:      {true_mass:.2f} kg")
    print(f"Estimated mass: {estimated_mass:.2f} kg")
    print(f"True drag:      {true_drag:.2f}")
    print(f"Estimated drag: {estimated_drag:.2f}")



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
