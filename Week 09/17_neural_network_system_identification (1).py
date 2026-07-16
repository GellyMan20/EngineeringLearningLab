"""
Neural-network system identification using scikit-learn.

Learn:
- Nonlinear black-box modeling
- Train/test split
- Feature construction

Install:
    pip install scikit-learn
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error


def main():
    rng = np.random.default_rng(17)
    n = 2500
    u = rng.normal(0,1,n)
    y = np.zeros(n)

    for k in range(2,n):
        y[k] = (
            0.8*y[k-1]
            - 0.15*y[k-2]
            + 0.25*np.tanh(u[k-1])
            + 0.05*u[k-2]**2
            + rng.normal(0,0.02)
        )

    X = []
    target = []
    for k in range(2,n):
        X.append([y[k-1],y[k-2],u[k-1],u[k-2]])
        target.append(y[k])

    X = np.asarray(X)
    target = np.asarray(target)
    split = 1800

    model = MLPRegressor(
        hidden_layer_sizes=(32,32),
        activation="tanh",
        max_iter=1000,
        random_state=17,
    )
    model.fit(X[:split], target[:split])

    pred = model.predict(X[split:])
    rmse = np.sqrt(mean_squared_error(target[split:], pred))
    print(f"Validation RMSE: {rmse:.5f}")

    plt.figure()
    plt.plot(target[split:split+300], label="Truth")
    plt.plot(pred[:300], label="Neural network")
    plt.title("Neural Network System Identification")
    plt.xlabel("Sample")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
