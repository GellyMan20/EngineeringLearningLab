"""
Project 06 — Dubins Path Generator
Learn: minimum turning radius and heading-constrained path planning.
Teaching approximation, not a complete Dubins solver.
"""
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle): return (angle + np.pi) % (2*np.pi) - np.pi

def simulate_arc_line_arc(start, goal, turn_radius=8.0, ds=0.2):
    x, y, heading = start; gx, gy, gheading = goal
    xs, ys = [x], [y]
    goal_line_heading = np.arctan2(gy-y, gx-x)
    for _ in range(400):
        err = wrap_angle(goal_line_heading - heading)
        if abs(err) < np.deg2rad(2): break
        heading = wrap_angle(heading + np.sign(err)*ds/turn_radius)
        x += ds*np.cos(heading); y += ds*np.sin(heading); xs.append(x); ys.append(y)
    for _ in range(1000):
        dx, dy = gx-x, gy-y
        if np.hypot(dx,dy) < turn_radius: break
        heading = np.arctan2(dy, dx)
        x += ds*np.cos(heading); y += ds*np.sin(heading); xs.append(x); ys.append(y)
    for _ in range(500):
        err = wrap_angle(gheading-heading)
        if abs(err) < np.deg2rad(2) and np.hypot(gx-x, gy-y) < 2.0: break
        turn = np.sign(err) if abs(err) > np.deg2rad(2) else 0
        heading = wrap_angle(heading + turn*ds/turn_radius)
        desired = np.arctan2(gy-y, gx-x)
        heading = wrap_angle(0.85*heading + 0.15*desired)
        x += ds*np.cos(heading); y += ds*np.sin(heading); xs.append(x); ys.append(y)
    return np.array(xs), np.array(ys)

def main():
    start = (0.0, 0.0, np.deg2rad(0)); goal = (60.0, 35.0, np.deg2rad(90))
    xs, ys = simulate_arc_line_arc(start, goal)
    plt.figure(); plt.plot(xs, ys, label='Approximate Dubins-style path'); plt.scatter([start[0], goal[0]], [start[1], goal[1]], marker='x', label='Start / Goal')
    plt.title('Dubins Path Generator — Teaching Approximation'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
if __name__ == '__main__': main()
