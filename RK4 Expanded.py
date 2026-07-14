import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# WEEK 4: RK4 AND ORBITAL MECHANICS
#
# Goal:
# Learn why RK4 is better than Euler for orbital simulation.
#
# This script demonstrates:
# - Earth drawn as a circle
# - Circular orbit
# - Elliptical orbit
# - Escape velocity test
# - Euler vs RK4 comparison
# - Small thruster burn to raise orbit
# - Energy error plot
# ============================================================

# ============================================================
# PHYSICAL CONSTANTS
# ============================================================

MU = 398600.0      # Earth's gravitational parameter, km^3/s^2
R_EARTH = 6371.0   # Earth's radius, km

# ============================================================
# SIMULATION SETTINGS
# ============================================================

dt = 10.0          # timestep, seconds
t_end = 20000.0    # total simulation time, seconds


# ============================================================
# DYNAMICS FUNCTION
#
# State vector:
# state = [x, y, vx, vy]
#
# x, y   = position in km
# vx, vy = velocity in km/s
#
# This function returns:
# [dx/dt, dy/dt, dvx/dt, dvy/dt]
# ============================================================

def dynamics(state):
    x, y, vx, vy = state

    # Distance from Earth's center
    r = np.sqrt(x**2 + y**2)

    # Gravitational acceleration
    # Gravity points back toward Earth, hence the negative sign.
    ax = -MU * x / r**3
    ay = -MU * y / r**3

    return np.array([vx, vy, ax, ay])


# ============================================================
# EULER INTEGRATION
#
# Simple but inaccurate for orbits.
#
# new_state = old_state + derivative * dt
# ============================================================

def euler_step(state, dt):
    return state + dynamics(state) * dt


# ============================================================
# RK4 INTEGRATION
#
# RK4 samples the derivative four times:
# k1 = slope at beginning
# k2 = slope at midpoint estimate
# k3 = improved midpoint slope
# k4 = slope at end estimate
#
# Then it takes a weighted average.
# This is much more accurate than Euler.
# ============================================================

def rk4_step(state, dt):
    k1 = dynamics(state)
    k2 = dynamics(state + 0.5 * dt * k1)
    k3 = dynamics(state + 0.5 * dt * k2)
    k4 = dynamics(state + dt * k3)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


# ============================================================
# ORBITAL ENERGY
#
# Specific mechanical energy:
#
# energy = kinetic energy + potential energy
# energy = 0.5*v^2 - MU/r
#
# In a perfect orbit simulation, energy should stay constant.
# If energy drifts, the numerical method is adding/removing energy.
# ============================================================

def energy(state):
    x, y, vx, vy = state

    r = np.sqrt(x**2 + y**2)
    v = np.sqrt(vx**2 + vy**2)

    return 0.5 * v**2 - MU / r


# ============================================================
# SIMULATION FUNCTION
#
# This function runs one orbit case.
#
# Optional thruster burn:
# - burn_time = when burn happens
# - delta_v = velocity change in km/s
#
# A positive delta_v in the direction of travel raises the orbit.
# ============================================================

def simulate(initial_state, method="rk4", burn_time=None, delta_v=0.0):
    state = initial_state.copy()

    xs = []
    ys = []
    rs = []
    speeds = []
    energies = []
    times = []

    burn_done = False
    time = 0.0

    while time <= t_end:
        x, y, vx, vy = state

        r = np.sqrt(x**2 + y**2)
        v = np.sqrt(vx**2 + vy**2)

        # Store current data
        xs.append(x)
        ys.append(y)
        rs.append(r)
        speeds.append(v)
        energies.append(energy(state))
        times.append(time)

        # Apply one-time thruster burn
        if burn_time is not None and time >= burn_time and not burn_done:
            velocity_direction = np.array([vx, vy]) / v

            state[2] += delta_v * velocity_direction[0]
            state[3] += delta_v * velocity_direction[1]

            burn_done = True

        # Advance state using selected integration method
        if method == "euler":
            state = euler_step(state, dt)
        elif method == "rk4":
            state = rk4_step(state, dt)
        else:
            raise ValueError("method must be 'euler' or 'rk4'")

        time += dt

    return {
        "times": np.array(times),
        "xs": np.array(xs),
        "ys": np.array(ys),
        "rs": np.array(rs),
        "speeds": np.array(speeds),
        "energies": np.array(energies)
    }


