"""
Week 4 Engineering Learning Plan
Monte Carlo Foundations

Covers:
1. Sampling distributions
2. Uncertainty propagation
3. Projectile hit probability
4. Rocket altitude Monte Carlo
5. Failure-region analysis
6. Basic sensitivity analysis
7. pandas result table + CSV export
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# GLOBAL SETTINGS
# ============================================================

np.random.seed(42)

N = 10_000
GRAVITY = 9.81


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def plot_histogram(data, title, xlabel, bins=50):
    plt.figure()
    plt.hist(data, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.grid(True)
    plt.show()


def summarize_array(name, data):
    print(f"\n{name}")
    print("-" * len(name))
    print(f"Mean:   {np.mean(data):.3f}")
    print(f"Median: {np.median(data):.3f}")
    print(f"Std:    {np.std(data):.3f}")
    print(f"Min:    {np.min(data):.3f}")
    print(f"Max:    {np.max(data):.3f}")
    print(f"95% Range: {np.percentile(data, 2.5):.3f} to {np.percentile(data, 97.5):.3f}")


# ============================================================
# PART 1 — BASIC DISTRIBUTIONS
# ============================================================

uniform_samples = np.random.uniform(low=0, high=10, size=N)
normal_samples = np.random.normal(loc=0, scale=1, size=N)

summarize_array("Uniform Distribution Samples", uniform_samples)
summarize_array("Normal Distribution Samples", normal_samples)

plot_histogram(uniform_samples, "Uniform Distribution", "Value")
plot_histogram(normal_samples, "Normal Distribution", "Value")


# ============================================================
# PART 2 — UNCERTAINTY PROPAGATION
# distance = velocity * time
# ============================================================

velocity_samples = np.random.normal(loc=100, scale=5, size=N)
time_samples = np.random.normal(loc=10, scale=0.2, size=N)

distance_samples = velocity_samples * time_samples

summarize_array("Distance = Velocity x Time", distance_samples)

plot_histogram(distance_samples, "Distance Distribution", "Distance")


# ============================================================
# PART 3 — PROJECTILE MONTE CARLO
# Range equation:
# range = v^2 * sin(2theta) / g
# ============================================================

def projectile_range(velocity, angle_degrees):
    angle_radians = np.radians(angle_degrees)
    return velocity**2 * np.sin(2 * angle_radians) / GRAVITY


target_distance = 1000
hit_tolerance = 75

projectile_velocity = np.random.normal(loc=100, scale=5, size=N)
projectile_angle = np.random.normal(loc=45, scale=2, size=N)

projectile_ranges = projectile_range(projectile_velocity, projectile_angle)

hits = np.abs(projectile_ranges - target_distance) <= hit_tolerance
hit_probability = np.mean(hits)

summarize_array("Projectile Range Results", projectile_ranges)

print("\nProjectile Hit Analysis")
print("-----------------------")
print(f"Target distance: {target_distance} m")
print(f"Hit tolerance:   ±{hit_tolerance} m")
print(f"Hit probability: {hit_probability * 100:.2f}%")

plot_histogram(projectile_ranges, "Projectile Range Distribution", "Range")


# ============================================================
# PART 4 — ROCKET SIMULATION
# Simple vertical rocket using Euler integration
# ============================================================

def run_rocket_simulation(mass, thrust, fuel_time, dt=0.05):
    height = 0.0
    velocity = 0.0
    time = 0.0

    max_height = 0.0
    landing_velocity = None

    while True:
        if time < fuel_time:
            acceleration = thrust / mass - GRAVITY
        else:
            acceleration = -GRAVITY

        velocity += acceleration * dt
        height += velocity * dt
        time += dt

        max_height = max(max_height, height)

        if height <= 0 and time > fuel_time:
            landing_velocity = velocity
            break

        if time > 120:
            landing_velocity = velocity
            break

    return max_height, landing_velocity


rocket_mass = np.random.normal(loc=1.0, scale=0.05, size=N)
rocket_thrust = np.random.normal(loc=15.0, scale=1.0, size=N)
rocket_fuel_time = np.random.normal(loc=5.0, scale=0.3, size=N)

rocket_max_heights = []
rocket_landing_velocities = []

for mass, thrust, fuel_time in zip(rocket_mass, rocket_thrust, rocket_fuel_time):
    max_height, landing_velocity = run_rocket_simulation(
        mass=mass,
        thrust=thrust,
        fuel_time=fuel_time
    )

    rocket_max_heights.append(max_height)
    rocket_landing_velocities.append(landing_velocity)

rocket_max_heights = np.array(rocket_max_heights)
rocket_landing_velocities = np.array(rocket_landing_velocities)

summarize_array("Rocket Maximum Height Results", rocket_max_heights)
summarize_array("Rocket Landing Velocity Results", rocket_landing_velocities)

plot_histogram(rocket_max_heights, "Rocket Max Height Distribution", "Maximum Height")
plot_histogram(rocket_landing_velocities, "Rocket Landing Velocity Distribution", "Landing Velocity")


# ============================================================
# PART 5 — FAILURE REGION ANALYSIS
# Failure if landing speed magnitude is greater than 5 m/s
# ============================================================

safe_landing_limit = 5.0

rocket_failures = np.abs(rocket_landing_velocities) > safe_landing_limit
rocket_failure_rate = np.mean(rocket_failures)

print("\nRocket Failure Analysis")
print("-----------------------")
print(f"Safe landing limit: {safe_landing_limit} m/s")
print(f"Failure rate:       {rocket_failure_rate * 100:.2f}%")
print(f"Success rate:       {(1 - rocket_failure_rate) * 100:.2f}%")


# ============================================================
# PART 6 — SAVE RESULTS IN A DATAFRAME
# ============================================================

results = pd.DataFrame({
    "mass": rocket_mass,
    "thrust": rocket_thrust,
    "fuel_time": rocket_fuel_time,
    "max_height": rocket_max_heights,
    "landing_velocity": rocket_landing_velocities,
    "failure": rocket_failures
})

print("\nRocket Monte Carlo Results Table")
print("--------------------------------")
print(results.head())

print("\nSummary Statistics")
print("------------------")
print(results.describe())

results.to_csv("week4_monte_carlo_results.csv", index=False)
print("\nSaved results to: week4_monte_carlo_results.csv")


# ============================================================
# PART 7 — FAILURE REGION SCATTER PLOT
# ============================================================

plt.figure()
plt.scatter(results["thrust"], results["max_height"], s=8, alpha=0.4)
plt.title("Rocket Max Height vs Thrust")
plt.xlabel("Thrust")
plt.ylabel("Maximum Height")
plt.grid(True)
plt.show()

plt.figure()
plt.scatter(results["fuel_time"], results["max_height"], s=8, alpha=0.4)
plt.title("Rocket Max Height vs Fuel Time")
plt.xlabel("Fuel Time")
plt.ylabel("Maximum Height")
plt.grid(True)
plt.show()

plt.figure()
plt.scatter(results["mass"], results["max_height"], s=8, alpha=0.4)
plt.title("Rocket Max Height vs Mass")
plt.xlabel("Mass")
plt.ylabel("Maximum Height")
plt.grid(True)
plt.show()


# ============================================================
# PART 8 — BASIC SENSITIVITY ANALYSIS
# Correlation is a quick first-pass way to see what matters.
# ============================================================

correlations = results[
    ["mass", "thrust", "fuel_time", "max_height", "landing_velocity"]
].corr()

print("\nCorrelation Matrix")
print("------------------")
print(correlations)

print("\nSensitivity to Max Height")
print("-------------------------")
print(correlations["max_height"].sort_values(ascending=False))


# ============================================================
# PART 9 — SIMPLE TEXT REPORT
# ============================================================

report = f"""
WEEK 4 MONTE CARLO FRAMEWORK REPORT

Objective:
Simulate uncertain engineering systems using Monte Carlo methods.

Number of samples:
{N}

Projectile Analysis:
Target distance: {target_distance} m
Hit tolerance: ±{hit_tolerance} m
Hit probability: {hit_probability * 100:.2f}%

Rocket Analysis:
Mass distribution: N(1.0, 0.05)
Thrust distribution: N(15.0, 1.0)
Fuel time distribution: N(5.0, 0.3)

Mean max height:
{np.mean(rocket_max_heights):.2f} m

95% max height range:
{np.percentile(rocket_max_heights, 2.5):.2f} m to {np.percentile(rocket_max_heights, 97.5):.2f} m

Safe landing limit:
{safe_landing_limit} m/s

Failure rate:
{rocket_failure_rate * 100:.2f}%

Engineering conclusion:
Monte Carlo simulation allows us to estimate performance variation,
failure probability, and sensitivity to uncertain inputs. In this simulation,
fuel time and thrust are expected to strongly influence maximum height,
while landing velocity is mostly driven by the ballistic return phase.
"""

with open("week4_monte_carlo_report.txt", "w") as file:
    file.write(report)

print(report)
print("Saved report to: week4_monte_carlo_report.txt")