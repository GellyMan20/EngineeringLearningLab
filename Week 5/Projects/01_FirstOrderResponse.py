"""
First-Order Step Response Explorer
Learn: time constant, rise time, settling behavior.
"""
import numpy as np
import matplotlib.pyplot as plt

def first_order_step(t, tau, gain=1.0):
    return gain * (1.0 - np.exp(-t / tau))

def main():
    t = np.linspace(0, 10, 1000)
    for tau in [0.25, 0.5, 1.0, 2.0, 4.0]:
        plt.plot(t, first_order_step(t, tau), label=f"tau={tau}")
    plt.axhline(0.632, linestyle="--", label="63.2%")
    plt.axhline(0.95, linestyle=":", label="95%")
    plt.title("First-Order Step Response")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
