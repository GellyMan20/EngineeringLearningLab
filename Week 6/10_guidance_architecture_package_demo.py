"""
Project 10 — Guidance Architecture Package Demo
Learn: mission manager, planner, guidance law, vehicle model, analyzer architecture.
"""
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt

def wrap_angle(angle): return (angle + np.pi) % (2*np.pi) - np.pi

@dataclass
class VehicleState:
    x: float; y: float; heading: float; speed: float

@dataclass
class Mission:
    waypoints: np.ndarray; acceptance_radius: float = 1.5

class MissionManager:
    def __init__(self, mission): self.mission = mission; self.index = 1
    def current_target(self): return self.mission.waypoints[self.index]
    def update(self, state):
        target = self.current_target(); dist = np.hypot(target[0]-state.x, target[1]-state.y)
        if dist < self.mission.acceptance_radius and self.index < len(self.mission.waypoints)-1: self.index += 1
        return self.index == len(self.mission.waypoints)-1 and dist < self.mission.acceptance_radius

class StraightLinePlanner:
    def plan(self, mission): return mission.waypoints

class LOSGuidance:
    def __init__(self, heading_gain=2.0, max_turn_rate=np.deg2rad(40)):
        self.heading_gain = heading_gain; self.max_turn_rate = max_turn_rate
    def command(self, state, target, dt):
        desired = np.arctan2(target[1]-state.y, target[0]-state.x)
        err = wrap_angle(desired - state.heading)
        return np.clip(self.heading_gain*err, -self.max_turn_rate, self.max_turn_rate), err

class SimpleVehicle:
    def __init__(self, wind=np.array([0.0,0.0])): self.wind = wind
    def step(self, state, turn_rate, dt):
        state.heading = wrap_angle(state.heading + turn_rate*dt)
        state.x += state.speed*np.cos(state.heading)*dt + self.wind[0]*dt
        state.y += state.speed*np.sin(state.heading)*dt + self.wind[1]*dt
        return state

class Analyzer:
    def __init__(self): self.xs=[]; self.ys=[]; self.heading_errors=[]
    def log(self, state, heading_error):
        self.xs.append(state.x); self.ys.append(state.y); self.heading_errors.append(np.rad2deg(heading_error))
    def report(self):
        print('Guidance Architecture Demo Metrics')
        print(f'Samples: {len(self.xs)}')
        print(f'Mean abs heading error: {np.mean(np.abs(self.heading_errors)):.2f} deg')
        print(f'Max abs heading error:  {np.max(np.abs(self.heading_errors)):.2f} deg')

def main():
    dt = 0.05; t = np.arange(0, 160, dt)
    mission = Mission(np.array([[0,0], [25,5], [50,25], [35,50], [10,40]], dtype=float))
    path = StraightLinePlanner().plan(mission); manager = MissionManager(mission)
    guidance = LOSGuidance(); vehicle = SimpleVehicle(wind=np.array([0.08,-0.03])); analyzer = Analyzer()
    state = VehicleState(0.0, 0.0, np.deg2rad(10), 3.5)
    for _ in t:
        target = manager.current_target(); turn_rate, err = guidance.command(state, target, dt)
        state = vehicle.step(state, turn_rate, dt); analyzer.log(state, err)
        if manager.update(state): break
    analyzer.report()
    plt.figure(); plt.plot(path[:,0], path[:,1], '--', label='Mission path'); plt.plot(analyzer.xs, analyzer.ys, label='Vehicle path'); plt.scatter(path[:,0], path[:,1], marker='x', label='Waypoints')
    plt.title('Guidance Architecture Package Demo'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
    plt.figure(); plt.plot(analyzer.heading_errors); plt.title('Heading Error'); plt.xlabel('Step'); plt.ylabel('Heading Error [deg]'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
