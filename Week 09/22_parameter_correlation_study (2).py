# Project 22 — Parameter Correlation Study
# Purpose:
# This script demonstrates how correlated regressors make parameters difficult to distinguish and uses condition number as a warning metric.
#
# Key Concepts:
# - Parameter correlation
# - Collinearity
# - Condition number
# - Weak identifiability
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np



# Main project workflow
def main():
    rng=np.random.default_rng(22)
    n=1000

    x1=rng.normal(0,1,n)
    x2=0.98*x1+rng.normal(0,0.05,n)
    X=np.column_stack((x1,x2))
    theta_true=np.array([2.0,-1.0])
    y=X@theta_true+rng.normal(0,0.2,n)

# Solve for the parameter values that minimize the total squared prediction error.
    theta=np.linalg.lstsq(X,y,rcond=None)[0]
# Calculate the condition number to assess numerical sensitivity and parameter separability.
    condition=np.linalg.cond(X)

    print("Estimated parameters:",theta)
    print(f"Design-matrix condition number: {condition:.2f}")
    print("Large condition numbers indicate weak parameter separability.")



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
