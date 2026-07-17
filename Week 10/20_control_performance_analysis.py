# ==========================================================================
# Project 20 — Control Performance Analysis
# ==========================================================================
#
# Purpose:
# Calculate standard time-domain and effort metrics from a controller response.
#
# Why This Matters:
# Quantitative metrics connect simulation results to system requirements and acceptance criteria.
#
# Key Concepts:
# - Rise time
# - Settling time
# - Overshoot
# - Integrated error and effort
#
# Mathematical Foundation:
# - IAE = integral |e(t)| dt
# - Control effort = integral u(t)^2 dt
#
# Learning Objectives:
# - Explain the controller or analysis method in engineering terms.
# - Connect the governing equations to their implementation in Python.
# - Interpret the plots and calculated performance metrics.
# - Identify assumptions, implementation limits, and useful extensions.
#
# Suggested Experiments:
# - Change the plant parameters and observe the effect on stability and response.
# - Change controller gains or LQR weights and compare tracking versus effort.
# - Add disturbances, sensor noise, or actuator limits where appropriate.
# - Replace Euler integration with a higher-order numerical method.
# ==========================================================================
# Import NumPy for vectors, matrices, numerical integration, and performance calculations.
import numpy as np



# Execute this portion of the controller design or analysis workflow.
def performance_metrics(t, y, u, target):
    """Execute this portion of the controller design or analysis workflow."""
    error = target - y
    final = target

    overshoot = max(0.0, (np.max(y) - final) / abs(final) * 100)

    rise_indices = np.where(y >= 0.9 * final)[0]
    rise_time = t[rise_indices[0]] if len(rise_indices) else np.nan

    band = 0.02 * abs(final)
    settling_time = np.nan
    # Step through the simulation or design cases one sample at a time.
    for i in range(len(y)):
        if np.all(np.abs(y[i:] - final) <= band):
            settling_time = t[i]
            break

    iae = np.trapz(np.abs(error), t)
    effort = np.trapz(np.abs(u), t)

    return {
        "rise_time": rise_time,
        "settling_time": settling_time,
        "overshoot_percent": overshoot,
        "IAE": iae,
        "control_effort": effort,
    }



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    t = np.linspace(0, 10, 1000)
    y = 1 - np.exp(-t) * np.cos(2 * t)
    u = 2 * np.exp(-0.4 * t)
    metrics = performance_metrics(t, y, u, target=1.0)

    # Step through the simulation or design cases one sample at a time.
    for key, value in metrics.items():
        print(f"{key:>20}: {value:.4f}")



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
