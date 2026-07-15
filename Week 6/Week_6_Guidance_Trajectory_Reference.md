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
1. **Navigation**: Determines the current state (e.g., position, velocity) of the vehicle using sensors like GPS, IMU (Inertial Measurement Unit), and filters like the Extended Kalman Filter (EKF).
2. **Guidance**: Determines the desired trajectory to achieve the vehicle's goal. This can involve path planning, waypoint navigation, or following a predefined trajectory.
3. **Control**: Executes low-level actuator commands (steering, acceleration, throttle) to follow the planned trajectory and achieve the guidance requirements.

---

## **2. Coordinate Frames**

### Common Frames:
1. **World/Inertial Frame**: Fixed global reference frame, typically used for absolute positioning.
2. **Body Frame**: Moves relative to the vehicle, with the x-axis pointing forward.
3. **NED (North-East-Down Frame)**: Common in aviation, where "North" is the x-axis, "East" is the y-axis, and "Down" is the z-axis.
4. **ENU (East-North-Up Frame)**: Often used in ground robotics and mapping, where "East" is the x-axis, "North" is the y-axis, and "Up" is the z-axis.

### Position Representation:
Position is often represented as a 2D vector:
\[
\mathbf{p} = \begin{bmatrix} x \\ y \end{bmatrix}
\]

### Heading Representation:
- **Heading (\( \psi \))** represents the vehicle's orientation relative to the reference frame (e.g., direction of travel in 2D space).
- Positive values of \( \psi \) represent counterclockwise orientation relative to the reference frame's x-axis.

---

## **3. Distance Calculation**

The **Euclidean distance** between two points \( (x_1, y_1) \) and \( (x_2, y_2) \) is calculated as:
\[
d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
\]

### Applications:
- Determines if the vehicle has arrived at a waypoint.
- Checks for safe distances from obstacles.
- Measures how far the vehicle has deviated from a planned trajectory.

---

## **4. Desired Heading**

To calculate the **desired heading** \( \psi_d \) from a current position \( (x, y) \) to a target position \( (x_t, y_t) \):
\[
\psi_d = \text{atan2}(y_t - y, x_t - x)
\]

### Heading Error:
The heading error \( e_\psi \) is the difference between the desired heading \( \psi_d \) and the current heading \( \psi \). To prevent angular wraparound, the error is normalized to the range \( [-\pi, \pi] \):
\[
e_\psi = \text{wrap}(\psi_d - \psi)
\]
where the **wrap function** ensures no discontinuities in angular computations.

---

## **5. Waypoint Navigation**

### Steps:
1. Compute the distance to the current waypoint:
   \[
   d = \sqrt{(x_t - x)^2 + (y_t - y)^2}
   \]
   If \( d < d_{\text{threshold}} \), the waypoint is considered reached.
2. Compute the desired heading \( \psi_d \):
   \[
   \psi_d = \text{atan2}(y_t - y, x_t - x)
   \]
3. Calculate the heading error \( e_\psi \): 
   \[
   e_\psi = \text{wrap}(\psi_d - \psi)
   \]
4. Adjust the vehicle's heading to minimize \( e_\psi \):
   Use proportional control:
   \[
   \Delta \psi(t) = K_h \cdot e_\psi
   \]
   where \( K_h \) is the heading gain.
5. Move to the next waypoint:
   - Focus shifts to the next waypoint once \( d < d_{\text{threshold}} \).

---

## **6. Path Following**

Path-following focuses on continuously tracking a pre-defined or dynamically generated trajectory, instead of discrete waypoints.

### Metrics:
- **Cross-Track Error (\( e_{\text{CT}} \)):**
  \[
  e_{\text{CT}} = \text{minimum distance from vehicle to path}
  \]
- **Along-Track Progress:**
  Measures the distance of the vehicle along the given path.
- **Heading Error (\( e_\psi \)):**
  Quantifies the difference between the vehicle's heading and the desired path's tangent angle.

---

## **7. Pure Pursuit**

Pure Pursuit is a simple and efficient path-following algorithm that uses a **lookahead point** located on the desired path to guide the vehicle.

### Curvature Calculation:
\[
\kappa = \frac{2 \sin(\alpha)}{L_d}
\]
Where:
- \( \kappa \): Curvature of the turning path (inverse of the turning radius).
- \( \alpha \): Angle between the vehicle's current heading and the lookahead point.
- \( L_d \): Lookahead distance to the target point.

### Trade-offs:
- **Small Lookahead:**
  - Provides greater accuracy but may lead to oscillations.
- **Large Lookahead:**
  - Results in smoother tracking but at the cost of less accuracy and increased path deviation.

---

## **8. Proportional Navigation**

Proportional Navigation (PN) guides a pursuer to intercept a target by turning proportionally to the rate of change of the **line-of-sight (LOS)** to the target.

### Equation:
\[
\dot{\psi} = \frac{N \cdot V_c \cdot \dot{\lambda}}{V}
\]
Where:
- \( \dot{\psi} \): Rate of turn.
- \( N \): Proportional navigation constant (gain), typically between 3–5 for effective interception.
- \( V_c \): Closing velocity.
- \( \dot{\lambda} \): LOS rate (rate of change in LOS angle).
- \( V \): Speed of the pursuer.

### Applications:
- Missile guidance systems.
- Collision-avoidance systems in autonomous vehicles and UAVs.

---

## **9. Dubins Paths**

Dubins paths are the shortest trajectories for a vehicle with a **minimum turning radius** constraint to travel between two poses (position + heading).

### Path Components:
Dubins paths consist of three segments:
1. **Left Turn (L)**: Arc in the counterclockwise direction.
2. **Right Turn (R)**: Arc in the clockwise direction.
3. **Straight Line (S)**: Linear segment connecting arcs.

---

## **10. Smooth Trajectories**

Smooth trajectories ensure continuous position, velocity, and acceleration to improve performance and reduce mechanical loads.

### Key Variables for Trajectory Planning:
- **Position** (\( p \)): 2D or 3D coordinates of the vehicle.
- **Velocity** (\( v \)): Change in position over time.
- **Acceleration** (\( a \)): Change in velocity over time.
- **Jerk** (\( j \)): Change in acceleration over time (optional, for extreme smoothness).

### Advantages:
- Ensures smooth transitions (no sharp changes in velocity or acceleration).
- Reduces wear on actuators.
- Improves trajectory tracking for robotics and autonomous systems.

---

## **Applications**

The provided mathematical foundations and guidance techniques are applicable to many areas:
- **Robotics**: For autonomous robots needing accurate and smooth path-following control.
- **Aerial Navigation**: Algorithms like Dubins paths and smooth trajectories are essential for UAVs and fixed-wing aircraft.
- **Autonomous Driving**: Pure pursuit for lane following or path tracking.
- **Missile Systems**: PN for interception and collision avoidance.

Let me know if you need to dive deeper into specific topics or additional concepts!
- **Dubins Paths**: Solutions for vehicles with turning constraints.
- **Monte Carlo Testing**: Simulates robust performance under varying conditions.
