# Project 09 — Parameter Sensitivity Study
# Purpose:
# This script varies mass and drag independently and observes how each parameter changes the simulated vehicle response.
#
# Key Concepts:
# - Sensitivity analysis
# - Trade studies
# - Parameter influence
# - Identifiability intuition
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


def simulate(mass, drag, force, dt):
    v = np.zeros(len(force))
    for k in range(1, len(force)):
        a = (force[k-1] - drag*v[k-1]) / mass
        v[k] = v[k-1] + a*dt
    return v



# Main project workflow
def main():
    dt = 0.05
    t = np.arange(0, 40, dt)
    force = 2000 + 800*np.sin(0.3*t)

    nominal_mass = 1000.0
    nominal_drag = 80.0


# Create a new figure for this result.
    plt.figure()
    for mass in [800, 900, 1000, 1100, 1200]:
        v = simulate(mass, nominal_drag, force, dt)
        plt.plot(t, v, label=f"mass={mass}")
    plt.title("Sensitivity to Mass")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()


# Create a new figure for this result.
    plt.figure()
    for drag in [40, 60, 80, 100, 120]:
        v = simulate(nominal_mass, drag, force, dt)
        plt.plot(t, v, label=f"drag={drag}")
    plt.title("Sensitivity to Drag")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
