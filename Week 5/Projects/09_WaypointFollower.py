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
Waypoint Following Vehicle
Learn: multiple PID loops, heading control, speed control, waypoint tracking.
"""
def wrap_angle(a):
    return (a + np.pi) % (2*np.pi) - np.pi

def main():
    dt = 0.05
    t = np.arange(0, 180, dt)
    waypoints = np.array([[0,0], [30,0], [30,30], [0,30], [0,0]], dtype=float)
    wp = 1
    x, y, heading, speed = 0.0, 0.0, 0.0, 0.0
    wheelbase = 2.5
    heading_pid = PID(2.5, 0.0, 0.4, output_limits=(-0.5, 0.5))
    speed_pid = PID(1.2, 0.2, 0.0, output_limits=(-2, 2))
    xs, ys = [], []
    for _ in t:
        target = waypoints[wp]
        dx, dy = target[0] - x, target[1] - y
        if np.hypot(dx, dy) < 1.5 and wp < len(waypoints)-1:
            wp += 1
            target = waypoints[wp]
            dx, dy = target[0] - x, target[1] - y
        desired_heading = np.arctan2(dy, dx)
        steering = heading_pid.update(wrap_angle(desired_heading - heading), dt)
        accel = speed_pid.update(5.0 - speed, dt)
        speed = max(0, speed + accel*dt)
        heading += (speed/wheelbase)*np.tan(steering)*dt
        x += speed*np.cos(heading)*dt + 0.15*dt
        y += speed*np.sin(heading)*dt - 0.05*dt
        xs.append(x); ys.append(y)
    plt.figure()
    plt.plot(xs, ys, label="Path")
    plt.scatter(waypoints[:,0], waypoints[:,1], marker="x", label="Waypoints")
    plt.title("Waypoint Following Vehicle")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
