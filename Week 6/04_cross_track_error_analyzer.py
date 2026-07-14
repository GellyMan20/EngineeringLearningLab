"""
Project 04 — Cross-Track Error Analyzer
Learn: path deviation metrics: mean, RMS, max cross-track error.
"""
import numpy as np
import matplotlib.pyplot as plt

def distance_to_polyline(point, path):
    min_dist = float('inf')
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]
        ab = b - a; ap = point - a
        projection = np.clip(np.dot(ap, ab) / np.dot(ab, ab), 0.0, 1.0)
        candidate = a + projection*ab
        min_dist = min(min_dist, np.linalg.norm(point-candidate))
    return min_dist

def main():
    path_x = np.linspace(0, 100, 400); path_y = 8*np.sin(path_x/10)
    path = np.column_stack((path_x, path_y))
    rng = np.random.default_rng(4)
    vehicle_x = path_x
    vehicle_y = 8*np.sin((vehicle_x-4)/10) + 1.5*np.sin(vehicle_x/5) + rng.normal(0, 0.5, len(vehicle_x))
    vehicle_path = np.column_stack((vehicle_x, vehicle_y))
    errors = np.array([distance_to_polyline(p, path) for p in vehicle_path])
    print('Cross-Track Error Metrics')
    print(f'Mean error: {np.mean(errors):.3f} m')
    print(f'RMS error:  {np.sqrt(np.mean(errors**2)):.3f} m')
    print(f'Max error:  {np.max(errors):.3f} m')
    plt.figure(); plt.plot(path[:,0], path[:,1], '--', label='Desired path'); plt.plot(vehicle_path[:,0], vehicle_path[:,1], label='Vehicle path')
    plt.title('Cross-Track Error Analyzer'); plt.xlabel('X [m]'); plt.ylabel('Y [m]'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
    plt.figure(); plt.plot(errors); plt.title('Cross-Track Error'); plt.xlabel('Sample'); plt.ylabel('Error [m]'); plt.grid(True); plt.show()
if __name__ == '__main__': main()
