"""Reporting utilities for recommendation outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _format_markdown_table(df: pd.DataFrame) -> str:
    """Return a markdown table with numeric values rounded to 4 decimals."""
    formatted_df = df.copy()
    numeric_columns = formatted_df.select_dtypes(include="number").columns
    formatted_df[numeric_columns] = formatted_df[numeric_columns].round(4)

    headers = [str(column) for column in formatted_df.columns]
    rows = [
        [str(value) for value in row]
        for row in formatted_df.itertuples(index=False, name=None)
    ]

    table_lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    table_lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(table_lines)


def create_recommendation_summary_report(
    recommendations_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Create a markdown summary report for recommendation results.

    Parameters
    ----------
    recommendations_df:
        Recommendation output DataFrame. The input DataFrame is not modified.
    output_path:
        Path where the markdown report should be written.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """
    required_columns = {
        "recommended_action",
        "risk_score",
        "fuel_cost",
        "mission_priority",
        "no_action_score",
        "monitor_score",
        "small_maneuver_score",
        "major_maneuver_score",
        "event_id",
    }
    missing_columns = required_columns.difference(recommendations_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    report_df = recommendations_df.copy()

    action_counts = (
        report_df["recommended_action"]
        .value_counts()
        .rename_axis("recommended_action")
        .reset_index(name="count")
    )

    action_percentages = (
        report_df["recommended_action"]
        .value_counts(normalize=True)
        .mul(100)
        .rename_axis("recommended_action")
        .reset_index(name="percentage")
    )

    average_risk_score = (
        report_df.groupby("recommended_action", as_index=False)["risk_score"]
        .mean()
        .rename(columns={"risk_score": "mean_risk_score"})
    )

    average_fuel_cost = (
        report_df.groupby("recommended_action", as_index=False)["fuel_cost"]
        .mean()
        .rename(columns={"fuel_cost": "mean_fuel_cost"})
    )

    example_columns = [
        "event_id",
        "risk_score",
        "fuel_cost",
        "mission_priority",
        "no_action_score",
        "monitor_score",
        "small_maneuver_score",
        "major_maneuver_score",
        "recommended_action",
    ]
    example_recommendations = report_df[example_columns].head(10)

    ml_comparison_content = []
    ml_comparison_columns = {"recommended_action", "ml_recommended_action"}
    if ml_comparison_columns.issubset(report_df.columns):
        ml_action_counts = (
            report_df["ml_recommended_action"]
            .value_counts()
            .rename_axis("ml_recommended_action")
            .reset_index(name="count")
        )
        matching_recommendations = (
            report_df["recommended_action"] == report_df["ml_recommended_action"]
        )
        match_count = int(matching_recommendations.sum())
        match_percentage = (
            float(matching_recommendations.mean() * 100)
            if len(report_df) > 0
            else 0.0
        )
        ml_comparison_content = [
            "",
            "## ML recommendation comparison",
            "Distribution of `ml_recommended_action`:",
            _format_markdown_table(ml_action_counts),
            "",
            f"- Matching recommendations: {match_count}",
            f"- Matching recommendation percentage: {match_percentage:.4f}%",
        ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# Recommendation System Summary Report",
        "",
        "## Dataset overview",
        f"- Number of events: {len(report_df)}",
        f"- Number of columns: {len(report_df.columns)}",
        "",
        "## Recommendation distribution",
        _format_markdown_table(action_counts),
        "",
        "## Recommendation distribution percentage",
        _format_markdown_table(action_percentages),
        "",
        "## Average risk score by recommendation",
        _format_markdown_table(average_risk_score),
        "",
        "## Average fuel cost by recommendation",
        _format_markdown_table(average_fuel_cost),
        "",
        "## Example recommendations",
        _format_markdown_table(example_recommendations),
        *ml_comparison_content,
        "",
    ]

    output_path.write_text("\n".join(content), encoding="utf-8")


def create_recommendation_validation_report(
    recommendations_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Create a markdown report validating recommendation coherence.

    Parameters
    ----------
    recommendations_df:
        Recommendation output DataFrame. The input DataFrame is not modified.
    output_path:
        Path where the markdown report should be written.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """
    required_columns = {
        "recommended_action",
        "risk_score",
        "fuel_cost",
        "mission_priority",
        "urgency",
        "distance_risk",
        "relative_speed_norm",
        "no_action_score",
        "monitor_score",
        "small_maneuver_score",
        "major_maneuver_score",
    }
    missing_columns = required_columns.difference(recommendations_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    report_df = recommendations_df.copy()

    feature_columns = [
        "risk_score",
        "fuel_cost",
        "mission_priority",
        "urgency",
        "distance_risk",
        "relative_speed_norm",
    ]
    average_features = report_df.groupby(
        "recommended_action", as_index=False
    )[feature_columns].mean()

    action_score_columns = [
        "no_action_score",
        "monitor_score",
        "small_maneuver_score",
        "major_maneuver_score",
    ]
    action_score_consistency = report_df.groupby(
        "recommended_action", as_index=False
    )[action_score_columns].mean()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# Recommendation Validation Report",
        "",
        "## Purpose",
        (
            "This report checks whether the generated recommendations are "
            "coherent with the scoring logic."
        ),
        "",
        "## Average feature values by recommendation",
        _format_markdown_table(average_features),
        "",
        "## Action score consistency check",
        _format_markdown_table(action_score_consistency),
        "",
        "## Interpretation notes",
        "- `no_action` should generally have lower `risk_score`.",
        "- `monitor` should generally be associated with intermediate risk.",
        "- Maneuver actions should generally have higher `risk_score`.",
        (
            "- `major_maneuver` should generally be associated with high risk "
            "and/or high mission priority."
        ),
        (
            "- Because `fuel_cost` and `mission_priority` are synthetic, they "
            "must be interpreted as modeling assumptions rather than real "
            "operational measurements."
        ),
        "",
    ]

    output_path.write_text("\n".join(content), encoding="utf-8")
