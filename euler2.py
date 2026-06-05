import numpy as np
import matplotlib.pyplot as plt


def body_to_world(vector_body, heading_rad):
    rotation_matrix = np.array([
        [np.cos(heading_rad), -np.sin(heading_rad)],
        [np.sin(heading_rad),  np.cos(heading_rad)]
    ])
    return rotation_matrix @ vector_body


def simulate_vehicle(total_time=20.0, dt=0.1):
    x = 0.0
    y = 0.0
    heading = np.deg2rad(20.0)

    speed_body = 5.0
    yaw_rate = np.deg2rad(12.0)

    time_history = []
    x_history = []
    y_history = []
    heading_history = []
    velocity_world_history = []

    time = 0.0

    while time <= total_time:
        velocity_body = np.array([speed_body, 0.0])
        velocity_world = body_to_world(velocity_body, heading)

        x += velocity_world[0] * dt
        y += velocity_world[1] * dt
        heading += yaw_rate * dt

        time_history.append(time)
        x_history.append(x)
        y_history.append(y)
        heading_history.append(heading)
        velocity_world_history.append(velocity_world)

        time += dt

    return (
        np.array(time_history),
        np.array(x_history),
        np.array(y_history),
        np.array(heading_history),
        np.array(velocity_world_history)
    )


def plot_results(time, x, y, heading, velocity_world):
    # Plot 1
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, linewidth=2, label="Trajectory")

    step = max(1, len(time) // 12)
    for i in range(0, len(time), step):
        forward_world = body_to_world(np.array([2.5, 0]), heading[i])
        plt.arrow(
            x[i], y[i],
            forward_world[0], forward_world[1],
            head_width=0.4,
            length_includes_head=True
        )

    plt.scatter(x[0], y[0], s=80, label="Start")
    plt.scatter(x[-1], y[-1], s=80, label="End")
    plt.title("Euler Integration + Body-to-World Coordinate Transformation")
    plt.xlabel("World X Position [m]")
    plt.ylabel("World Y Position [m]")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.savefig("trajectory_plot.png", dpi=200, bbox_inches="tight")

    # Plot 2
    plt.figure(figsize=(10, 5))
    plt.plot(time, velocity_world[:, 0], linewidth=2, label="Vx")
    plt.plot(time, velocity_world[:, 1], linewidth=2, label="Vy")
    plt.title("World Frame Velocity Components")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
    plt.savefig("velocity_components_plot.png", dpi=200, bbox_inches="tight")

    # Plot 3
    plt.figure(figsize=(10, 5))
    plt.plot(time, np.rad2deg(heading), linewidth=2, label="Heading")
    plt.title("Vehicle Heading vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("Heading [deg]")
    plt.grid(True)
    plt.legend()
    plt.savefig("heading_plot.png", dpi=200, bbox_inches="tight")

    print("Saved plots:")
    print("trajectory_plot.png")
    print("velocity_components_plot.png")
    print("heading_plot.png")

    plt.show(block=True)


if __name__ == "__main__":
    time, x, y, heading, velocity_world = simulate_vehicle()
    plot_results(time, x, y, heading, velocity_world)