# Purpose:
# This script implements a **particle filter** for estimating the position of a moving object.
# The object's true position changes over time, and noisy sensor observations of distances to fixed landmarks are provided.
# The particle filter tracks the object's location by maintaining a set of particles and their weights, which are iteratively updated using sensor measurements.
# Resampling is performed when the particle weights become too imbalanced, ensuring robust tracking performance.
# The results are visualized to show the "true" position of the object and its estimated position based on the particle filter.

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For visualization

# Resample function for the particle filter
def resample(w, rng):
    """
    Resample particles based on their weights using the systematic resampling method.

    Parameters:
    - w: Particle weights (array)
    - rng: Random number generator

    Returns:
    - idx: Indices of resampled particles
    """
    n = len(w)  # Number of particles
    pos = (rng.random() + np.arange(n)) / n  # Systematic sampling positions
    idx = np.zeros(n, dtype=int)  # Initialize resampled indices
    c = np.cumsum(w)  # Cumulative sum of weights
    i = j = 0  # Indices for position and weight arrays
    while i < n:
        if pos[i] < c[j]:  # If the sampling position falls under this cumulative weight
            idx[i] = j  # Assign the particle index
            i += 1  # Move to the next position
        else:
            j += 1  # Move to the next cumulative weight
    return idx

# Main function
def main():
    """
    Simulates a 1D particle filter tracking an object's position over time using noisy sensor observations
    of distances to fixed landmarks. Visualizes the true position of the object and the particle filter's estimate.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(19)

    # Define fixed landmarks and simulation parameters
    landmarks = np.array([20., 50., 75.])  # Positions of landmarks in 1D space
    true_x = 0.  # Initial true position of the object
    vel = 0.35  # Constant velocity of the object
    n = 1000  # Number of particles
    p = rng.normal(0, 5, n)  # Initialize particle positions with Gaussian distribution (mean=0, std=5)
    w = np.full(n, 1 / n)  # Initialize particle weights uniformly
    truth = []  # List to store the true position at each time step
    est = []  # List to store the particle filter's estimated position

    # Particle filter loop
    for _ in range(250):  # Iterate over 250 time steps
        # Update the true position
        true_x += vel + rng.normal(0, 0.03)  # True position update with added process noise

        # Predict particle positions based on motion and noise
        p += vel + rng.normal(0, 0.12, n)

        # Simulate range observations (distance from landmarks)
        obs = np.abs(landmarks - true_x) + rng.normal(0, 0.8, len(landmarks))

        # Reset weights to uniform
        w.fill(1.)

        # Update weights based on observations
        for lm, z in zip(landmarks, obs):  # Loop over each landmark and observation
            w *= np.exp(-0.5 * ((z - np.abs(lm - p)) / 0.8)**2) + 1e-12  # Gaussian likelihood
        w /= np.sum(w)  # Normalize weights

        # Store the true position and particle filter estimate
        truth.append(true_x)  # Store true position
        est.append(np.sum(w * p))  # Compute and store the weighted mean as the estimate

        # Resample particles if the effective number of particles is too low
        if 1 / np.sum(w**2) < n / 2:  # Resample condition based on particle degeneracy
            p = p[resample(w, rng)]  # Resample particles based on weights
            w.fill(1 / n)  # Reset particle weights to uniform

    # Visualization of results
    plt.figure()
    plt.plot(t, truth, label='Truth')  # Plot the true position trajectory
    plt.plot(t, est, label='Particle filter')  # Plot the particle filter's estimate
    plt.grid(True)  # Add a grid for better visualization
    plt.legend()  # Add a legend to differentiate the lines
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
