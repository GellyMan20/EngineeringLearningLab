# Week 10 Primer — Advanced Control

## 1. Purpose of this week

Week 10 moves from classical single-loop thinking into modern state-space control. The goal is not to declare PID obsolete. The goal is to understand when a multivariable model, full-state feedback, optimal-control formulation, estimator, or robustness study provides a better engineering solution.

By the end of the week, you should be able to represent a dynamic system in state-space form, assess whether it can be controlled and observed, design pole-placement and LQR controllers, add integral action and reference tracking, account for sampled implementation, combine LQR with a state estimator, and compare controllers across uncertainty, noise, disturbances, and actuator limits.

The central engineering habit is this: **a controller is not good because one nominal plot looks good.** A controller is good when it meets requirements across the relevant operating envelope with acceptable effort, robustness, implementation complexity, and verification burden.

---

## 2. From transfer functions to state space

A transfer function describes the input-to-output relationship of a linear time-invariant system. State space describes the internal dynamic variables as well:

\[
\dot{x}=Ax+Bu
\]

\[
y=Cx+Du
\]

The state vector may contain position and velocity, attitude and angular rate, flexible-mode amplitudes, actuator states, thermal states, or any other variables needed to predict future behavior. The matrix meanings are:

- **A**: internal state dynamics and coupling.
- **B**: how control inputs influence state derivatives.
- **C**: how states map to measured or controlled outputs.
- **D**: direct input-to-output feedthrough.

State-space models are valuable because they naturally support multiple inputs, multiple outputs, coupled dynamics, state estimation, and modern control design.

### Engineering interpretation

For a longitudinal aircraft model, the state vector might include forward-speed perturbation, angle of attack, pitch rate, and pitch attitude. Elevator deflection enters through B. Sensors provide only some combinations of the states through C. A flight-control law then commands elevator based on measured or estimated states.

### Modeling caution

A state-space model is usually local. Linearization around one trim point does not guarantee accuracy at another airspeed, altitude, configuration, or angle of attack. That limitation motivates gain scheduling and operating-region validation.

---

## 3. Stability and closed-loop eigenvalues

For the autonomous system

\[
\dot{x}=Ax,
\]

the eigenvalues of A determine the natural modes. Continuous-time stability requires every eigenvalue to have a negative real part. State feedback uses

\[
u=-Kx
\]

so the closed-loop dynamics become

\[
\dot{x}=(A-BK)x.
\]

The eigenvalues of \(A-BK\) are the closed-loop poles. Moving them farther left generally speeds the response, but aggressive poles increase actuator demand, noise sensitivity, and sensitivity to unmodeled high-frequency dynamics.

A stable simulation is not enough. Check damping, settling time, overshoot, control effort, saturation, and robustness.

---

## 4. Controllability

A system is controllable when the available inputs can move the state from any initial condition to any desired final condition in finite time. For an n-state single-input system, construct

\[
\mathcal{C}=[B\;AB\;A^2B\;\dots\;A^{n-1}B].
\]

The system is controllable when

\[
\operatorname{rank}(\mathcal{C})=n.
\]

### Physical meaning

A mathematical state may exist in the model but be unreachable with the selected actuator. For example, a control surface might have weak authority over a flexible mode, or a reaction wheel might not provide torque around a failed axis. No gain-selection method can fix a fundamentally uncontrollable architecture.

### Numerical caution

Binary rank tests can hide weak controllability. A matrix may technically have full rank but be ill-conditioned, meaning extreme control effort is required. Singular values and controllability Gramians provide richer information.

---

## 5. Observability

A system is observable when the initial state can be reconstructed from known inputs and measured outputs. Construct

\[
\mathcal{O}=\begin{bmatrix}C\\CA\\CA^2\\\vdots\\CA^{n-1}\end{bmatrix}.
\]

The system is observable when

\[
\operatorname{rank}(\mathcal{O})=n.
\]

### Physical meaning

