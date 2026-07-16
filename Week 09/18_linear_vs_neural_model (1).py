"""
Compare linear ARX and neural-network models.

Learn:
- White-box vs black-box tradeoffs
- Nonlinearity capture
"""

import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error


def main():
    rng = np.random.default_rng(18)
    n = 2200
    u = rng.normal(0,1,n)
    y = np.zeros(n)

    for k in range(2,n):
        y[k] = (
            0.75*y[k-1]
            - 0.1*y[k-2]
            + 0.3*np.tanh(1.5*u[k-1])
            + 0.08*u[k-2]**2
            + rng.normal(0,0.025)
        )

    X=[]; Y=[]
    for k in range(2,n):
        X.append([y[k-1],y[k-2],u[k-1],u[k-2]])
        Y.append(y[k])
    X=np.asarray(X); Y=np.asarray(Y)
    split=1600

    theta=np.linalg.lstsq(X[:split],Y[:split],rcond=None)[0]
    linear_pred=X[split:]@theta

    nn=MLPRegressor(hidden_layer_sizes=(24,24),max_iter=800,random_state=18)
    nn.fit(X[:split],Y[:split])
    nn_pred=nn.predict(X[split:])

    linear_rmse=np.sqrt(mean_squared_error(Y[split:],linear_pred))
    nn_rmse=np.sqrt(mean_squared_error(Y[split:],nn_pred))

    print(f"Linear RMSE: {linear_rmse:.5f}")
    print(f"Neural RMSE: {nn_rmse:.5f}")


if __name__ == "__main__":
    main()
