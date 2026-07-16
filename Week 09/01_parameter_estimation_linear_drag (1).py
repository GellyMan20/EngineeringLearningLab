"""
Estimate vehicle mass-normalized drag from noisy telemetry.

Learn:
- Linear regression
- Parameter estimation
- Model structure
"""

import numpy as np
import matplotlib.pyplot as plt


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
    measured_acceleration = np.gradient(measured_velocity, dt)

    # a = force - c*v  => force - a = c*v
    x = measured_velocity.reshape(-1, 1)
    y = force - measured_acceleration
    estimated_drag = float(np.linalg.lstsq(x, y, rcond=None)[0][0])

    print(f"True drag coefficient:      {true_drag:.4f}")
    print(f"Estimated drag coefficient: {estimated_drag:.4f}")

    predicted_acceleration = force - estimated_drag * measured_velocity

    plt.figure()
    plt.plot(t, measured_acceleration, label="Measured acceleration")
    plt.plot(t, predicted_acceleration, label="Model acceleration")
    plt.title("Linear Drag Parameter Estimation")
    plt.xlabel("Time [s]")
    plt.ylabel("Acceleration")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
