```text
NOTE: crtl+shift+V to preview markdown file
NOTE: ctrl+K V to view and preview markdown
```

# Week 3 – Dynamics & Simulation

## Theme

**Learning How Physical Systems Move**

### Primary Goal

Build a foundational understanding of dynamic systems and simulation.

By the end of this week, you should understand how engineers model moving systems, propagate states through time, and simulate vehicle behavior using numerical methods.

This is the first major step toward:

- Controls
- GNC
- Robotics
- Autonomous Systems
- Aerospace Vehicle Design

---

# Learning Objectives

Understand:

- States
- Inputs
- Outputs
- Dynamic systems
- Numerical integration
- Coordinate frames
- Motion models

---

# Technical Accomplishments

## 1. Dynamic System Fundamentals

### Topics

- State
- Input
- Output
- System Dynamics

### Example

Vehicle State:

```text
Position
Velocity
Heading
```

Control Inputs:

```text
Throttle
Steering
```

Outputs:

```text
Position
Velocity
```

### Success Criteria

Able to explain:

```text
Current State
      +
Future Input
      =
Future State
```

---

## 2. Learn State-Space Thinking

### Topics

- State vectors
- State propagation
- Continuous systems
- Discrete systems

### Example State Vector

```text
x = [
    position_x
    position_y
    velocity
    heading
]
```

### Success Criteria

Able to define states for:

- Aircraft
- Ground vehicle
- Drone

---

## 3. Numerical Integration

### Topics

- Time stepping
- Euler integration
- RK4 overview

### Euler Method



### Success Criteria

Understand:

- Why simulations require time steps
- Integration error
- Stability considerations

---

## 4. Coordinate Frames

### Topics

- Global frame
- Local frame
- Body frame

### Example

```text
North-East

Vehicle Body Frame

Heading Angle
```

### Success Criteria

Able to explain:

```text
Vehicle Frame
      ↔
World Frame
```

and why coordinate transforms are necessary.

---

## 5. Motion Models

### Topics

- Constant velocity
- Constant acceleration
- Simple turn-rate models

### Success Criteria

Understand:

- Position update
- Velocity update
- Heading update

---

# Engineering Project

## Project – 2D Vehicle Simulator

### Objective

Simulate a vehicle moving through a 2D environment.

---

## Vehicle State

```python
x
y
velocity
heading
```

---

## Inputs

```python
throttle
turn_rate
```

---

## Outputs

```python
trajectory
velocity
heading
```

---

## Simulation Loop

```text
Initialize State

Loop:
    Apply Input
    Update State
    Store History
    Plot Results
```

---

## Example Simulation

Vehicle starts:

```text
x = 0
y = 0
velocity = 10 m/s
heading = 0 deg
```

Vehicle turns:

```text
5 deg/sec
```

Simulate:

```text
60 seconds
```

Plot resulting trajectory.

---

# Data Visualization

## Install

```bash
pip install matplotlib
```

---

## Generate Plots

### Position

```text
X vs Y
```

### Velocity

```text
Velocity vs Time
```

### Heading

```text
Heading vs Time
```

### Success Criteria

Produce engineering-quality plots.

---

# Architecture Thinking

## Simulation Architecture Diagram

```text
Vehicle State
      ↓
Dynamics Model
      ↓
Integrator
      ↓
Updated State
      ↓
Data Logger
      ↓
Visualization
```

### Success Criteria

Understand major simulation components.

---

# Monte Carlo Integration

## Introduce Randomized Inputs

Examples:

```text
Different Starting Positions

Different Speeds

Different Turn Rates
```

Run:

```text
100 Simulations
```

Observe:

```text
Trajectory Variation
```

### Success Criteria

Understand why Monte Carlo is useful.

---

# Documentation Accomplishments

## Create Notes

### File

```text
notes/dynamics-fundamentals.md
```

Include:

- State-space concepts
- Dynamic systems
- Euler integration
- Coordinate frames

---

## Create Simulation Notes

### File

```text
notes/simulation-methods.md
```

Include:

- Time stepping
- Numerical integration
- Sources of simulation error

---

# Git Accomplishments

Continue:

```bash
git status
git add
git commit
git push
```

### Example Commits

```text
Created vehicle state model

Implemented Euler integration

Added trajectory plotting

Created Monte Carlo runs

Completed dynamics notes
```

---

# Aerospace Relevance

This week forms the foundation for:

- Flight Dynamics
- Guidance Systems
- Navigation Systems
- Control Systems
- Vehicle Simulation
- Digital Twins
- Mission Analysis

Nearly every autonomy system begins with a simulation model.

---

# AI Integration Opportunities

Potential future applications:

```text
Trajectory Prediction

System Identification

Surrogate Models

Reinforcement Learning Environments
```

No AI implementation required this week.

Focus on understanding physics and simulation.

---

# Engineering Artifact

Produce:

## Software

```text
2D Vehicle Simulator
```

---

## Documentation

```text
Dynamics Notes

Simulation Notes
```

---

## Plots

```text
Trajectory Plot

Velocity Plot

Heading Plot
```

---

## Architecture Diagram

```text
Simulation Architecture
```

---

# Week 3 Definition of Success

You can confidently explain:

- What a state is
- What a dynamic system is
- How simulation works
- What Euler integration does
- Why coordinate transforms matter
- How vehicle motion is modeled

And demonstrate:

```text
Vehicle State
      ↓
Dynamics Model
      ↓
Simulation
      ↓
Plots
```

running on your machine.

---

# Stretch Goals (Excellent Outcome)

## Add Wind Disturbances

```text
Crosswind

Headwind

Random Gusts
```

Observe trajectory deviations.

---

## Compare Integrators

Implement:

```text
Euler

RK4
```

Compare accuracy.

---

## Multiple Vehicle Types

Simulate:

```text
Ground Vehicle

Aircraft

Simple Drone
```

using the same framework.

---

# Why Week 3 Matters

Simulation is where engineering, software, and mathematics begin to merge.

Before designing:

- Controllers
- Kalman Filters
- Guidance Laws
- Autonomy Systems

you must first understand how the vehicle behaves.

A good simulation environment becomes the foundation for nearly every future unit in the roadmap.
