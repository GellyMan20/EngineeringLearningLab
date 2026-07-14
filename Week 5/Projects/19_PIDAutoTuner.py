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
PID Auto-Tuner
Learn: gain recommendation using grid search and objective functions.
"""
def simulate(kp, ki, kd, return_series=False):
    dt = 0.01
    t = np.arange(0, 12, dt)
    x, v, target = 0.0, 0.0, 1.0
    pid = PID(kp, ki, kd, output_limits=(-20, 20))
    xs, us = [], []
    for _ in t:
        u = pid.update(target - x, dt)
        v += (u - 0.8*v - x)*dt
        x += v*dt
        xs.append(x); us.append(u)
    xs, us = np.array(xs), np.array(us)
    score = np.mean(abs(target-xs)) + 2*max(0, np.max(xs)-target) + 0.02*np.mean(abs(us))
    if return_series:
        return score, t, xs, us
    return score

def main():
    best = None
    for kp in np.linspace(1, 10, 10):
        for ki in np.linspace(0, 2, 5):
            for kd in np.linspace(0, 5, 8):
                score = simulate(kp, ki, kd)
                if best is None or score < best[0]:
                    best = (score, kp, ki, kd)
    score, kp, ki, kd = best
    print(f"Best score: {score:.4f}")
    print(f"Recommended gains: Kp={kp:.2f}, Ki={ki:.2f}, Kd={kd:.2f}")
    _, t, xs, _ = simulate(kp, ki, kd, True)
    plt.figure()
    plt.plot(t, xs, label="Output")
    plt.axhline(1, linestyle="--", label="Target")
    plt.title("PID Auto-Tuner Best Response")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
