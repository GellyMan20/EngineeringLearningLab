"""
Project: Bode Plot Explorer
Purpose:
This script demonstrates the generation of **Bode plots** to analyze the frequency response of a first-order system. Bode plots are essential tools in control systems and signal processing for characterizing system behavior in terms of:
- **Frequency Response**: Evaluates how a system responds to different input frequencies.
- **Magnitude**: Describes how much a particular frequency is amplified or attenuated (in decibels, dB).
- **Phase**: Represents the phase shift between input and output signals (in degrees).
- **Bandwidth**: Identifies the range of frequencies over which the system operates effectively.

Applications:
- **Control Systems Engineering**: Tuning compensators and understanding system stability.
- **Signal Processing**: Frequency-selective filtering design.
- **Education**: Teaching the fundamentals of system dynamics and frequency analysis.

Key Concepts:
- The response of a **first-order system** is characterized by a time constant (\( \tau \)).
- The system behaves differently at low, high, and corner frequencies, and this behavior is visualized through magnitude and phase plots.
"""

# Import necessary libraries
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For plotting Bode magnitude and phase plots

# Function to compute the magnitude and phase of a first-order system
def bode_first_order(tau, omega):
    """
    Computes the magnitude and phase of a first-order system for a range of frequencies.

    Parameters:
        tau (float): Time constant of the first-order system.
        omega (ndarray): Array of angular frequencies (rad/s).

    Returns:
        tuple: Magnitude in decibels (dB) and phase in degrees.
    """
    G = 1 / (tau * 1j * omega + 1)  # First-order transfer function: G(s) = 1 / (τs + 1)
    magnitude = 20 * np.log10(np.abs(G))  # Magnitude response in dB
    phase = np.angle(G, deg=True)  # Phase response in degrees
    return magnitude, phase

# Main function to generate and visualize Bode plots
def main():
    """
    Visualizes the Bode magnitude and phase plots for a first-order system with various time constants.
    Demonstrates the impact of the system's time constant (\( \tau \)) on frequency response.
    """

    # Generate a set of logarithmically spaced angular frequencies (rad/s)
    omega = np.logspace(-2, 2, 1000)  # Frequencies from 0.01 to 100 rad/s

    # Plot Bode magnitude (dB vs frequency) for different time constants
    plt.figure()
    for tau in [0.1, 0.5, 1.0, 3.0]:  # Test time constants
        mag, _ = bode_first_order(tau, omega)  # Compute magnitude response
        plt.semilogx(omega, mag, label=f"τ = {tau}")  # Plot magnitude vs. frequency
    plt.title("Bode Magnitude")  # Title of the plot
    plt.xlabel("Frequency [rad/s]")  # Label for x-axis
    plt.ylabel("Magnitude [dB]")  # Label for y-axis
    plt.grid(True, which="both")  # Add gridlines for logarithmic scales
    plt.legend()  # Add legend to distinguish time constants
    plt.show()  # Display the magnitude plot

    # Plot Bode phase (Phase vs frequency) for different time constants
    plt.figure()
    for tau in [0.1, 0.5, 1.0, 3.0]:  # Test time constants
        _, phase = bode_first_order(tau, omega)  # Compute phase response
        plt.semilogx(omega, phase, label=f"τ = {tau}")  # Plot phase vs. frequency
    plt.title("Bode Phase")  # Title of the phase plot
    plt.xlabel("Frequency [rad/s]")  # Label for x-axis
    plt.ylabel("Phase [deg]")  # Label for y-axis
    plt.grid(True, which="both")  # Add grid for logarithmic x-scale
    plt.legend()  # Add legend to distinguish time constants
    plt.show()  # Display the phase plot

# Entry point: Execute the script to generate Bode plots
if __name__ == "__main__":
    main()
