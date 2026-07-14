"""
Project 02 — Line-of-Sight Guidance Simulator
Learn: LOS angle, heading command generation, guidance law vs control law.
"""
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle): return (angle + np.pi) % (2*np.pi) - np.pi

def main():
    dt = 0.05; t = np.arange(0, 80, dt)
    x, y, heading, speed = 0.0, -20.0, np.deg2rad(30), 4.0
    target = np.array([60.0, 20.0])
    heading_gain = 1.8; max_turn_rate = np.deg2rad(35)
    xs, ys, heading_errors = [], [], []
    for _ in t:
        dx, dy = target[0]-x, target[1]-y
        rng = np.hypot(dx, dy)
        los_angle = np.arctan2(dy, dx)
        err = wrap_angle(los_angle - heading)
        turn_rate = np.clip(heading_gain*err, -max_turn_rate, max_turn_rate)
        heading = wrap_angle(heading + turn_rate*dt)
        x += speed*np.cos(heading)*dt; y += speed*np.sin(heading)*dt
        xs.append(x); ys.append(y); heading_errors.append(np.rad2deg(err))
        if rng < 1.0: break
    plt.figure(); plt.plot(xs, ys, label='Vehicle path'); plt.scatter([target[0]], [target[1]], marker='x', label='Target')
    plt.title('Line-of-Sight Guidance'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
    plt.figure(); plt.plot(heading_errors); plt.title('Heading Error'); plt.xlabel('Step'); plt.ylabel('Error [deg]'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
