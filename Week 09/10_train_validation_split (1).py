"""
Fit on one dataset and validate on another.

Learn:
- Training vs validation
- Generalization
- Overfitting avoidance
"""

import numpy as np


def simulate(theta, u, y0=(0.0, 0.0)):
    y = np.zeros(len(u))
    y[0], y[1] = y0
    for k in range(2, len(u)):
        y[k] = (
            theta[0]*y[k-1]
            + theta[1]*y[k-2]
            + theta[2]*u[k-1]
            + theta[3]*u[k-2]
        )
    return y


def fit_arx(u, y):
    Phi, Y = [], []
    for k in range(2, len(y)):
        Phi.append([y[k-1], y[k-2], u[k-1], u[k-2]])
        Y.append(y[k])
    return np.linalg.lstsq(np.asarray(Phi), np.asarray(Y), rcond=None)[0]


def main():
    rng = np.random.default_rng(10)
    true_theta = np.array([1.35, -0.48, 0.22, 0.10])

    u_train = rng.normal(0, 1, 1200)
    y_train = simulate(true_theta, u_train)
    y_train += rng.normal(0, 0.03, len(y_train))

    u_val = 0.8*np.sin(np.linspace(0, 40, 800)) + rng.normal(0, 0.25, 800)
    y_val = simulate(true_theta, u_val)
    y_val += rng.normal(0, 0.03, len(y_val))

    theta_est = fit_arx(u_train, y_train)
    y_pred = simulate(theta_est, u_val, y0=(y_val[0], y_val[1]))

    rmse = np.sqrt(np.mean((y_val - y_pred)**2))

    print("Estimated parameters:", theta_est)
    print(f"Validation RMSE: {rmse:.4f}")


if __name__ == "__main__":
    main()
