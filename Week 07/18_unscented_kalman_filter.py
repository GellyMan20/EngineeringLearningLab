# Purpose:
# This script demonstrates the implementation of an **Unscented Kalman Filter (UKF)** to estimate the state of a nonlinear system.
# A synthetic nonlinear process (`truth`) is simulated, and noisy measurements (`z`) based on the square of the state 
# are used as observations. The UKF is applied to estimate the state over time by propagating sigma points through the nonlinear system.
# The results are visualized in a plot showing the true state, noisy measurements, and the UKF's estimate.

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Main function
def main():
    """
    Simulates a nonlinear system and estimates its state using
    an Unscented Kalman Filter (UKF). Visualizes the true state,
    noisy measurements, and the UKF's state estimate.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(18)

    # Time settings and nonlinear true motion ("truth")
    dt = 0.1  # Time step in seconds
    t = np.arange(0, 30, dt)  # Time vector from 0 to 30 seconds with intervals of 0.1
    truth = np.zeros_like(t)  # Initialize true state array
    for k in range(1, len(t)):  # Simulate nonlinear process (recursive computation)
        truth[k] = truth[k - 1] + dt * np.sin(truth[k - 1]) + 0.05

    # Simulate noisy measurements
    z = truth**2 / 20 + rng.normal(0, 0.25, len(t))  # Measurements with Gaussian noise added to a nonlinear observation model

    # UKF parameters and initialization
    x = 0.2  # Initial state estimate
    P = 1.0  # Initial uncertainty (variance) of the state estimate
    Q = 0.03  # Process noise covariance
    R = 0.25**2  # Measurement noise covariance
    alpha = 0.4  # UKF alpha parameter (scaling factor for SPREAD of sigma points)
    beta = 2.0  # UKF beta parameter (distribution prior knowledge, 2 is optimal for Gaussian distributions)
    kappa = 0.0  # UKF kappa parameter (secondary scaling)
    n = 1  # State dimension
    lam = alpha**2 * (n + kappa) - n  # Scaling parameter lambda

    # Weights for mean and covariance calculations
    wm = np.array([lam / (n + lam), 1 / (2 * (n + lam)), 1 / (2 * (n + lam))])  # Mean weights
    wc = wm.copy()  # Covariance weights
    wc[0] += 1 - alpha**2 + beta  # Adjust weight for the first sigma point for covariance

    # UKF process variables to store estimates
    est = []  # List to store the estimate of the state

    # UKF loop for processing measurements
    for m in z:
        # Generate sigma points around the current estimate
        spread = np.sqrt((n + lam) * P)  # Spread of sigma points
        sigma = np.array([x, x + spread, x - spread])  # Sigma points

        # Predict the sigma points through the nonlinear process model
        sp = sigma + dt * np.sin(sigma) + 0.05  # Propagate sigma points
        xp = np.sum(wm * sp)  # Compute predicted mean state
        Pp = np.sum(wc * (sp - xp)**2) + Q  # Compute predicted state covariance

        # Transform the predicted sigma points through the measurement model
        zs = sp**2 / 20  # Apply nonlinear measurement function
        zp = np.sum(wm * zs)  # Compute predicted measurement mean
        S = np.sum(wc * (zs - zp)**2) + R  # Compute innovation covariance
        C = np.sum(wc * (sp - xp) * (zs - zp))  # Compute cross-covariance

        # Kalman gain and update step
        K = C / S  # Compute Kalman gain
        x = xp + K * (m - zp)  # Update state estimate
        P = Pp - K * S * K  # Update state covariance

        # Store the current estimate
        est.append(x)

    # Convert list of estimates to a numpy array for visualization
    est = np.array(est)

    # Visualization
    plt.figure()
    plt.plot(t, truth, label='Truth')  # Plot the true state
    plt.scatter(t, z, s=10, alpha=0.4, label='Measurements')  # Scatter plot of noisy measurements
    plt.plot(t, est, label='UKF')  # Plot the UKF's state estimate
    plt.grid(True)  # Add grid for clarity
    plt.legend()  # Add legend to identify the lines
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
