from pathlib import Path

import pandas as pd

from src.recommender import add_action_scores, add_recommended_action
from src.reporting import (
    create_recommendation_summary_report,
    create_recommendation_validation_report,
)
from src.preprocessing import (
    add_normalized_risk_feature,
    add_normalized_velocity_feature,
    add_operational_risk_features,
    add_probability_features,
    add_risk_score,
    add_synthetic_decision_features,
    create_event_level_dataset,
)
from src.visualization import create_example_event_plots


TRAIN_DATA_PATH = Path("dataset/data/kelvins_competition_data/train_data.csv")
OUTPUT_DIR = Path("outputs/tables")
EVENT_LEVEL_OUTPUT_PATH = OUTPUT_DIR / "event_level_data.csv"
RECOMMENDATIONS_OUTPUT_DIR = Path("outputs/recommendations")
RECOMMENDATIONS_OUTPUT_PATH = RECOMMENDATIONS_OUTPUT_DIR / "recommendations.csv"
REPORT_OUTPUT_PATH = Path("reports/recommendation_summary.md")
VALIDATION_REPORT_OUTPUT_PATH = Path("reports/recommendation_validation.md")
FIGURES_OUTPUT_DIR = Path("outputs/figures")

RECOMMENDATION_COLUMNS = [
    "event_id",
    "mission_id",
    "c_object_type",
    "time_to_tca",
    "risk",
    "risk_norm",
    "collision_probability",
    "miss_distance",
    "distance_risk",
    "relative_speed",
    "relative_speed_norm",
    "urgency",
    "fuel_cost",
    "mission_priority",
    "risk_score",
    "no_action_score",
    "monitor_score",
    "small_maneuver_score",
    "major_maneuver_score",
    "recommended_action",
]


def main() -> None:
    """Create and save the event-level dataset with engineered risk features."""
    original_df = pd.read_csv(TRAIN_DATA_PATH)
    event_level_df = create_event_level_dataset(original_df)
    probability_df = add_probability_features(event_level_df)
    operational_risk_df = add_operational_risk_features(probability_df)
    velocity_df = add_normalized_velocity_feature(operational_risk_df)
    risk_df = add_normalized_risk_feature(velocity_df)
    synthetic_df = add_synthetic_decision_features(risk_df)
    scored_df = add_risk_score(synthetic_df)
    action_scores_df = add_action_scores(scored_df)
    final_df = add_recommended_action(action_scores_df)
    create_example_event_plots(
        recommendations_df=final_df,
        output_dir=FIGURES_OUTPUT_DIR,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RECOMMENDATIONS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    recommendations_df = final_df[RECOMMENDATION_COLUMNS].copy()
    create_recommendation_summary_report(
        recommendations_df=recommendations_df,
        output_path=REPORT_OUTPUT_PATH,
    )
    create_recommendation_validation_report(
        recommendations_df=recommendations_df,
        output_path=VALIDATION_REPORT_OUTPUT_PATH,
    )

    final_df.to_csv(EVENT_LEVEL_OUTPUT_PATH, index=False)
    recommendations_df.to_csv(RECOMMENDATIONS_OUTPUT_PATH, index=False)

    print(f"Original dataset shape: {original_df.shape}")
    print(f"Event-level dataset shape: {event_level_df.shape}")
    print(f"Dataset shape after risk score: {scored_df.shape}")
    print(f"Dataset shape after action scores: {action_scores_df.shape}")
    print(f"Final dataset shape after recommended action: {final_df.shape}")
    print(f"Clean recommendations shape: {recommendations_df.shape}")
    print(f"Full dataset output path: {EVENT_LEVEL_OUTPUT_PATH}")
    print(f"Clean recommendations output path: {RECOMMENDATIONS_OUTPUT_PATH}")
    print(f"Recommendation summary report output path: {REPORT_OUTPUT_PATH}")
    print(
        "Recommendation validation report output path: "
        f"{VALIDATION_REPORT_OUTPUT_PATH}"
    )
    print(f"Figures output directory path: {FIGURES_OUTPUT_DIR}")
    print("Added column: recommended_action")


if __name__ == "__main__":
    main()
