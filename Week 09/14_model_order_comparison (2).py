# Project 14 — Model Order Comparison
# Purpose:
# This script compares ARX models of different orders using validation error.
#
# Key Concepts:
# - Model order selection
# - Underfitting
# - Overfitting
# - Validation RMSE
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np


def make_features(y, u, order):
    rows, targets = [], []
    for k in range(order, len(y)):
        row = []
        for lag in range(1, order+1):
            row.append(y[k-lag])
        for lag in range(1, order+1):
            row.append(u[k-lag])
        rows.append(row)
        targets.append(y[k])
    return np.asarray(rows), np.asarray(targets)



# Main project workflow
def main():
    rng = np.random.default_rng(14)
    n = 1600
    u = rng.normal(0, 1, n)
    y = np.zeros(n)

    for k in range(2, n):
        y[k] = 1.3*y[k-1] - 0.45*y[k-2] + 0.28*u[k-1] + 0.08*u[k-2] + rng.normal(0,0.04)

    split = 1000

    for order in [1,2,3,4,5]:
        Phi, Y = make_features(y, u, order)
        train_rows = split - order

# Solve for the parameter values that minimize the total squared prediction error.
        theta = np.linalg.lstsq(Phi[:train_rows], Y[:train_rows], rcond=None)[0]
        pred = Phi[train_rows:] @ theta
# Compute root-mean-square error as a summary of model prediction accuracy.
        rmse = np.sqrt(np.mean((Y[train_rows:] - pred)**2))

        print(f"Order {order}: validation RMSE={rmse:.5f}")



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
