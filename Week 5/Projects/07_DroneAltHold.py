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
Drone Altitude Hold
Learn: PID altitude control, wind disturbance, actuator limits.
"""
def main():
    dt = 0.01
    t = np.arange(0, 30, dt)
    mass, g, target = 1.5, 9.81, 20.0
    z, vz = 0.0, 0.0
    pid = PID(4.0, 0.8, 3.0, output_limits=(0, 35))
    zs, thrusts = [], []
    for time in t:
        wind_down = 3.0 if 12 <= time <= 18 else 0.0
        thrust = pid.update(target - z, dt)
        vz += ((thrust - mass*g - wind_down) / mass) * dt
        z += vz*dt
        if z < 0:
            z, vz = 0, max(0, vz)
        zs.append(z)
        thrusts.append(thrust)
    plt.figure()
    plt.plot(t, zs, label="Altitude")
    plt.axhline(target, linestyle="--", label="Target")
    plt.title("Drone Altitude Hold")
    plt.xlabel("Time [s]")
    plt.ylabel("Altitude [m]")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
