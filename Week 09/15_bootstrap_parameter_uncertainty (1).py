"""
Estimate parameter uncertainty using bootstrap resampling.

Learn:
- Confidence intervals
- Parameter uncertainty
"""

import numpy as np


def main():
    rng = np.random.default_rng(15)
    n = 1000
    x = rng.uniform(0, 10, n)
    true_slope = 2.5
    y = true_slope*x + rng.normal(0, 2.0, n)

    estimates = []
    for _ in range(500):
        idx = rng.integers(0, n, n)
        slope = np.linalg.lstsq(x[idx].reshape(-1,1), y[idx], rcond=None)[0][0]
        estimates.append(slope)

    estimates = np.asarray(estimates)
    print(f"Mean estimate: {np.mean(estimates):.4f}")
    print(f"95% CI: [{np.percentile(estimates,2.5):.4f}, {np.percentile(estimates,97.5):.4f}]")


if __name__ == "__main__":
    main()
