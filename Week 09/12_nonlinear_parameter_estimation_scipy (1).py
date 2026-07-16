"""
Estimate nonlinear quadratic drag using scipy.optimize.

Model:
    m*dv/dt = u - c1*v - c2*v*|v|

Learn:
- Nonlinear least squares
- SciPy optimization
"""

import numpy as np
from scipy.optimize import least_squares


def simulate(params, force, dt):
    mass, c1, c2 = params
    v = np.zeros(len(force))
    for k in range(1, len(force)):
        drag = c1*v[k-1] + c2*v[k-1]*abs(v[k-1])
        a = (force[k-1] - drag) / mass
        v[k] = v[k-1] + a*dt
    return v


def main():
    rng = np.random.default_rng(12)
    dt = 0.05
    t = np.arange(0, 50, dt)
    force = 2200 + 900*np.sin(0.2*t) + 500*np.sin(0.9*t)

    true_params = np.array([1100.0, 50.0, 2.0])
    measured = simulate(true_params, force, dt) + rng.normal(0, 0.04, len(t))

    def residual(params):
        return simulate(params, force, dt) - measured

    result = least_squares(
        residual,
        x0=np.array([900.0, 30.0, 1.0]),
        bounds=([500, 0, 0], [2000, 200, 10]),
    )

    print("True parameters:     ", true_params)
    print("Estimated parameters:", result.x)
    print("Cost:", result.cost)


if __name__ == "__main__":
    main()
