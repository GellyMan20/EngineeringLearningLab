# Project 16 — Cross-Validation for Identification
# Purpose:
# This script uses K-fold cross-validation to measure how consistently a fitted model performs across different telemetry subsets.
#
# Key Concepts:
# - K-fold validation
# - Generalization
# - Dataset dependence
# - Model reliability
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np



# Main project workflow
def main():
    rng = np.random.default_rng(16)
    n = 1200
    x = rng.normal(0,1,(n,3))
    theta_true = np.array([1.2,-0.7,0.35])
    y = x @ theta_true + rng.normal(0,0.2,n)

    folds = 5
    indices = np.arange(n)
    rng.shuffle(indices)
    fold_size = n // folds

    rmses = []

    for fold in range(folds):
        val_idx = indices[fold*fold_size:(fold+1)*fold_size]
        train_idx = np.setdiff1d(indices, val_idx)

# Solve for the parameter values that minimize the total squared prediction error.
        theta = np.linalg.lstsq(x[train_idx], y[train_idx], rcond=None)[0]
        pred = x[val_idx] @ theta
# Compute root-mean-square error as a summary of model prediction accuracy.
        rmse = np.sqrt(np.mean((y[val_idx]-pred)**2))
        rmses.append(rmse)

    print("Fold RMSEs:", np.round(rmses,4))
    print("Mean RMSE:", np.mean(rmses))



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
