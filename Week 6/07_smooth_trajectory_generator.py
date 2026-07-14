"""
Project 07 — Smooth Trajectory Generator
Learn: position, velocity, acceleration profiles with a fifth-order smoothstep.
"""
import numpy as np
import matplotlib.pyplot as plt

def smoothstep_trajectory(p0, pf, duration, dt):
    t = np.arange(0, duration + dt, dt); a = t/duration
    s = 10*a**3 - 15*a**4 + 6*a**5
    ds = 30*a**2 - 60*a**3 + 30*a**4
    d2s = 60*a - 180*a**2 + 120*a**3
    pos = p0 + (pf-p0)*s[:, None]
    vel = (pf-p0)*ds[:, None]/duration
    acc = (pf-p0)*d2s[:, None]/duration**2
    return t, pos, vel, acc

def main():
    p0 = np.array([0.0,0.0]); pf = np.array([50.0,30.0])
    t, pos, vel, acc = smoothstep_trajectory(p0, pf, 12.0, 0.02)
    plt.figure(); plt.plot(pos[:,0], pos[:,1]); plt.scatter([p0[0], pf[0]], [p0[1], pf[1]], marker='x')
    plt.title('Smooth 2D Trajectory'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.show()
    plt.figure(); plt.plot(t, np.linalg.norm(vel, axis=1)); plt.title('Speed Profile'); plt.xlabel('Time [s]'); plt.ylabel('Speed [m/s]'); plt.grid(True); plt.show()
    plt.figure(); plt.plot(t, np.linalg.norm(acc, axis=1)); plt.title('Acceleration Magnitude'); plt.xlabel('Time [s]'); plt.ylabel('Acceleration [m/s²]'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
