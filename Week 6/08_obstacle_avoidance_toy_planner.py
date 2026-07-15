"""
Project 08 — Obstacle Avoidance Toy Planner
Purpose:
This script demonstrates a basic **path planning algorithm** using the A* (A-star) algorithm. 
A* is a widely-used algorithm for grid-based pathfinding and obstacle avoidance, commonly used in 
robotics, games, and real-world navigation systems. Key concepts covered include:
- Building a grid environment with configurable obstacle costs.
- Utilizing the A* algorithm to find an optimized path from a start to a goal location.
- Calculating heuristic costs (e.g., Euclidean distance for navigation).
- Visualizing the environment, the planning grid, and the planned path.

This example serves as an educational tool for understanding path planning and optimization in 
a simplified 2D grid environment while accounting for obstacles and varying terrain costs.
"""

# Import necessary libraries
import heapq  # For a priority queue implementation of the open set
import numpy as np  # For numerical operations on arrays
import matplotlib.pyplot as plt  # For visualization of the grid and planned path

# A* Algorithm for Grid-Based Path Planning
def astar(grid, start, goal):
    """
    Performs path planning using the A* algorithm on a grid-based environment.

    Parameters:
        grid (ndarray): 2D array representing the environment with obstacle costs.
        start (tuple): Starting position (row, column).
        goal (tuple): Goal position (row, column).

    Returns:
        list: Optimized path from start to goal as a list of (row, column) tuples.
    """
    rows, cols = grid.shape  # Grid dimensions

    def h(a, b):
        """
        Compute the heuristic distance (Euclidean distance) between two points.

        Parameters:
            a (tuple): Point A (row, column).
            b (tuple): Point B (row, column).

        Returns:
            float: Euclidean distance between A and B.
        """
        return np.hypot(a[0] - b[0], a[1] - b[1])

    # Allowed movements: horizontal, vertical, and diagonal (8 neighbors)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Open set: priority queue of nodes to explore
    open_set = [(0, start)]  # (priority, node)
    came_from = {}  # Dictionary to track the optimal path
    g_score = {start: 0.0}  # Cost from start to current node

    # A* algorithm loop
    while open_set:
        _, current = heapq.heappop(open_set)  # Get node with smallest f-score (priority)

        # If goal is reached, reconstruct and return the path
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]  # Return the reconstructed path, in correct order from start to goal

        # Explore neighbors
        for dr, dc in neighbors:
            nr, nc = current[0] + dr, current[1] + dc  # Compute neighbor coordinates
            # Skip invalid neighbors (out of bounds or obstacles)
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr, nc] >= 100:
                continue

            # Compute tentative cost to reach this neighbor
            neighbor = (nr, nc)
            tentative = g_score[current] + np.hypot(dr, dc) + grid[nr, nc]

            # Update path and costs if this path is better
            if tentative < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                heapq.heappush(open_set, (tentative + h(neighbor, goal), neighbor))

    return []  # Return an empty list if no path is found

# Main function
def main():
    """
    Constructs a grid-based environment with predefined obstacles and varying terrain costs. 
    The A* algorithm is used to calculate an optimized path from the start to the goal, avoiding 
    obstacles and minimizing movement cost. Results are visualized in a 2D grid plot.
    """

    # Define the grid environment
    grid = np.zeros((80, 100))  # Create an 80x100 grid
    grid[25:55, 40:48] = 100  # Define obstacle region (high-cost areas to avoid)
    grid[10:25, 65:72] = 100  # Another obstacle region
    grid[50:70, 70:78] = 100  # Another obstacle region
    grid[30:60, 10:30] = 3.0  # Higher-cost region (e.g., rough terrain)

    # Define the start and goal positions
    start, goal = (70, 5), (10, 90)  # Starting position and goal position

    # Compute the path using the A* algorithm
    path = np.array(astar(grid, start, goal))  # Call A* to find the path

    # Visualization: Plot the grid-based environment with path
    plt.figure()
    plt.imshow(grid, origin='upper')  # Display the grid with obstacles and costs
    if len(path) > 0:  # If a path is found, plot it
        plt.plot(path[:, 1], path[:, 0], label='Planned path')  # Plot the path in row-column format
    plt.scatter([start[1], goal[1]], [start[0], goal[0]], marker='x', label='Start / Goal')  # Mark start and goal points
    plt.title('Obstacle Avoidance Toy Planner')  # Add title
    plt.xlabel('Column')  # X-axis label
    plt.ylabel('Row')  # Y-axis label
    plt.legend()  # Add legend
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
