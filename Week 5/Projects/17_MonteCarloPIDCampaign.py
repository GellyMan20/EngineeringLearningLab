"""
Project: Monte Carlo PID Campaign  
Purpose:
This script demonstrates a **Monte Carlo simulation** to evaluate the robustness of a PID (Proportional-Integral-Derivative) controller 
under varying external conditions, such as random variations in vehicle mass, drag coefficient, wind resistance, and hill forces. 
The experiment calculates the mean and maximum errors in speed tracking for 300 randomized trials to assess the controller’s 
performance and reliability.

Key Concepts:
- **Monte Carlo Simulation**: Used to test the system's behavior under a range of randomly generated conditions.
- **Robustness Testing**: Evaluates the performance of the PID controller when subjected to disturbances and variability.
- **PID Control**: Used to adjust throttle commands to maintain a desired speed in the presence of external disturbances.

Applications:
- **Automotive Industry**: Evaluates cruise control systems' performance and reliability in diverse driving conditions.
- **Robots and UAVs**: Analyze speed regulation under environmental disturbances for autonomous systems.
- **Engineering Education**: Illustrates the importance of robustness and system testing via Monte Carlo analysis.
"""

# Import necessary libraries
import numpy as np  # For random number generation and numerical computations
import matplotlib.pyplot as plt  # For visualizing error distributions

# Define the PID controller class
class PID:
    def __init__(self, kp, ki, kd, output_limits=(-1e9, 1e9)):
        """
        Initializes the PID controller.

        Parameters:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            output_limits (tuple): Limits for output values (e.g., throttle range; default: unlimited).
        """
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.output_limits = output_limits  # Maximum and minimum allowed control output
        self.integral = 0.0  # Accumulator for integral term
        self.prev_error = 0.0  # Previous error for derivative calculation

    def update(self, error, dt):
        """
        Updates the PID control output based on the current error.

        Parameters:
            error (float): The difference between the desired and actual speed.
            dt (float): Time step between updates.

        Returns:
            float: Control output (throttle), limited to `output_limits`.
        """
        # Update integral term
        self.integral += error * dt

        # Compute derivative term
        derivative = (error - self.prev_error) / dt

        # Update the previous error for the next control step
        self.prev_error = error

        # PID control law
        u = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Clamp the output to the defined limits
        return float(np.clip(u, self.output_limits[0], self.output_limits[1]))

# Function to simulate a single randomized trial
def run_trial(rng):
    """
    Simulates a single trial in the Monte Carlo campaign to evaluate the robustness of the PID controller.

    Parameters:
        rng (Generator): Random number generator for reproducible random conditions.

    Returns:
        tuple: Mean speed error and maximum speed error for the trial.
    """

    # Simulation parameters
    dt = 0.05  # Time step (seconds)
    t = np.arange(0, 60, dt)  # Simulation duration (60 seconds)

    # Generate random test conditions
    mass = rng.normal(1500, 150)  # Vehicle mass (mean: 1500 kg, std: 150 kg)
    drag = rng.normal(0.35, 0.05)  # Drag coefficient (mean: 0.35, std: 0.05)
    hill_force = rng.uniform(400, 1500)  # Hill resistance force (uniformly distributed)
    wind_force = rng.uniform(0, 800)  # Wind force (uniformly distributed)

    # PID controller setup
    pid = PID(0.08, 0.015, 0.01, output_limits=(0, 1))  # Tuned PID for speed tracking

    # Initial conditions
    target = 27.0  # Target speed (m/s)
    speed = 0.0  # Initial speed
    errors = []  # List to log speed errors during simulation

    # Simulation loop
    for time in t:
        # Determine external disturbances (hill force and wind force)
        disturbance = 0
        if 20 <= time <= 40:
            disturbance += hill_force  # Hill resistance active from 20s to 40s
        if time > 35:
            disturbance += wind_force  # Wind force active after 35s

        # Compute throttle using PID controller
        throttle = pid.update(target - speed, dt)  # Use speed error (target - speed)

        # Update speed considering throttle, drag, and disturbances
        speed += ((throttle * 4500 - drag * speed**2 - disturbance) / mass) * dt

        # Log absolute speed error
        errors.append(abs(target - speed))

    # Return mean and maximum speed error for this trial
    return np.mean(errors), np.max(errors)

# Main function to execute the Monte Carlo campaign
def main():
    """
    Executes a Monte Carlo PID simulation campaign with 300 trials.
    Visualizes the robustness of the PID controller by plotting error distributions 
    and scatter plots of mean vs. max errors.
    """

    # Initialize random number generator for consistent results
    rng = np.random.default_rng(5)

    # Perform 300 randomized trials
    results = np.array([run_trial(rng) for _ in range(300)])  # Run simulation for 300 trials

    # Evaluate success rate: Trials where mean speed error < 3 m/s
    success = np.mean(results[:, 0] < 3.0) * 100  # Percent success rate
    print(f"Success Rate: {success:.1f}%")

    # Visualization: Histogram of mean speed errors
    plt.figure()
    plt.hist(results[:, 0], bins=30, alpha=0.7, label="Mean Error")
    plt.title(f"Monte Carlo PID Campaign — Success Rate: {success:.1f}%")
    plt.xlabel("Mean Speed Error [m/s]")  # Label for histogram x-axis
    plt.ylabel("Trial Count")  # Label for histogram y-axis
    plt.grid(True)  # Add grid
    plt.legend()
    plt.show()

    # Visualization: Scatter plot of mean vs max errors
    plt.figure()
    plt.scatter(results[:, 0], results[:, 1], alpha=0.6, label="Results")
    plt.title("Mean Error vs. Max Error")
    plt.xlabel("Mean Error [m/s]")  # Label for x-axis
    plt.ylabel("Max Error [m/s]")  # Label for y-axis
    plt.grid(True)  # Add grid
    plt.show()

# Entry point: Run the simulation
if __name__ == "__main__":
    main()