# ============================================================
# INITIAL CONDITIONS
# ============================================================

# Starting radius from Earth's center
r0 = 7000.0  # km

# Circular orbit speed:
# v = sqrt(MU / r)
v_circular = np.sqrt(MU / r0)

# Escape velocity:
# v_escape = sqrt(2*MU / r)
v_escape = np.sqrt(2 * MU / r0)

# Circular orbit state
circular_state = np.array([
    r0,          # x position, km
    0.0,         # y position, km
    0.0,         # x velocity, km/s
    v_circular   # y velocity, km/s
])

# Elliptical orbit:
# Slightly slower than circular orbit speed.
elliptical_state = np.array([
    r0,
    0.0,
    0.0,
    6.8
])

# Escape trajectory:
# Slightly above escape velocity.
escape_state = np.array([
    r0,
    0.0,
    0.0,
    v_escape * 1.01
])


# ============================================================
# RUN SIMULATION CASES
# ============================================================

circular_euler = simulate(circular_state, method="euler")
circular_rk4 = simulate(circular_state, method="rk4")

elliptical_rk4 = simulate(elliptical_state, method="rk4")
escape_rk4 = simulate(escape_state, method="rk4")

# Thruster burn:
# Add 0.2 km/s in direction of travel after 4000 seconds.
burn_rk4 = simulate(
    circular_state,
    method="rk4",
    burn_time=4000.0,
    delta_v=0.2
)


# ============================================================
# PRINT SUMMARY
# ============================================================

print("Circular orbit speed:", round(v_circular, 3), "km/s")
print("Escape velocity:", round(v_escape, 3), "km/s")
print("Euler final radius:", round(circular_euler["rs"][-1], 2), "km")
print("RK4 final radius:", round(circular_rk4["rs"][-1], 2), "km")


# ============================================================
# PLOT 1: ORBIT CASES
# ============================================================

plt.figure(figsize=(9, 9))

earth = plt.Circle((0, 0), R_EARTH, fill=False, linewidth=2)
plt.gca().add_artist(earth)

plt.plot(circular_rk4["xs"], circular_rk4["ys"], label="Circular Orbit - RK4")
plt.plot(elliptical_rk4["xs"], elliptical_rk4["ys"], label="Elliptical Orbit - RK4")
plt.plot(escape_rk4["xs"], escape_rk4["ys"], label="Escape Trajectory - RK4")
plt.plot(burn_rk4["xs"], burn_rk4["ys"], label="Thruster Burn Orbit - RK4")

plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("Orbit Cases")
plt.axis("equal")
plt.grid(True)
plt.legend()


# ============================================================
# PLOT 2: EULER VS RK4
# ============================================================

plt.figure(figsize=(9, 9))

earth = plt.Circle((0, 0), R_EARTH, fill=False, linewidth=2)
plt.gca().add_artist(earth)

plt.plot(circular_euler["xs"], circular_euler["ys"], label="Euler")
plt.plot(circular_rk4["xs"], circular_rk4["ys"], label="RK4")

plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("Euler vs RK4 Orbit Comparison")
plt.axis("equal")
plt.grid(True)
plt.legend()


# ============================================================
# PLOT 3: RADIUS OVER TIME
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(circular_euler["times"], circular_euler["rs"], label="Euler Radius")
plt.plot(circular_rk4["times"], circular_rk4["rs"], label="RK4 Radius")

plt.xlabel("Time (s)")
plt.ylabel("Distance from Earth Center (km)")
plt.title("Radius Over Time: Euler vs RK4")
plt.grid(True)
plt.legend()


# ============================================================
# PLOT 4: ENERGY ERROR
# ============================================================

euler_energy_error = circular_euler["energies"] - circular_euler["energies"][0]
rk4_energy_error = circular_rk4["energies"] - circular_rk4["energies"][0]

plt.figure(figsize=(10, 5))

plt.plot(circular_euler["times"], euler_energy_error, label="Euler Energy Error")
plt.plot(circular_rk4["times"], rk4_energy_error, label="RK4 Energy Error")

plt.xlabel("Time (s)")
plt.ylabel("Energy Error (km²/s²)")
plt.title("Numerical Energy Error")
plt.grid(True)
plt.legend()


# ============================================================
# SHOW ALL PLOTS
# ============================================================

plt.show()