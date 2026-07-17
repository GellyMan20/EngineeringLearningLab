# Project 08 — Input Excitation Comparison
# Purpose:
# This script compares parameter estimates obtained from weak and rich excitation signals to demonstrate why informative telemetry matters.
#
# Key Concepts:
# - Persistent excitation
# - Experiment design
# - Parameter reliability
# - Telemetry quality
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np


def identify(u, rng):
    dt = 0.05
    true_mass = 900.0
    true_drag = 65.0
    v = np.zeros(len(u))

    for k in range(1, len(u)):
        a = (u[k-1] - true_drag*v[k-1]) / true_mass
        v[k] = v[k-1] + a*dt

    measured_v = v + rng.normal(0, 0.04, len(v))
# Estimate acceleration numerically from the measured velocity history.
    measured_a = np.gradient(measured_v, dt)

    phi = np.column_stack((u, measured_v))
# Solve for the parameter values that minimize the total squared prediction error.
    alpha, beta = np.linalg.lstsq(phi, measured_a, rcond=None)[0]
    mass = 1 / alpha
    drag = -beta * mass
    return mass, drag



# Main project workflow
def main():
    rng = np.random.default_rng(8)
    n = 2000
    t = np.arange(n) * 0.05

    weak_input = np.full(n, 1800.0)
    rich_input = 1800 + 900*np.sin(0.2*t) + 500*np.sin(0.9*t) + rng.normal(0, 120, n)

    weak_est = identify(weak_input, rng)
    rich_est = identify(rich_input, rng)

    print("Weak excitation estimate (mass, drag):", weak_est)
    print("Rich excitation estimate (mass, drag):", rich_est)



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
