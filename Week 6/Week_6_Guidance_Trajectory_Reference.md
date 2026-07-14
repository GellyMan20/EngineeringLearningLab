
# Week 6 Reference Sheet — Guidance & Trajectory Generation

> **Purpose:** This document is a quick-reference guide for the mathematical foundations, engineering intuition, and practical applications of guidance and trajectory generation. It complements the Week 6 Python projects and serves as a condensed reference while studying autonomous navigation.

## 1. Guidance vs Navigation vs Control (GNC)

| Discipline | Purpose | Example |
|---|---|---|
| Navigation | Estimate where the vehicle is | GPS, IMU, EKF |
| Guidance | Decide where the vehicle should go | Waypoints, path following |
| Control | Generate actuator commands | Steering, throttle, elevator |

Mission → Planner → Guidance → Controller → Vehicle

## 2. Coordinate Frames

Common frames:
- World/Inertial
- Body
- NED
- ENU

Position vector:
p = [x, y]^T

Heading:
ψ

## 3. Distance

d = sqrt((x2-x1)^2 + (y2-y1)^2)

Used for waypoint acceptance, obstacle clearance, and mission completion.

## 4. Desired Heading

ψd = atan2(yt - y, xt - x)

Heading error:

eψ = wrap(ψd − ψ)

Wrap angles into [-π, π].

## 5. Waypoint Navigation

1. Compute distance
2. Compute desired heading
3. Compute heading error
4. Turn vehicle
5. Repeat

## 6. Path Following

Track a continuous path instead of individual waypoints.

Metrics:
- Cross-track error
- Along-track progress
- Heading error

## 7. Pure Pursuit

Lookahead distance: Ld

Curvature:

κ = 2 sin(α) / Ld

Small lookahead:
- More accurate
- More oscillation

Large lookahead:
- Smoother
- Cuts corners

## 8. Proportional Navigation

Turn proportional to line-of-sight rate.

ψ̇ = N(Vc λ̇)/V

Used for interception and collision avoidance.

## 9. Dubins Paths

Respect a minimum turning radius.

Built from:
- Left turn
- Right turn
- Straight segment

Useful for fixed-wing aircraft and cars.

## 10. Smooth Trajectories

Trajectory consists of:
- Position
- Velocity
- Acceleration
- Sometimes jerk

Smooth commands improve tracking and reduce actuator stress.

## 11. Cross-Track Error

Distance between vehicle and desired path.

Common metrics:
- Mean
- RMS
- Maximum

## 12. Mission Planning

Optimize:
- Distance
- Fuel
- Time
- Safety
- Obstacle clearance

## 13. Obstacle Avoidance

Common planners:
- A*
- Dijkstra
- RRT*
- PRM

## 14. Performance Metrics

- Mission completion rate
- Time-to-goal
- Cross-track error
- Path length
- Smoothness
- Maximum curvature
- Control effort

## 15. Monte Carlo Testing

Randomize:
- Start location
- Goal
- Wind
- Noise
- Speed
- Turn limits

Measure robustness over hundreds of missions.

## 16. AI and Guidance

Classical guidance determines how to follow a path.

AI often determines which path should be followed.

Together they form the basis of modern autonomous systems.

## Key Takeaways

- Navigation estimates state.
- Guidance generates the path.
- Control executes the path.
- Pure Pursuit is a simple, robust path follower.
- Proportional Navigation solves interception.
- Dubins paths respect turning constraints.
- Cross-track error is a key performance metric.
- Monte Carlo testing measures robustness.
