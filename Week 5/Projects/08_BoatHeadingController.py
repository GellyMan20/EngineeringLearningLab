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
Boat Heading Controller
Learn: heading control, integral action, constant disturbances.
"""
def wrap_angle(a):
    return (a + np.pi) % (2*np.pi) - np.pi

def main():
    dt = 0.05
    t = np.arange(0, 120, dt)
    desired, heading, yaw_rate = 0.0, np.deg2rad(45), 0.0
    pid = PID(1.8, 0.04, 0.8, output_limits=(-0.5, 0.5))
    headings, rudders = [], []
    for _ in t:
        rudder = pid.update(wrap_angle(desired - heading), dt)
        yaw_accel = 0.25*rudder - 0.5*yaw_rate + np.deg2rad(0.4)
        yaw_rate += yaw_accel*dt
        heading = wrap_angle(heading + yaw_rate*dt)
        headings.append(np.rad2deg(heading))
        rudders.append(rudder)
    plt.figure()
    plt.plot(t, headings, label="Heading")
    plt.axhline(0, linestyle="--", label="Desired")
    plt.title("Boat Heading Controller")
    plt.xlabel("Time [s]")
    plt.ylabel("Heading [deg]")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