The controller may require velocity, angular rate, bias, or disturbance states that are not directly measured. Observability tells you whether those states can be inferred from sensor histories and the model. Poor sensor geometry, missing excitation, or redundant measurements can make important states weakly observable.

Controllability and observability should be checked before detailed controller or estimator tuning.

---

## 6. Pole placement

Pole placement selects K so that \(A-BK\) has chosen eigenvalues. This gives direct control over nominal linear modes.

A useful second-order relationship is

\[
s^2+2\zeta\omega_n s+\omega_n^2=0,
\]

where \(\zeta\) is damping ratio and \(\omega_n\) is natural frequency. Desired overshoot and settling-time requirements can be translated into approximate pole locations.

### Strengths

- Direct and intuitive modal design.
- Useful for small systems.
- Good educational bridge from classical poles to state feedback.

### Limitations

- Does not directly optimize control effort.
- Many pole sets can satisfy the same rough response target.
- Aggressive placement can demand impossible actuator commands.
- Sensitivity and robustness are not automatically addressed.

---

## 7. Linear Quadratic Regulator

LQR chooses the state-feedback law that minimizes

\[
J=\int_0^\infty (x^TQx+u^TRu)\,dt.
\]

The matrix Q penalizes state deviation. R penalizes control effort. The continuous algebraic Riccati equation is

\[
A^TP+PA-PBR^{-1}B^TP+Q=0.
\]

The optimal gain is

\[
K=R^{-1}B^TP.
\]

### What “optimal” means

LQR is optimal only for the selected linear model and cost function. It does not mean globally best, inherently robust, or automatically compliant with physical constraints. The engineer defines what matters through Q and R.

### Tuning intuition

- Increase a Q diagonal term to regulate that state more strongly.
- Increase R to reduce control activity.
- Normalize states and inputs so numerical magnitudes reflect meaningful engineering limits.
- Bryson’s rule provides a practical initial guess: assign each diagonal weight approximately as the inverse square of the maximum acceptable value.

### Common mistake

Using arbitrary Q and R values until the plot looks attractive can produce a controller with hidden saturation, poor noise behavior, or inadequate robustness. Tie weights to requirements and physical limits whenever possible.

---

## 8. Regulation versus tracking

Basic LQR is a regulator: it drives the state toward zero. Tracking a nonzero command requires additional structure.

### Reference prefilter

A prefilter or feedforward term can correct steady-state gain:

\[
u=-Kx+N_{bar}r.
\]

This works well when the model is accurate and disturbances are limited.

### Integral augmentation

Introduce an integrated tracking-error state:

\[
\dot{z}=r-y.
\]

Then design LQR on the augmented state \([x^T\;z]^T\). Integral action removes constant steady-state error caused by constant disturbances or model mismatch.

### Caution

Integral action can drive commands into saturation. In real implementations, add anti-windup logic, command limits, and mode-management protections.

---

## 9. Continuous versus discrete control

Flight software runs at a fixed sample rate. The implemented model is

\[
x_{k+1}=A_dx_k+B_du_k.
\]

Discrete LQR uses the discrete algebraic Riccati equation. A controller designed in continuous time and simply evaluated slowly may behave differently from its design assumptions.

Important implementation issues include:

- Sample rate relative to plant bandwidth.
- Computation delay.
- Sensor timestamp alignment.
- Zero-order hold behavior.
- Numerical precision.
- Missed deadlines and jitter.

As a rough starting point, control update frequency should be comfortably faster than the closed-loop bandwidth, but the correct margin depends on phase, delay, and implementation details.

---

## 10. PID versus LQR

PID acts on an error signal and is often easy to understand, tune, verify, and implement. LQR uses a model and state vector to coordinate multiple dynamic variables.

### PID advantages

- Simple architecture.
- Low computational burden.
- Familiar certification and troubleshooting path.
- Effective for decoupled single-loop systems.

### LQR advantages

- Natural multivariable control.
- Explicit state-versus-effort tradeoff.
- Systematic use of coupled dynamics.
- Scales well when state estimates are already available.

