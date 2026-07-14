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
Servo Position Controller
Learn: overshoot, settling time, PD/PID position control.
"""
def main():
    dt = 0.001
    t = np.arange(0, 5, dt)
    inertia, damping = 0.04, 0.03
    target, angle, rate = np.deg2rad(90), 0.0, 0.0
    pid = PID(12.0, 0.0, 1.2, output_limits=(-10, 10))
    angles, torques = [], []
    for _ in t:
        torque = pid.update(target - angle, dt)
        rate += ((torque - damping*rate) / inertia) * dt
        angle += rate*dt
        angles.append(np.rad2deg(angle))
        torques.append(torque)
    plt.figure()
    plt.plot(t, angles, label="Angle")
    plt.axhline(90, linestyle="--", label="Target")
    plt.title("Servo Position Controller")
    plt.xlabel("Time [s]")
    plt.ylabel("Angle [deg]")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
