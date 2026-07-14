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
Disturbance Rejection Challenge
Learn: step disturbances, gusts, sensor bias.
"""
def simulate(case):
    dt = 0.01
    t = np.arange(0, 30, dt)
    x, v, target = 0.0, 0.0, 1.0
    pid = PID(4.0, 0.8, 2.5, output_limits=(-10, 10))
    xs = []
    for time in t:
        disturbance = 0.0
        bias = 0.0
        if case == "step_force" and time >= 10:
            disturbance = -1.5
        if case == "gust" and 10 <= time <= 14:
            disturbance = -4.0
        if case == "sensor_bias" and time >= 10:
            bias = 0.25
        u = pid.update(target - (x + bias), dt)
        v += (u + disturbance - 0.6*v - x)*dt
        x += v*dt
        xs.append(x)
    return t, np.array(xs)

def main():
    plt.figure()
    for case in ["step_force", "gust", "sensor_bias"]:
        t, x = simulate(case)
        plt.plot(t, x, label=case)
    plt.axhline(1, linestyle="--", label="Target")
    plt.title("Disturbance Rejection Challenge")
    plt.xlabel("Time [s]")
    plt.ylabel("Output")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
