# Purpose:
# This script implements a **Kalman Filter** to estimate position and velocity in a 1D system
# while evaluating its consistency using special metrics: NIS (Normalized Innovation Squared) and NEES (Normalized Estimation Error Squared).
# NIS assesses the consistency of the filter with respect to measurement innovation, while NEES evaluates the consistency of the estimation error.
# The script visualizes NIS and NEES over time, checking if their mean values are close to expected theoretical values (1 for NIS and 2 for NEES).

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Main function
def main():
    """
    Implements a Kalman filter to estimate position and velocity from noisy observations,
    and analyzes the filter's consistency using NIS and NEES metrics.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(24)

    # Time settings and true motion
    dt = 0.1  # Time step in seconds
    t = np.arange(0, 40, dt)  # Time vector from 0 to 40 seconds with increments of 0.1
    tp = 1.2 * t  # True position as a linear function of time
    tv = np.full_like(t, 1.2)  # True velocity (constant)

    # Simulate noisy measurements
    z = tp + rng.normal(0, 2, len(t))  # Generate noisy measurements with Gaussian noise (std = 2)

    # Kalman filter initialization
    x = np.zeros((2, 1))  # Initial state [position, velocity]
    P = np.diag([30., 10.])  # Initial state covariance matrix
    F = np.array([[1, dt], [0, 1.]])  # State transition matrix
    H = np.array([[1., 0.]])  # Measurement matrix (maps state to position observation)
    Q = np.diag([0.01, 0.05])  # Process noise covariance matrix
    R = np.array([[4.]])  # Measurement noise covariance matrix (variance of observation noise)
    I = np.eye(2)  # Identity matrix for update step

    # Lists to store Normalized Innovation Squared (NIS) and Normalized Estimation Error Squared (NEES)
    nees = []  # NEES values to evaluate estimation consistency
    nis = []  # NIS values to evaluate innovation consistency

    # Kalman filter loop
    for k, m in enumerate(z):  # Iterate through each measurement
        # Predict step
        x = F @ x  # Predict the next state
        P = F @ P @ F.T + Q  # Predict the covariance matrix

        # Update step
        y = np.array([[m]]) - H @ x  # Compute the measurement residual (innovation)
        S = H @ P @ H.T + R  # Innovation covariance
        nis.append(float(y.T @ np.linalg.inv(S) @ y))  # Compute NIS for consistency of innovation
        K = P @ H.T @ np.linalg.inv(S)  # Kalman gain
        x = x + K @ y  # Update state using measurement
        P = (I - K @ H) @ P  # Update covariance matrix

        # Compute NEES values for consistency of estimation
        truth = np.array([[tp[k]], [tv[k]]])  # True state (position, velocity)
        e = truth - x  # Estimation error
        nees.append(float(e.T @ np.linalg.inv(P) @ e))  # Compute NEES for state estimation consistency

    # Print computed mean consistency metrics
    print(f'Mean NIS: {np.mean(nis):.2f} (expected near 1)')  # Check if mean NIS is close to 1
    print(f'Mean NEES: {np.mean(nees):.2f} (expected near 2)')  # Check if mean NEES is close to 2

    # Visualization - NIS (Normalized Innovation Squared)
    plt.figure()
    plt.plot(t, nis, label='NIS')  # Plot NIS over time
    plt.axhline(1, linestyle='--')  # Add a reference line for expected mean NIS (1)
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add a legend
    plt.show()

    # Visualization - NEES (Normalized Estimation Error Squared)
    plt.figure()
    plt.plot(t, nees, label='NEES')  # Plot NEES over time
    plt.axhline(2, linestyle='--')  # Add a reference line for expected mean NEES (2)
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add a legend
    plt.show()

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
