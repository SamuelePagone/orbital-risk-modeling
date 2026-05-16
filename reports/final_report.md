# Satellite Collision Avoidance Recommendation System - Final Report

## 1. Introduction

Satellite conjunction events occur when an operational satellite is predicted to pass close to another space object, such as debris, a defunct satellite, or another active spacecraft. In orbital operations, these events require careful decision making because unnecessary maneuvers can consume fuel and disrupt mission plans, while delayed or insufficient action can increase collision risk.

For each conjunction event, operators may decide to take no action, continue monitoring the event, or perform an avoidance maneuver. This project builds an explainable recommendation system to support that decision. The system transforms raw conjunction indicators into interpretable event-level scores and then recommends an operational action.

The recommended action is intended for mission operators or a decision-support workflow, not as an autonomous command sent directly to a satellite.

## 2. Project objective

The objective of this project is to recommend one of four possible actions for each conjunction event:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

The goal is not only to estimate collision risk. The project also translates risk indicators into an operational recommendation that can support decision making. This makes the system a decision-support prototype rather than only a risk-estimation tool.

## 3. Dataset description

The main dataset used in this project is:

```text
dataset/data/kelvins_competition_data/train_data.csv
```

The original dataset contains:

- 162634 rows
- 103 columns

The dataset includes multiple temporal observations for each `event_id`. This means that a single conjunction event may appear several times, with different values of `time_to_tca` and updated risk or state information.

The main groups of variables are:

- `event_id`: identifies a conjunction event.
- `time_to_tca`: indicates the time remaining to closest approach.
- `risk` and `max_risk_estimate`: represent collision-risk information in log-scale form.
- `miss_distance`: represents the closest approach distance between the two objects.
- `relative_speed`: represents the speed between the two objects.
- `t_` columns: describe the target object.
- `c_` columns: describe the chaser or secondary object.
- Relative position and relative velocity columns: describe the encounter geometry and motion between the two objects.

Each final event-level row represents an encounter between a target object and a secondary or chaser object, not the state of a single satellite alone.

## 4. Event-level preprocessing

The original dataset cannot be used directly as one row equals one recommendation because each `event_id` may appear multiple times. A recommendation should be generated once per conjunction event, not once per temporal observation.

The project creates an event-level dataset by selecting, for each `event_id`, the row with the smallest non-negative `time_to_tca`.

Non-negative `time_to_tca` is used because the recommendation should be made before or at closest approach, not after the event has already passed. Selecting the smallest non-negative value keeps the closest available pre-TCA observation for each event.

The resulting event-level dataset contains:

- 13143 events

## 5. Feature engineering

The project creates several engineered features to make the recommendation logic interpretable and operationally meaningful.

### 5.1 Probability features

The original `risk` and `max_risk_estimate` columns appear to be represented on a log10 scale. Values closer to zero indicate higher probability.

The project derives:

```text
collision_probability = 10 ** risk
max_collision_probability = 10 ** max_risk_estimate
```

These probability-like features make the log-scale risk values easier to interpret.

### 5.2 Operational risk features

`distance_risk` is an inverted normalized version of `miss_distance`. Smaller `miss_distance` means a closer approach, so it receives a higher `distance_risk` value.

`urgency` is an inverted normalized version of `time_to_tca`. Smaller `time_to_tca` means less time remains before closest approach, so it receives a higher urgency value.

### 5.3 Normalized velocity feature

`relative_speed_norm` converts `relative_speed` to a 0-1 scale. This makes relative velocity comparable with the other normalized risk features used in scoring.

### 5.4 Normalized risk feature

`risk_norm` converts the original log-scale `risk` into a 0-1 score. Higher `risk_norm` values indicate higher collision risk.

### 5.5 Synthetic decision features

The project creates two synthetic decision-support features:

- `fuel_cost`
- `mission_priority`

These are synthetic assumptions because the original dataset does not contain real maneuver fuel cost, delta-v, or mission priority values.

`fuel_cost` is a proxy for operational maneuver complexity. It is based on `relative_speed_norm` and `urgency`.

`mission_priority` is deterministically derived from `mission_id` to simulate different mission importance levels.

These variables are useful for building a more realistic recommendation prototype, but they must be interpreted as modeling assumptions rather than observed operational measurements.

## 6. Risk score design

The `risk_score` represents the overall severity of the conjunction event. It combines physical risk, encounter distance, urgency, relative speed, and mission priority.

The formula is:

```text
risk_score =
    0.35 * risk_norm
    + 0.25 * distance_risk
    + 0.20 * urgency
    + 0.10 * relative_speed_norm
    + 0.10 * mission_priority
```

`fuel_cost` is not included in `risk_score` because fuel cost affects action desirability, not the physical severity of the conjunction event. Fuel cost is used later when scoring candidate actions.

The weights are designed as follows:

- `risk_norm` has the highest weight because it directly represents collision risk.
- `distance_risk` is important because close approaches are dangerous.
- `urgency` matters because less time means more operational pressure.
- `relative_speed_norm` contributes to encounter severity.
- `mission_priority` adds operational importance.

