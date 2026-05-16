"""Scenario-based demo for one satellite conjunction recommendation."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.modeling import get_model_feature_columns
from src.visualization import plot_event_encounter


PROCESSED_DATA_PATH = Path("outputs/tables/event_level_data.csv")
MODEL_PATH = Path("outputs/models/risk_prediction_model.joblib")
FIGURES_OUTPUT_DIR = Path("outputs/figures")


SUMMARY_COLUMNS = {
    "event_id",
    "time_to_tca",
    "miss_distance",
    "relative_speed",
    "c_object_type",
    "max_risk_estimate",
    "risk_score",
    "fuel_cost",
    "mission_priority",
    "no_action_score",
    "monitor_score",
    "small_maneuver_score",
    "major_maneuver_score",
    "recommended_action",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect one processed conjunction event scenario."
    )
    parser.add_argument(
        "--event-id",
        type=int,
        required=True,
        help="Event ID to inspect, for example: --event-id 8",
    )
    return parser.parse_args()


def _validate_file_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} does not exist: {path}")


def _validate_columns(df: pd.DataFrame, required_columns: set[str]) -> None:
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")


def _format_value(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def main() -> None:
    """Run the scenario demo for a selected event ID."""
    args = _parse_args()

    _validate_file_exists(PROCESSED_DATA_PATH, "Processed dataset file")
    _validate_file_exists(MODEL_PATH, "Trained model file")

    recommendations_df = pd.read_csv(PROCESSED_DATA_PATH)
    model = joblib.load(MODEL_PATH)

    numeric_features, categorical_features = get_model_feature_columns()
    model_feature_columns = numeric_features + categorical_features
    required_columns = SUMMARY_COLUMNS.union(model_feature_columns)
    _validate_columns(recommendations_df, required_columns)

    event_rows = recommendations_df[
        recommendations_df["event_id"] == args.event_id
    ]
    if event_rows.empty:
        raise ValueError(f"event_id not found in processed dataset: {args.event_id}")

    event_row = event_rows.iloc[[0]].copy()
    event = event_row.iloc[0]

    predicted_max_risk = model.predict(event_row[model_feature_columns])[0]
    plot_output_path = FIGURES_OUTPUT_DIR / f"scenario_event_{args.event_id}.png"
    plot_event_encounter(
        recommendations_df=recommendations_df,
        event_id=args.event_id,
        output_path=plot_output_path,
    )

    print("\nSatellite Collision Avoidance Scenario Demo")
    print("=" * 52)

    print("\nScenario information")
    print(f"- event_id: {_format_value(event['event_id'])}")
    print(f"- time_to_tca: {_format_value(event['time_to_tca'])}")
    print(f"- miss_distance: {_format_value(event['miss_distance'])}")
    print(f"- relative_speed: {_format_value(event['relative_speed'])}")
    print(f"- c_object_type: {_format_value(event['c_object_type'])}")

    print("\nML risk prediction")
    print(f"- actual max_risk_estimate: {_format_value(event['max_risk_estimate'])}")
    print(f"- predicted max_risk_estimate: {predicted_max_risk:.4f}")

    print("\nRecommendation features")
    print(f"- risk_score: {_format_value(event['risk_score'])}")
    print(f"- fuel_cost: {_format_value(event['fuel_cost'])}")
    print(f"- mission_priority: {_format_value(event['mission_priority'])}")

    print("\nAction scores")
    print(f"- no_action_score: {_format_value(event['no_action_score'])}")
    print(f"- monitor_score: {_format_value(event['monitor_score'])}")
    print(
        "- small_maneuver_score: "
        f"{_format_value(event['small_maneuver_score'])}"
    )
    print(
        "- major_maneuver_score: "
        f"{_format_value(event['major_maneuver_score'])}"
    )

    print("\nFinal recommendation")
    print(f"- recommended_action: {_format_value(event['recommended_action'])}")

    print("\nGenerated visualization")
    print(f"- plot output path: {plot_output_path}")


if __name__ == "__main__":
    main()
