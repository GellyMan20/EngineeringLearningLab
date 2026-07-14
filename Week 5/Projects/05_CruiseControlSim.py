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
Cruise Control Simulator
Learn: PID tuning and disturbance rejection.
"""
def main():
    dt = 0.05
    t = np.arange(0, 80, dt)
    mass, drag, max_force = 1500.0, 0.38, 4500.0
    target_speed, speed = 27.0, 0.0
    pid = PID(0.08, 0.015, 0.01, output_limits=(0, 1))
    speeds, throttles = [], []
    for time in t:
        hill = 1200.0 if 30 <= time <= 50 else 0.0
        wind = 600.0 if time >= 55 else 0.0
        throttle = pid.update(target_speed - speed, dt)
        accel = (throttle*max_force - drag*speed**2 - hill - wind) / mass
        speed += accel*dt
        speeds.append(speed)
        throttles.append(throttle)
    plt.figure()
    plt.plot(t, speeds, label="Speed")
    plt.axhline(target_speed, linestyle="--", label="Target")
    plt.title("Cruise Control PID")
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [m/s]")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.figure()
    plt.plot(t, throttles)
    plt.title("Throttle")
    plt.xlabel("Time [s]")
    plt.ylabel("Throttle [0-1]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
