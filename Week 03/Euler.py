import matplotlib.pyplot as plt

dt = 0.05
time = 0

height = 100.0
velocity = 0.0
mass = 1.0

gravity = -9.81
thrust = 15.0
fuel_time = 5.0

times = []
heights = []
velocities = []
accelerations = []

while height > 0:
    if time < fuel_time:
        acceleration = gravity + thrust / mass
    else:
        acceleration = gravity

    velocity = velocity + acceleration * dt
    height = height + velocity * dt

    times.append(time)
    heights.append(height)
    velocities.append(velocity)
    accelerations.append(acceleration)

    time += dt

landing_speed = abs(velocity)

if landing_speed < 5:
    print(f"Safe landing! Speed: {landing_speed:.2f} m/s")
else:
    print(f"Crash landing. Speed: {landing_speed:.2f} m/s")

print(f"Simulation points generated: {len(times)}")

fig, ax = plt.subplots(3, 1, figsize=(8, 12))

ax[0].plot(times, heights)
ax[0].set_title("Rocket Height Over Time")
ax[0].set_ylabel("Height (m)")
ax[0].grid(True)

ax[1].plot(times, velocities)
ax[1].set_title("Rocket Velocity Over Time")
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Velocity (m/s)")
ax[1].grid(True)

# Acceleration
ax[2].plot(times, accelerations)
ax[2].set_title("Rocket Acceleration")
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Acceleration (m/s²)")
ax[2].grid(True)

plt.tight_layout()

# Save the plot so you know it was created
plt.savefig("rocket_plot.png", dpi=150)
print("Saved plot as rocket_plot.png")

plt.show()