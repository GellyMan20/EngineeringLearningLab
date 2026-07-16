"""
Project 10 — Guidance Architecture Package Demo
Purpose:
This project demonstrates a **Guidance Architecture Package** that integrates various navigation components to simulate 
a vehicle navigating a mission with multiple waypoints. The architecture involves:
- A **Mission Manager** to define mission goals and handle waypoint transitions.
- A **Straight Line Planner** to generate paths connecting waypoints.
- A **Guidance Law** (Line-of-Sight or LOS guidance) to compute heading commands.
- A **Vehicle Model** accounting for motion dynamics and environmental effects, such as wind.
- An **Analyzer** to evaluate performance metrics like heading error and vehicle trajectory.

Key Concepts:
- Integration of mission planning, guidance, and control into a cohesive architecture.
- Testing path-following algorithms with realistic motions and environmental effects.
- Logging metrics like heading error to evaluate navigation performance.
- Visualizing the planned trajectory, executed path, and heading adjustments.
"""

# Import necessary libraries
from dataclasses import dataclass  # For structured data representation
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For plotting and visualization

# Helper function to wrap angles within the range [-π, π]
def wrap_angle(angle):
    """
    Wrap an angle to the range [-π, π].

    Parameters:
        angle (float): Angle in radians.

    Returns:
        float: Wrapped angle within [-π, π].
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi

# Vehicle state representation (position, heading, and speed)
@dataclass
class VehicleState:
    x: float  # X position
    y: float  # Y position
    heading: float  # Heading angle (radians)
    speed: float  # Speed (m/s)

# Mission details, including waypoints and a waypoint acceptance radius
@dataclass
class Mission:
    waypoints: np.ndarray  # Array of 2D [x, y] waypoint coordinates
    acceptance_radius: float = 1.5  # Radius for waypoint acceptance (meters)

# Mission Manager that tracks waypoint progress and mission completion
class MissionManager:
    def __init__(self, mission):
        """
        Mission Manager to track progress through waypoints.

        Parameters:
            mission (Mission): The mission containing waypoints and acceptance radius.
        """
        self.mission = mission
        self.index = 1  # Start with the second waypoint as the target

    def current_target(self):
        """Returns the current target waypoint."""
        return self.mission.waypoints[self.index]

    def update(self, state):
        """
        Checks if the vehicle reached the current target. Updates to the next waypoint if necessary.

        Parameters:
            state (VehicleState): Current state of the vehicle.

        Returns:
            bool: True if the mission is complete, False otherwise.
        """
        target = self.current_target()
        distance = np.hypot(target[0] - state.x, target[1] - state.y)  # Compute distance to waypoint
        if distance < self.mission.acceptance_radius and self.index < len(self.mission.waypoints) - 1:
            self.index += 1  # Move to the next waypoint
        return self.index == len(self.mission.waypoints) - 1 and distance < self.mission.acceptance_radius

# Path planner that generates a straight-line path between waypoints
class StraightLinePlanner:
    def plan(self, mission):
        """Returns the waypoint sequence as the planned path."""
        return mission.waypoints

# Line-of-Sight (LOS) Guidance module for heading control
class LOSGuidance:
    def __init__(self, heading_gain=2.0, max_turn_rate=np.deg2rad(40)):
        """
        Initializes the LOS guidance system with proportional heading gain and turn rate limits.

        Parameters:
            heading_gain (float): Proportional gain for heading control.
            max_turn_rate (float): Maximum allowable turn rate (radians/second).
        """
        self.heading_gain = heading_gain
        self.max_turn_rate = max_turn_rate

    def command(self, state, target, dt):
        """
        Computes the turn rate and heading error based on LOS guidance.

        Parameters:
            state (VehicleState): Current state of the vehicle.
            target (ndarray): Current waypoint [x, y].
            dt (float): Time step.

        Returns:
            float: Turn rate (radians/second).
            float: Heading error (radians).
        """
        desired = np.arctan2(target[1] - state.y, target[0] - state.x)  # Desired heading
        heading_error = wrap_angle(desired - state.heading)  # Compute heading error
        # Compute turn rate using proportional control with constraints
        turn_rate = np.clip(self.heading_gain * heading_error, -self.max_turn_rate, self.max_turn_rate)
        return turn_rate, heading_error

# Simple vehicle model to simulate movement and environmental effects
class SimpleVehicle:
    def __init__(self, wind=np.array([0.0, 0.0])):
        """
        Initializes the vehicle model with external wind effects.

        Parameters:
            wind (ndarray): Wind vector affecting the vehicle's motion [x, y].
        """
        self.wind = wind

    def step(self, state, turn_rate, dt):
        """
        Updates the vehicle state (position, heading) based on turn rate, speed, and wind.

        Parameters:
            state (VehicleState): Current state of the vehicle.
            turn_rate (float): Turn rate (radians/second).
            dt (float): Time step (seconds).

        Returns:
            VehicleState: Updated state of the vehicle.
        """
        state.heading = wrap_angle(state.heading + turn_rate * dt)  # Update heading based on turn rate
        state.x += state.speed * np.cos(state.heading) * dt + self.wind[0] * dt  # Update x-position
        state.y += state.speed * np.sin(state.heading) * dt + self.wind[1] * dt  # Update y-position
        return state

# Analyzer to log data and compute performance metrics
class Analyzer:
    def __init__(self):
        """Initializes the data logger for the vehicle's performance."""
        self.xs = []  # X-coordinates of the vehicle's path
        self.ys = []  # Y-coordinates of the vehicle's path
        self.heading_errors = []  # Heading error log (in degrees)

    def log(self, state, heading_error):
        """Logs the vehicle state and heading error."""
        self.xs.append(state.x)
        self.ys.append(state.y)
        self.heading_errors.append(np.rad2deg(heading_error))

    def report(self):
        """Prints performance metrics for the mission."""
        print('Guidance Architecture Demo Metrics')
        print(f'Samples: {len(self.xs)}')
        print(f'Mean abs heading error: {np.mean(np.abs(self.heading_errors)):.2f} deg')
        print(f'Max abs heading error:  {np.max(np.abs(self.heading_errors)):.2f} deg')