### Fair comparison

Use the same plant, command, disturbances, actuator limits, noise assumptions, and performance metrics. Compare tracking, settling, overshoot, integrated error, control effort, saturation time, robustness, and implementation complexity.

There is no universal winner. Cascaded PID, scheduled classical control, LQR, and hybrid architectures can all be correct choices.

---

## 11. Model uncertainty and robustness

The controller is designed using a nominal model, but the real plant differs. Sources include:

- Mass and inertia dispersion.
- Aerodynamic coefficient uncertainty.
- Center-of-gravity travel.
- Actuator dynamics and delay.
- Flexible modes.
- Environmental disturbances.
- Sensor errors.
- Linearization error.

A robustness study should vary uncertain parameters over justified ranges and evaluate both average and worst-case behavior. One-at-a-time sweeps are useful for intuition; Monte Carlo studies capture combined effects.

### Monte Carlo workflow

1. Define uncertain parameters and distributions.
2. Sample a plant instance.
3. Simulate the controller against the instance.
4. Calculate standard metrics.
5. Record failures and margins.
6. Analyze distributions and worst cases.
7. Investigate the failure region instead of reporting only pass rate.

Monte Carlo results are only credible when distributions and correlations are defensible.

---

## 12. Gain scheduling

A single linear controller may not cover a nonlinear flight envelope. Gain scheduling uses

\[
K=K(\rho),
\]

where \(\rho\) is a measurable scheduling variable such as airspeed, altitude, Mach number, dynamic pressure, mass, or configuration.

Design controllers at representative operating points, then switch or interpolate between gains.

Key hazards include:

- Discontinuous commands during switching.
- Scheduling on a noisy or delayed variable.
- Instability between design points.
- Rapid parameter variation invalidating frozen-time assumptions.
- Incorrect mode or configuration logic.

Validate the entire scheduled system, including transition behavior—not only each fixed operating point.

---

## 13. Actuator saturation

The commanded input is not the applied input when physical limits are reached:

\[
u_{applied}=\operatorname{clip}(u_{commanded},u_{min},u_{max}).
\]

Actuator constraints may include position, rate, acceleration, force, torque, voltage, current, thermal, propellant, or momentum limits.

Saturation invalidates the linear closed-loop model. It can cause slow recovery, large tracking error, limit cycles, or loss of stability. Always plot both commanded and applied input and record saturation duration.

LQR does not inherently enforce hard constraints. Model Predictive Control is attractive partly because constraints can be included directly, though at greater computational and verification cost.

---

## 14. Noise sensitivity

Measurements contain noise. Derivative action can amplify high-frequency noise, while aggressive state feedback can convert noisy estimates into control chatter.

Assess:

- RMS command activity.
- High-frequency content.
- Actuator rate usage.
- Structural excitation.
- Tracking degradation.
- Filter phase delay.

Do not solve noise problems by adding heavy filtering without checking the lost phase margin and slower response.

---

## 15. LQG: estimation plus control

LQR assumes the state is known. A Kalman filter estimates it:

\[
\dot{\hat{x}}=A\hat{x}+Bu+L(y-C\hat{x}).
\]

The controller uses

\[
u=-K\hat{x}.
\]

For the ideal linear-Gaussian problem, estimator and controller can be designed separately through the separation principle. The combination is called LQG.

### Practical caution

LQG nominal stability does not guarantee strong robustness margins. Model uncertainty, estimator tuning, sensor failure, delays, and unmodeled dynamics must still be evaluated. Estimator transients and covariance consistency should be included in control testing.

---

## 16. Performance metrics

Useful time-domain metrics include:

- **Rise time:** how quickly the response reaches the command neighborhood.
- **Settling time:** when it enters and remains within a specified error band.
- **Overshoot:** maximum excursion beyond the target.
- **Steady-state error:** final command offset.
- **IAE:** \(\int |e(t)|dt\).
- **ISE:** \(\int e(t)^2dt\).
- **Control energy:** \(\int u(t)^2dt\).
- **Peak command:** maximum absolute actuator demand.
- **Saturation duration:** total time at a limit.
- **Robust success rate:** percentage of dispersed cases meeting all criteria.

