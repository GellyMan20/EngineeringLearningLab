"""
Gain Margin Experiment
Learn: excessive gain, oscillation, instability.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate(kp, dt=0.001, t_end=10):
    t = np.arange(0, t_end, dt)
    x, v, r = 0.0, 0.0, 1.0
    xs = []
    for _ in t:
        u = kp*(r - x)
        a = u - 0.5*v - x
        v += a*dt
        x += v*dt
        xs.append(x)
    return t, np.array(xs)

def main():
    plt.figure()
    for kp in [0.5, 1, 2, 5, 10, 20]:
        t, y = simulate(kp)
        plt.plot(t, y, label=f"Kp={kp}")
    plt.axhline(1, linestyle="--", label="Command")
    plt.title("Gain Margin Experiment")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
