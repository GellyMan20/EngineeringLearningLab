"""
Estimate frequency response from sinusoidal input/output experiments.

Learn:
- Frequency-domain identification
- Gain and phase estimation
"""

import numpy as np
import matplotlib.pyplot as plt


def simulate_first_order(u, dt, gain=2.0, tau=1.5):
    y = np.zeros_like(u)
    for k in range(1, len(u)):
        y_dot = (-y[k-1] + gain*u[k-1]) / tau
        y[k] = y[k-1] + y_dot*dt
    return y


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

    plt.figure()
    plt.semilogx(frequencies, 20*np.log10(gains))
    plt.title("Estimated Frequency Response Magnitude")
    plt.xlabel("Frequency [rad/s]")
    plt.ylabel("Magnitude [dB]")
    plt.grid(True, which="both")
    plt.show()

    plt.figure()
    plt.semilogx(frequencies, phases)
    plt.title("Estimated Frequency Response Phase")
    plt.xlabel("Frequency [rad/s]")
    plt.ylabel("Phase [deg]")
    plt.grid(True, which="both")
    plt.show()


if __name__ == "__main__":
    main()
