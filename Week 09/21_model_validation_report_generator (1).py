"""
Generate a simple markdown model-validation report.

Learn:
- Engineering reporting
- Traceable metrics
"""

from pathlib import Path
import numpy as np


def main():
    rng=np.random.default_rng(21)
    truth=np.linspace(0,20,400)
    prediction=truth+rng.normal(0,0.35,400)

    error=prediction-truth
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


if __name__ == "__main__":
    main()
