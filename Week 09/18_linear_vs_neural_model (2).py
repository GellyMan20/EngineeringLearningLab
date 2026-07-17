# Project 18 — Linear versus Neural Model
# Purpose:
# This script compares a linear model with a neural-network model on nonlinear dynamics.
#
# Key Concepts:
# - Linear models
# - Neural models
# - Interpretability
# - Validation comparison
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np
# Import scikit-learn tools for neural-network modeling and validation metrics.
from sklearn.neural_network import MLPRegressor
# Import scikit-learn tools for neural-network modeling and validation metrics.
from sklearn.metrics import mean_squared_error



# Main project workflow
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

# Solve for the parameter values that minimize the total squared prediction error.
    theta=np.linalg.lstsq(X[:split],Y[:split],rcond=None)[0]
    linear_pred=X[split:]@theta

    nn=MLPRegressor(hidden_layer_sizes=(24,24),max_iter=800,random_state=18)
    nn.fit(X[:split],Y[:split])
    nn_pred=nn.predict(X[split:])

    linear_rmse=np.sqrt(mean_squared_error(Y[split:],linear_pred))
    nn_rmse=np.sqrt(mean_squared_error(Y[split:],nn_pred))

    print(f"Linear RMSE: {linear_rmse:.5f}")
    print(f"Neural RMSE: {nn_rmse:.5f}")



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
