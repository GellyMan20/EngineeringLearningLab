# README: Understanding Kalman Filters, Unscented Kalman Filters, and Particle Filters through Python Scripts

This document provides an overview of the core concepts, mathematical foundations, and implementation details behind the provided Python scripts simulating Kalman Filters (KF), Unscented Kalman Filters (UKF), and Particle Filters in various scenarios such as position estimation, fault detection, anomaly detection, and Monte Carlo simulations.

---

## **Overview of Concepts**

### **Kalman Filter (KF)**
The Kalman Filter is a recursive algorithm used for **state estimation** of a system when measurements are noisy or uncertain. It predicts the next state of a system (e.g., position and velocity) and updates the prediction based on observed measurements. It is widely used in control systems, robotics, satellite navigation, and sensor fusion.

#### **Core Process**
1. **Prediction**:
    - Predict the next state (\(x_k\)) using the system's dynamics and update the covariance matrix (\(P_k\)) to reflect the uncertainty.
    - **State transition**:  
      \[
      x_{k|k-1} = F \cdot x_{k-1|k-1} + B \cdot u_k
      \]
    - **Covariance prediction**:  
      \[
      P_{k|k-1} = F \cdot P_{k-1|k-1} \cdot F^T + Q
      \]

2. **Update**:
    - Incorporate the new measurement into the estimate, adjusting the state and reducing uncertainty.
    - **Innovation (residual)**:  
      \[
      y_k = z_k - H \cdot x_{k|k-1}
      \]
    - **Kalman Gain (weight given to the measurement)**:  
      \[
      K_k = P_{k|k-1} \cdot H^T \cdot (H \cdot P_{k|k-1} \cdot H^T + R)^{-1}
      \]
    - **Updated state and covariance**:  
      \[
      x_{k|k} = x_{k|k-1} + K_k \cdot y_k
      \]  
      \[
      P_{k|k} = (I - K_k \cdot H) \cdot P_{k|k-1}
      \]

---

### **Unscented Kalman Filter (UKF)**
The Unscented Kalman Filter extends the Kalman Filter to **nonlinear systems**, where the dynamics and measurements are represented by nonlinear functions. Instead of linearizing the system (as in EKF), the UKF uses a deterministic sampling technique with **sigma points** to approximate the distributions.

#### **Key Concepts**:
1. **Sigma Points**: Selects a minimal set of points representing the system's uncertainty and propagates these points through the nonlinear equations.
2. **Transformation**: The sigma points are passed through the nonlinear process and measurement models to compute the predicted state and covariance.

#### **Mathematics**:
1. **Sigma point selection**:  
   \[
   \sigma_i = x_k \pm \sqrt{(n + \lambda)P_k} \quad \text{for \(i \in \{1, \dots, n\}\)},
   \]  
   where \(P_k\) is the covariance matrix, and \(n\) is the state dimension.

2. **Compute predictive mean and covariance**:  
   \[
   x_{pred} = \sum_i w_m^i \cdot \sigma_i
   \]  
   \[
   P_{pred} = \sum_i w_c^i \cdot (\sigma_i - x_{pred}) \cdot (\sigma_i - x_{pred})^T + Q
   \]

3. **Map sigma points to measurement space**:  
   \[
   z_{pred} = \sum_j w_m^j \cdot h(\sigma_j)
   \]

---

### **Particle Filter**
The Particle Filter is a non-parametric approach that approximates a probability distribution by representing it with weighted samples (particles). It is often used for **nonlinear, non-Gaussian systems**.

#### **Key Concepts**:
1. Particles represent possible states of the system.
2. Each particle has a weight, updated based on how consistent its prediction is with the observations.
3. Resampling maintains particle diversity when weights become unevenly distributed.

#### **Mathematics**:
1. **Initialize `n` particles**:  
   \[
   \{x_i\}_{i=1}^n \quad \text{(with equal weights)}
   \]

2. **Predict particle states** based on the motion model:  
   \[
   x_i' = f(x_i) + \text{process noise}
   \]

3. **Update particle weights** based on observation \(z\):  
   \[
   w_i \propto p(z | x_i')
   \]

4. Normalize the weights:  
   \[
   w_i \rightarrow \frac{w_i}{\sum_j w_j}
   \]

5. **Resample particles** based on the weights:
   Resample when the **effective particle size** falls below a predefined threshold.

---

## **Relationship between Concepts**

- **Kalman Filter**: Assumes linear dynamics and Gaussian noise for predictable environments.
- **UKF**: Handles **nonlinear systems** using sigma points, which avoids linearization errors found in the EKF.
- **Particle Filter**: Handles severe nonlinearities and **non-Gaussian distributions** but is computationally heavy, making it less efficient for some use cases.

---

## **Implementation Overview**

These scripts demonstrate various Kalman Filter variants applied to real-world scenarios:

1. **Basic Kalman Filter**:
    - Estimates 1D position and velocity with noisy measurements.
    - Commonly used for tracking applications.

2. **Unscented Kalman Filter (UKF)**:
    - Solves nonlinear systems with sigma points.
    - More accurate for systems with nonlinear process or measurement models.

3. **Particle Filter**:
    - Handles extreme non-Gaussian or highly nonlinear problems using weighted particles and resampling.

4. **Fault Detection and Anomaly Detection**:
    - Identifies anomalies caused by step changes or outliers using residual thresholds.

5. **Monte Carlo Simulation**:
    - Evaluates robustness by running repeated trials of randomized noise and sensor characteristics.

6. **Adaptive Kalman Filter**:
    - Adjusts the measurement noise covariance in real-time to handle dynamic noise conditions.

---

## **Running the Scripts**

1. Ensure you have Python 3.x installed along with `numpy` and `matplotlib` libraries.
2. Save the scripts and run them with:
   ```bash
   python your_script_name.py
