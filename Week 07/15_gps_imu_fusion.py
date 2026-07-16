# Purpose:
# This script demonstrates the fusion of IMU (inertial measurement unit) and GPS (Global Positioning System) data using a Kalman filter 
# to estimate position over time. The IMU provides high-frequency but noisy and drift-prone acceleration measurements, 
# while the GPS provides low-frequency but accurate position measurements. By combining both sources of data, the Kalman filter 
# generates a smoother and more accurate position estimate compared to either sensor alone. 

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Main function
def main():
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(15)

    # Time settings and ground truth motion
    dt = 0.01  # Time step in seconds
    t = np.arange(0, 50, dt)  # Time vector from 0 to 50 seconds with intervals of 0.01
    a = 0.2 * np.sin(0.3 * t)  # True acceleration signal (sine-modulated)
    v = np.cumsum(a) * dt  # Integrate acceleration to get velocity
    truth = np.cumsum(v) * dt  # Integrate velocity to get position

    # Simulate IMU and GPS measurements
    imu = a + 0.015 + rng.normal(0, 0.04, len(t))  # IMU readings (acceleration) with bias and noise
    gps = np.full(len(t), np.nan)  # Initialize GPS position measurements as NaN
    gps[::100] = truth[::100] + rng.normal(0, 1.2, len(gps[::100]))  # GPS measurements every 100 steps with noise

    # Kalman filter setup:
    # State vector: [position, velocity]
    x = np.zeros((2, 1))  # Initial state vector [position, velocity]
    P = np.diag([25., 9.])  # Initial covariance matrix (uncertainty in position and velocity)
    H = np.array([[1., 0.]])  # Measurement matrix (maps position from state vector)
    I = np.eye(2)  # Identity matrix for the update step
    est = []  # List to store position estimates

    # Kalman filter loop
    for k in range(len(t)):
        # State transition matrix and control input matrix
        F = np.array([[1, dt], [0, 1.]])  # State transition matrix modeling motion
        B = np.array([[0.5 * dt**2], [dt]])  # Control input matrix for acceleration
        Q = np.diag([0.0005, 0.02])  # Process noise covariance matrix

        # Predict step
        x = F @ x + B * imu[k]  # Predict the next state
        P = F @ P @ F.T + Q  # Update state covariance with process noise

        # Update step (if GPS measurement is available)
        if not np.isnan(gps[k]):  # Check if the current GPS measurement is valid (not NaN)
            R = np.array([[1.2**2]])  # Measurement noise covariance (for GPS)
            y = np.array([[gps[k]]]) - H @ x  # Compute measurement residual (innovation)
            S = H @ P @ H.T + R  # Innovation covariance
            K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
            x = x + K @ y  # Update state estimate with GPS measurement
            P = (I - K @ H) @ P  # Update covariance matrix

        # Store the position estimate
        est.append(x[0, 0])  # Store the position estimate (first element of state vector)

    # Convert list of estimates to a numpy array for plotting
    est = np.array(est)

    # Visualization
    plt.figure()
    plt.plot(t, truth, label='Truth')  # Plot the true position
    plt.scatter(t[::100], gps[::100], s=15, label='GPS')  # Scatter plot of GPS measurements
    plt.plot(t, est, label='Fused')  # Plot the Kalman filter position estimates
    plt.grid(True)  # Add a grid for visual clarity
    plt.legend()  # Add a legend to differentiate the lines
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
