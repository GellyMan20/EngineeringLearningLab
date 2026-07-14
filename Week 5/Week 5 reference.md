# Week 5 Reference Sheet --- Classical Controls

> **Purpose:** This document is a quick-reference guide for the
> mathematical foundations, intuition, and engineering applications of
> classical feedback control. It is intended to accompany the Week 5
> projects, especially the PID Waypoint Vehicle.

------------------------------------------------------------------------

# 1. Why Feedback Exists

Most engineering systems experience disturbances:

-   Wind pushes a drone.
-   Hills slow a car.
-   Waves move a boat.
-   Sensor noise corrupts measurements.

Open-loop control cannot compensate for these effects because it never
measures the result.

Closed-loop control continuously compares the desired output to the
measured output and corrects the error.

## Feedback Loop

Desired State → Controller → Plant → Sensors → Measured State

The controller repeatedly asks:

> "How far am I from where I want to be?"

------------------------------------------------------------------------

# 2. Error

The most important equation in classical controls:

\[ e(t)=r(t)-y(t) \]

where:

-   **r(t)** = desired value (reference)
-   **y(t)** = measured value
-   **e(t)** = error

The controller attempts to drive

\[ e(t)`\rightarrow0`{=tex} \]

### Engineering Examples

  Desired          Measured   Error
  ---------------- ---------- --------
  100 m altitude   95 m       +5 m
  60 mph           55 mph     +5 mph
  90° heading      100°       -10°

------------------------------------------------------------------------

# 3. Dynamic Systems

Control systems work because systems have dynamics.

General state equation

\[ `\dot{x}`{=tex}=f(x,u) \]

where

-   x = system state
-   u = control input

Examples:

-   throttle
-   steering angle
-   motor torque
-   elevator deflection

------------------------------------------------------------------------

# 4. First-Order Systems

Transfer function

\[ G(s)=`\frac{1}{\tau s+1}`{=tex} \]

**τ (time constant)** determines how quickly the system responds.

Approximate behavior:

-   1τ → 63%
-   2τ → 86%
-   3τ → 95%
-   4τ → 98%
-   5τ → \~99%

Examples:

-   Heating systems
-   Battery charging
-   Cruise control approximation

------------------------------------------------------------------------

# 5. Second-Order Systems

Many aerospace systems are naturally second order.

\[ G(s)= `\frac{\omega_n^2}`{=tex} {s\^2+2`\zeta`{=tex}`\omega`{=tex}\_n
s+`\omega`{=tex}\_n\^2} \]

Important parameters:

**Natural Frequency (ωₙ)**

-   How quickly the system wants to move.

Higher ωₙ → Faster response.

**Damping Ratio (ζ)**

Controls oscillation.

  ζ     Behavior
  ----- ----------------------------------
  0     Never settles
  0.2   Very oscillatory
  0.5   Moderate overshoot
  0.7   Excellent engineering compromise
  1.0   Critical damping
  \>1   Overdamped (slow)

------------------------------------------------------------------------

# 6. Step Response Metrics

The step response is the most common way to evaluate a controller.

Important measurements:

-   Rise Time
-   Peak Time
-   Overshoot
-   Settling Time
-   Steady-State Error

A well-designed controller generally aims for:

-   Fast rise time
-   Low overshoot
-   Short settling time
-   Near-zero steady-state error

------------------------------------------------------------------------

# 7. PID Control

The most widely used controller:

\[ u=K_pe+K_i`\int `{=tex}e,dt+K_d`\frac{de}{dt}`{=tex} \]

### Proportional (P)

Responds to the current error.

Increase **Kp**:

-   Faster response
-   Larger overshoot
-   Potential oscillation

### Integral (I)

Responds to accumulated error.

Increase **Ki**:

-   Removes steady-state error
-   Can create oscillations and integral windup

### Derivative (D)

Responds to how quickly the error changes.

Increase **Kd**:

-   Adds damping
-   Reduces overshoot
-   Improves stability
-   Sensitive to noisy sensors

------------------------------------------------------------------------

# 8. Stability

A stable controller always brings the system back toward equilibrium
after a disturbance.

Signs of instability:

-   Oscillations grow
-   Output diverges
-   Never settles

Good tuning balances speed with robustness.

------------------------------------------------------------------------

# 9. Frequency Response

Instead of asking how the system responds to a step, ask:

> "How does it respond to sine waves of different frequencies?"

This leads to Bode plots.

## Magnitude Plot

Shows how much signals are amplified or attenuated.

## Phase Plot

Shows the delay introduced by the system.

Important concepts:

-   Gain Margin
-   Phase Margin
-   Bandwidth

Higher margins generally indicate greater robustness.

------------------------------------------------------------------------

# 10. Practical Tuning Strategy

A simple workflow:

1.  Start with **Ki = 0**, **Kd = 0**.
2.  Increase **Kp** until the response becomes slightly oscillatory.
3.  Add **Kd** to damp oscillations.
4.  Add **Ki** only to eliminate steady-state error.
5.  Validate against disturbances.

------------------------------------------------------------------------

# 11. Where You Will Use This Week

## PID Waypoint Vehicle

Outer loop:

Waypoint → Desired Heading

Inner loop:

Desired Heading → Steering

Second controller:

Desired Speed → Throttle

------------------------------------------------------------------------

## Disturbance Campaign

Randomize:

-   Wind
-   Mass
-   Sensor noise
-   Delay

Measure:

-   Tracking error
-   Overshoot
-   Settling time
-   Success rate

------------------------------------------------------------------------

## Failure Pareto Analysis

Classify failures such as:

-   Overshoot
-   Oscillation
-   Integral windup
-   Saturation
-   Slow response

Use this to determine the dominant failure modes.

------------------------------------------------------------------------

# 12. Engineering Intuition

Increasing **Kp** makes the controller more aggressive.

Increasing **Ki** makes the controller more persistent.

Increasing **Kd** makes the controller more cautious.

The goal is not to maximize any single gain---it is to balance speed,
accuracy, robustness, and stability.

------------------------------------------------------------------------

# 13. Key Takeaways

-   Feedback compares the desired and measured states.
-   Error drives every control decision.
-   First-order systems are governed primarily by a time constant.
-   Second-order systems are governed by natural frequency and damping
    ratio.
-   PID controllers combine present, past, and predicted error.
-   Stability is the primary requirement of any controller.
-   Frequency-response tools (Bode plots) help quantify robustness.
-   Real engineering controllers must tolerate uncertainty,
    disturbances, and noisy sensors.
