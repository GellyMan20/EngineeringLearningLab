"""
Project 08 — Obstacle Avoidance Toy Planner
Learn: path planning, obstacle cost, route optimization concepts with A*.
"""
import heapq
import numpy as np
import matplotlib.pyplot as plt

def astar(grid, start, goal):
    rows, cols = grid.shape
    def h(a,b): return np.hypot(a[0]-b[0], a[1]-b[1])
    neighbors = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    open_set = [(0, start)]; came_from = {}; g_score = {start: 0.0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]; path.append(current)
            return path[::-1]
        for dr, dc in neighbors:
            nr, nc = current[0]+dr, current[1]+dc
            if nr<0 or nr>=rows or nc<0 or nc>=cols or grid[nr,nc] >= 100: continue
            neighbor = (nr,nc); tentative = g_score[current] + np.hypot(dr,dc) + grid[nr,nc]
            if tentative < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current; g_score[neighbor] = tentative
                heapq.heappush(open_set, (tentative + h(neighbor, goal), neighbor))
    return []

def main():
    grid = np.zeros((80,100)); grid[25:55,40:48] = 100; grid[10:25,65:72] = 100; grid[50:70,70:78] = 100; grid[30:60,10:30] = 3.0
    start, goal = (70,5), (10,90); path = np.array(astar(grid, start, goal))
    plt.figure(); plt.imshow(grid, origin='upper')
    if len(path) > 0: plt.plot(path[:,1], path[:,0], label='Planned path')
    plt.scatter([start[1], goal[1]], [start[0], goal[0]], marker='x', label='Start / Goal')
    plt.title('Obstacle Avoidance Toy Planner'); plt.xlabel('Column'); plt.ylabel('Row'); plt.legend(); plt.show()
if __name__ == '__main__': main()
