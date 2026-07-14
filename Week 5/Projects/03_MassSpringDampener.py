"""
Mass-Spring-Damper Simulator
Learn: physical second-order dynamics and damping.
"""
import numpy as np
import matplotlib.pyplot as plt

def simulate(m, c, k, x0, v0, t_end=10, dt=0.001):
    t = np.arange(0, t_end, dt)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    x[0], v[0] = x0, v0
    for i in range(1, len(t)):
        a = -(c/m)*v[i-1] - (k/m)*x[i-1]
        v[i] = v[i-1] + a*dt
        x[i] = x[i-1] + v[i]*dt
    return t, x

def main():
    for c in [0.0, 0.5, 2.0, 6.5]:
        t, x = simulate(m=1.0, c=c, k=10.0, x0=1.0, v0=0.0)
        plt.plot(t, x, label=f"c={c}")
    plt.title("Mass-Spring-Damper Free Response")
    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
