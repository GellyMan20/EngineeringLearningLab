# Project 21 — Model Validation Report Generator
# Purpose:
# This script calculates standard model-error metrics and writes a concise markdown validation report.
#
# Key Concepts:
# - RMSE
# - MAE
# - Maximum error
# - Engineering reporting
#
# Learning Outcomes:
# - Understand the identification problem and its engineering value.
# - Follow how telemetry is converted into a mathematical model.
# - Interpret estimation and validation results.
# - Recognize assumptions, limitations, and possible extensions.

# Import Path for writing generated engineering reports.
from pathlib import Path
# Import NumPy for arrays, matrix operations, random sampling, and numerical calculations.
import numpy as np



# Main project workflow
def main():
    rng=np.random.default_rng(21)
    truth=np.linspace(0,20,400)
    prediction=truth+rng.normal(0,0.35,400)

    error=prediction-truth
# Compute root-mean-square error as a summary of model prediction accuracy.
    rmse=np.sqrt(np.mean(error**2))
    mae=np.mean(np.abs(error))
    max_error=np.max(np.abs(error))
    bias=np.mean(error)

    report=f"""# Model Validation Report

## Summary

The identified model was evaluated against an independent validation dataset.

## Metrics

- RMSE: {rmse:.4f}
- MAE: {mae:.4f}
- Maximum absolute error: {max_error:.4f}
- Mean error (bias): {bias:.4f}

## Interpretation

The model should be considered acceptable only if these values satisfy the project's predefined performance thresholds.

## Recommended Follow-Up

- Inspect residual autocorrelation.
- Validate on additional operating conditions.
- Perform parameter sensitivity analysis.
- Check whether nonlinear terms improve accuracy.
"""

    path=Path("generated_model_validation_report.md")
    path.write_text(report,encoding="utf-8")
    print(f"Wrote {path.resolve()}")



# Entry point: run the project when this file is executed directly.
if __name__ == "__main__":
    main()
