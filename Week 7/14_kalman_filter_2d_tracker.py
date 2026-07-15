# Purpose:
# This script implements a 2D Kalman filter to estimate the position of an object moving in a 2D plane.
# The "true" position is based on a defined trajectory, and noisy measurements are provided as input. 
# The Kalman filter combines these noisy measurements with a motion model to produce smoothed position estimates over time.
# The results are visualized, showing the true trajectory, noisy measurements, and the Kalman filter estimates.

# Import necessary libraries
import numpy as np  # For numerical computations and matrix operations
import matplotlib.pyplot as plt  # For plotting and visualization

# Main function
def main():
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(14)

    # Time settings and true motion trajectory
    dt = 0.2  # Time step in seconds
    t = np.arange(0, 60, dt)  # Time vector from 0 to 60 seconds with intervals of 0.2
    tx = 2 * t  # True x-coordinate as a linear function of time
    ty = 0.8 * t + 10 * np.sin(t / 10)  # True y-coordinate as a sine-modulated function of time

    # Simulate noisy 2D measurements of the position
    z = np.column_stack((tx + rng.normal(0, 2, len(t)),  # Noisy x-measurements
                         ty + rng.normal(0, 2, len(t))))  # Noisy y-measurements

    # Kalman filter setup:
    # State vector: [x_position, y_position, x_velocity, y_velocity]
    x = np.zeros((4, 1))  # Initial state vector (position and velocity set to 0)
    P = np.diag([100, 100, 25, 25]).astype(float)  # Initial uncertainty (covariance matrix)
    F = np.array([[1, 0, dt, 0],  # State transition matrix (models motion dynamics)
                  [0, 1, 0, dt],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1.]], float)
    H = np.array([[1, 0, 0, 0],  # Measurement matrix, mapping state to observed values
                  [0, 1, 0, 0.]], float)
    Q = np.diag([0.1, 0.1, 0.8, 0.8])  # Process noise covariance (models uncertainty in system dynamics)
    R = np.diag([4., 4.])  # Measurement noise covariance (uncertainty in measurements)
    I = np.eye(4)  # Identity matrix for update step

    # Container for storing estimated states
    est = []  # List to store position estimates

    # Kalman filter loop
    for m in z:  # Loop through each measurement
        # Prediction step
        x = F @ x  # Predict the next state
        P = F @ P @ F.T + Q  # Predict the state covariance

        # Update step
        y = m.reshape(2, 1) - H @ x  # Measurement residual (innovation)
        S = H @ P @ H.T + R  # Innovation covariance
        K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
        x = x + K @ y  # Update state with measurement
        P = (I - K @ H) @ P  # Update covariance matrix

        # Store the position estimate (first two elements of the state vector)
        est.append(x.ravel())

    # Convert list to numpy array for easier handling
    est = np.array(est)

    # Visualization
    plt.figure()
    plt.plot(tx, ty, label='Truth')  # Plot the true trajectory
    plt.scatter(z[:, 0], z[:, 1], s=10, alpha=0.4, label='Measurements')  # Scatter plot of noisy measurements
    plt.plot(est[:, 0], est[:, 1], label='Estimate')  # Plot the Kalman filter estimates
    plt.axis('equal')  # Ensure the x and y axes have equal scaling for accuracy
    plt.grid(True)  # Add a grid for better visualization
    plt.legend()  # Add a legend to differentiate the lines
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
