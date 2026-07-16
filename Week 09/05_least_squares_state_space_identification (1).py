"""
Identify a discrete-time linear state-space model:

    x[k+1] = A*x[k] + B*u[k]

Learn:
- State-space identification
- Matrix least squares
"""

import numpy as np


def main():
    rng = np.random.default_rng(5)

    A_true = np.array([[1.0, 0.1], [0.0, 0.96]])
    B_true = np.array([[0.005], [0.10]])

    n = 1200
    x = np.zeros((2, n))
    u = rng.normal(0, 1.0, n - 1)

    for k in range(n - 1):
        process_noise = rng.normal(0, 0.005, 2)
        x[:, k+1] = A_true @ x[:, k] + B_true[:, 0] * u[k] + process_noise

    X = x[:, :-1]
    X_next = x[:, 1:]
    U = u.reshape(1, -1)

    regressor = np.vstack((X, U))
    theta = X_next @ np.linalg.pinv(regressor)

    A_est = theta[:, :2]
    B_est = theta[:, 2:]

    print("True A:")
    print(A_true)
    print("\nEstimated A:")
    print(A_est)
    print("\nTrue B:")
    print(B_true)
    print("\nEstimated B:")
    print(B_est)


if __name__ == "__main__":
    main()
