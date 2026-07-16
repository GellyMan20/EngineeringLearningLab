"""
03_renewable_energy_monte_carlo.py

Monte Carlo Simulation: Renewable Energy Production

What this script does:
- Simulates annual wind farm energy output
- Uses a simple turbine power curve instead of a purely linear model
- Adds turbine availability/downtime uncertainty
- Estimates annual MWh distribution, low-production risk, and capacity factor
- Plots annual production and example daily traces

Dependencies:
    pip install numpy pandas matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(42)

N_SIMULATIONS = 5_000
DAYS = 365

N_TURBINES = 20
RATED_POWER_MW_PER_TURBINE = 3.0

CUT_IN_SPEED = 3.0
RATED_SPEED = 12.0
CUT_OUT_SPEED = 25.0

MEAN_WIND_SPEED = 9.5
WIND_SPEED_STD = 3.8

MEAN_AVAILABILITY = 0.94
AVAILABILITY_STD = 0.03


def turbine_power_curve(wind_speed):
    """
    Simplified power curve:
    - No power below cut-in
    - Cubic ramp from cut-in to rated speed
    - Rated power from rated speed to cut-out
    - No power above cut-out for safety shutdown
    """
    wind_speed = np.asarray(wind_speed)
    power = np.zeros_like(wind_speed, dtype=float)

    ramp_region = (wind_speed >= CUT_IN_SPEED) & (wind_speed < RATED_SPEED)
    rated_region = (wind_speed >= RATED_SPEED) & (wind_speed <= CUT_OUT_SPEED)

    normalized = (wind_speed[ramp_region] - CUT_IN_SPEED) / (RATED_SPEED - CUT_IN_SPEED)
    power[ramp_region] = RATED_POWER_MW_PER_TURBINE * normalized**3
    power[rated_region] = RATED_POWER_MW_PER_TURBINE

    return power


def simulate_annual_energy():
    # Use Weibull-ish wind behavior through a clipped normal for simplicity.
    wind_speeds = np.random.normal(MEAN_WIND_SPEED, WIND_SPEED_STD, DAYS)
    wind_speeds = np.clip(wind_speeds, 0, None)

    availability = np.random.normal(MEAN_AVAILABILITY, AVAILABILITY_STD, DAYS)
    availability = np.clip(availability, 0.70, 1.00)

    daily_power_mw_per_turbine = turbine_power_curve(wind_speeds)

    # Daily energy = MW * 24 hours * turbines * availability
    daily_energy_mwh = daily_power_mw_per_turbine * 24 * N_TURBINES * availability

    annual_energy_mwh = daily_energy_mwh.sum()

    return annual_energy_mwh, daily_energy_mwh, wind_speeds


def main():
    annual_energy = []
    daily_examples = []
    wind_examples = []

    for i in range(N_SIMULATIONS):
        annual_mwh, daily_mwh, wind_speeds = simulate_annual_energy()
        annual_energy.append(annual_mwh)

        if i < 5:
            daily_examples.append(daily_mwh)
            wind_examples.append(wind_speeds)

    annual_energy = np.array(annual_energy)

    max_possible_mwh = N_TURBINES * RATED_POWER_MW_PER_TURBINE * 24 * DAYS
    capacity_factors = annual_energy / max_possible_mwh

    summary = pd.DataFrame([{
        "mean_annual_mwh": annual_energy.mean(),
        "median_annual_mwh": np.median(annual_energy),
        "p05_annual_mwh": np.percentile(annual_energy, 5),
        "p95_annual_mwh": np.percentile(annual_energy, 95),
        "mean_capacity_factor": capacity_factors.mean(),
        "prob_below_30pct_capacity_factor": np.mean(capacity_factors < 0.30),
    }])

    print("\nRENEWABLE ENERGY MONTE CARLO SUMMARY")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))

    summary.to_csv("renewable_energy_summary.csv", index=False)

    # Plot annual production distribution.
    plt.figure(figsize=(10, 6))
    plt.hist(annual_energy, bins=70)
    plt.axvline(np.percentile(annual_energy, 5), linestyle="--", label="5th Percentile")
    plt.axvline(np.mean(annual_energy), linestyle="-", label="Mean")
    plt.axvline(np.percentile(annual_energy, 95), linestyle="--", label="95th Percentile")
    plt.title("Annual Wind Farm Energy Production")
    plt.xlabel("Annual Energy (MWh)")
    plt.ylabel("Simulation Count")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot example daily production traces.
    plt.figure(figsize=(12, 6))
    days = np.arange(DAYS)

    for idx, daily_mwh in enumerate(daily_examples, start=1):
        plt.plot(days, daily_mwh, alpha=0.75, label=f"Example Year {idx}")

    plt.title("Example Daily Wind Farm Production Traces")
    plt.xlabel("Day")
    plt.ylabel("Daily Energy (MWh)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot power curve.
    speeds = np.linspace(0, 30, 300)
    power = turbine_power_curve(speeds)

    plt.figure(figsize=(8, 5))
    plt.plot(speeds, power)
    plt.title("Simplified Turbine Power Curve")
    plt.xlabel("Wind Speed (m/s)")
    plt.ylabel("Power per Turbine (MW)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("\nSaved: renewable_energy_summary.csv")


if __name__ == "__main__":
    main()
