# Purpose:
# This script demonstrates the implementation of an **Extended Kalman Filter (EKF)** for tracking the 2D position of a moving object.
# The object's "true" position is modeled with linear motion in a 2D plane, and noisy range and bearing measurements (polar coordinates) 
# are provided as input. The EKF estimates the object's position and velocity while handling the nonlinearities of range and bearing data.
# The results are visualized by comparing the true trajectory with the EKF-estimated trajectory.

# Import necessary libraries
import numpy as np  # For numerical operations and random number generation
import matplotlib.pyplot as plt  # For plotting and visualization

# Function to wrap angles into the range [-π, π]
def wrap(a):
    """
    Wrap an angle in radians to the range [-π, π].

    Parameters:
    - a: Angle in radians

    Returns:
    - Wrapped angle in radians
    """
    return (a + np.pi) % (2 * np.pi) - np.pi

# Function to compute the observation model for the EKF
def h(x):
    """
    Observation model: Converts the state vector (Cartesian coordinates) to range and bearing.

    Parameters:
    - x: State vector [px, py, vx, vy] in Cartesian coordinates

    Returns:
    - Observation (range and bearing)
    """
    px, py = x[0, 0], x[1, 0]  # Extract position components
    return np.array([[np.hypot(px, py)],  # Range (Euclidean distance)
                     [np.arctan2(py, px)]])  # Bearing (angle in radians)

# Jacobian matrix of the observation model
def H_jac(x):
    """
    Compute the Jacobian matrix of the observation model (h) for the EKF.
    
    Parameters:
    - x: State vector [px, py, vx, vy]

    Returns:
    - Jacobian matrix (4x2) of the observation model
    """
    px, py = x[0, 0], x[1, 0]  # Extract position components
    r2 = max(px**2 + py**2, 1e-9)  # Ensure no division by zero (add a small value as lower bound)
    r = np.sqrt(r2)  # Range (Euclidean distance)
    return np.array([[px / r, py / r, 0, 0],  # Partial derivatives for range
                     [-py / r2, px / r2, 0, 0]])  # Partial derivatives for bearing

# Main function
def main():
    """
    Simulates a 2D tracking scenario where noisy polar observations (range and bearing) are used to estimate position and velocity.
    The EKF updates its state estimate iteratively using these measurements.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(17)

    # Time settings and true motion trajectory
    dt = 0.1  # Time step in seconds
    t = np.arange(0, 50, dt)  # Time vector from 0 to 50 seconds with intervals of 0.1
    tx = 25 + 1.2 * t  # True x-coordinate, linear in time
    ty = 15 + 0.7 * t  # True y-coordinate, linear in time

    # Simulate noisy range (zr) and bearing (zb) measurements
    zr = np.hypot(tx, ty) + rng.normal(0, 1, len(t))  # Range with Gaussian noise
    zb = np.arctan2(ty, tx) + rng.normal(0, np.deg2rad(1), len(t))  # Bearing with Gaussian noise

    # Initialize Kalman filter variables
    x = np.array([[20.], [10.], [0.], [0.]])  # Initial state vector: position [px, py] and velocity [vx, vy]
    P = np.diag([100., 100., 10., 10.])  # Initial covariance matrix (uncertainty in position and velocity)
    F = np.array([[1, 0, dt, 0],  # State transition matrix
                  [0, 1, 0, dt],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1.]], float)
    Q = np.diag([0.05, 0.05, 0.2, 0.2])  # Process noise covariance matrix
    R = np.diag([1., np.deg2rad(1)**2])  # Measurement noise covariance
    I = np.eye(4)  # Identity matrix for update step
    est = []  # List to store position estimates

    # Kalman filter loop
    for r, b in zip(zr, zb):  # Loop through range and bearing measurements
        # Predict step
        x = F @ x  # Predict the next state
        P = F @ P @ F.T + Q  # Predict the state covariance

        # Update step
        z = np.array([[r], [b]])  # Current measurement (range and bearing)
        y = z - h(x)  # Compute measurement residual (innovation)
        y[1, 0] = wrap(y[1, 0])  # Wrap the bearing residual to [-π, π]
        H = H_jac(x)  # Compute the Jacobian of the observation model
        S = H @ P @ H.T + R  # Innovation covariance
        K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
        x = x + K @ y  # Update state estimate
        P = (I - K @ H) @ P  # Update covariance matrix

        # Store the position estimate
        est.append(x.ravel())

    # Convert list of estimates to a numpy array for easier handling
    est = np.array(est)

    # Visualization
    plt.figure()
    plt.plot(tx, ty, label='Truth')  # Plot the true trajectory
    plt.plot(est[:, 0], est[:, 1], label='EKF')  # Plot the EKF-estimated trajectory
    plt.axis('equal')  # Ensure equal scaling for x and y axes
    plt.grid(True)  # Add a grid for better visualization
    plt.legend()  # Add a legend to differentiate the lines
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
