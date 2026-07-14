import numpy as np
import matplotlib.pyplot as plt

class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limits = output_limits
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        u = self.kp * error + self.ki * self.integral + self.kd * derivative
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

"""
Sensor Noise Investigation
Learn: derivative sensitivity and noisy control commands.
"""
def main():
    rng = np.random.default_rng(2)
    dt = 0.01
    t = np.arange(0, 20, dt)
    x, v, r = 0.0, 0.0, 1.0
    pid = PID(3.0, 0.0, 2.0, output_limits=(-20, 20))
    xs, meas, us = [], [], []
    for _ in t:
        y = x + rng.normal(0, 0.05)
        u = pid.update(r - y, dt)
        a = u - 0.7*v - x
        v += a*dt
        x += v*dt
        xs.append(x); meas.append(y); us.append(u)
    plt.figure()
    plt.plot(t, xs, label="True output")
    plt.plot(t, meas, alpha=0.5, label="Noisy measurement")
    plt.axhline(r, linestyle="--", label="Command")
    plt.title("Sensor Noise Investigation")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.figure()
    plt.plot(t, us)
    plt.title("Derivative Noise in Control Command")
    plt.xlabel("Time [s]")
    plt.ylabel("Control")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
