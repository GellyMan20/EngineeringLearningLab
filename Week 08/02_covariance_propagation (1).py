# Project 02 — Covariance Propagation
#
# Purpose:
# This project demonstrates the engineering concepts behind Covariance Propagation.
#
# Topics:
# - State estimation
# - Sensor fusion
# - Covariance analysis
#
# Learning Outcomes:
# - Understand the estimation concept.
# - Relate the mathematics to code.
# - Visualize estimator performance.

# Import numerical library
import numpy as np

# Import plotting library
import matplotlib.pyplot as plt


def main():
    """
    Main simulation entry point.

    This example intentionally keeps the implementation simple so the
    focus remains on understanding the algorithm structure.
    """

    # --------------------------------------------------
    # Simulation parameters
    # --------------------------------------------------
    dt = 0.1
    t = np.arange(0,20,dt)

    # --------------------------------------------------
    # Generate truth
    # --------------------------------------------------
    truth = np.sin(0.3*t)

    # --------------------------------------------------
    # Simulate noisy measurements
    # --------------------------------------------------
    rng = np.random.default_rng(42)
    measurement = truth + rng.normal(0,0.15,len(t))

    # --------------------------------------------------
    # Placeholder estimation algorithm
    # --------------------------------------------------
    # Replace this section with the full algorithm while
    # preserving the surrounding educational comments.
    estimate = np.convolve(measurement,np.ones(5)/5,mode="same")

    # --------------------------------------------------
    # Visualize results
    # --------------------------------------------------
    plt.figure()
    plt.plot(t,truth,label="Truth")
    plt.plot(t,measurement,label="Measurement",alpha=0.5)
    plt.plot(t,estimate,label="Estimate")
    plt.title("Covariance Propagation")
    plt.xlabel("Time [s]")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
