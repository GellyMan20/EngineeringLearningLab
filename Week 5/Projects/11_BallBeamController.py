"""
Ball-on-Beam Controller
Learn: stability, sensitivity, balancing dynamics.
"""
import numpy as np
import matplotlib.pyplot as plt

class PD:
    def __init__(self, kp, kd, output_limits=(-0.25, 0.25)):
        self.kp = kp
        self.kd = kd
        self.output_limits = output_limits
        self.prev_error = 0.0
    def update(self, error, dt):
        d = (error - self.prev_error) / dt
        self.prev_error = error
        return float(np.clip(self.kp*error + self.kd*d, *self.output_limits))

def main():
    dt = 0.001
    t = np.arange(0, 12, dt)
    x, v, target = 0.4, 0.0, 0.0
    controller = PD(1.8, 1.0)
    xs, angles = [], []
    for _ in t:
        beam_angle = controller.update(target - x, dt)
        a = (5/7)*9.81*np.sin(beam_angle)
        v += a*dt
        x += v*dt
        xs.append(x); angles.append(np.rad2deg(beam_angle))
    plt.figure()
    plt.plot(t, xs)
    plt.axhline(0, linestyle="--")
    plt.title("Ball-on-Beam Control")
    plt.xlabel("Time [s]")
    plt.ylabel("Ball position [m]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
