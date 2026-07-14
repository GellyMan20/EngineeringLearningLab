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
Monte Carlo PID Campaign
Learn: robustness under randomized mass, drag, wind, hills.
"""
def run_trial(rng):
    dt = 0.05
    t = np.arange(0, 60, dt)
    mass = rng.normal(1500, 150)
    drag = rng.normal(0.35, 0.05)
    hill_force = rng.uniform(400, 1500)
    wind_force = rng.uniform(0, 800)
    target, speed = 27.0, 0.0
    pid = PID(0.08, 0.015, 0.01, output_limits=(0, 1))
    errors = []
    for time in t:
        disturbance = (hill_force if 20 <= time <= 40 else 0) + (wind_force if time > 35 else 0)
        throttle = pid.update(target - speed, dt)
        speed += ((throttle*4500 - drag*speed**2 - disturbance) / mass)*dt
        errors.append(abs(target - speed))
    return np.mean(errors), np.max(errors)

def main():
    rng = np.random.default_rng(5)
    results = np.array([run_trial(rng) for _ in range(300)])
    success = np.mean(results[:,0] < 3.0)*100
    plt.figure()
    plt.hist(results[:,0], bins=30)
    plt.title(f"Monte Carlo PID Campaign — Success Rate {success:.1f}%")
    plt.xlabel("Mean speed error [m/s]")
    plt.ylabel("Trial count")
    plt.grid(True)
    plt.show()
    plt.figure()
    plt.scatter(results[:,0], results[:,1])
    plt.title("Mean Error vs Max Error")
    plt.xlabel("Mean error [m/s]")
    plt.ylabel("Max error [m/s]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
