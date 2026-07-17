# Project 20 — Dynamics Identification Tool
# Purpose:
# This capstone script generates telemetry, estimates vehicle mass and drag, validates the model on a different input profile, and reports model error.
#
# Key Concepts:
# - End-to-end identification
# - Training telemetry
# - Validation telemetry
# - Performance reporting
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np
# Import Matplotlib to visualize telemetry, model predictions, residuals, and trade studies.
import matplotlib.pyplot as plt


def simulate(mass, drag, force, dt):
    velocity = np.zeros(len(force))
    for k in range(1,len(force)):
        acceleration=(force[k-1]-drag*velocity[k-1])/mass
        velocity[k]=velocity[k-1]+acceleration*dt
    return velocity


def estimate(force, measured_velocity, dt):
# Estimate acceleration numerically from the measured velocity history.
    acceleration=np.gradient(measured_velocity,dt)
    Phi=np.column_stack((force,measured_velocity))
# Solve for the parameter values that minimize the total squared prediction error.
    alpha,beta=np.linalg.lstsq(Phi,acceleration,rcond=None)[0]
    mass=1/alpha
    drag=-beta*mass
    return mass,drag



# Main project workflow
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

# Compute root-mean-square error as a summary of model prediction accuracy.
    rmse=np.sqrt(np.mean((truth_val-model_val)**2))

    print(f"Estimated mass: {mass_est:.2f} kg")
    print(f"Estimated drag: {drag_est:.2f}")
    print(f"Validation RMSE: {rmse:.4f} m/s")


# Create a new figure for this result.
    plt.figure()
    plt.plot(t,truth_val,label="Validation truth")
    plt.plot(t,model_val,label="Identified model")
    plt.title("Dynamics Identification Tool")
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True)
    plt.legend()
# Display the completed visualization.
    plt.show()



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
