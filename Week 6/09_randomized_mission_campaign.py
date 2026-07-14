"""
Project 09 — Randomized Mission Campaign
Learn: mission-level Monte Carlo testing and robustness metrics.
"""
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle): return (angle + np.pi) % (2*np.pi) - np.pi

def run_mission(rng):
    dt = 0.05; t = np.arange(0, 80.0, dt)
    start = rng.uniform([-20,-20], [20,20]); goal = rng.uniform([50,30], [90,70])
    x, y = start; heading = rng.uniform(-np.pi, np.pi); speed = rng.uniform(2.5,5.5)
    max_turn = rng.uniform(np.deg2rad(20), np.deg2rad(55)); wind = rng.normal(0, 0.15, 2)
    xs, ys = [], []
    for time in t:
        dx, dy = goal[0]-x, goal[1]-y; dist = np.hypot(dx,dy)
        if dist < 1.5: return True, time, np.array(xs), np.array(ys), start, goal
        desired = np.arctan2(dy, dx); err = wrap_angle(desired-heading)
        turn_rate = np.clip(1.8*err, -max_turn, max_turn)
        heading = wrap_angle(heading + turn_rate*dt)
        x += speed*np.cos(heading)*dt + wind[0]*dt; y += speed*np.sin(heading)*dt + wind[1]*dt
        xs.append(x); ys.append(y)
    return False, 80.0, np.array(xs), np.array(ys), start, goal

def main():
    rng = np.random.default_rng(7); n = 250
    successes, times, examples = [], [], []
    for i in range(n):
        result = run_mission(rng); success, time, xs, ys, start, goal = result
        successes.append(success); times.append(time)
        if i < 8: examples.append(result)
    print(f'Mission success rate: {100*np.mean(successes):.1f}%')
    print(f'Mean completion/time-limit time: {np.mean(times):.2f} s')
    plt.figure()
    for success, time, xs, ys, start, goal in examples:
        if len(xs)>0: plt.plot(xs, ys)
        plt.scatter([start[0]], [start[1]], marker='o'); plt.scatter([goal[0]], [goal[1]], marker='x')
    plt.title('Example Randomized Missions'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.show()
    plt.figure(); plt.hist(times, bins=25); plt.title('Mission Completion / Timeout Times'); plt.xlabel('Time [s]'); plt.ylabel('Count'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
