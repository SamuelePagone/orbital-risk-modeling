# ML Risk Prediction Model Evaluation

This report evaluates regression models that predict `max_risk_estimate`.

The machine learning task is a regression task. The model does not predict the final action directly; final actions are still produced by the rule-based recommendation layer.

## Metrics
| Model | MAE | RMSE | R2 |
| --- | --- | --- | --- |
| DummyRegressor | 0.8350 | 1.0488 | -0.0002 |
| RandomForestRegressor | 0.3802 | 0.5213 | 0.7529 |

## Metric interpretation
- `MAE` is the average absolute prediction error.
- `RMSE` is the square root of the average squared prediction error.
- `R2` measures the proportion of target variance explained by the model.

## Leakage prevention
Risk-derived columns and recommendation-output columns are excluded from the input features. This prevents leakage from the target or downstream recommendation outputs into the model.

## Limitations
- The model predicts a dataset risk estimate, not a real operator action.
- The target is not an operator decision.
- Real deployment would require expert validation.
