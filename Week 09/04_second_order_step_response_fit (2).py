# Project 04 — Second-Order Step Response Fit
# Purpose:
# This script identifies damping ratio and natural frequency for a second-order system by finding the candidate model that best matches measured telemetry.
#
# Key Concepts:
# - Second-order dynamics
# - Damping ratio
# - Natural frequency
# - Grid-search fitting
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


def simulate(zeta, omega_n, dt=0.002, t_end=12.0):
    t = np.arange(0, t_end, dt)
    x = np.zeros_like(t)
    v = np.zeros_like(t)

    for k in range(1, len(t)):
        a = omega_n**2 * (1 - x[k-1]) - 2*zeta*omega_n*v[k-1]
        v[k] = v[k-1] + a * dt
        x[k] = x[k-1] + v[k] * dt

    return t, x



# Main project workflow
def main():
    rng = np.random.default_rng(4)
    true_zeta = 0.45
    true_omega_n = 2.2

    t, y = simulate(true_zeta, true_omega_n)
    measured = y + rng.normal(0, 0.01, len(y))

    best = None
    for zeta in np.linspace(0.1, 1.2, 45):
        for omega_n in np.linspace(0.8, 4.0, 50):
            _, candidate = simulate(zeta, omega_n, dt=t[1]-t[0], t_end=t[-1] + (t[1]-t[0]))
            score = np.mean((candidate - measured)**2)
            if best is None or score < best[0]:
                best = (score, zeta, omega_n, candidate)

    score, est_zeta, est_omega_n, fitted = best

    print(f"True zeta: {true_zeta:.3f}, estimated: {est_zeta:.3f}")
    print(f"True omega_n: {true_omega_n:.3f}, estimated: {est_omega_n:.3f}")


# Create a new figure for this result.
    plt.figure()
    plt.plot(t, measured, alpha=0.5, label="Telemetry")
    plt.plot(t, fitted, label="Fitted second-order model")
    plt.title("Second-Order Step Response Fit")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
