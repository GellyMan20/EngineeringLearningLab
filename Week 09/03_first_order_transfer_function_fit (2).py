# Project 03 — First-Order Transfer Function Fit
# Purpose:
# This script estimates the gain and time constant of a first-order dynamic system from a noisy step response.
#
# Key Concepts:
# - First-order dynamics
# - Steady-state gain
# - Time constant
# - Step-response fitting
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
    rng = np.random.default_rng(3)
    dt = 0.02
    t = np.arange(0, 20, dt)

    true_gain = 2.5
    true_tau = 1.8
    y = true_gain * (1 - np.exp(-t / true_tau))
    measured = y + rng.normal(0, 0.04, len(t))

    estimated_gain = np.mean(measured[-100:])
    target_63 = 0.632 * estimated_gain
    tau_index = np.argmin(np.abs(measured - target_63))
    estimated_tau = t[tau_index]

    fitted = estimated_gain * (1 - np.exp(-t / estimated_tau))

    print(f"True gain: {true_gain:.3f}, estimated: {estimated_gain:.3f}")
    print(f"True tau:  {true_tau:.3f}, estimated: {estimated_tau:.3f}")


# Create a new figure for this result.
    plt.figure()
    plt.plot(t, measured, alpha=0.6, label="Telemetry")
    plt.plot(t, fitted, label="Fitted first-order model")
    plt.title("First-Order Transfer Function Fit")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
