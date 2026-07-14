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
Controller Comparison Suite
Learn: P vs PI vs PD vs PID using common metrics.
"""
def simulate(label, gains):
    dt = 0.01
    t = np.arange(0, 16, dt)
    x, v, target = 0.0, 0.0, 1.0
    pid = PID(*gains, output_limits=(-20, 20))
    xs, us = [], []
    for time in t:
        disturbance = -1.0 if 8 <= time <= 10 else 0.0
        u = pid.update(target - x, dt)
        v += (u + disturbance - 0.7*v - x)*dt
        x += v*dt
        xs.append(x); us.append(u)
    xs, us = np.array(xs), np.array(us)
    return label, t, xs, np.mean(abs(target-xs)), max(0, np.max(xs)-target), np.mean(abs(us))

def main():
    controllers = {"P": (4,0,0), "PI": (3,0.8,0), "PD": (4,0,2), "PID": (4,0.6,2)}
    results = [simulate(name, gains) for name, gains in controllers.items()]
    plt.figure()
    for label, t, xs, mean_error, overshoot, effort in results:
        plt.plot(t, xs, label=label)
    plt.axhline(1, linestyle="--", label="Target")
    plt.title("Controller Comparison Suite")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()
    print("\nController Metrics")
    for label, _, _, mean_error, overshoot, effort in results:
        print(f"{label:>3} | mean error={mean_error:.3f} | overshoot={overshoot:.3f} | effort={effort:.3f}")

if __name__ == "__main__":
    main()
