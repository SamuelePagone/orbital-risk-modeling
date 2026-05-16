# Recommendation System Summary Report

## Dataset overview
- Number of events: 13143
- Number of columns: 20

## Recommendation distribution
| recommended_action | count |
| --- | --- |
| monitor | 10927 |
| major_maneuver | 1945 |
| small_maneuver | 209 |
| no_action | 62 |

## Recommendation distribution percentage
| recommended_action | percentage |
| --- | --- |
| monitor | 83.1393 |
| major_maneuver | 14.7988 |
| small_maneuver | 1.5902 |
| no_action | 0.4717 |

## Average risk score by recommendation
| recommended_action | mean_risk_score |
| --- | --- |
| major_maneuver | 0.7602 |
| monitor | 0.5152 |
| no_action | 0.2059 |
| small_maneuver | 0.7467 |

## Average fuel cost by recommendation
| recommended_action | mean_fuel_cost |
| --- | --- |
| major_maneuver | 0.6984 |
| monitor | 0.6905 |
| no_action | 0.2542 |
| small_maneuver | 0.7721 |

## Example recommendations
| event_id | risk_score | fuel_cost | mission_priority | no_action_score | monitor_score | small_maneuver_score | major_maneuver_score | recommended_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.7613 | 0.8676 | 0.5 | 0.0 | 0.5019 | 0.6971 | 0.688 | small_maneuver |
| 1 | 0.5709 | 0.3089 | 0.5 | 0.2007 | 0.8065 | 0.5226 | 0.5576 | monitor |
| 2 | 0.5273 | 0.8785 | 0.75 | 0.2618 | 0.8763 | 0.4987 | 0.5566 | monitor |
| 3 | 0.5321 | 0.8585 | 1.0 | 0.255 | 0.8686 | 0.5098 | 0.617 | monitor |
| 4 | 0.5557 | 0.8072 | 1.0 | 0.222 | 0.8309 | 0.5377 | 0.6442 | monitor |
| 5 | 0.508 | 0.465 | 0.5 | 0.2888 | 0.9072 | 0.5595 | 0.5751 | monitor |
| 6 | 0.5293 | 0.7486 | 0.625 | 0.259 | 0.8731 | 0.5329 | 0.5661 | monitor |
| 7 | 0.4353 | 0.7981 | 0.5 | 0.3906 | 0.9765 | 0.4293 | 0.4465 | monitor |
| 8 | 0.7345 | 0.8091 | 1.0 | 0.0 | 0.5447 | 0.6826 | 0.7769 | major_maneuver |
| 9 | 0.7121 | 0.8923 | 1.0 | 0.0031 | 0.5807 | 0.661 | 0.7533 | major_maneuver |
