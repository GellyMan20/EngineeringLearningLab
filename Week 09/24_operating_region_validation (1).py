"""
Validate an identified model across multiple operating regions.

Learn:
- Local vs global model validity
- Extrapolation risk
"""

import numpy as np


def simulate_nonlinear(force,dt):
    mass=1000.0
    c1=40.0
    c2=2.5
    v=np.zeros(len(force))
    for k in range(1,len(force)):
        drag=c1*v[k-1]+c2*v[k-1]*abs(v[k-1])
        v[k]=v[k-1]+((force[k-1]-drag)/mass)*dt
    return v


def fit_linear(force,v,dt):
    a=np.gradient(v,dt)
    Phi=np.column_stack((force,v))
    alpha,beta=np.linalg.lstsq(Phi,a,rcond=None)[0]
    mass=1/alpha
    drag=-beta*mass
    return mass,drag


def simulate_linear(force,dt,mass,drag):
    v=np.zeros(len(force))
    for k in range(1,len(force)):
        v[k]=v[k-1]+((force[k-1]-drag*v[k-1])/mass)*dt
    return v


def main():
    dt=0.05
    t=np.arange(0,50,dt)

    force_train=1200+400*np.sin(0.2*t)
    v_train=simulate_nonlinear(force_train,dt)
    mass,drag=fit_linear(force_train,v_train,dt)

    regions={
        "low":800+250*np.sin(0.2*t),
        "medium":1600+500*np.sin(0.2*t),
        "high":3000+900*np.sin(0.2*t),
    }

    print(f"Identified linear model: mass={mass:.2f}, drag={drag:.2f}")
    for name,force in regions.items():
        truth=simulate_nonlinear(force,dt)
        pred=simulate_linear(force,dt,mass,drag)
        rmse=np.sqrt(np.mean((truth-pred)**2))
        print(f"{name:>6} region RMSE: {rmse:.4f}")


if __name__ == "__main__":
    main()
