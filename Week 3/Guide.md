# Runge-Kutta 4 (RK4) --- An Intuitive Guide

## Why Do We Need RK4?

Many engineering systems are governed by differential equations.

Examples:

-   Aircraft motion
-   Spacecraft orbits
-   Robot movement
-   Missile trajectories
-   Electrical circuits

Usually we know **how a system is changing**, not exactly where it will
be later.

For example:

-   Velocity changes because of acceleration.
-   Position changes because of velocity.

A computer must approximate the future state.

------------------------------------------------------------------------

# Euler Integration

Euler asks a very simple question:

> If I know the current slope, what happens if I follow that slope for a
> short time?

Mathematically:

    x_new = x_old + slope * dt

For a rocket:

    velocity = velocity + acceleration * dt
    position = position + velocity * dt

Graphically:

Current State \| v Compute Slope \| v Take One Step \| +-----\> Repeat

## Strengths

-   Very simple
-   Easy to code
-   Fast

## Weaknesses

-   Error accumulates
-   Can become unstable
-   Long simulations drift

A satellite orbit simulated with Euler often spirals inward or outward.

------------------------------------------------------------------------

# The Main Idea Behind RK4

Euler assumes the slope never changes during the timestep.

RK4 says:

> The slope probably changes while I move. Let's estimate that change.

Instead of asking once,

"What is the slope right now?"

RK4 asks four questions.

------------------------------------------------------------------------

# The Four Slopes

Suppose you are hiking.

Euler:

"I know the hill's slope where I stand. I'll walk forward."

RK4:

1.  What is the slope here?
2.  What might the slope be halfway through?
3.  If that halfway estimate is better, what is the slope there?
4.  What will the slope be at the end?

Then combine all four estimates.

This dramatically improves accuracy.

------------------------------------------------------------------------

# The RK4 Algorithm

k1 = slope at the beginning

k2 = slope halfway using k1

k3 = improved halfway slope

k4 = slope at the end

Weighted average:

    (k1 + 2*k2 + 2*k3 + k4) / 6

Notice the middle estimates get extra weight.

------------------------------------------------------------------------

# Visual Thought Process

Euler:

Start \| v Measure Slope \| v Take Step

RK4:

Start \| v Measure Beginning Slope \| v Estimate Midpoint \| v Measure
Midpoint Slope \| v Estimate Better Midpoint \| v Measure Better
Midpoint \| v Estimate End \| v Measure End Slope \| v Average
Everything \| v Take Step

------------------------------------------------------------------------

# Why RK4 Works Better

Suppose a satellite is turning around Earth.

The direction of gravity changes continuously.

Euler only sees gravity at the start.

RK4 samples gravity throughout the step.

The result:

-   Better trajectory
-   Better energy conservation
-   Better long-term stability

------------------------------------------------------------------------

# Euler vs RK4

  Property           Euler          RK4
  ------------------ -------------- ----------------
  Difficulty         Easy           Moderate
  Slopes per step    1              4
  Accuracy           Low            High
  Long simulations   Poor           Very good
  Orbit simulation   Often drifts   Usually stable
  Learning value     Excellent      Excellent

------------------------------------------------------------------------

# Orbital Mechanics Example

State vector:

    [x, y, vx, vy]

Simulation loop:

1.  Calculate gravity.
2.  Calculate acceleration.
3.  Integrate velocity.
4.  Integrate position.
5.  Repeat.

Euler:

Uses one slope.

RK4:

Uses four slope estimates.

------------------------------------------------------------------------

# Mental Model

Imagine driving.

Euler:

"I know my speed right now. I'll assume it never changes."

RK4:

"I know my speed now. I estimate my speed halfway. I estimate it again.
I estimate it at the end. Now I make a smarter prediction."

------------------------------------------------------------------------

# Why Aerospace Engineers Care

RK4 appears everywhere:

-   Flight simulation
-   Spacecraft propagation
-   Missile modeling
-   Robotics
-   Guidance and Navigation
-   Monte Carlo analysis
-   Autonomous systems

------------------------------------------------------------------------

# What You Should Remember

If you forget everything else, remember:

Euler:

    One slope.

RK4:

    Four carefully chosen slopes.

Euler:

    "Move using what I know now."

RK4:

    "Estimate what happens during the movement."

That simple change is why RK4 can simulate complex systems far more
accurately.

------------------------------------------------------------------------

# Suggested Learning Progression

1.  Euler integration
2.  Rocket simulator
3.  Orbit simulator with Euler
4.  Observe numerical drift
5.  Replace Euler with RK4
6.  Compare energy conservation
7.  Add thruster burns
8.  Build 6-DOF aircraft models
9.  Learn Kalman filters
10. Learn guidance and control

The transition from Euler to RK4 is one of the most important conceptual
steps in numerical simulation and aerospace engineering.
