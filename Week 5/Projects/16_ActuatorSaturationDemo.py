"""
Actuator Saturation Demo
Learn: integral windup and anti-windup.
"""
import numpy as np
import matplotlib.pyplot as plt

class PI:
    def __init__(self, kp, ki, limits=(-1, 1), anti_windup=False):
        self.kp = kp; self.ki = ki; self.limits = limits
        self.anti_windup = anti_windup; self.integral = 0.0
    def update(self, error, dt):
        proposed = self.integral + error*dt
        raw = self.kp*error + self.ki*proposed
        sat = float(np.clip(raw, *self.limits))
        if not self.anti_windup or raw == sat:
            self.integral = proposed
        return sat

def run(anti_windup):
    dt = 0.01
    t = np.arange(0, 30, dt)
    x = 0.0
    c = PI(0.8, 0.5, anti_windup=anti_windup)
    xs, us = [], []
    for time in t:
        target = 10.0 if time <= 15 else 0.0
        u = c.update(target - x, dt)
        x += (-0.4*x + u)*dt
        xs.append(x); us.append(u)
    return t, np.array(xs), np.array(us)

def main():
    t, x1, u1 = run(False)
    _, x2, u2 = run(True)
    plt.figure()
    plt.plot(t, x1, label="No anti-windup")
    plt.plot(t, x2, label="With anti-windup")
    plt.title("Integral Windup")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()