Metrics must use consistent definitions. A settling-time algorithm should verify that the response remains inside the band, not merely enters it once.

---

## 17. Trade studies and scorecards

Controllers should be evaluated using a scenario matrix:

| Dimension | Example cases |
|---|---|
| Commands | small step, large step, ramp, trajectory |
| Disturbances | impulse, step load, gust, torque |
| Plant | nominal, light/heavy, low/high damping |
| Sensors | nominal noise, degraded noise, bias |
| Actuators | nominal, saturated, rate limited, delayed |
| Implementation | nominal sample rate, delay, jitter |

Normalize metrics before weighted scoring so unlike units do not dominate. Keep the raw metrics visible; a single composite score can hide unacceptable failure in one critical requirement.

A recommendation should state:

1. Mission priorities.
2. Compared alternatives.
3. Models and assumptions.
4. Metrics and acceptance criteria.
5. Nominal and off-nominal evidence.
6. Key risks and unresolved questions.
7. Recommended controller and rationale.

---

## 18. Pareto fronts

When objectives conflict, there may be no single best controller. A design is Pareto-dominated when another design is at least as good in every objective and strictly better in one. The remaining non-dominated designs form the Pareto front.

Typical conflicts include:

- Faster tracking versus larger control effort.
- Better disturbance rejection versus more noise amplification.
- Higher robustness versus slower nominal response.
- Better performance versus greater implementation complexity.

The Pareto front gives decision-makers honest tradeoffs instead of hiding value judgments inside one score.

---

## 19. Verification mindset

For every controller, ask:

- What assumptions make the design valid?
- Which states are measured and which are estimated?
- Is the model controllable and observable throughout the envelope?
- What are the actuator position and rate limits?
- What delays and sample rates exist?
- Which uncertainties dominate performance?
- What happens after sensor loss or estimator divergence?
- Are transitions between modes and gains safe?
- Which metrics trace directly to requirements?
- What evidence is needed before hardware or flight test?

A professional controller package includes the model, tuning rationale, implementation details, verification cases, results, limits, and open risks.

---

## 20. Recommended activity sequence

1. **State-space basics:** identify every state and matrix entry physically.
2. **Controllability and observability:** test architecture feasibility before tuning.
3. **Pole placement:** connect pole locations to response characteristics.
4. **LQR from scratch:** understand Q, R, P, and K.
5. **Weight tuning:** create a tracking-effort trade table.
6. **PID versus LQR:** compare with common conditions and metrics.
7. **Disturbance rejection:** inject matched disturbances.
8. **Integral LQR:** eliminate constant offset and inspect saturation.
9. **Discrete LQR:** vary sample time and identify degradation.
10. **Tracking prefilter:** compare feedforward with integral action.
11. **Model uncertainty:** sweep physical parameters.
12. **Monte Carlo:** quantify distributions and failures.
13. **Gain scheduling:** test operating-point transitions.
14. **Saturation:** separate commanded and applied control.
15. **Noise sensitivity:** quantify command chatter.
16. **LQG:** compare true and estimated states.
17–24. **Trade studies:** convert simulations into a defensible recommendation.

---

## 21. Capstone standard

The Week 10 capstone is a PID-versus-LQR controller recommendation. A strong submission includes:

- Plant definition and assumptions.
- Requirements and mission priorities.
- PID and LQR design rationale.
- Nominal command tracking.
- Disturbance rejection.
- Sensor-noise sensitivity.
- Actuator saturation and rate effects.
- Plant uncertainty and Monte Carlo results.
- Consistent performance metrics.
- Pareto or scorecard analysis.
- Final recommendation, risks, and next tests.

The best result is not the most complicated controller. It is the simplest architecture that credibly satisfies the mission requirements with acceptable margin and verification burden.
