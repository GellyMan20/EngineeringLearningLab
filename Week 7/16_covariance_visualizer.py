# Purpose:
# This script generates a 2D scatter plot of random samples drawn from a multivariate normal distribution.
# It visualizes the confidence ellipses (at 1, 2, and 3 standard deviations) derived from the covariance matrix of the distribution.
# The confidence ellipses show regions where data points are expected to fall with a specified probability 
# and help visually understand the spread and orientation of the distribution.

# Import necessary libraries
import numpy as np  # For numerical operations, including random sampling and eigenvalue computations
import matplotlib.pyplot as plt  # For plotting and visualization
from matplotlib.patches import Ellipse  # For drawing ellipses

# Function to create an ellipse representing a confidence region for a multivariate normal distribution
def ell(mean, cov, n):
    """
    Create a confidence ellipse for a multivariate normal distribution.

    Parameters:
    - mean: 1D array-like, coordinates of the mean of the distribution
    - cov: 2D array-like, covariance matrix of the distribution
    - n: Number of standard deviations for the ellipse (1, 2, 3)

    Returns:
    - Matplotlib Ellipse object
    """
    vals, vecs = np.linalg.eigh(cov)  # Compute eigenvalues and eigenvectors
    o = vals.argsort()[::-1]  # Sort eigenvalues in descending order
    vals = vals[o]  # Sort eigenvalues
    vecs = vecs[:, o]  # Sort eigenvectors accordingly
    ang = np.degrees(np.arctan2(vecs[1, 0], vecs[0, 0]))  # Rotation angle of ellipse (in degrees)
    w, h = 2 * n * np.sqrt(vals)  # Width and height of ellipse (scaled by n standard deviations)
    return Ellipse(mean, w, h, angle=ang, fill=False, linewidth=2)  # Create and return ellipse

# Main function
def main():
    """
    Main function to simulate a multivariate normal distribution, 
    plot the samples, and overlay confidence ellipses.
    """
    # Initialize random number generator for reproducibility
    rng = np.random.default_rng(16)
    
    # Define the mean and covariance of the multivariate normal distribution
    mean = np.array([10., 5.])  # Mean vector (center of the distribution)
    cov = np.array([[9., 5.5], [5.5, 6.]])  # Covariance matrix (defines the spread and shape)
    
    # Generate random samples from the distribution
    s = rng.multivariate_normal(mean, cov, 800)  # 800 samples from the multivariate normal distribution

    # Create the plot
    fig, ax = plt.subplots()
    ax.scatter(s[:, 0], s[:, 1], s=8, alpha=0.3)  # Scatter plot of samples
    ax.scatter([mean[0]], [mean[1]], marker='x', label='Mean')  # Mark the mean point on the plot

    # Add confidence ellipses at 1, 2, and 3 standard deviations
    for n in [1, 2, 3]:  # Loop through 1-STD, 2-STD, and 3-STD confidence levels
        ax.add_patch(ell(mean, cov, n))  # Add confidence ellipse to the plot

    # Adjust plot settings
    ax.axis('equal')  # Ensure equal scaling for both axes
    ax.grid(True)  # Add a grid for better readability
    ax.legend()  # Include a legend to identify the mean point
    plt.show()  # Display the plot

# Entry point: Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
