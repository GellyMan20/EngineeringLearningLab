"""
Project 05 — Proportional Navigation Intercept
Learn: LOS rate, closing velocity, navigation constant, target intercept.
"""
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle): return (angle + np.pi) % (2*np.pi) - np.pi

def main():
    dt = 0.02; t = np.arange(0, 80, dt)
    pursuer_pos = np.array([0.0, 0.0]); pursuer_heading = np.deg2rad(20); pursuer_speed = 12.0
    target_pos = np.array([120.0, 40.0]); target_vel = np.array([-2.0, 1.0])
    N = 3.0; max_turn_rate = np.deg2rad(60)
    pursuer_path, target_path = [], []
    prev_los = None
    for _ in t:
        rel_pos = target_pos - pursuer_pos; rng = np.linalg.norm(rel_pos)
        if rng < 1.0:
            print('Intercept achieved.'); break
        los = np.arctan2(rel_pos[1], rel_pos[0])
        los_rate = 0.0 if prev_los is None else wrap_angle(los - prev_los)/dt
        prev_los = los
        pursuer_vel = pursuer_speed*np.array([np.cos(pursuer_heading), np.sin(pursuer_heading)])
        rel_vel = target_vel - pursuer_vel
        closing_velocity = -np.dot(rel_pos, rel_vel)/rng
        turn_rate = np.clip(N*closing_velocity*los_rate/pursuer_speed, -max_turn_rate, max_turn_rate)
        pursuer_heading = wrap_angle(pursuer_heading + turn_rate*dt)
        pursuer_pos += pursuer_speed*np.array([np.cos(pursuer_heading), np.sin(pursuer_heading)])*dt
        target_pos += target_vel*dt
        pursuer_path.append(pursuer_pos.copy()); target_path.append(target_pos.copy())
    pursuer_path = np.array(pursuer_path); target_path = np.array(target_path)
    plt.figure(); plt.plot(pursuer_path[:,0], pursuer_path[:,1], label='Pursuer'); plt.plot(target_path[:,0], target_path[:,1], label='Target')
    plt.title('Proportional Navigation Intercept'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
if __name__ == '__main__': main()
