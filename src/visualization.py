"""Visualization utilities for recommendation outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def plot_event_encounter(
    recommendations_df: pd.DataFrame,
    event_id: int,
    output_path: Path,
) -> None:
    """Create a simple 2D encounter plot for one conjunction event.

    The target object is shown at the origin. The chaser or secondary object
    is shown using the relative radial/transverse position components.

    Parameters
    ----------
    recommendations_df:
        DataFrame containing event-level recommendations and encounter data.
    event_id:
        Event identifier to plot.
    output_path:
        Path where the PNG figure should be saved.
    """
    required_columns = {
        "event_id",
        "relative_position_r",
        "relative_position_t",
        "relative_position_n",
        "miss_distance",
        "relative_speed",
        "time_to_tca",
        "risk_score",
        "recommended_action",
    }
    missing_columns = required_columns.difference(recommendations_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    event_rows = recommendations_df[recommendations_df["event_id"] == event_id]
    if event_rows.empty:
        raise ValueError(f"No row found for event_id: {event_id}")

    row = event_rows.iloc[0]
    chaser_x = row["relative_position_r"]
    chaser_y = row["relative_position_t"]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(0, 0, color="#1f77b4", s=90, label="Target")
    ax.scatter(chaser_x, chaser_y, color="#d62728", s=90, label="Chaser")
    ax.plot([0, chaser_x], [0, chaser_y], color="#555555", linewidth=1.5)

    ax.annotate("Target", xy=(0, 0), xytext=(8, 8), textcoords="offset points")
    ax.annotate(
        "Chaser",
        xy=(chaser_x, chaser_y),
        xytext=(8, 8),
        textcoords="offset points",
    )

    info_text = (
        f"miss_distance: {row['miss_distance']:.4f}\n"
        f"relative_speed: {row['relative_speed']:.4f}\n"
        f"time_to_tca: {row['time_to_tca']:.4f}\n"
        f"risk_score: {row['risk_score']:.4f}\n"
        f"recommended_action: {row['recommended_action']}"
    )
    ax.text(
        0.02,
        0.98,
        info_text,
        transform=ax.transAxes,
        va="top",
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85},
    )

    ax.set_title(
        f"Event {event_id} - Recommended action: {row['recommended_action']}"
    )
    ax.set_xlabel("Relative position R")
    ax.set_ylabel("Relative position T")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    ax.set_aspect("equal", adjustable="datalim")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def create_example_event_plots(
    recommendations_df: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Create one example encounter plot for each available action class.

    For each action, the first matching event in ``recommendations_df`` is
    plotted. If an action is not present in the DataFrame, it is skipped.
    """
    required_columns = {"event_id", "recommended_action"}
    missing_columns = required_columns.difference(recommendations_df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    actions = [
        "no_action",
        "monitor",
        "small_maneuver",
        "major_maneuver",
    ]

    for action in actions:
        action_rows = recommendations_df[
            recommendations_df["recommended_action"] == action
        ]
        if action_rows.empty:
            continue

        example_event_id = int(action_rows.iloc[0]["event_id"])
        output_path = output_dir / f"example_{action}.png"
        plot_event_encounter(
            recommendations_df=recommendations_df,
            event_id=example_event_id,
            output_path=output_path,
        )
