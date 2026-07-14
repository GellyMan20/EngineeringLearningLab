"""
Project 03 — Pure Pursuit Path Follower
Learn: lookahead point, curvature command, smooth path tracking.
"""
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle): return (angle + np.pi) % (2*np.pi) - np.pi

def find_lookahead_point(path, position, lookahead_distance):
    distances = np.linalg.norm(path - position, axis=1)
    candidates = np.where(distances >= lookahead_distance)[0]
    if len(candidates) == 0: return path[-1], len(path)-1
    return path[candidates[0]], candidates[0]

def main():
    dt = 0.05; t = np.arange(0, 120, dt)
    path_x = np.linspace(0, 100, 500); path_y = 10*np.sin(path_x/12)
    path = np.column_stack((path_x, path_y))
    x, y, heading, speed = 0.0, -8.0, 0.0, 4.0
    wheelbase, lookahead_distance = 2.5, 8.0
    xs, ys, steer = [], [], []
    for _ in t:
        lookahead, idx = find_lookahead_point(path, np.array([x, y]), lookahead_distance)
        alpha = wrap_angle(np.arctan2(lookahead[1]-y, lookahead[0]-x) - heading)
        curvature = 2*np.sin(alpha)/lookahead_distance
        steering = np.clip(np.arctan(wheelbase*curvature), np.deg2rad(-35), np.deg2rad(35))
        heading = wrap_angle(heading + (speed/wheelbase)*np.tan(steering)*dt)
        x += speed*np.cos(heading)*dt; y += speed*np.sin(heading)*dt
        xs.append(x); ys.append(y); steer.append(np.rad2deg(steering))
        if idx >= len(path)-2: break
    plt.figure(); plt.plot(path[:,0], path[:,1], '--', label='Desired path'); plt.plot(xs, ys, label='Vehicle path')
    plt.title('Pure Pursuit Path Follower'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
    plt.figure(); plt.plot(steer); plt.title('Steering Command'); plt.xlabel('Step'); plt.ylabel('Steering [deg]'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
