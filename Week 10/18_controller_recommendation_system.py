# ==========================================================================
# Project 18 — Controller Recommendation System
# ==========================================================================
#
# Purpose:
# Translate mission priorities and measured controller performance into a repeatable controller recommendation.
#
# Why This Matters:
# Formal decision logic makes design rationale reviewable and reduces reliance on subjective preference.
#
# Key Concepts:
# - Decision logic
# - Mission priorities
# - Weighted scoring
# - Engineering recommendation
#
# Mathematical Foundation:
# - score = sum(weight_i * normalized_metric_i)
#
# Learning Objectives:
# - Explain the controller or analysis method in engineering terms.
# - Connect the governing equations to their implementation in Python.
# - Interpret the plots and calculated performance metrics.
# - Identify assumptions, implementation limits, and useful extensions.
#
# Suggested Experiments:
# - Change the plant parameters and observe the effect on stability and response.
# - Change controller gains or LQR weights and compare tracking versus effort.
# - Add disturbances, sensor noise, or actuator limits where appropriate.
# - Replace Euler integration with a higher-order numerical method.
# ==========================================================================
# Execute this portion of the controller design or analysis workflow.
def recommend(
    full_state_available,
    strong_model_available,
    actuator_limited,
    high_disturbance_bias,
    tuning_budget_low,
):
    if tuning_budget_low and not full_state_available:
        return "PID"

    if full_state_available and strong_model_available:
        if high_disturbance_bias:
            return "LQR with integral action"
        if actuator_limited:
            return "Conservative LQR or constrained MPC"
        return "LQR"

    if not full_state_available and strong_model_available:
        return "LQG"

    return "PID with gain scheduling"



# Configure the example, run the simulation or trade study, and present the results.
def main():
    """Configure the example, run the simulation or trade study, and present the results."""
    scenarios = [
        {
            "name": "Simple industrial loop",
            "full_state_available": False,
            "strong_model_available": False,
            "actuator_limited": False,
            "high_disturbance_bias": True,
            "tuning_budget_low": True,
        },
        {
            "name": "Autonomous aircraft inner loop",
            "full_state_available": True,
            "strong_model_available": True,
            "actuator_limited": False,
            "high_disturbance_bias": False,
            "tuning_budget_low": False,
        },
        {
            "name": "Noisy navigation-based control",
            "full_state_available": False,
            "strong_model_available": True,
            "actuator_limited": False,
            "high_disturbance_bias": False,
            "tuning_budget_low": False,
        },
    ]

    # Step through the simulation or design cases one sample at a time.
    for scenario in scenarios:
        name = scenario.pop("name")
        print(f"{name}: {recommend(**scenario)}")



# Entry point: run the project only when this file is executed directly.
if __name__ == "__main__":
    main()
