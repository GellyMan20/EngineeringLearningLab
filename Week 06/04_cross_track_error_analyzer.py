"""
Project 04 — Cross-Track Error Analyzer
Purpose:
This script demonstrates how to compute and analyze **cross-track error (CTE)** for a vehicle following a predefined path. 
Cross-track error measures the lateral deviation (perpendicular distance) between the vehicle's actual path 
and the desired path. Key concepts and metrics learned include:
- Calculating the **mean cross-track error**, **root mean square (RMS) error**, and **maximum cross-track error**.
- Measuring the deviation of the vehicle's path from the desired trajectory.
- Visualizing the errors and their relationship to vehicle path deviation.

The results include visualization of the desired path against the actual vehicle path and the computed cross-track errors.
"""

# Import necessary libraries
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For visualization

# Function to compute the perpendicular distance from a point to a polyline
def distance_to_polyline(point, path):
    """
    Calculate the minimum distance from a point to a polyline.

    Parameters:
        point (ndarray): A 2D coordinate [x, y].
        path (ndarray): Array of 2D points representing the desired path.

    Returns:
        float: The minimum distance from the point to the polyline.
    """
    min_dist = float('inf')  # Initialize with a large value
    for i in range(len(path) - 1):  # Iterate through line segments in the polyline
        a, b = path[i], path[i + 1]  # Two consecutive points defining a line segment
        ab = b - a  # Vector from a to b
        ap = point - a  # Vector from a to the point

        # Project the point onto the line segment and clamp to [0, 1]
        projection = np.clip(np.dot(ap, ab) / np.dot(ab, ab), 0.0, 1.0)
        candidate = a + projection * ab  # Closest point on the segment

        # Calculate the distance from the point to the candidate point
        min_dist = min(min_dist, np.linalg.norm(point - candidate))
    return min_dist

# Main function for simulating cross-track error analysis
def main():
    """
    Simulates a vehicle following a path and calculates the cross-track error (mean, 
    RMS, and max). Visualizes the actual vehicle path against the desired path 
    and plots the cross-track error over time.
    """

    # Define the desired path (sinusoidal curve)
    path_x = np.linspace(0, 100, 400)  # X-coordinates of the path
    path_y = 8 * np.sin(path_x / 10)  # Y-coordinates (sinusoidal shape)
    path = np.column_stack((path_x, path_y))  # Combine x and y into an array representing the desired path

    # Simulate a noisy vehicle path
    rng = np.random.default_rng(4)  # Random number generator for reproducibility
    vehicle_x = path_x  # We assume the vehicle progresses along the x-coordinates of the path
    vehicle_y = (8 * np.sin((vehicle_x - 4) / 10) +  # Perturbed sinusoidal motion
                 1.5 * np.sin(vehicle_x / 5) +       # Additional distortion
                 rng.normal(0, 0.5, len(vehicle_x)))  # Random Gaussian noise
    vehicle_path = np.column_stack((vehicle_x, vehicle_y))  # Combine noisy x and y into the vehicle path

    # Calculate cross-track errors
    errors = np.array([distance_to_polyline(point, path) for point in vehicle_path])

    # Output metrics
    print('Cross-Track Error Metrics')
    print(f'Mean error: {np.mean(errors):.3f} m')  # Mean cross-track error
    print(f'RMS error:  {np.sqrt(np.mean(errors**2)):.3f} m')  # Root mean square error (RMS)
    print(f'Max error:  {np.max(errors):.3f} m')  # Maximum cross-track error

    # Visualization: Vehicle path vs desired path
    plt.figure()
    plt.plot(path[:, 0], path[:, 1], '--', label='Desired path')  # Plot desired path
    plt.plot(vehicle_path[:, 0], vehicle_path[:, 1], label='Vehicle path')  # Plot vehicle's actual path
    plt.title('Cross-Track Error Analyzer')  # Add plot title
    plt.xlabel('X [m]')  # Add x-axis label
    plt.ylabel('Y [m]')  # Add y-axis label
    plt.axis('equal')  # Set equal axis scaling
    plt.grid(True)  # Add grid for better readability
    plt.legend()  # Add legend
    plt.show()

    # Visualization: Cross-track error
    plt.figure()
    plt.plot(errors)  # Plot errors over time
    plt.title('Cross-Track Error')  # Add plot title
    plt.xlabel('Sample')  # Add x-axis label
    plt.ylabel('Error [m]')  # Add y-axis label
    plt.grid(True)  # Add grid
    plt.show()

# Entry point: Run the simulation
if __name__ == '__main__':
    main()
