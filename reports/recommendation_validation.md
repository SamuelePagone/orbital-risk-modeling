# Recommendation Validation Report

## Purpose
This report checks whether the generated recommendations are coherent with the scoring logic.

## Average feature values by recommendation
| recommended_action | risk_score | fuel_cost | mission_priority | urgency | distance_risk | relative_speed_norm |
| --- | --- | --- | --- | --- | --- | --- |
| major_maneuver | 0.7602 | 0.6984 | 0.7281 | 0.7893 | 0.866 | 0.6378 |
| monitor | 0.5152 | 0.6905 | 0.6611 | 0.8222 | 0.6926 | 0.6027 |
| no_action | 0.2059 | 0.2542 | 0.6089 | 0.3381 | 0.227 | 0.1984 |
| small_maneuver | 0.7467 | 0.7721 | 0.5 | 0.9526 | 0.8604 | 0.6517 |

## Action score consistency check
| recommended_action | no_action_score | monitor_score | small_maneuver_score | major_maneuver_score |
| --- | --- | --- | --- | --- |
| major_maneuver | 0.0114 | 0.5037 | 0.6853 | 0.775 |
| monitor | 0.2788 | 0.8578 | 0.4928 | 0.5423 |
| no_action | 0.7117 | 0.6095 | 0.2026 | 0.2913 |
| small_maneuver | 0.0044 | 0.5252 | 0.6984 | 0.6926 |

## Interpretation notes
- `no_action` should generally have lower `risk_score`.
- `monitor` should generally be associated with intermediate risk.
- Maneuver actions should generally have higher `risk_score`.
- `major_maneuver` should generally be associated with high risk and/or high mission priority.
- Because `fuel_cost` and `mission_priority` are synthetic, they must be interpreted as modeling assumptions rather than real operational measurements.
