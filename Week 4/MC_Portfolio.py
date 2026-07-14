"""
01_portfolio_risk_monte_carlo.py

Monte Carlo Simulation: Portfolio Risk Assessment

What this script does:
- Simulates correlated annual asset returns
- Computes portfolio return distribution
- Estimates probability of loss
- Calculates VaR and CVaR
- Compares multiple portfolio allocations
- Plots return distributions and efficient-style risk/return comparison

Dependencies:
    pip install numpy pandas matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(42)

N_SIMULATIONS = 50_000
INITIAL_PORTFOLIO_VALUE = 100_000

ASSET_NAMES = ["Defensive Asset", "Growth Asset", "Income Asset"]

MEAN_RETURNS = np.array([0.08, 0.12, 0.06])
STD_DEVS = np.array([0.20, 0.30, 0.15])

CORRELATION_MATRIX = np.array([
    [1.00, 0.20, 0.40],
    [0.20, 1.00, 0.30],
    [0.40, 0.30, 1.00]
])

PORTFOLIOS = {
    "Balanced": np.array([0.40, 0.40, 0.20]),
    "Conservative": np.array([0.60, 0.15, 0.25]),
    "Aggressive": np.array([0.20, 0.65, 0.15]),
    "Income Tilt": np.array([0.25, 0.25, 0.50]),
}


def make_covariance_matrix(std_devs, corr_matrix):
    return np.diag(std_devs) @ corr_matrix @ np.diag(std_devs)


def summarize_returns(name, returns):
    final_values = INITIAL_PORTFOLIO_VALUE * (1 + returns)

    var_95 = np.percentile(returns, 5)
    cvar_95 = returns[returns <= var_95].mean()

    summary = {
        "portfolio": name,
        "mean_return": np.mean(returns),
        "median_return": np.median(returns),
        "volatility": np.std(returns),
        "probability_of_loss": np.mean(returns < 0),
        "var_95_return": var_95,
        "cvar_95_return": cvar_95,
        "mean_final_value": np.mean(final_values),
        "p05_final_value": np.percentile(final_values, 5),
        "p95_final_value": np.percentile(final_values, 95),
    }

    return summary


def main():
    cov_matrix = make_covariance_matrix(STD_DEVS, CORRELATION_MATRIX)

    asset_returns = np.random.multivariate_normal(
        mean=MEAN_RETURNS,
        cov=cov_matrix,
        size=N_SIMULATIONS
    )

    all_portfolio_returns = {}
    summary_rows = []

    for name, weights in PORTFOLIOS.items():
        portfolio_returns = asset_returns @ weights
        all_portfolio_returns[name] = portfolio_returns
        summary_rows.append(summarize_returns(name, portfolio_returns))

    summary = pd.DataFrame(summary_rows)

    print("\nPORTFOLIO MONTE CARLO SUMMARY")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))

    summary.to_csv("portfolio_risk_summary.csv", index=False)

    # Plot 1: return distributions
    plt.figure(figsize=(12, 6))
    for name, returns in all_portfolio_returns.items():
        plt.hist(returns, bins=80, alpha=0.35, density=True, label=name)

    plt.axvline(0, linestyle="--", label="Break-even")
    plt.title("Portfolio Return Distributions")
    plt.xlabel("Annual Return")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 2: risk vs expected return
    plt.figure(figsize=(8, 6))
    plt.scatter(summary["volatility"], summary["mean_return"], s=90)

    for _, row in summary.iterrows():
        plt.annotate(
            row["portfolio"],
            (row["volatility"], row["mean_return"]),
            xytext=(6, 6),
            textcoords="offset points"
        )

    plt.title("Risk vs Expected Return")
    plt.xlabel("Volatility / Standard Deviation")
    plt.ylabel("Expected Return")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 3: downside risk comparison
    plt.figure(figsize=(9, 5))
    plt.bar(summary["portfolio"], summary["probability_of_loss"] * 100)
    plt.title("Probability of Loss by Portfolio")
    plt.ylabel("Probability of Loss (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("\nSaved: portfolio_risk_summary.csv")


if __name__ == "__main__":
    main()