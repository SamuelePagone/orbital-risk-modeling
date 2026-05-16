"""Machine learning utilities for conjunction risk prediction.

This module is intentionally separate from the rule-based recommendation
pipeline. It provides reusable regression utilities for predicting
``max_risk_estimate`` from physical and orbital conjunction-event features.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


TARGET_COLUMN = "max_risk_estimate"


def get_model_feature_columns() -> tuple[list[str], list[str]]:
    """Return the input feature lists used by the ML risk model.

    Risk-derived columns, target columns, and recommendation outputs are
    intentionally excluded to prevent target leakage.
    """
    numeric_features = [
        "time_to_tca",
        "miss_distance",
        "relative_speed",
        "relative_position_r",
        "relative_position_t",
        "relative_position_n",
        "relative_velocity_r",
        "relative_velocity_t",
        "relative_velocity_n",
        "mahalanobis_distance",
        "mission_id",
    ]
    categorical_features = ["c_object_type"]

    return numeric_features, categorical_features


def validate_modeling_columns(df: pd.DataFrame) -> None:
    """Validate that all required model input and target columns exist.

    Parameters
    ----------
    df:
        Input DataFrame to validate.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """
    numeric_features, categorical_features = get_model_feature_columns()
    required_columns = set(numeric_features + categorical_features + [TARGET_COLUMN])
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")


def _make_one_hot_encoder() -> OneHotEncoder:
    """Create a dense OneHotEncoder across supported scikit-learn versions."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def _build_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
) -> ColumnTransformer:
    """Build the shared preprocessing transformer for risk models."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", _make_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ]
    )


def _rmse(y_true: pd.Series, y_pred: np.ndarray) -> float:
    """Compute RMSE with compatibility across scikit-learn versions."""
    try:
        return float(mean_squared_error(y_true, y_pred, squared=False))
    except TypeError:
        return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def _evaluate_regression(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    """Compute standard regression metrics."""
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": _rmse(y_true, y_pred),
        "R2": float(r2_score(y_true, y_pred)),
    }


def train_risk_prediction_models(
    df: pd.DataFrame,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train baseline and random forest regressors for risk prediction.

    The regression target is ``max_risk_estimate``. The model predicts this
    dataset risk estimate from physical/orbital input features; it does not
    predict the final recommended action.

    Parameters
    ----------
    df:
        Input event-level or observation-level DataFrame.
    random_state:
        Random seed used for train/test splitting and the random forest model.

    Returns
    -------
    dict
        Dictionary containing fitted pipelines, metrics, test targets,
        predictions, and feature lists.
    """
    validate_modeling_columns(df)

    numeric_features, categorical_features = get_model_feature_columns()
    feature_columns = numeric_features + categorical_features

    X = df[feature_columns].copy()
    y = df[TARGET_COLUMN].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=random_state,
    )

    baseline_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                _build_preprocessor(numeric_features, categorical_features),
            ),
            ("model", DummyRegressor(strategy="mean")),
        ]
    )

    random_forest_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                _build_preprocessor(numeric_features, categorical_features),
            ),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    baseline_pipeline.fit(X_train, y_train)
    random_forest_pipeline.fit(X_train, y_train)

    baseline_predictions = baseline_pipeline.predict(X_test)
    random_forest_predictions = random_forest_pipeline.predict(X_test)

    return {
        "baseline_pipeline": baseline_pipeline,
        "random_forest_pipeline": random_forest_pipeline,
        "metrics": {
            "DummyRegressor": _evaluate_regression(
                y_test,
                baseline_predictions,
            ),
            "RandomForestRegressor": _evaluate_regression(
                y_test,
                random_forest_predictions,
            ),
        },
        "y_test": y_test,
        "baseline_predictions": baseline_predictions,
        "random_forest_predictions": random_forest_predictions,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "target_column": TARGET_COLUMN,
    }


def _markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    """Create a small markdown table without optional dependencies."""
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def create_model_evaluation_report(results: dict, output_path: Path) -> None:
    """Write a markdown evaluation report for trained risk models.

    The report documents regression metrics for the baseline and random forest
    models and clarifies that the ML model predicts ``max_risk_estimate``, not
    the final recommended action.
    """
    metrics = results.get("metrics")
    if not isinstance(metrics, dict):
        raise ValueError("results must contain a 'metrics' dictionary")

    metric_rows = []
    for model_name in ["DummyRegressor", "RandomForestRegressor"]:
        if model_name not in metrics:
            raise ValueError(f"Missing metrics for model: {model_name}")
        model_metrics = metrics[model_name]
        metric_rows.append(
            [
                model_name,
                f"{model_metrics['MAE']:.4f}",
                f"{model_metrics['RMSE']:.4f}",
                f"{model_metrics['R2']:.4f}",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# ML Risk Prediction Model Evaluation",
        "",
        "This report evaluates regression models that predict `max_risk_estimate`.",
        "",
        (
            "The machine learning task is a regression task. The model does "
            "not predict the final action directly; final actions are still "
            "produced by the rule-based recommendation layer."
        ),
        "",
        "## Metrics",
        _markdown_table(
            ["Model", "MAE", "RMSE", "R2"],
            metric_rows,
        ),
        "",
        "## Metric interpretation",
        "- `MAE` is the average absolute prediction error.",
        "- `RMSE` is the square root of the average squared prediction error.",
        "- `R2` measures the proportion of target variance explained by the model.",
        "",
        "## Leakage prevention",
        (
            "Risk-derived columns and recommendation-output columns are "
            "excluded from the input features. This prevents leakage from "
            "the target or downstream recommendation outputs into the model."
        ),
        "",
        "## Limitations",
        "- The model predicts a dataset risk estimate, not a real operator action.",
        "- The target is not an operator decision.",
        "- Real deployment would require expert validation.",
        "",
    ]

    output_path.write_text("\n".join(content), encoding="utf-8")


def save_model(results: dict, output_path: Path) -> None:
    """Save the fitted random forest pipeline with joblib."""
    if "random_forest_pipeline" not in results:
        raise ValueError("results must contain 'random_forest_pipeline'")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(results["random_forest_pipeline"], output_path)


def add_ml_risk_predictions(
    df: pd.DataFrame,
    trained_model: Any,
) -> pd.DataFrame:
    """Add ML-predicted max risk estimates to a copy of the DataFrame.

    The model uses the same physical/orbital input features returned by
    ``get_model_feature_columns``. The resulting
    ``predicted_max_risk_estimate`` column is used by the ML-based
    recommendation layer while preserving the original rule-based
    ``recommended_action`` for comparison.
    """
    numeric_features, categorical_features = get_model_feature_columns()
    feature_columns = numeric_features + categorical_features
    missing_columns = set(feature_columns).difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")
    if "predicted_max_risk_estimate" in df.columns:
        raise ValueError("Column already exists: predicted_max_risk_estimate")

    df_with_predictions = df.copy()
    df_with_predictions["predicted_max_risk_estimate"] = trained_model.predict(
        df_with_predictions[feature_columns]
    )

    return df_with_predictions
