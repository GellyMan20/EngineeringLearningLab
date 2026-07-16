"""
Study output sensitivity to model parameters.

Learn:
- Parameter sensitivity
- Identifiability intuition
- Engineering trade studies
"""

import numpy as np
import matplotlib.pyplot as plt


def simulate(mass, drag, force, dt):
    v = np.zeros(len(force))
    for k in range(1, len(force)):
        a = (force[k-1] - drag*v[k-1]) / mass
        v[k] = v[k-1] + a*dt
    return v


def main():
    dt = 0.05
    t = np.arange(0, 40, dt)
    force = 2000 + 800*np.sin(0.3*t)

    nominal_mass = 1000.0
    nominal_drag = 80.0

    plt.figure()
    for mass in [800, 900, 1000, 1100, 1200]:
        v = simulate(mass, nominal_drag, force, dt)
        plt.plot(t, v, label=f"mass={mass}")
    plt.title("Sensitivity to Mass")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure()
    for drag in [40, 60, 80, 100, 120]:
        v = simulate(nominal_mass, drag, force, dt)
        plt.plot(t, v, label=f"drag={drag}")
    plt.title("Sensitivity to Drag")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
