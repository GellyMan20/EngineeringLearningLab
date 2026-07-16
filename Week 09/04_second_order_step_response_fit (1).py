"""
Fit a second-order model from step-response metrics.

Learn:
- Overshoot
- Damping ratio
- Natural frequency
- Settling behavior
"""

import numpy as np
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

    plt.figure()
    plt.plot(t, measured, alpha=0.5, label="Telemetry")
    plt.plot(t, fitted, label="Fitted second-order model")
    plt.title("Second-Order Step Response Fit")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
