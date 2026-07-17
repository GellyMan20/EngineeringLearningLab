# ==========================================================================
# Project 02 — Controllability and Observability
# ==========================================================================
#
# Purpose:
# Determine whether available actuators can influence every state and whether available sensors contain enough information to reconstruct every state.
#
# Why This Matters:
# These tests are early design gates for flight-control actuator placement and navigation-sensor selection.
#
# Key Concepts:
# - Controllability matrix
# - Observability matrix
# - Matrix rank
# - Architecture feasibility
#
# Mathematical Foundation:
# - C = [B, AB, ..., A^(n-1)B]
# - O = [C; CA; ...; CA^(n-1)]
#
# Learning Objectives:
# - Explain the controller or analysis method in engineering terms.
# - Connect the governing equations to their implementation in Python.
# - Interpret the plots and calculated performance metrics.
# - Identify assumptions, implementation limits, and useful extensions.
#
# Suggested Experiments:
# - Change the plant parameters and observe the effect on stability and response.
# - Change controller gains or LQR weights and compare tracking versus effort.
# - Add disturbances, sensor noise, or actuator limits where appropriate.
# - Replace Euler integration with a higher-order numerical method.
# ==========================================================================
# Import NumPy for vectors, matrices, numerical integration, and performance calculations.
import numpy as np



# Execute this portion of the controller design or analysis workflow.
def controllability_matrix(A, B):
    """Execute this portion of the controller design or analysis workflow."""
    blocks = [B]
    current = B.copy()
    # Step through the simulation or design cases one sample at a time.
    for _ in range(1, A.shape[0]):
        current = A @ current
        blocks.append(current)
    return np.hstack(blocks)



# Execute this portion of the controller design or analysis workflow.
def observability_matrix(A, C):
    """Execute this portion of the controller design or analysis workflow."""
    blocks = [C]
    current = C.copy()
    # Step through the simulation or design cases one sample at a time.
    for _ in range(1, A.shape[0]):
        current = current @ A
        blocks.append(current)
    return np.vstack(blocks)



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""

    # Define the state matrix A. It describes how the uncontrolled states evolve and interact.
    A = np.array([[0.0, 1.0], [-2.0, -0.7]])
    # Define the input matrix B. It maps the commanded control input into the state derivatives.
    B = np.array([[0.0], [1.0]])
    # Define the output matrix C. It selects or combines states to form the measured output.
    C = np.array([[1.0, 0.0]])

    ctrb = controllability_matrix(A, B)
    obsv = observability_matrix(A, C)

    print("Controllability matrix:")
    print(ctrb)
    print("Controllability rank:", np.linalg.matrix_rank(ctrb))

    print("\nObservability matrix:")
    print(obsv)
    print("Observability rank:", np.linalg.matrix_rank(obsv))



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
