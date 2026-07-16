# Purpose:
# This script simulates measurement data with Gaussian noise and computes various error metrics
# to evaluate the accuracy of the measurements compared to the true values. The key metrics calculated include:
# bias, standard deviation (std), root mean square error (RMSE), mean absolute error (MAE), 
# 95th percentile of absolute errors, and the maximum absolute error. The results are displayed 
# in a concise and human-readable format.

# Import necessary libraries
import numpy as np  # For numerical operations, including random number generation and mathematical functions
import pandas as pd  # For creating and managing structured tabular data

# Main function
def main():
    # Initialize the random number generator with a fixed seed for reproducibility
    rng = np.random.default_rng(9)  # Ensures consistent random results across runs

    # Configure the size of the dataset and generate a "true" signal
    n = 5000  # Number of data points
    truth = np.linspace(0, 100, n)  # True values evenly spaced between 0 and 100

    # Simulate measurements by adding Gaussian noise to the true values
    m = truth + 0.7 + rng.normal(0, 1.4, n)  # Add a constant bias of 0.7 and noise with std dev of 1.4
    e = m - truth  # Calculate the error between the true values and the measurements
    
    # Create a Pandas DataFrame to organize and store the data
    df = pd.DataFrame({'truth': truth, 'measurement': m, 'error': e})

    # Compute error metrics
    metrics = {
        'bias': df.error.mean(),  # Average error (difference between measurement and truth)
        'std': df.error.std(ddof=1),  # Standard deviation of the errors
        'rmse': np.sqrt(np.mean(e**2)),  # Root mean square error
        'mae': np.mean(np.abs(e)),  # Mean absolute error
        'p95_abs_error': np.percentile(np.abs(e), 95),  # 95th percentile of the absolute error
        'max_abs_error': np.max(np.abs(e))  # Maximum absolute error
    }

    # Print each metric with its corresponding value in a readable format
    for k, v in metrics.items():
        print(f'{k:>15}: {v:.3f}')  # Align and format the values with 3 decimal places

# Entry point for the program: Execute the main function if this script is run directly
if __name__ == '__main__':
    main()
