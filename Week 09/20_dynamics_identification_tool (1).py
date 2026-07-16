"""
Mini dynamics-identification tool.

Capabilities:
- Generate telemetry
- Estimate mass and drag
- Validate model
- Report RMSE
"""

import numpy as np
import matplotlib.pyplot as plt


def simulate(mass, drag, force, dt):
    velocity = np.zeros(len(force))
    for k in range(1,len(force)):
        acceleration=(force[k-1]-drag*velocity[k-1])/mass
        velocity[k]=velocity[k-1]+acceleration*dt
    return velocity


def estimate(force, measured_velocity, dt):
    acceleration=np.gradient(measured_velocity,dt)
    Phi=np.column_stack((force,measured_velocity))
    alpha,beta=np.linalg.lstsq(Phi,acceleration,rcond=None)[0]
    mass=1/alpha
    drag=-beta*mass
    return mass,drag


def main():
    rng=np.random.default_rng(20)
    dt=0.05
    t=np.arange(0,60,dt)

    true_mass=1250.0
    true_drag=85.0

    force_train=2200+1000*np.sin(0.2*t)+500*np.sin(0.8*t)
    velocity_train=simulate(true_mass,true_drag,force_train,dt)
    measured_train=velocity_train+rng.normal(0,0.05,len(t))

    mass_est,drag_est=estimate(force_train,measured_train,dt)

    force_val=1800+700*np.sin(0.15*t)+350*np.sin(1.1*t)
    truth_val=simulate(true_mass,true_drag,force_val,dt)
    model_val=simulate(mass_est,drag_est,force_val,dt)

    rmse=np.sqrt(np.mean((truth_val-model_val)**2))

    print(f"Estimated mass: {mass_est:.2f} kg")
    print(f"Estimated drag: {drag_est:.2f}")
    print(f"Validation RMSE: {rmse:.4f} m/s")

    plt.figure()
    plt.plot(t,truth_val,label="Validation truth")
    plt.plot(t,model_val,label="Identified model")
    plt.title("Dynamics Identification Tool")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
