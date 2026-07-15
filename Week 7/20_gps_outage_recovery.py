# Purpose:
# This script demonstrates the use of a **Kalman Filter** to estimate position over time by fusing data from an IMU (inertial measurement unit)
# providing acceleration measurements and GPS providing sparse but more accurate position measurements.
# The Kalman Filter is used to smooth out IMU noise and to handle occasional GPS outages (from t=25 to t=50 in this simulation).
# The result includes an estimate of position along with a confidence region (±2 standard deviations), plotted against the true position.

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Main function
def main():
    """
    Simulates a Kalman Filter for fusing IMU and GPS data for position estimation
    over time. Accounts for sporadic GPS outages.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(20)

    # Time settings and nonlinear true motion ("truth")
    dt = 0.02  # Time step in seconds
    t = np.arange(0, 80, dt)  # Time vector from 0 to 80 seconds with intervals of 0.02
    a = 0.1 * np.sin(0.2 * t)  # True acceleration as sine wave
    v = np.cumsum(a) * dt  # True velocity (integrated acceleration)
    truth = np.cumsum(v) * dt  # True position (integrated velocity)

    # Simulate IMU and GPS measurements
    imu = a + 0.02 + rng.normal(0, 0.035, len(t))  # IMU acceleration with bias and Gaussian noise
    gps = np.full(len(t), np.nan)  # Initialize GPS as NaN
    gps[::50] = truth[::50] + rng.normal(0, 1, len(gps[::50]))  # GPS position sampled every 50 steps with noise
    gps[(t >= 25) & (t <= 50)] = np.nan  # Simulate GPS outage between t=25 and t=50 seconds

    # Kalman filter variables initialization
    x = np.zeros((2, 1))  # Initial state vector: [position, velocity]
    P = np.diag([20., 8.])  # Initial state covariance matrix
    H = np.array([[1., 0.]])  # Measurement matrix, mapping state to position
    I = np.eye(2)  # Identity matrix for update step
    est = []  # List to store position estimates
    sig = []  # List to store standard deviation of position estimates

    # Kalman filter loop
    for k in range(len(t)):
        # State transition matrix (motion model) and control input matrix
        F = np.array([[1, dt], [0, 1.]])  # State transition matrix
        B = np.array([[0.5 * dt**2], [dt]])  # Control input matrix for acceleration

        # Process noise covariance matrix
        Q = np.diag([0.0008, 0.03])  # Small process noise (position and velocity)

        # Predict step
        x = F @ x + B * imu[k]  # Predict state using the IMU acceleration measurement
        P = F @ P @ F.T + Q  # Predict covariance matrix

        # Update step (if there is a valid GPS measurement)
        if not np.isnan(gps[k]):  # Check if the GPS measurement is valid (not NaN)
            R = np.array([[1.]])  # Measurement noise covariance for GPS
            y = np.array([[gps[k]]]) - H @ x  # Measurement residual (innovation)
            S = H @ P @ H.T + R  # Innovation covariance
            K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
            x = x + K @ y  # Update state estimate
            P = (I - K @ H) @ P  # Update covariance matrix

        # Store the current position estimate and its uncertainty
        est.append(x[0, 0])  # Position estimate (first element of state vector)
        sig.append(np.sqrt(P[0, 0]))  # Standard deviation (uncertainty) of position estimate

    # Convert lists to numpy arrays for plotting
    est = np.array(est)
    sig = np.array(sig)

    # Visualization
    plt.figure()
    plt.plot(t, truth, label='Truth')  # Plot the true position
    plt.plot(t, est, label='Estimate')  # Plot the Kalman filter position estimates
    plt.axvspan(25, 50, alpha=0.2, label='GPS outage')  # Highlight GPS outage interval
    plt.fill_between(t, est - 2 * sig, est + 2 * sig, alpha=0.2, label='±2σ')  # Plot ±2 standard deviation confidence bounds
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add legend to differentiate components
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
