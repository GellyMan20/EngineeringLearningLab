# Week 9 — System Identification

This package contains standalone Python projects for learning how to build mathematical models from telemetry.

## Install

```bash
pip install numpy matplotlib scipy
```

For the neural-network projects:

```bash
pip install scikit-learn
```

## Recommended sequence

### Foundations

1. `01_parameter_estimation_linear_drag.py`
2. `02_mass_and_drag_estimation.py`
3. `03_first_order_transfer_function_fit.py`
4. `04_second_order_step_response_fit.py`
5. `05_least_squares_state_space_identification.py`
6. `06_arx_model_identification.py`

### Validation and analysis

7. `07_residual_analysis.py`
8. `08_input_excitation_comparison.py`
9. `09_parameter_sensitivity_study.py`
10. `10_train_validation_split.py`
11. `11_frequency_response_identification.py`
12. `12_nonlinear_parameter_estimation_scipy.py`
13. `13_recursive_least_squares.py`
14. `14_model_order_comparison.py`
15. `15_bootstrap_parameter_uncertainty.py`
16. `16_cross_validation_identification.py`

### Extended and capstone projects

17. `17_neural_network_system_identification.py`
18. `18_linear_vs_neural_model.py`
19. `19_anomaly_detection_from_residuals.py`
20. `20_dynamics_identification_tool.py`
21. `21_model_validation_report_generator.py`
22. `22_parameter_correlation_study.py`
23. `23_residual_whiteness_test.py`
24. `24_operating_region_validation.py`

## Week 9 outcomes

By the end of this package, you should be able to:

- Estimate physical parameters from telemetry.
- Fit first-order and second-order transfer functions.
- Identify discrete state-space and ARX models.
- Evaluate residuals and check whether they are approximately white.
- Understand persistent excitation and identifiability.
- Compare model orders and validation performance.
- Quantify parameter uncertainty.
- Fit nonlinear models with SciPy.
- Track changing parameters online with recursive least squares.
- Compare physics-based and neural-network models.
- Detect anomalies from model residuals.
- Produce a model-validation report.

## Main capstone

The main capstone is:

```text
20_dynamics_identification_tool.py
```

It generates training telemetry, estimates vehicle mass and drag, validates the identified model on a different input profile, and reports validation RMSE.
