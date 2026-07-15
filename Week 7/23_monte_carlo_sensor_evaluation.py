# Purpose:
# This script performs a Monte Carlo simulation to evaluate the performance of a Kalman filter that estimates 
# the position of an object based on noisy IMU and GPS data. Randomized sensor noise, biases, and variances 
# are used in each trial to assess the filter's robustness. Metrics such as RMSE (Root Mean Square Error) 
# and maximum error are calculated, and the results are visualized in a histogram of RMSE values across the trials.

# Import necessary libraries
import numpy as np  # For numerical operations and random number generation
import matplotlib.pyplot as plt  # For plotting and visualization

# Function to run a single trial of the Kalman filter simulation
def trial(rng):
    """
    Simulates a single trial of position estimation using a Kalman filter
    with noisy IMU and GPS data.

    Parameters:
    - rng: Random number generator for reproducibility.

    Returns:
    - RMSE (Root Mean Square Error) and maximum absolute error for the trial.
    """
    # Time parameters and true motion
    dt = 0.05  # Time step
    t = np.arange(0, 40, dt)  # Time array
    a = 0.15 * np.sin(0.25 * t)  # True acceleration
    v = np.cumsum(a) * dt  # True velocity
    truth = np.cumsum(v) * dt  # True position based on double integration of acceleration

    # Simulate IMU and GPS noise parameters
    bias = rng.normal(0, 0.03)  # Bias in IMU measurement
    imu_std = rng.uniform(0.02, 0.08)  # Random IMU standard deviation
    gps_std = rng.uniform(0.7, 2.5)  # Random GPS standard deviation

    # Generate noisy IMU and GPS data
    imu = a + bias + rng.normal(0, imu_std, len(t))  # IMU noise
    gps = np.full(len(t), np.nan)  # Initialize GPS readings as NaN
    gps[::20] = truth[::20] + rng.normal(0, gps_std, len(gps[::20]))  # GPS measurements every 20 steps

    # Initialize Kalman filter variables
    x = np.zeros((2, 1))  # Initial state [position, velocity]
    P = np.diag([20., 8.])  # Initial covariance matrix
    H = np.array([[1., 0.]])  # Measurement matrix to extract position
    I = np.eye(2)  # Identity matrix for update step
    est = []  # To store Kalman filter position estimates

    # Kalman filter process
    for k in range(len(t)):
        # State transition matrix and control model
        F = np.array([[1, dt], [0, 1.]])  # State transition matrix
        B = np.array([[0.5 * dt**2], [dt]])  # Input model for acceleration
        Q = np.diag([0.001, 0.03])  # Process noise covariance

        # Prediction step
        x = F @ x + B * imu[k]  # Predict next state
        P = F @ P @ F.T + Q  # Predict covariance

        # Update step if GPS measurement is available
        if not np.isnan(gps[k]):  # Skip update if GPS measurement is missing
            R = np.array([[gps_std**2]])  # Measurement noise covariance
            y = np.array([[gps[k]]]) - H @ x  # Measurement residual (innovation)
            S = H @ P @ H.T + R  # Innovation covariance
            K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
            x = x + K @ y  # Updated state estimate incorporating GPS
            P = (I - K @ H) @ P  # Updated covariance

        # Store the position estimate
        est.append(x[0, 0])

    # Calculate errors for this trial
    est = np.array(est)
    e = est - truth  # Error between estimated and truth
    rmse = np.sqrt(np.mean(e**2))  # Root Mean Square Error
    max_error = np.max(np.abs(e))  # Maximum absolute error

    return rmse, max_error  # Return error metrics for this trial

# Main function to perform Monte Carlo simulation
def main():
    """
    Runs a Monte Carlo simulation to evaluate the Kalman filter
    main()
