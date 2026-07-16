"""
Recursive least squares for online parameter estimation.

Learn:
- Online identification
- Forgetting factor
- Time-varying parameter tracking
"""

import numpy as np
import matplotlib.pyplot as plt


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

    plt.figure()
    plt.plot(a_true[1:], label="True a")
    plt.plot(history[:,0], label="Estimated a")
    plt.title("Recursive Least Squares")
    plt.xlabel("Sample")
    plt.ylabel("Parameter")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
