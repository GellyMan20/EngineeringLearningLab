import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------
# Simulation Settings
# ---------------------------------

dt = 1.0          # seconds
t_end = 6000      # total simulation time

# Earth's gravitational parameter
mu = 398600.0     # km^3/s^2

# ---------------------------------
# Initial Conditions
# ---------------------------------

# Position (km)
x = 7000.0
y = 0.0

# Velocity (km/s)
vx = 0.0
vy = 7.5

# ---------------------------------
# Data Storage
# ---------------------------------

xs = []
ys = []
vxs = []
vys = []
times = []

time = 0

# ---------------------------------
# Simulation Loop
# ---------------------------------

while time < t_end:

    # Distance from Earth
    r = np.sqrt(x**2 + y**2)

    # Gravitational acceleration
    ax = -mu * x / r**3
    ay = -mu * y / r**3

    # Euler Integration
    vx = vx + ax * dt
    vy = vy + ay * dt

    x = x + vx * dt
    y = y + vy * dt

    # Store data
    xs.append(x)
    ys.append(y)
    vxs.append(vx)
    vys.append(vy)
    times.append(time)

    time += dt

# ---------------------------------
# Plot Orbit
# ---------------------------------

plt.figure(figsize=(8,8))

# Earth
earth = plt.Circle((0,0), 6371, fill=False, linewidth=2)
plt.gca().add_artist(earth)

# Satellite trajectory
plt.plot(xs, ys)

plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("Satellite Orbit")
plt.axis("equal")
plt.grid(True)

plt.show()