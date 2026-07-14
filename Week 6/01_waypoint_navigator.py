"""
Project 01 — Waypoint Navigator
Learn: waypoint navigation, desired heading, distance-to-go, simple heading control.
"""
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi

def main():
    dt = 0.05
    t = np.arange(0, 140, dt)
    waypoints = np.array([[0,0], [30,0], [45,25], [20,45], [0,20]], dtype=float)
    x, y = waypoints[0]
    heading = np.deg2rad(20)
    speed = 3.0
    waypoint_index = 1
    heading_gain = 2.0
    max_turn_rate = np.deg2rad(45)
    xs, ys, dists = [], [], []
    for _ in t:
        target = waypoints[waypoint_index]
        dx, dy = target[0] - x, target[1] - y
        distance = np.hypot(dx, dy)
        if distance < 1.0 and waypoint_index < len(waypoints) - 1:
            waypoint_index += 1
            target = waypoints[waypoint_index]
            dx, dy = target[0] - x, target[1] - y
            distance = np.hypot(dx, dy)
        desired_heading = np.arctan2(dy, dx)
        heading_error = wrap_angle(desired_heading - heading)
        turn_rate = np.clip(heading_gain * heading_error, -max_turn_rate, max_turn_rate)
        heading = wrap_angle(heading + turn_rate * dt)
        x += speed * np.cos(heading) * dt
        y += speed * np.sin(heading) * dt
        xs.append(x); ys.append(y); dists.append(distance)
        if waypoint_index == len(waypoints) - 1 and distance < 1.0:
            break
    plt.figure(); plt.plot(xs, ys, label='Vehicle path'); plt.scatter(waypoints[:,0], waypoints[:,1], marker='x', label='Waypoints')
    plt.title('Waypoint Navigator'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
    plt.figure(); plt.plot(dists); plt.title('Distance to Current Waypoint'); plt.xlabel('Step'); plt.ylabel('Distance [m]'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
