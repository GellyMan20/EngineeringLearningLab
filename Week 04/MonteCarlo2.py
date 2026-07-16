import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

N = 10_000
GRAVITY = 9.81


def summarize_array(name, data):
    print(f"\n{name}")
    print("-" * len(name))
    print(f"Mean:   {np.mean(data):.3f}")
    print(f"Median: {np.median(data):.3f}")
    print(f"Std:    {np.std(data):.3f}")
    print(f"Min:    {np.min(data):.3f}")
    print(f"Max:    {np.max(data):.3f}")
    print(f"95% Range: {np.percentile(data, 2.5):.3f} to {np.percentile(data, 97.5):.3f}")


def projectile_range(velocity, angle_degrees):
    angle_radians = np.radians(angle_degrees)
    return velocity**2 * np.sin(2 * angle_radians) / GRAVITY


def run_rocket_simulation(mass, thrust, fuel_time, dt=0.05):
    height = 0.0
    velocity = 0.0
    time = 0.0
    max_height = 0.0

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


# ============================================================
# PART 1 — BASIC DISTRIBUTIONS
# ============================================================

uniform_samples = np.random.uniform(0, 10, N)
normal_samples = np.random.normal(0, 1, N)

summarize_array("Uniform Distribution Samples", uniform_samples)
summarize_array("Normal Distribution Samples", normal_samples)


# ============================================================
# PART 2 — UNCERTAINTY PROPAGATION
# distance = velocity * time
# ============================================================

velocity_samples = np.random.normal(100, 5, N)
time_samples = np.random.normal(10, 0.2, N)
distance_samples = velocity_samples * time_samples

summarize_array("Distance = Velocity x Time", distance_samples)


# ============================================================
# PART 3 — PROJECTILE MONTE CARLO
# ============================================================

target_distance = 1000
hit_tolerance = 75

projectile_velocity = np.random.normal(100, 5, N)
projectile_angle = np.random.normal(45, 2, N)

projectile_ranges = projectile_range(projectile_velocity, projectile_angle)

hits = np.abs(projectile_ranges - target_distance) <= hit_tolerance
hit_probability = np.mean(hits)

summarize_array("Projectile Range Results", projectile_ranges)

print("\nProjectile Hit Analysis")
print("-----------------------")
print(f"Target distance: {target_distance} m")
print(f"Hit tolerance:   ±{hit_tolerance} m")
print(f"Hit probability: {hit_probability * 100:.2f}%")


# ============================================================
# PART 4 — ROCKET MONTE CARLO
# ============================================================

rocket_mass = np.random.normal(1.0, 0.05, N)
rocket_thrust = np.random.normal(15.0, 1.0, N)
rocket_fuel_time = np.random.normal(5.0, 0.3, N)

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


# ============================================================
# PART 5 — FAILURE REGION ANALYSIS
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
# PART 6 — SAVE RESULTS
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


# ============================================================
# PART 7 — CORRELATION / SENSITIVITY
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
# PART 8 — COMPARISON PLOTS
# ============================================================

# 1. Compare basic sampling distributions
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(uniform_samples, bins=50)
plt.title("Uniform Distribution")
plt.xlabel("Value")
plt.ylabel("Count")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.hist(normal_samples, bins=50)
plt.title("Normal Distribution")
plt.xlabel("Value")
plt.ylabel("Count")
plt.grid(True)

plt.tight_layout()
plt.show()


# 2. Compare velocity, time, and propagated distance
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.hist(velocity_samples, bins=50)
plt.title("Velocity Samples")
plt.xlabel("Velocity")
plt.ylabel("Count")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.hist(time_samples, bins=50)
plt.title("Time Samples")
plt.xlabel("Time")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.hist(distance_samples, bins=50)
plt.title("Distance Output")
plt.xlabel("Distance")
plt.grid(True)

plt.tight_layout()
plt.show()