## 7. Action scoring and recommendation logic

The system computes four action scores:

- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`

The intended behavior is:

- `no_action` is favored when risk is low.
- `monitor` is favored for intermediate risk.
- `small_maneuver` is favored for medium-high risk cases.
- `major_maneuver` is reserved for more severe cases, especially when mission priority is high.

The final `recommended_action` is selected as the action with the highest score.

If two or more actions have exactly the same highest score, ties are resolved by selecting the least aggressive action in this order:

```text
no_action -> monitor -> small_maneuver -> major_maneuver
```

This tie-breaking rule avoids unnecessary maneuvers when two actions are equally suitable.

## 8. Outputs generated by the pipeline

The pipeline generates the following outputs:

- `outputs/tables/event_level_data.csv`  
  Full processed dataset with original columns, engineered features, scores, and recommendations.

- `outputs/recommendations/recommendations.csv`  
  Clean recommendation output with the main columns only.

- `reports/recommendation_summary.md`  
  Summary report with recommendation distribution, percentages, average scores, and examples.

- `reports/recommendation_validation.md`  
  Validation report checking whether the recommendations are coherent with the scoring logic.

- `outputs/figures/`  
  Static example encounter plots for the four recommendation classes.

The visualization utility creates one example plot for each recommendation type: `no_action`, `monitor`, `small_maneuver`, and `major_maneuver`.

These figures are visual aids, not physical orbital simulations. They do not simulate trajectory propagation, delta-v, or post-maneuver dynamics.

## 9. Results

The final recommendation distribution is:

- `monitor`: 10927
- `major_maneuver`: 1945
- `small_maneuver`: 209
- `no_action`: 62

The corresponding percentages are:

- `monitor`: 83.1393%
- `major_maneuver`: 14.7988%
- `small_maneuver`: 1.5902%
- `no_action`: 0.4717%

`monitor` is the most frequent recommendation. This means most events require continued observation but not immediate maneuvering.

`major_maneuver` appears for a smaller but significant group of high-risk or high-priority cases.

`small_maneuver` appears in fewer intermediate cases where a maneuver is useful but a major maneuver is not the best option.

`no_action` appears only in low-risk cases.

## 10. Validation and interpretation

The validation report shows that the recommendations are coherent with the scoring logic.

`no_action` has a low average `risk_score`, `monitor` has an intermediate average `risk_score`, and maneuver actions have higher average `risk_score` values. `small_maneuver` has high risk and high urgency, while `major_maneuver` has high risk and higher mission priority.

Average feature values by recommendation are:

### major_maneuver

- `risk_score`: 0.7602
- `fuel_cost`: 0.6984
- `mission_priority`: 0.7281
- `urgency`: 0.7893
- `distance_risk`: 0.8660
- `relative_speed_norm`: 0.6378

### monitor

- `risk_score`: 0.5152
- `fuel_cost`: 0.6905
- `mission_priority`: 0.6611
- `urgency`: 0.8222
- `distance_risk`: 0.6926
- `relative_speed_norm`: 0.6027

### no_action

- `risk_score`: 0.2059
- `fuel_cost`: 0.2542
- `mission_priority`: 0.6089
- `urgency`: 0.3381
- `distance_risk`: 0.2270
- `relative_speed_norm`: 0.1984

### small_maneuver

- `risk_score`: 0.7467
- `fuel_cost`: 0.7721
- `mission_priority`: 0.5000
- `urgency`: 0.9526
- `distance_risk`: 0.8604
- `relative_speed_norm`: 0.6517

These values show that the recommender is coherent and explainable. Low-risk cases are associated with `no_action`, intermediate cases are mostly assigned to `monitor`, and higher-risk cases are assigned to maneuver actions.

## 11. Limitations

This project has several limitations:

- It is a rule-based system, not a trained machine learning model.
- `fuel_cost` and `mission_priority` are synthetic assumptions.
- Real operational deployment would require validated thresholds, real maneuver cost, satellite constraints, and expert review.
- The score weights are manually designed and tuned.
- The system does not simulate orbital maneuvers.
- The system does not predict actual collision outcomes, but supports decision making.

## 12. Future work

Possible improvements include:

- Use real mission-priority metadata if available.
- Estimate maneuver cost using real delta-v calculations.
- Validate scoring rules with expert-labeled decisions.
- Add machine learning models for risk classification or recommendation learning.
- Add visual dashboards.
- Include uncertainty-aware analysis using covariance features.
- Compare rule-based recommendations with historical operator decisions.

## 13. Conclusion

This project successfully builds an explainable decision-support recommendation system for satellite collision avoidance.

The system transforms raw conjunction data into event-level recommendations and produces reproducible tabular outputs, reports, and visual examples of representative conjunction scenarios. It combines risk indicators, operational urgency, encounter geometry, synthetic decision-support assumptions, and action scoring into a transparent pipeline.

The final prototype is suitable as a first complete, interpretable version of a satellite collision avoidance recommendation system.
