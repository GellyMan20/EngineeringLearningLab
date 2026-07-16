"""
K-fold cross-validation for model identification.

Learn:
- Robust validation
- Dataset dependence
"""

import numpy as np


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

        theta = np.linalg.lstsq(x[train_idx], y[train_idx], rcond=None)[0]
        pred = x[val_idx] @ theta
        rmse = np.sqrt(np.mean((y[val_idx]-pred)**2))
        rmses.append(rmse)

    print("Fold RMSEs:", np.round(rmses,4))
    print("Mean RMSE:", np.mean(rmses))


if __name__ == "__main__":
    main()
