import numpy as np
import matplotlib.pyplot as plt

def body_to_world(vector_body, heading_rad):
    """
    Convert a vector from the vehicle's body frame into the world frame.

    Body frame:
        +X body = vehicle forward direction
        +Y body = vehicle right-side direction

    World frame:
        +X world = right/east on the plot
        +Y world = up/north on the plot
    """

    rotation_matrix = np.array([
        [np.cos(heading_rad), -np.sin(heading_rad)],
        [np.sin(heading_rad),  np.cos(heading_rad)]
    ])

    return rotation_matrix @ vector_body


def simulate_vehicle(total_time=20.0, dt=0.1):
    """
    Simulate a simple 2D vehicle using Euler integration.

    State:
        x position
        y position
        heading angle

    Inputs:
        forward speed in body frame
        yaw rate / turn rate
    """

    # Initial vehicle state
    x = 0.0
    y = 0.0
    heading = np.deg2rad(20.0)

    # Vehicle inputs
    speed_body = 5.0
    yaw_rate = np.deg2rad(12.0)

    # History arrays for plotting
    time_history = []
    x_history = []
    y_history = []
    heading_history = []
    velocity_world_history = []

    time = 0.0

    while time <= total_time:

        # ==================================================
        # BODY-FRAME VELOCITY
        #
        # In the vehicle's own frame, it is moving forward.
        #
        # [5, 0] means:
        #     5 m/s forward
        #     0 m/s sideways
        # ==================================================

        velocity_body = np.array([
            speed_body,
            0.0
        ])

        # ==================================================
        # COORDINATE TRANSFORMATION
        #
        # Convert velocity from body frame into world frame.
        #
        # This tells us how much of the vehicle's velocity
        # points in the world X direction and world Y direction.
        # ==================================================

        velocity_world = body_to_world(
            velocity_body,
            heading
        )

        # ==================================================
        # EULER INTEGRATION
        #
        # Position derivatives:
        #
        # dx/dt = Vx
        # dy/dt = Vy
        #
        # Euler method:
        #
        # x_new = x_old + Vx * dt
        # y_new = y_old + Vy * dt
        #
        # heading_new = heading_old + yaw_rate * dt
        # ==================================================

        x = x + velocity_world[0] * dt
        y = y + velocity_world[1] * dt
        heading = heading + yaw_rate * dt

        # Save data for plotting later
        time_history.append(time)
        x_history.append(x)
        y_history.append(y)
        heading_history.append(heading)
        velocity_world_history.append(velocity_world)

        time = time + dt

    return (
        np.array(time_history),
        np.array(x_history),
        np.array(y_history),
        np.array(heading_history),
        np.array(velocity_world_history)
    )


def plot_results(time, x, y, heading, velocity_world):
    """
    Create three plots:

    1. Vehicle trajectory with body-frame arrows
    2. World-frame velocity components
    3. Vehicle heading over time
    """

    # ==================================================
    # PLOT 1: TRAJECTORY WITH BODY AXES
    # ==================================================

    plt.figure(figsize=(10, 8))

    plt.plot(
        x,
        y,
        linewidth=2,
        label="Vehicle trajectory"
    )

    step = max(1, len(time) // 12)

    for i in range(0, len(time), step):

        axis_length = 4.0

        # Body-frame axes
        forward_body = np.array([axis_length, 0.0])
        right_body = np.array([0.0, axis_length])

        # Transform body axes into world frame
        forward_world = body_to_world(forward_body, heading[i])
        right_world = body_to_world(right_body, heading[i])

        # Draw forward body axis
        plt.arrow(
            x[i],
            y[i],
            forward_world[0],
            forward_world[1],
            head_width=0.6,
            length_includes_head=True
        )

        # Draw right body axis
        plt.arrow(
            x[i],
            y[i],
            right_world[0],
            right_world[1],
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

    plt.savefig(
        "trajectory_plot.png",
        dpi=200,
        bbox_inches="tight"
    )

    # ==================================================
    # PLOT 2: WORLD-FRAME VELOCITY COMPONENTS
    # ==================================================

    plt.figure(figsize=(10, 5))

    plt.plot(
        time,
        velocity_world[:, 0],
        linewidth=2,
        label="World Vx"
    )

    plt.plot(
        time,
        velocity_world[:, 1],
        linewidth=2,
        label="World Vy"
    )

    plt.title("World-Frame Velocity Components")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        "velocity_components_plot.png",
        dpi=200,
        bbox_inches="tight"
    )

    # ==================================================
    # PLOT 3: HEADING VS TIME
    # ==================================================

    plt.figure(figsize=(10, 5))

    plt.plot(
        time,
        np.rad2deg(heading),
        linewidth=2,
        label="Heading"
    )

    plt.title("Vehicle Heading vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("Heading [deg]")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        "heading_plot.png",
        dpi=200,
        bbox_inches="tight"
    )

    print("Saved plots:")
    print(" - trajectory_plot.png")
    print(" - velocity_components_plot.png")
    print(" - heading_plot.png")

    plt.show(block=True)


if __name__ == "__main__":
    time, x, y, heading, velocity_world = simulate_vehicle()

    plot_results(
        time,
        x,
        y,
        heading,
        velocity_world
    )