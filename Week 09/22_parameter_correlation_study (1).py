"""
Study parameter correlation and conditioning.

Learn:
- Collinearity
- Poor identifiability
- Condition number
"""

import numpy as np


def main():
    rng=np.random.default_rng(22)
    n=1000

    x1=rng.normal(0,1,n)
    x2=0.98*x1+rng.normal(0,0.05,n)
    X=np.column_stack((x1,x2))
    theta_true=np.array([2.0,-1.0])
    y=X@theta_true+rng.normal(0,0.2,n)

    theta=np.linalg.lstsq(X,y,rcond=None)[0]
    condition=np.linalg.cond(X)

    print("Estimated parameters:",theta)
    print(f"Design-matrix condition number: {condition:.2f}")
    print("Large condition numbers indicate weak parameter separability.")


if __name__ == "__main__":
    main()
