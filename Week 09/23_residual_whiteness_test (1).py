"""
Simple residual-whiteness test using autocorrelation bounds.

Learn:
- White residual expectation
- Model validation
"""

import numpy as np
import matplotlib.pyplot as plt


def acf(x,max_lag):
    x=x-np.mean(x)
    denom=np.dot(x,x)
    return np.array([
        np.dot(x[:len(x)-lag],x[lag:])/denom
        for lag in range(max_lag+1)
    ])


def main():
    rng=np.random.default_rng(23)
    residual=rng.normal(0,1,1000)
    residual[1:]+=0.25*residual[:-1]  # add correlation

    values=acf(residual,40)
    bound=1.96/np.sqrt(len(residual))

    print(f"Approximate 95% autocorrelation bound: ±{bound:.4f}")
    print("Out-of-bound lags:",np.where(np.abs(values[1:])>bound)[0]+1)

    plt.figure()
    plt.stem(np.arange(len(values)),values)
    plt.axhline(bound,linestyle="--")
    plt.axhline(-bound,linestyle="--")
    plt.title("Residual Whiteness Test")
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
