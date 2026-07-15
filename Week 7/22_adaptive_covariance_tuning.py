# Purpose:
# This script demonstrates an **adaptive Kalman filter** where the measurement noise covariance (`R`) is dynamically updated
# based on the innovation (residual) at each time step. The system's true position follows a linear trajectory, while the noise 
# in the measurements varies over different time intervals (higher noise from `t=20` to `t=40`).
# The adaptive Kalman filter adjusts itself to account for this changing measurement noise.

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Main function
def main():
    """
    Implements an adaptive Kalman filter to estimate the position of an object,
    accounting for changing measurement noise over time. The adaptive filter 
    adjusts the measurement noise covariance dynamically based on the residuals.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(22)

    # Time settings and true motion
    dt = 0.1  # Time step in seconds
    t = np.arange(0, 60, dt)  # Time vector from 0 to 60 seconds with increments of 0.1
    truth = 0.8 * t  # True position (linear motion)

    # Simulate noisy sensor measurements with time-varying noise
    std = np.where((t >= 20) & (t <= 40), 5., 1.)  # Standard deviation of measurement noise (high between t=20 and t=40)
    z = truth + rng.normal(0, std)  # Noisy measurements

    # Initial state and covariance matrix
    x = np.array([[0.], [0.]])  # State vector: [position, velocity]
    P = np.diag([50., 10.])  # Initial state covariance matrix
    F = np.array([[1, dt], [0, 1.]])  # State transition matrix
    H = np.array([[1., 0.]])  # Measurement matrix
    Q = np.diag([0.02, 0.2])  # Process noise covariance matrix
    I = np.eye(2)  # Identity matrix for update step
    Rv = 1.  # Initial measurement noise covariance estimate

    # Lists to store results
    est = []  # Position estimates
    rh = []  # Adaptively updated measurement noise covariance values

    # Kalman filter loop
    for m in z:  # Iterate through each measurement
        # Predict step
        x = F @ x  # Predict the next state
        P = F @ P @ F.T + Q  # Predict the covariance matrix

        # Compute innovation and adapt measurement noise covariance (R)
        innov = float(m - (H @ x)[0, 0])  # Measurement residual (innovation)
        Rv = 0.97 * Rv + 0.03 * np.clip(innov**2, 0.5, 36.)  # Update adaptive measurement noise covariance
        R = np.array([[Rv]])  # New measurement noise covariance

        # Update step
        S = H @ P @ H.T + R  # Innovation covariance
        K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
        x = x + K @ np.array([[innov]])  # Update state with measurement residual
        P = (I - K @ H) @ P  # Update state covariance

        # Store the current estimate and adaptive measurement noise estimate
        est.append(x[0, 0])  # Position estimate
        rh.append(Rv)  # Adaptive measurement noise covariance

    # Convert results to numpy arrays for visualization
    est = np.array(est)
    rh = np.array(rh)

    # Visualization - Plot true position, noisy measurements, and Kalman filter estimates
    plt.figure()
    plt.plot(t, truth, label='Truth')  # Plot the true position
    plt.scatter(t, z, s=10, alpha=0.35, label='Measurements')  # Scatter plot of measurements
    plt.plot(t, est, label='Adaptive')  # Plot the adaptive Kalman filter position estimates
    plt.grid(True)  # Add a grid for clarity
    plt.legend()  # Add a legend to differentiate elements
    plt.show()

    # Visualization - Plot the adaptive measurement noise covariance
    plt.figure()
    plt.plot(t, rh)  # Plot the adaptive R values over time
    plt.title('Adaptive R')  # Title of the plot
    plt.grid(True)  # Add grid for clarity
    plt.show()

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
