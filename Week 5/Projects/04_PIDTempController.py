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
PID Temperature Controller
Learn: P, I, D behavior and steady-state error.
"""
def main():
    dt = 0.1
    t = np.arange(0, 300, dt)
    ambient, target, temp = 20.0, 70.0, 20.0
    thermal_mass, loss = 50.0, 0.08
    pid = PID(3.0, 0.04, 8.0, output_limits=(0, 100))
    temps, controls = [], []
    for time in t:
        disturbance = -10.0 if 120 <= time <= 160 else 0.0
        power = pid.update(target - temp, dt)
        temp += ((power - loss*(temp - ambient) + disturbance) / thermal_mass) * dt
        temps.append(temp)
        controls.append(power)
    plt.figure()
    plt.plot(t, temps, label="Temperature")
    plt.axhline(target, linestyle="--", label="Target")
    plt.title("PID Temperature Controller")
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.figure()
    plt.plot(t, controls)
    plt.title("Heater Command")
    plt.xlabel("Time [s]")
    plt.ylabel("Power [%]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
