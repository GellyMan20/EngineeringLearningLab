"""
Estimate mass and linear drag from input/output data.

Model:
    m*a = u - c*v
    a = (1/m)u - (c/m)v

Learn:
- Multi-parameter least squares
- Physical parameter recovery
"""

import numpy as np


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
    measured_a = np.gradient(measured_v, dt)

    # a = alpha*u + beta*v, where alpha=1/m, beta=-c/m
    phi = np.column_stack((force, measured_v))
    theta = np.linalg.lstsq(phi, measured_a, rcond=None)[0]

    alpha, beta = theta
    estimated_mass = 1.0 / alpha
    estimated_drag = -beta * estimated_mass

    print(f"True mass:      {true_mass:.2f} kg")
    print(f"Estimated mass: {estimated_mass:.2f} kg")
    print(f"True drag:      {true_drag:.2f}")
    print(f"Estimated drag: {estimated_drag:.2f}")


if __name__ == "__main__":
    main()
