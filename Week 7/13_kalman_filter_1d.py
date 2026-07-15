# Purpose:
# This script demonstrates the implementation of a 1D Kalman filter for estimating the position of an object
# undergoing constant acceleration. It takes noisy measurements of position and uses the Kalman filter to
# estimate the true position along with a measure of uncertainty. The results are visualized as the "true" position,
# noisy measurements, Kalman filter estimates, and the ±2σ confidence interval.

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For data visualization

# Main function
def main():
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(13)

    # Time settings and true motion equation
    dt = 0.1  # Time step in seconds
    t = np.arange(0, 40, dt)  # Time vector from 0 to 40 seconds with intervals of 0.1
    truth = 0.5 * t**2  # True position (constant acceleration motion: x = 0.5 * a * t^2)

    # Simulate noisy measurements of the position
    z = truth + rng.normal(0, 8, len(t))  # Noisy measurements with Gaussian noise (std dev = 8)

    # Kalman filter setup:
    # State vector: [position, velocity]
    x = np.array([[0.], [0.]])  # Initial state (start from position = 0, velocity = 0)
    P = np.diag([100., 100.])  # Initial uncertainty (covariance matrix)
    F = np.array([[1, dt], [0, 1.]])  # State transition matrix
    H = np.array([[1., 0.]])  # Measurement matrix, mapping from state to measurement
    Q = np.diag([0.05, 0.5])  # Process noise covariance matrix (uncertainty in state transitions)
    R = np.array([[64.]])  # Measurement noise covariance (variance of the measurement noise)
    I = np.eye(2)  # Identity matrix for update step

    # Containers for storing estimates and uncertainties
    est = []  # List to store position estimates
    sig = []  # List to store standard deviations of position estimates

    # Kalman filter loop
    for meas in z:
        # Prediction step
        x = F @ x  # Predict the state vector
        P = F @ P @ F.T + Q  # Predict the state covariance

        # Update step
        y = np.array([[meas]]) - H @ x  # Compute measurement residual (innovation)
        S = H @ P @ H.T + R  # Compute innovation covariance
        K = P @ H.T @ np.linalg.inv(S)  # Compute Kalman gain
        x = x + K @ y  # Update state estimate
        P = (I - K @ H) @ P  # Update state covariance

        # Store estimate and uncertainty
        est.append(x[0, 0])  # Store the position estimate
        sig.append(np.sqrt(P[0, 0]))  # Store the standard deviation of the position estimate

    # Convert lists to arrays for plotting
    est = np.array(est)
    sig = np.array(sig)

    # Visualization
    plt.figure()
    plt.plot(t, truth, label='Truth')  # Plot the true position
    plt.scatter(t, z, s=10, alpha=0.4, label='Measurements')  # Scatter plot of noisy measurements
    plt.plot(t, est, label='Estimate')  # Plot the Kalman filter position estimates
    plt.fill_between(t, est - 2 * sig, est + 2 * sig, alpha=0.2, label='±2σ')  # Plot the ±2 standard deviation confidence interval
    plt.grid(True)  # Add a grid for better visualization
    plt.legend()  # Add a legend to the plot
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
