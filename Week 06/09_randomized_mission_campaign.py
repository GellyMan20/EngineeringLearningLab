"""
Project 09 — Randomized Mission Campaign
Purpose:
This script demonstrates **mission-level Monte Carlo testing** for assessing the robustness of a vehicle's mission planning 
capabilities. The Monte Carlo approach evaluates performance metrics such as mission success rate and time to completion 
over a large number of randomized simulations.

Key concepts learned:
- **Monte Carlo testing**: Random generation of mission parameters (start, goal, wind conditions).
- **Robustness metrics**: Measure of mission success rates, completion times, and path behavior.
- **Randomized Scenarios**: Incorporates variability in mission elements like start/goal positions, wind perturbations, 
  and vehicle constraints.
- **Data analysis**: Histograms and path visualizations to analyze performance trends statistically.

The results include the mission success rate, average completion time, and example missions visualized dynamically.
"""

# Import necessary libraries
import numpy as np  # For numerical operations and randomness
import matplotlib.pyplot as plt  # For visualizing results (paths and metrics)

# Function to wrap angles into the range [-π, π]
def wrap_angle(angle):
    """
    Wrap an angle to the range [-π, π].
    Ensures that angular computations are normalized to avoid discrepancies.

    Parameters:
        angle (float): Angle in radians.

    Returns:
        float: Angle wrapped to [-π, π].
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

# Function to perform a single randomized mission
def run_mission(rng):
    """
    Simulates a single mission for a vehicle navigating from a random start position to a random goal.

    Parameters:
        rng (Generator): NumPy random number generator for reproducibility.

    Returns:
        tuple: 
            - success (bool): True if the mission succeeded by reaching the goal, False otherwise (timeout).
            - time (float): Time at which the mission succeeded or ended.
            - xs, ys (ndarray): Arrays of x, y coordinates of the vehicle's path.
            - start (ndarray): Starting position.
            - goal (ndarray): Goal position.
    """
    # Time settings
    dt = 0.05  # Simulation time step
    t = np.arange(0, 80.0, dt)  # Simulation time vector from 0 to 80 seconds

    # Randomize mission parameters
    start = rng.uniform([-20, -20], [20, 20])  # Random start position within a 40x40 area
    goal = rng.uniform([50, 30], [90, 70])  # Random goal position within specified bounds
    x, y = start  # Current vehicle position
    heading = rng.uniform(-np.pi, np.pi)  # Random initial heading (angle)
    speed = rng.uniform(2.5, 5.5)  # Random constant vehicle speed (m/s)
    max_turn = rng.uniform(np.deg2rad(20), np.deg2rad(55))  # Random maximum turn rate (radians/s)
    wind = rng.normal(0, 0.15, 2)  # Random wind perturbation in x and y (Gaussian noise)

    # Logs for plotting vehicle path
    xs, ys = [], []

    # Mission loop
    for time in t:
        # Calculate the relative position and distance to the goal
        dx, dy = goal[0] - x, goal[1] - y
        dist = np.hypot(dx, dy)  # Euclidean distance to the goal

        # Check if the goal is reached
        if dist < 1.5:  # Close enough to consider the goal reached
            return True, time, np.array(xs), np.array(ys), start, goal

        # Guidance law: Turn towards the goal
        desired = np.arctan2(dy, dx)  # Desired heading to the goal
        err = wrap_angle(desired - heading)  # Heading error
        turn_rate = np.clip(1.8 * err, -max_turn, max_turn)  # Proportional heading adjustment

        # Update vehicle heading and position
        heading = wrap_angle(heading + turn_rate * dt)  # Update heading
        x += speed * np.cos(heading) * dt + wind[0] * dt  # Update x-position with wind effect
        y += speed * np.sin(heading) * dt + wind[1] * dt  # Update y-position with wind effect
        xs.append(x)  # Log x-position
        ys.append(y)  # Log y-position

    # If time runs out, return timeout result
    return False, 80.0, np.array(xs), np.array(ys), start, goal

# Main function to perform Monte Carlo campaign and analyze results
def main():
    """
    Executes multiple randomized missions and evaluates the performance of a 
    vehicle navigating in a wind-disturbed environment. Visualizes example paths 
    and provides aggregated statistics such as success rates and time distributions.
    """

    # Set random number generator seed for reproducibility
    rng = np.random.default_rng(7)  # Random number generator
    n = 250  # Number of Monte Carlo trials

    # Initialize logs for performance metrics
    successes, times, examples = [], [], []

    # Perform Monte Carlo mission trials
    for i in range(n):
        result = run_mission(rng)  # Perform a single randomized mission
        success, time, xs, ys, start, goal = result  # Unpack the mission result
        successes.append(success)  # Log mission success
        times.append(time)  # Log time to completion or timeout
        if i < 8:  # Collect a few example mission paths for visualization
            examples.append(result)

    # Output aggregated results
    print(f'Mission success rate: {100 * np.mean(successes):.1f}%')  # Success rate percentage
    print(f'Mean completion/time-limit time: {np.mean(times):.2f} s')  # Average mission duration or timeout

    # Visualization: Plot example randomized missions
    plt.figure()
    for success, time, xs, ys, start, goal in examples:
        if len(xs) > 0:
            plt.plot(xs, ys, label='Vehicle path')  # Plot vehicle path
        plt.scatter([start[0]], [start[1]], marker='o', label='Start')  # Start position
        plt.scatter([goal[0]], [goal[1]], marker='x', label='Goal')  # Goal position
    plt.title('Example Randomized Missions')  # Add title
    plt.xlabel('X [m]')  # X-axis label
    plt.ylabel('Y [m]')  # Y-axis label
    plt.axis('equal')  # Equal x-y scaling
    plt.grid(True)  # Add a grid
    plt.legend()  # Add a legend
    plt.show()

    # Visualization: Histogram of mission completion times
    plt.figure()
    plt.hist(times, bins=25)  # Plot histogram of completion times
    plt.title('Mission Completion / Timeout Times')  # Add title
    plt.xlabel('Time [s]')  # X-axis label
    plt.ylabel('Count')  # Y-axis label
    plt.grid(True)  # Add grid
    plt.show()

# Entry point: Run the mission campaign
if __name__ == '__main__':
    main()