# Main function
def main():
    """
    Simulates a vehicle executing a mission with multiple waypoints using the guidance architecture package.
    Visualizes the planned path, executed vehicle trajectory, and heading errors.
    """

    # Time settings
    dt = 0.05  # Simulation time step
    t = np.arange(0, 160, dt)  # Time array for simulation

    # Define the mission with waypoints and an acceptance radius
    mission = Mission(np.array([[0, 0], [25, 5], [50, 25], [35, 50], [10, 40]], dtype=float))

    # Initialize components of the guidance architecture
    path = StraightLinePlanner().plan(mission)  # Plan the straight-line path
    manager = MissionManager(mission)  # Mission manager to monitor waypoint progress
    guidance = LOSGuidance()  # Line-of-sight guidance law
    vehicle = SimpleVehicle(wind=np.array([0.08, -0.03]))  # Vehicle model with wind effects
    analyzer = Analyzer()  # Analyzer for logging metrics and visualization

    # Initialize the vehicle's state
    state = VehicleState(0.0, 0.0, np.deg2rad(10), 3.5)  # Starting from (0,0) with a 10° heading

    # Mission execution loop
    for _ in t:
        target = manager.current_target()  # Get current waypoint target
        turn_rate, error = guidance.command(state, target, dt)  # Compute guidance command
        state = vehicle.step(state, turn_rate, dt)  # Update vehicle state
        analyzer.log(state, error)  # Log state and heading error
        if manager.update(state):  # Check if mission is complete
            break

    # Output performance metrics
    analyzer.report()

    # Visualization: Plot the mission and vehicle path
    plt.figure()
    plt.plot(path[:, 0], path[:, 1], '--', label='Mission path')  # Planned path
    plt.plot(analyzer.xs, analyzer.ys, label='Vehicle path')  # Actual vehicle path
    plt.scatter(path[:, 0], path[:, 1], marker='x', label='Waypoints')  # Waypoints
    plt.title('Guidance Architecture Package Demo')
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Visualization: Plot heading error over time
    plt.figure()
    plt.plot(analyzer.heading_errors)
    plt.title('Heading Error')
    plt.xlabel('Step')
    plt.ylabel('Heading Error [deg]')
    plt.grid(True)
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
