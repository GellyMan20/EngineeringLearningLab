"""
Phase Margin Experiment
Learn: delay-induced instability and phase lag.
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def simulate(delay_s, kp=3.0, kd=1.0, dt=0.001, t_end=10):
    t = np.arange(0, t_end, dt)
    delay_steps = max(1, int(delay_s/dt))
    q = deque([0.0]*delay_steps, maxlen=delay_steps)
    x, v, r = 0.0, 0.0, 1.0
    xs = []
    for _ in t:
        q.append(x)
        delayed_x = q[0]
        u = kp*(r - delayed_x) - kd*v
        a = u - 0.5*v - x
        v += a*dt
        x += v*dt
        xs.append(x)
    return t, np.array(xs)

def main():
    plt.figure()
    for delay in [0.0, 0.05, 0.15, 0.3, 0.5]:
        t, y = simulate(delay)
        plt.plot(t, y, label=f"delay={delay}s")
    plt.axhline(1, linestyle="--", label="Command")
    plt.title("Phase Margin Experiment")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
