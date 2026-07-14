"""
Inverted Pendulum
Learn: unstable systems and stabilizing feedback.
"""
import numpy as np
import matplotlib.pyplot as plt

def main():
    dt = 0.001
    t = np.arange(0, 10, dt)
    g, length = 9.81, 1.0
    theta, theta_dot = np.deg2rad(8), 0.0
    kp, kd = 45.0, 10.0
    angles, controls = [], []
    for _ in t:
        u = np.clip(-kp*theta - kd*theta_dot, -80, 80)
        theta_dot += ((g/length)*theta + u)*dt
        theta += theta_dot*dt
        angles.append(np.rad2deg(theta))
        controls.append(u)
    plt.figure()
    plt.plot(t, angles)
    plt.axhline(0, linestyle="--")
    plt.title("Inverted Pendulum Stabilization")
    plt.xlabel("Time [s]")
    plt.ylabel("Angle from upright [deg]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
