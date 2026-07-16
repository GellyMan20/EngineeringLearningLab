"""
Perform residual analysis after model fitting.

Learn:
- Residual mean
- Residual variance
- Autocorrelation
- Model adequacy
"""

import numpy as np
import matplotlib.pyplot as plt


def autocorrelation(x, max_lag):
    x = x - np.mean(x)
    result = []
    denom = np.dot(x, x)
    for lag in range(max_lag + 1):
        result.append(np.dot(x[:len(x)-lag], x[lag:]) / denom)
    return np.array(result)


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
    theta = np.linalg.lstsq(Phi, target, rcond=None)[0]
    prediction = Phi @ theta
    residual = target - prediction

    print(f"Residual mean: {np.mean(residual):.5f}")
    print(f"Residual std:  {np.std(residual, ddof=1):.5f}")

    acf = autocorrelation(residual, 40)

    plt.figure()
    plt.plot(residual)
    plt.title("Residual Sequence")
    plt.xlabel("Sample")
    plt.ylabel("Residual")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.stem(np.arange(len(acf)), acf)
    plt.title("Residual Autocorrelation")
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
