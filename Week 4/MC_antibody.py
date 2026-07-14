"""
04_antibody_affinity_maturation.py

Monte Carlo Simulation: Antibody Affinity Maturation

What this script does:
- Simulates a population of candidate antibodies
- Applies random mutation over generations
- Applies selection pressure based on affinity
- Compares different mutation-rate strategies
- Tracks mean affinity, best affinity, diversity, and extinction risk

This is a toy educational model, not a biological research model.

Dependencies:
    pip install numpy pandas matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(42)

N_SIMULATIONS = 300
GENERATIONS = 80
POPULATION_SIZE = 500

INITIAL_AFFINITY_MEAN = 0.25
INITIAL_AFFINITY_STD = 0.08

SELECTION_FRACTION = 0.25
OFFSPRING_PER_SURVIVOR = int(1 / SELECTION_FRACTION)

STRATEGIES = {
    "Low Mutation": {
        "mutation_std": 0.025,
        "deleterious_bias": -0.002,
    },
    "Moderate Mutation": {
        "mutation_std": 0.055,
        "deleterious_bias": -0.006,
    },
    "High Mutation": {
        "mutation_std": 0.110,
        "deleterious_bias": -0.020,
    },
}


def initialize_population():
    affinities = np.random.normal(
        INITIAL_AFFINITY_MEAN,
        INITIAL_AFFINITY_STD,
        POPULATION_SIZE
    )
    return np.clip(affinities, 0.0, 1.0)


def mutate_population(population, mutation_std, deleterious_bias):
    mutations = np.random.normal(deleterious_bias, mutation_std, len(population))

    # Rare beneficial jump mutation.
    jump_mask = np.random.random(len(population)) < 0.01
    mutations[jump_mask] += np.random.uniform(0.03, 0.12, jump_mask.sum())

    mutated = population + mutations
    return np.clip(mutated, 0.0, 1.0)


def select_and_reproduce(population):
    n_survivors = max(2, int(SELECTION_FRACTION * len(population)))

    threshold = np.percentile(population, 100 * (1 - SELECTION_FRACTION))
    survivors = population[population >= threshold]

    if len(survivors) == 0:
        return np.array([])

    reproduced = np.random.choice(
        survivors,
        size=POPULATION_SIZE,
        replace=True
    )

    return reproduced


def simulate_one_lineage(mutation_std, deleterious_bias):
    population = initialize_population()

    mean_affinity = []
    best_affinity = []
    diversity = []

    for _ in range(GENERATIONS):
        population = mutate_population(population, mutation_std, deleterious_bias)
        population = select_and_reproduce(population)

        if len(population) == 0:
            mean_affinity.append(0.0)
            best_affinity.append(0.0)
            diversity.append(0.0)
            continue

        mean_affinity.append(np.mean(population))
        best_affinity.append(np.max(population))
        diversity.append(np.std(population))

    return np.array(mean_affinity), np.array(best_affinity), np.array(diversity)


def main():
    results = {}
    summary_rows = []

    for strategy_name, params in STRATEGIES.items():
        mean_runs = []
        best_runs = []
        diversity_runs = []

        for _ in range(N_SIMULATIONS):
            mean_a, best_a, div_a = simulate_one_lineage(
                mutation_std=params["mutation_std"],
                deleterious_bias=params["deleterious_bias"]
            )
            mean_runs.append(mean_a)
            best_runs.append(best_a)
            diversity_runs.append(div_a)

        mean_runs = np.array(mean_runs)
        best_runs = np.array(best_runs)
        diversity_runs = np.array(diversity_runs)

        results[strategy_name] = {
            "mean": mean_runs,
            "best": best_runs,
            "diversity": diversity_runs,
        }

        summary_rows.append({
            "strategy": strategy_name,
            "final_mean_affinity": mean_runs[:, -1].mean(),
            "final_best_affinity": best_runs[:, -1].mean(),
            "final_diversity": diversity_runs[:, -1].mean(),
            "prob_reaches_0p90_best_affinity": np.mean(best_runs[:, -1] >= 0.90),
        })

    summary = pd.DataFrame(summary_rows)

    print("\nANTIBODY AFFINITY MATURATION SUMMARY")
    print(summary.to_string(index=False, float_format=lambda x: f"{x:,.4f}"))

    summary.to_csv("antibody_affinity_summary.csv", index=False)

    generations = np.arange(GENERATIONS)

    # Plot mean affinity.
    plt.figure(figsize=(12, 6))

    for strategy_name, data in results.items():
        mean_runs = data["mean"]
        mean_curve = mean_runs.mean(axis=0)
        low_curve = np.percentile(mean_runs, 5, axis=0)
        high_curve = np.percentile(mean_runs, 95, axis=0)

        plt.plot(generations, mean_curve, label=strategy_name)
        plt.fill_between(generations, low_curve, high_curve, alpha=0.15)

    plt.title("Mean Antibody Affinity Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Mean Affinity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot best affinity.
    plt.figure(figsize=(12, 6))

    for strategy_name, data in results.items():
        best_runs = data["best"]
        best_curve = best_runs.mean(axis=0)

        plt.plot(generations, best_curve, label=strategy_name)

    plt.title("Best Antibody Affinity Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Affinity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot final performance.
    plt.figure(figsize=(9, 5))
    plt.bar(summary["strategy"], summary["final_best_affinity"])
    plt.title("Final Best Affinity by Mutation Strategy")
    plt.ylabel("Final Best Affinity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("\nSaved: antibody_affinity_summary.csv")


if __name__ == "__main__":
    main()
