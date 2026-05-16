# Satellite Collision Avoidance Recommendation System

## Project overview

This project builds a decision-support recommendation system for satellite conjunction events. It uses event-level satellite conjunction data to recommend one of four possible operational actions:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

The goal is not only to estimate collision risk, but to translate risk indicators into an operational recommendation that can support collision-avoidance decision making.

## Dataset

The main dataset is:

```text
dataset/data/kelvins_competition_data/train_data.csv
```

The original dataset contains multiple temporal observations for each `event_id`. The project creates an event-level dataset by keeping, for each `event_id`, the row with the smallest non-negative `time_to_tca`. This selected row represents the closest available observation before the time of closest approach.

## Pipeline

The main pipeline performs these steps:

- Load original dataset
- Create event-level dataset
- Add probability features
- Add operational risk features
- Add normalized velocity feature
- Add normalized risk feature
- Add synthetic decision features
- Compute `risk_score`
- Compute action scores
- Select `recommended_action`
- Save full dataset
- Save clean recommendations file
- Generate summary and validation reports
- Train and evaluate the ML risk-prediction model

## Engineered features

- `collision_probability`: derived from log-scale `risk` as `10 ** risk`.
- `max_collision_probability`: derived from log-scale `max_risk_estimate` as `10 ** max_risk_estimate`.
- `distance_risk`: inverted normalized `miss_distance`; closer approaches receive higher scores.
- `urgency`: inverted normalized `time_to_tca`; events closer to TCA receive higher scores.
- `relative_speed_norm`: normalized `relative_speed` in the range `[0, 1]`.
- `risk_norm`: normalized log-scale `risk`; values closer to zero indicate higher collision risk.
- `fuel_cost`: synthetic operational cost feature based on normalized velocity and urgency.
- `mission_priority`: synthetic mission-priority feature derived deterministically from `mission_id`.
- `risk_score`: overall conjunction severity score based on normalized risk, distance, urgency, velocity, and mission priority.

`fuel_cost` and `mission_priority` are synthetic decision-support features because the original dataset does not contain real fuel cost or mission priority values.

## Recommendation logic

The system computes four action scores:

- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`

It then selects `recommended_action` as the action with the highest score.

If two or more actions have exactly the same highest score, ties are resolved by selecting the least aggressive action in this order:

```text
no_action -> monitor -> small_maneuver -> major_maneuver
```

## Machine Learning risk prediction

The project also includes an ML regression module in `src/modeling.py`. This module predicts `max_risk_estimate` from physical and orbital conjunction-event features. It does not predict the final recommended action directly; final actions are still produced by the explainable rule-based recommendation layer.

Input features used by the ML model are:

- `time_to_tca`
- `miss_distance`
- `relative_speed`
- `relative_position_r`
- `relative_position_t`
- `relative_position_n`
- `relative_velocity_r`
- `relative_velocity_t`
- `relative_velocity_n`
- `mahalanobis_distance`
- `mission_id`
- `c_object_type`

The module evaluates a `DummyRegressor` baseline and a `RandomForestRegressor` main model.

| Model | MAE | RMSE | R2 |
| --- | --- | --- | --- |
| `DummyRegressor` | 0.8350 | 1.0488 | -0.0002 |
| `RandomForestRegressor` | 0.3802 | 0.5213 | 0.7529 |

## Outputs

- `outputs/tables/event_level_data.csv`  
  Full processed dataset with all engineered features, scores, and recommendations.

- `outputs/recommendations/recommendations.csv`  
  Clean final recommendation output with the main columns.

- `reports/recommendation_summary.md`  
  Summary report with recommendation distribution and examples.

- `reports/recommendation_validation.md`  
  Validation report checking coherence of recommendations.

- `reports/model_evaluation.md`  
  Report with ML regression metrics.

- `outputs/models/risk_prediction_model.joblib`  
  Saved fitted `RandomForestRegressor` pipeline.

- `outputs/figures/`  
  Example static encounter plots, one for each available recommended action.

The example plots visualize the target object at the origin, the chaser or secondary object at its relative position, and a line between the two objects. They also show key event values such as `miss_distance`, `relative_speed`, `time_to_tca`, `risk_score`, and `recommended_action`.

These plots are not full orbital maneuver simulations. They are static visualizations of conjunction-event geometry for presentation and interpretation.

## How to run

Install dependencies:

```bash
pip3 install -r requirements.txt
```

Run the pipeline:

```bash
python3 main.py
```

## Current recommendation distribution

- `monitor`: 10927
- `major_maneuver`: 1945
- `small_maneuver`: 209
- `no_action`: 62

## Notes and assumptions

- The project includes both ML risk prediction and an explainable rule-based recommendation layer.
- The ML model predicts `max_risk_estimate`, not the final recommended action.
- `fuel_cost` and `mission_priority` are synthetic assumptions.
- The system is intended as a decision-support prototype.
- The original dataset is not modified.
- The recommendation logic is explainable and based on engineered scores.
