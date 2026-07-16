"""
Detect anomalies using model residuals.

Learn:
- Residual-based monitoring
- AI-assisted anomaly detection concept
"""

import numpy as np
import matplotlib.pyplot as plt


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
    theta = np.linalg.lstsq(Phi,target,rcond=None)[0]

    prediction = theta[0]*y[:-1] + theta[1]*u[:-1]
    residual = y[1:] - prediction

    baseline_std = np.std(residual[:500],ddof=1)
    threshold = 4*baseline_std
    flags = np.abs(residual) > threshold

    print(f"Anomaly samples detected: {flags.sum()}")

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
    plt.show()


if __name__ == "__main__":
    main()
