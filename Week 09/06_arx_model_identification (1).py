"""
Identify an ARX model:

    y[k] = a1*y[k-1] + a2*y[k-2] + b1*u[k-1] + b2*u[k-2]

Learn:
- Auto-regressive models
- Input/output telemetry modeling
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    rng = np.random.default_rng(6)
    n = 1500
    u = rng.normal(0, 1.0, n)
    y = np.zeros(n)

    true_theta = np.array([1.4, -0.52, 0.25, 0.08])

    for k in range(2, n):
        phi = np.array([y[k-1], y[k-2], u[k-1], u[k-2]])
        y[k] = phi @ true_theta + rng.normal(0, 0.03)

    Phi = []
    Y = []
    for k in range(2, n):
        Phi.append([y[k-1], y[k-2], u[k-1], u[k-2]])
        Y.append(y[k])

    Phi = np.asarray(Phi)
    Y = np.asarray(Y)
    theta_est = np.linalg.lstsq(Phi, Y, rcond=None)[0]

    y_hat = Phi @ theta_est

    print("True parameters:", true_theta)
    print("Estimated parameters:", theta_est)

    plt.figure()
    plt.plot(Y[:300], label="Measured output")
    plt.plot(y_hat[:300], label="ARX prediction")
    plt.title("ARX Model Identification")
    plt.xlabel("Sample")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
