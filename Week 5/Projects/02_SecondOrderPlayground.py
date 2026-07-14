"""
Second-Order System Playground
Learn: damping ratio, natural frequency, overshoot.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate_second_order(zeta, omega_n, t_end=10.0, dt=0.001):
    t = np.arange(0, t_end, dt)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    r = 1.0
    for k in range(1, len(t)):
        a = omega_n**2 * (r - x[k-1]) - 2*zeta*omega_n*v[k-1]
        v[k] = v[k-1] + a*dt
        x[k] = x[k-1] + v[k]*dt
    return t, x

def main():
    for zeta in [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]:
        t, y = simulate_second_order(zeta, omega_n=2.0)
        plt.plot(t, y, label=f"zeta={zeta}")
    plt.axhline(1.0, linestyle="--", label="Command")
    plt.title("Second-Order Step Response")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
