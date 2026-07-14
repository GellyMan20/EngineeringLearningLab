"""
Bode Plot Explorer
Learn: frequency response, magnitude, phase, bandwidth.
"""
import numpy as np
import matplotlib.pyplot as plt

def bode_first_order(tau, omega):
    G = 1 / (tau*1j*omega + 1)
    return 20*np.log10(np.abs(G)), np.angle(G, deg=True)

def main():
    omega = np.logspace(-2, 2, 1000)
    plt.figure()
    for tau in [0.1, 0.5, 1.0, 3.0]:
        mag, _ = bode_first_order(tau, omega)
        plt.semilogx(omega, mag, label=f"tau={tau}")
    plt.title("Bode Magnitude")
    plt.xlabel("Frequency [rad/s]")
    plt.ylabel("Magnitude [dB]")
    plt.grid(True, which="both")
    plt.legend()
    plt.show()
    plt.figure()
    for tau in [0.1, 0.5, 1.0, 3.0]:
        _, phase = bode_first_order(tau, omega)
        plt.semilogx(omega, phase, label=f"tau={tau}")
    plt.title("Bode Phase")
    plt.xlabel("Frequency [rad/s]")
    plt.ylabel("Phase [deg]")
    plt.grid(True, which="both")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
