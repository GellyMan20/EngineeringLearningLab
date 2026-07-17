# Project 01 — Linear Drag Parameter Estimation
# Purpose:
# This script estimates a linear drag coefficient from noisy vehicle telemetry
# It combines measured velocity, estimated acceleration, and known input force in a least-squares problem.
#
# Key Concepts:
# - Linear least squares
# - Physical parameter estimation
# - Telemetry differentiation
# - Model validation
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np
# Import Matplotlib to visualize telemetry, model predictions, residuals, and trade studies.
import matplotlib.pyplot as plt



# Main project workflow
def main():
    rng = np.random.default_rng(1)
    dt = 0.05
    t = np.arange(0, 50, dt)

    true_drag = 0.18
    force = 2.0 + 1.2 * np.sin(0.25 * t)
    velocity = np.zeros_like(t)

    for k in range(1, len(t)):
        acceleration = force[k - 1] - true_drag * velocity[k - 1]
        velocity[k] = velocity[k - 1] + acceleration * dt

    measured_velocity = velocity + rng.normal(0, 0.05, len(t))
# Estimate acceleration numerically from the measured velocity history.
    measured_acceleration = np.gradient(measured_velocity, dt)

    # a = force - c*v  => force - a = c*v
    x = measured_velocity.reshape(-1, 1)
    y = force - measured_acceleration
# Solve for the parameter values that minimize the total squared prediction error.
    estimated_drag = float(np.linalg.lstsq(x, y, rcond=None)[0][0])

    print(f"True drag coefficient:      {true_drag:.4f}")
    print(f"Estimated drag coefficient: {estimated_drag:.4f}")

    predicted_acceleration = force - estimated_drag * measured_velocity


# Create a new figure for this result.
    plt.figure()
    plt.plot(t, measured_acceleration, label="Measured acceleration")
    plt.plot(t, predicted_acceleration, label="Model acceleration")
    plt.title("Linear Drag Parameter Estimation")
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
