# Week 6 Reference Sheet — Guidance & Trajectory Generation

> **Purpose:**  
This document is a comprehensive guide to understanding the key concepts, mathematical foundations, and practical applications of guidance and trajectory generation. It complements the Week 6 Python projects, providing essential insights for autonomous navigation systems and their core algorithms.

---

## **1. Guidance vs Navigation vs Control (GNC)**

| **Discipline**  | **Purpose**                                  | **Example**               |
|------------------|----------------------------------------------|---------------------------|
| **Navigation**   | Estimate where the vehicle is               | GPS, IMU, EKF             |
| **Guidance**     | Decide where the vehicle should go          | Waypoints, path following |
| **Control**      | Generate actuator commands                  | Steering, throttle, elevator |

### Workflow:
The **Mission → Planner → Guidance → Controller → Vehicle** architecture breaks down into:
1. **Navigation**: Determines the current state (e.g., position, velocity) of the vehicle.
2. **Guidance**: Based on the mission planner or goal, determines the desired path or trajectory.
3. **Control**: Uses the trajectory to generate low-level commands for actuators to execute.

---

## **2. Coordinate Frames**

### Common Frames:
1. **World/Inertial Frame**: Fixed global reference frame.
2. **Body Frame**: Attached to the vehicle, moves with it (e.g., vehicle's forward is always the x-axis).
3. **NED (North-East-Down)**: Used in aviation, where "North" is the x-axis, "East" is the y-axis, and "Down" is the z-axis.
4. **ENU (East-North-Up)**: Common in mapping and ground robotics.

### Position Representation:
Position is typically represented as a 2D vector:
\[
\mathbf{p} = \begin{bmatrix} x \\ y \end{bmatrix}
\]

### Heading Representation:
Heading \( \psi \) represents the vehicle's orientation relative to the reference frame.

---

## **3. Distance Calculation**

The **Euclidean distance** between two points \( (x_1, y_1) \) and \( (x_2, y_2) \) is calculated as:
\[
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
\]

### Applications:
- Determines if a waypoint is reached.
- Measures obstacle clearance.
- Helps calculate trajectory completion.

---

## **4. Desired Heading**

To calculate the **desired heading** \( \psi_d \) from a current position \( (x, y) \) to a target position \( (x_t, y_t) \):
\[
\psi_d = \text{atan2}(y_t - y, x_t - x)
\]

### Heading Error:
The heading error \( e_\psi \) is the difference between the desired heading \( \psi_d \) and the current heading \( \psi \):
\[
e_\psi = \text{wrap}(\psi_d - \psi)
\]
where the **wrap function** ensures \( e_\psi \) is within \( [-\pi, \pi] \).

---

## **5. Waypoint Navigation**

### Steps:
1. Compute the distance to the current waypoint:
   \[
   d = \sqrt{(x_t - x)^2 + (y_t - y)^2}
   \]
2. Compute the desired heading \( \psi_d \).
3. Calculate the heading error \( e_\psi \).
4. Adjust the vehicle's heading to reduce \( e_\psi \).
5. Move to the next waypoint once the current one is reached.

### Practical Use:
- Ensures the vehicle follows multiple discrete points to a destination.

---

## **6. Path Following**

Instead of navigating discrete waypoints, this method tracks a **smooth continuous path**.

### Metrics:
- **Cross-Track Error (\( e_{\text{CT}} \))**: Distance from the vehicle to the desired path.
- **Along-Track Progress**: Measures how far the vehicle has progressed along the trajectory.
- **Heading Error (\( e_\psi \))**: Angle between the desired direction and the vehicle's heading.

---

## **7. Pure Pursuit**

A simple and widely-used **path following algorithm**.

### Curvature:
\[
\kappa = \frac{2 \sin(\alpha)}{L_d}
\]
Where:
- \( \alpha \): Angle between the vehicle's heading and the lookahead point.
- \( L_d \): Lookahead distance to the target point.

### Trade-offs:
1. **Small Lookahead**:
   - High accuracy.
   - Increased oscillations.
2. **Large Lookahead**:
   - Smoother trajectories.
   - Greater path deviation.

---

## **8. Proportional Navigation**

This approach uses the **line-of-sight rate** for interception, widely used in missile guidance and collision avoidance.

\[
\dot{\psi} = \frac{N \cdot V_c \cdot \dot{\lambda}}{V}
\]
Where:
- \( \dot{\psi} \): Rate of turn.
- \( N \): Proportional navigation constant (gain).
- \( V_c \): Closing velocity.
- \( \dot{\lambda} \): Rate of change of the line-of-sight angle.

---

## **9. Dubins Paths**

A geometric solution for path planning that maintains a minimum turning radius.

### Composed of 3 Possible Segments:
1. Left Turn (L)
2. Right Turn (R)
3. Straight Line (S)

### Applications:
- Planning paths for fixed-wing aircraft, ground vehicles, or any system with turning radius constraints.

---

## **10. Smooth Trajectories**

Trajectory planning considers:
- Position.
- Velocity.
- Acceleration.
- (Optional) Jerk.

**Advantages**:
- Reduces actuator wear and tear.
- Improves tracking accuracy.

---

## **11. Cross-Track Error (\( e_{\text{CT}} \))**

The perpendicular distance between the vehicle's position and the desired path.

### Common Metrics:
- **Mean Cross-Track Error**:
  \[
  \text{Mean } e_{\text{CT}} = \frac{1}{N} \sum_{i=1}^N e_{\text{CT}}^i
  \]
- **RMS (Root Mean Square)**:
  \[
  \text{RMS} = \sqrt{\frac{1}{N} \sum_{i=1}^N (e_{\text{CT}}^i)^2}
  \]

---

## **12. Mission Planning**

Optimizes performance based on:
- Distance.
- Fuel efficiency.
- Time-to-goal.
- Safety (e.g., avoiding collisions).
- Obstacle clearance.

---

## **13. Obstacle Avoidance**

Algorithms for dynamic path planning to avoid collisions:
- **A***: Graph-based shortest path algorithm.
- **Dijkstra**: Finds shortest paths in graphs with weighted edges.
- **RRT***: Generates random trees for path exploration.
- **PRM**: Builds a probabilistic roadmap for navigation in complex spaces.

---

## **14. Performance Metrics**

To evaluate guidance and trajectory systems:
- **Mission Completion Rate**: Successful task rate.
- **Time-to-Goal**: How quickly the destination is reached.
- **Path Length**: Total distance traveled.
- **Smoothness**: Minimized abrupt transitions in trajectory.
- **Control Effort**: Amount of control input needed for mission completion.

---

## **15. Monte Carlo Testing**

Monte Carlo simulations test the robustness of the guidance system by randomizing initial conditions:
- Start/Goal locations.
- Environmental disturbances (e.g., wind or noise).
- Vehicle parameters (e.g., turn rate limits, speed).

Monitor outcomes across hundreds of randomized scenarios.

---

## **16. AI and Guidance**

- **Classical Guidance**: Generates paths or commands based on precise models and algorithms.
- **AI-Based Guidance**: Leverages learning algorithms (e.g., reinforcement learning) to decide high-level paths or adapt in dynamic environments.
- **Integration**: AI determines the optimal path, while classical guidance executes the path.

---

## **Key Takeaways**
- **Navigation**: Estimates current state (position/velocity).
- **Guidance**: Defines where to go next.
- **Control**: Determines how to get there.
- **Pure Pursuit**: A simple, effective path-following algorithm.
- **Proportional Navigation**: Ideal for interception.
- **Dubins Paths**: Solutions for vehicles with turning constraints.
- **Monte Carlo Testing**: Simulates robust performance under varying conditions.
