# Week 6 Reference Sheet — Guidance & Trajectory Generation

## **Purpose**  
This document serves as a quick-reference guide for the mathematical foundations, engineering intuition, and practical applications of guidance and trajectory generation. It complements the Week 6 Python projects and acts as a condensed reference while studying autonomous navigation.

---

## **1. Guidance vs Navigation vs Control (GNC)**

| Discipline | Purpose                           | Example                       |
|------------|-----------------------------------|-------------------------------|
| Navigation | Estimate where the vehicle is     | GPS, IMU, EKF                 |
| Guidance   | Decide where the vehicle should go| Waypoints, path following     |
| Control    | Generate actuator commands        | Steering, throttle, elevator  |

### Workflow:
**Mission → Planner → Guidance → Controller → Vehicle**

- **Navigation** involves state estimation, giving the vehicle knowledge of its current position, velocity, and orientation.
- **Guidance** decides how to progress to the desired location or goals, such as generating waypoints or determining the best path forward.
- **Control** executes guidance decisions by adjusting actuators like steering or throttle to follow commands and stay on course.

---

## **2. Coordinate Frames**

Understanding coordinate frames is crucial for defining positions, velocities, and orientations consistently.

### Common Frames:
- **World/Inertial**: Fixed global frame, often the reference for absolute positioning.
- **Body**: The moving local frame attached to the vehicle.
- **NED (North-East-Down)**: Used in aerospace and UAV navigation.
- **ENU (East-North-Up)**: Often used in robotics.

### Key Variables:
- **Position Vector**:
  \[
  p = [x, y]^T
  \]
  Represents the 2D position in a given frame.
- **Heading** (denoted by \( \psi \)): Represents the angular orientation of the vehicle relative to a reference frame.

---

## **3. Distance**

The Euclidean distance between two points \( (x_1, y_1) \) and \( (x_2, y_2) \) is:
\[
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
\]

### Applications:
- Determining if a waypoint has been reached.
- Checking obstacle clearance.
- Evaluating mission success.

---

## **4. Desired Heading**

The desired heading \( \psi_d \) is the angle required to move from the current position \( (x, y) \) to a target position \( (x_t, y_t) \):
\[
\psi_d = \text{atan2}(y_t - y, x_t - x)
\]

### Heading Error:
The difference between the desired heading and the current heading \( \psi \):
\[
e_\psi = \text{wrap}(\psi_d - \psi)
\]
Where wrap ensures that \( e_\psi \) stays within \( [-\pi, \pi] \).

---

## **5. Waypoint Navigation**

Navigate through discrete points leading to the goal. Steps:
1. **Compute distance**: Distance to the current waypoint.
2. **Compute desired heading**: Direction towards the waypoint.
3. **Compute heading error**: Difference between current and desired heading.
4. **Turn the vehicle**: Adjust heading to reduce error.
5. **Repeat**: Move to the next waypoint once the current waypoint is reached.

---

## **6. Path Following**

Instead of discrete waypoints, the vehicle follows a continuous path.

### Metrics:
- **Cross-Track Error**: Lateral error perpendicular to the desired path.
- **Along-Track Progress**: How much progress is made along the path.
- **Heading Error**: Difference in vehicle heading and desired heading.

---

## **7. Pure Pursuit**

A simple and robust path-following algorithm.

### Definitions:
- **Lookahead Distance (\(L_d\))**: Determines how far ahead the vehicle should target on the path.

### Curvature Calculation:
\[
\kappa = \frac{2 \sin(\alpha)}{L_d}
\]
Where \( \alpha \) is the angle between the vehicle's heading and the lookahead point.

**Small Lookahead**:
- High accuracy but leads to oscillations.

**Large Lookahead**:
- Smoother trajectory but may cut corners.

---

## **8. Proportional Navigation**

A method for intercepting a target by turning proportionally to the rate of change of the line of sight.

\[
\dot{\psi} = \frac{N \cdot V_c \cdot \dot{\lambda}}{V}
\]

Where:
- \( \dot{\psi} \): Angular velocity of the heading.
- \( N \): Navigation constant (gain).
- \( V_c \): Closing velocity.
- \( \dot{\lambda} \): Rate of change of the line of sight.

---

## **9. Dubins Paths**

Dubins paths consist of:
- **Left turns**
- **Right turns**
- **Straight segments**

### Features:
- Ensures paths respect a **minimum turning radius**, useful for fixed-wing aircraft and cars.

---

## **10. Smooth Trajectories**

Smooth trajectories are represented by:
- Position
- Velocity
- Acceleration
- (Sometimes) Jerk

**Benefits**:
- Improve tracking accuracy.
- Reduce actuator stress.

---

## **11. Cross-Track Error**

The perpendicular distance between the vehicle and the desired path.

### Common Metrics:
- **Mean Cross-Track Error**: Average deviation over a path.
- **RMS (Root Mean Squared)**: Magnifies larger deviations.
- **Maximum Cross-Track Error**: Largest error over the trajectory.

---

## **12. Mission Planning**

Mission planning optimizes for:
- **Distance**
- **Fuel efficiency**
- **Time-to-goal**
- **Safety and obstacle avoidance**

---

## **13. Obstacle Avoidance**

Algorithms that find collision-free paths:
- **A***: Graph search for shortest paths.
- **Dijkstra**: Finds shortest paths in weighted graphs.
- **RRT***: Rapidly-exploring random tree for feasible path.
- **PRM**: Probabilistic road maps for multi-query planning.

---

## **14. Performance Metrics**

Evaluate guidance and trajectory generation performance with:
- Mission completion rate
- Time-to-goal
- Path length
- Cross-track error
- Smoothness
- Control effort

---

## **15. Monte Carlo Testing**

Simulate hundreds of missions with randomized variables:
- Start and goal locations
- Environmental factors (e.g., wind)
- Noise levels
- Speed and turn limits

**Purpose**: Assess system robustness under varying conditions.

---

## **16. AI and Guidance**

- **Classical Guidance**: Determines how to follow a path.
- **Artificial Intelligence**: Selects the path to follow and optimizes guidance dynamically.
- Combined, these form the core of modern autonomous systems.

---

## **Key Takeaways**

- **Navigation**: Estimates state (e.g., position/velocity).
- **Guidance**: Generates a desired trajectory or path.
- **Control**: Executes actions to follow the trajectory.
- **Pure Pursuit**: Effective for tracking paths with simple tuning.
- **Proportional Navigation**: Ideal for interception problems.
- **Dubins Paths**: Respect turning constraints for vehicles.
- **Monte Carlo Testing**: Measures robustness and reliability.
