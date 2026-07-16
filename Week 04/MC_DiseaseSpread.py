"""
02_stochastic_seir_interventions.py

Monte Carlo Simulation: Disease Spread Using a Stochastic SEIR Model

What this script does:
- Simulates disease spread using stochastic compartment transitions
- Compares Baseline, Social Distancing, Vaccination, and Combined Intervention scenarios
- Computes peak infections, day of peak, total infected, and probability of exceeding hospital capacity
- Plots mean infected curves with uncertainty bands

This is an educational model, not a medical decision tool.

Dependencies:
    pip install numpy pandas matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(42)

N_SIMULATIONS = 500
DAYS = 160
POPULATION = 10_000

INITIAL_INFECTED = 10
INITIAL_EXPOSED = 5

BASE_BETA = 0.22
BASE_SIGMA = 0.10
BASE_GAMMA = 0.055

HOSPITAL_CAPACITY_PROXY = 600

SCENARIOS = {
    "Baseline": {
        "beta_multiplier": 1.00,
        "vaccination_fraction": 0.00,
    },
    "Social Distancing": {
        "beta_multiplier": 0.55,
        "vaccination_fraction": 0.00,
    },
    "Vaccination": {
        "beta_multiplier": 1.00,
        "vaccination_fraction": 0.30,
    },
    "Combined": {
        "beta_multiplier": 0.55,
        "vaccination_fraction": 0.30,
    },
}


def simulate_one_run(beta_multiplier, vaccination_fraction):
    susceptible = POPULATION - INITIAL_INFECTED - INITIAL_EXPOSED
    exposed = INITIAL_EXPOSED
    infected = INITIAL_INFECTED
    recovered = 0

    vaccinated = int(vaccination_fraction * susceptible)
    susceptible -= vaccinated
    recovered += vaccinated

    S, E, I, R = [], [], [], []

    for _ in range(DAYS):
        # Add mild run-to-run and day-to-day parameter uncertainty.
        beta = max(0.0, np.random.normal(BASE_BETA * beta_multiplier, 0.015))
        sigma = np.clip(np.random.normal(BASE_SIGMA, 0.01), 0.01, 0.5)
        gamma = np.clip(np.random.normal(BASE_GAMMA, 0.008), 0.01, 0.5)

        exposure_probability = min(beta * infected / POPULATION, 1.0)

        new_exposed = np.random.binomial(susceptible, exposure_probability)
        new_infected = np.random.binomial(exposed, sigma)
        new_recovered = np.random.binomial(infected, gamma)

        susceptible -= new_exposed
        exposed += new_exposed - new_infected
        infected += new_infected - new_recovered
        recovered += new_recovered

        S.append(susceptible)
        E.append(exposed)
        I.append(infected)
        R.append(recovered)

    return np.array(S), np.array(E), np.array(I), np.array(R)


def summarize_scenario(name, infected_runs, recovered_runs):
    peak_infected_by_run = infected_runs.max(axis=1)
    day_of_peak_by_run = infected_runs.argmax(axis=1)
    final_recovered_by_run = recovered_runs[:, -1]

    return {
        "scenario": name,
        "mean_peak_infected": peak_infected_by_run.mean(),
        "p95_peak_infected": np.percentile(peak_infected_by_run, 95),
        "mean_day_of_peak": day_of_peak_by_run.mean(),
        "mean_total_recovered_or_removed": final_recovered_by_run.mean(),
        "prob_exceeds_capacity": np.mean(peak_infected_by_run > HOSPITAL_CAPACITY_PROXY),
    }


def main():
    results = {}
    summary_rows = []

    for scenario_name, params in SCENARIOS.items():
        S_runs, E_runs, I_runs, R_runs = [], [], [], []

        for _ in range(N_SIMULATIONS):
            S, E, I, R = simulate_one_run(
                beta_multiplier=params["beta_multiplier"],
                vaccination_fraction=params["vaccination_fraction"]
            )
            S_runs.append(S)
            E_runs.append(E)
            I_runs.append(I)
            R_runs.append(R)

        S_runs = np.array(S_runs)
        E_runs = np.array(E_runs)
        I_runs = np.array(I_runs)
        R_runs = np.array(R_runs)

        results[scenario_name] = {
            "S": S_runs,
            "E": E_runs,
            "I": I_runs,
            "R": R_runs,
        }

        summary_rows.append(summarize_scenario(scenario_name, I_runs, R_runs))

    summary = pd.DataFrame(summary_rows)

    print("\nSTOCHASTIC SEIR INTERVENTION SUMMARY")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:,.3f}"))

    summary.to_csv("seir_intervention_summary.csv", index=False)

    days = np.arange(DAYS)

    # Plot infected curves with 5th to 95th percentile bands.
    plt.figure(figsize=(12, 7))

    for scenario_name, data in results.items():
        infected = data["I"]
        mean_i = infected.mean(axis=0)
        low_i = np.percentile(infected, 5, axis=0)
        high_i = np.percentile(infected, 95, axis=0)

        plt.plot(days, mean_i, label=scenario_name)
        plt.fill_between(days, low_i, high_i, alpha=0.15)

    plt.axhline(HOSPITAL_CAPACITY_PROXY, linestyle="--", label="Capacity Proxy")
    plt.title("Stochastic SEIR: Infected Population by Scenario")
    plt.xlabel("Day")
    plt.ylabel("Infected Individuals")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot peak infections comparison.
    plt.figure(figsize=(9, 5))
    plt.bar(summary["scenario"], summary["mean_peak_infected"])
    plt.title("Mean Peak Infections by Scenario")
    plt.ylabel("Mean Peak Infected")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("\nSaved: seir_intervention_summary.csv")


if __name__ == "__main__":
    main()