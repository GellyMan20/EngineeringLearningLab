# Project 11 — Frequency Response Identification
# Purpose:
# This script excites a system with sinusoids at multiple frequencies and estimates the corresponding gain and phase response.
#
# Key Concepts:
# - Frequency-domain identification
# - Sinusoidal excitation
# - Gain estimation
# - Phase estimation
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


def simulate_first_order(u, dt, gain=2.0, tau=1.5):
    y = np.zeros_like(u)
    for k in range(1, len(u)):
        y_dot = (-y[k-1] + gain*u[k-1]) / tau
        y[k] = y[k-1] + y_dot*dt
    return y



# Main project workflow
def main():
    dt = 0.01
    frequencies = np.logspace(-1, 1, 18)
    gains = []
    phases = []

    for omega in frequencies:
        t = np.arange(0, max(30, 12*(2*np.pi/omega)), dt)
        u = np.sin(omega*t)
        y = simulate_first_order(u, dt)

        steady = int(0.6*len(t))
        u_ss = u[steady:]
        y_ss = y[steady:]

        gain_est = np.std(y_ss) / np.std(u_ss)
        phase_est = np.angle(np.vdot(u_ss - np.mean(u_ss), y_ss - np.mean(y_ss)), deg=True)

        gains.append(gain_est)
        phases.append(phase_est)


# Create a new figure for this result.
    plt.figure()
    plt.semilogx(frequencies, 20*np.log10(gains))
    plt.title("Estimated Frequency Response Magnitude")
    plt.xlabel("Frequency [rad/s]")
    plt.ylabel("Magnitude [dB]")
    plt.grid(True, which="both")
# Display the completed visualization.
    plt.show()


# Create a new figure for this result.
    plt.figure()
    plt.semilogx(frequencies, phases)
    plt.title("Estimated Frequency Response Phase")
    plt.xlabel("Frequency [rad/s]")
    plt.ylabel("Phase [deg]")
    plt.grid(True, which="both")
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