# 3. Projectile input/output comparison
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.hist(projectile_velocity, bins=50)
plt.title("Projectile Velocity")
plt.xlabel("Velocity")
plt.ylabel("Count")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.hist(projectile_angle, bins=50)
plt.title("Projectile Angle")
plt.xlabel("Angle")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.hist(projectile_ranges, bins=50)
plt.axvline(target_distance, linestyle="--", label="Target")
plt.axvline(target_distance - hit_tolerance, linestyle=":", label="Tolerance")
plt.axvline(target_distance + hit_tolerance, linestyle=":")
plt.title("Projectile Range")
plt.xlabel("Range")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


# 4. Rocket input uncertainty comparison
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.hist(results["mass"], bins=50)
plt.title("Mass Uncertainty")
plt.xlabel("Mass")
plt.ylabel("Count")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.hist(results["thrust"], bins=50)
plt.title("Thrust Uncertainty")
plt.xlabel("Thrust")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.hist(results["fuel_time"], bins=50)
plt.title("Fuel Time Uncertainty")
plt.xlabel("Fuel Time")
plt.grid(True)

plt.tight_layout()
plt.show()


# 5. Rocket output comparison
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(results["max_height"], bins=50)
plt.title("Rocket Max Height Distribution")
plt.xlabel("Maximum Height")
plt.ylabel("Count")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.hist(results["landing_velocity"], bins=50)
plt.title("Rocket Landing Velocity Distribution")
plt.xlabel("Landing Velocity")
plt.ylabel("Count")
plt.grid(True)

plt.tight_layout()
plt.show()


# 6. Input sensitivity scatter plots
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.scatter(results["mass"], results["max_height"], s=8, alpha=0.4)
plt.title("Mass vs Max Height")
plt.xlabel("Mass")
plt.ylabel("Max Height")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.scatter(results["thrust"], results["max_height"], s=8, alpha=0.4)
plt.title("Thrust vs Max Height")
plt.xlabel("Thrust")
plt.ylabel("Max Height")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.scatter(results["fuel_time"], results["max_height"], s=8, alpha=0.4)
plt.title("Fuel Time vs Max Height")
plt.xlabel("Fuel Time")
plt.ylabel("Max Height")
plt.grid(True)

plt.tight_layout()
plt.show()


# 7. Failure region scatter plot
successes = results[results["failure"] == False]
failures = results[results["failure"] == True]

plt.figure(figsize=(8, 6))

plt.scatter(successes["thrust"], successes["max_height"], s=8, alpha=0.25, label="Success")
plt.scatter(failures["thrust"], failures["max_height"], s=12, alpha=0.8, label="Failure")

plt.title("Failure Region: Thrust vs Max Height")
plt.xlabel("Thrust")
plt.ylabel("Maximum Height")
plt.legend()
plt.grid(True)
plt.show()


# 8. Success vs failure count
failure_counts = results["failure"].value_counts()

plt.figure(figsize=(6, 5))
plt.bar(
    ["Success", "Failure"],
    [
        failure_counts.get(False, 0),
        failure_counts.get(True, 0)
    ]
)
plt.title("Monte Carlo Success vs Failure Count")
plt.ylabel("Number of Runs")
plt.grid(True)
plt.show()


# 9. Sensitivity bar chart
sensitivity = correlations["max_height"].drop("max_height").sort_values()

plt.figure(figsize=(8, 5))
plt.barh(sensitivity.index, sensitivity.values)
plt.title("Sensitivity to Max Height")
plt.xlabel("Correlation with Max Height")
plt.grid(True)
plt.show()


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
fuel time and thrust strongly influence maximum height. The failure region
shows where uncertain input combinations lead to unacceptable outcomes.
"""

with open("week4_monte_carlo_report.txt", "w") as file:
    file.write(report)

print(report)
print("Saved results to: week4_monte_carlo_results.csv")
print("Saved report to: week4_monte_carlo_report.txt")