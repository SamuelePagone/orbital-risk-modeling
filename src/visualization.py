"""Visualization utilities for recommendation outputs."""

from __future__ import annotations

from pathlib import Path
import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, Rectangle
import pandas as pd


ACTION_COLORS = {
    "no_action": "#2ecc71",
    "monitor": "#3498db",
    "small_maneuver": "#f39c12",
    "major_maneuver": "#e74c3c",
}


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

    recommended_action = row["recommended_action"]
    action_color = ACTION_COLORS.get(recommended_action, "#f5f5f5")

    span = max(abs(chaser_x), abs(chaser_y), 1.0)
    margin = span * 0.35
    x_min = min(0, chaser_x) - margin
    x_max = max(0, chaser_x) + margin
    y_min = min(0, chaser_y) - margin
    y_max = max(0, chaser_y) + margin

    fig, ax = plt.subplots(figsize=(9, 7), facecolor="#030711")
    ax.set_facecolor("#030711")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    star_rng = random.Random(int(event_id))
    star_x = [star_rng.uniform(x_min, x_max) for _ in range(140)]
    star_y = [star_rng.uniform(y_min, y_max) for _ in range(140)]
    star_size = [star_rng.uniform(3, 14) for _ in range(140)]
    star_alpha = [star_rng.uniform(0.25, 0.85) for _ in range(140)]
    star_colors = [
        "#ffffff" if star_rng.random() > 0.35 else "#9aa6b2"
        for _ in range(140)
    ]
    ax.scatter(
        star_x,
        star_y,
        s=star_size,
        c=star_colors,
        alpha=star_alpha,
        linewidths=0,
        zorder=0,
    )

    ax.plot(
        [0, chaser_x],
        [0, chaser_y],
        color="#c9d6e3",
        linestyle="--",
        linewidth=1.6,
        alpha=0.75,
        zorder=1,
    )

    satellite_scale = span * 0.045
    body_width = satellite_scale * 0.9
    body_height = satellite_scale * 1.1
    panel_width = satellite_scale * 1.6
    panel_height = satellite_scale * 0.55

    ax.add_patch(
        Rectangle(
            (-body_width / 2, -body_height / 2),
            body_width,
            body_height,
            facecolor="#d8dee9",
            edgecolor="#ffffff",
            linewidth=1.0,
            zorder=4,
        )
    )
    ax.add_patch(
        Rectangle(
            (-body_width / 2 - panel_width, -panel_height / 2),
            panel_width,
            panel_height,
            facecolor="#4f8fd8",
            edgecolor="#b9d8ff",
            linewidth=0.8,
            zorder=3,
        )
    )
    ax.add_patch(
        Rectangle(
            (body_width / 2, -panel_height / 2),
            panel_width,
            panel_height,
            facecolor="#4f8fd8",
            edgecolor="#b9d8ff",
            linewidth=0.8,
            zorder=3,
        )
    )
    ax.add_patch(
        Circle(
            (0, 0),
            radius=satellite_scale * 0.18,
            facecolor="#ffd166",
            edgecolor="#fff4c2",
            linewidth=0.7,
            zorder=5,
        )
    )

    ax.scatter(
        chaser_x,
        chaser_y,
        s=850,
        color=action_color,
        alpha=0.16,
        linewidths=0,
        zorder=2,
    )
    ax.scatter(
        chaser_x,
        chaser_y,
        s=150,
        color="#ff6b35",
        edgecolor="#ffd1b3",
        linewidth=1.2,
        zorder=5,
    )

    ax.annotate(
        "Target satellite",
        xy=(0, 0),
        xytext=(12, 14),
        textcoords="offset points",
        color="#eef5ff",
        fontsize=10,
        weight="bold",
    )
    ax.annotate(
        "Chaser object",
        xy=(chaser_x, chaser_y),
        xytext=(12, 14),
        textcoords="offset points",
        color="#ffd1b3",
        fontsize=10,
        weight="bold",
    )

    info_text = (
        f"miss_distance: {row['miss_distance']:.4f}\n"
        f"relative_speed: {row['relative_speed']:.4f}\n"
        f"time_to_tca: {row['time_to_tca']:.4f}\n"
        f"risk_score: {row['risk_score']:.4f}\n"
        f"recommended_action: {recommended_action}"
    )
    ax.text(
        0.02,
        0.98,
        info_text,
        transform=ax.transAxes,
        va="top",
        color="#f4f7fb",
        fontsize=10,
        linespacing=1.45,
        bbox={
            "boxstyle": "round,pad=0.55",
            "facecolor": "#101826",
            "edgecolor": action_color,
            "alpha": 0.88,
        },
    )

    ax.set_title(
        f"Event {event_id} - Recommended action: {recommended_action}",
        color=action_color,
        fontsize=14,
        weight="bold",
        pad=14,
    )
    ax.set_xlabel("Relative position R", color="#d8dee9")
    ax.set_ylabel("Relative position T", color="#d8dee9")
    ax.tick_params(colors="#b8c2cc")
    for spine in ax.spines.values():
        spine.set_color("#415063")
    ax.grid(True, color="#2f3b4d", alpha=0.45, linestyle=":")
    ax.set_aspect("equal", adjustable="datalim")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, facecolor=fig.get_facecolor())
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


def create_event_animation(
    original_df: pd.DataFrame,
    processed_df: pd.DataFrame,
    event_id: int,
    output_path: Path,
    use_ml_recommendation: bool = True,
    frame_duration_ms: int = 180,
) -> None:
    """Create an animated GIF for one conjunction-event scenario.

    The animation is a visual decision-support demo. It shows the target
    satellite at the origin, the chaser object moving through the observed
    relative positions over time, and a simple visual avoidance offset based
    on the displayed recommendation. It is not a physical orbital simulation.

    Parameters
    ----------
    original_df:
        Observation-level dataset containing the temporal event history.
    processed_df:
        Event-level processed dataset containing recommendation outputs.
    event_id:
        Event identifier to animate.
    output_path:
        Path where the GIF should be saved.
    use_ml_recommendation:
        If True, use ``ml_recommended_action`` and ``ml_risk_score`` when
        available in ``processed_df``. Otherwise use the baseline
        ``recommended_action``.
    frame_duration_ms:
        Duration of each GIF frame in milliseconds. Larger values create a
        slower animation that is easier to follow.
    """
    original_required_columns = {
        "event_id",
        "time_to_tca",
        "relative_position_r",
        "relative_position_t",
    }
    missing_original_columns = original_required_columns.difference(
        original_df.columns
    )
    if missing_original_columns:
        missing = ", ".join(sorted(missing_original_columns))
        raise ValueError(f"Missing required original_df column(s): {missing}")

    processed_required_columns = {
        "event_id",
        "risk_score",
        "recommended_action",
    }
    if use_ml_recommendation:
        processed_required_columns.update(
            {
                "ml_recommended_action",
                "ml_risk_score",
            }
        )

    missing_processed_columns = processed_required_columns.difference(
        processed_df.columns
    )
    if missing_processed_columns:
        missing = ", ".join(sorted(missing_processed_columns))
        raise ValueError(f"Missing required processed_df column(s): {missing}")
    if frame_duration_ms <= 0:
        raise ValueError("frame_duration_ms must be greater than 0")

    event_observations = original_df[
        original_df["event_id"] == event_id
    ].sort_values("time_to_tca", ascending=False)
    if event_observations.empty:
        raise ValueError(f"No observation rows found for event_id: {event_id}")

    processed_rows = processed_df[processed_df["event_id"] == event_id]
    if processed_rows.empty:
        raise ValueError(f"No processed row found for event_id: {event_id}")

    if len(event_observations) > 80:
        sample_positions = [
            round(index * (len(event_observations) - 1) / 79)
            for index in range(80)
        ]
        event_observations = event_observations.iloc[sample_positions]

    event_observations = event_observations.reset_index(drop=True)
    processed_row = processed_rows.iloc[0]

    if use_ml_recommendation and "ml_recommended_action" in processed_df.columns:
        displayed_action = processed_row["ml_recommended_action"]
        risk_label = "ml_risk_score"
        risk_value = processed_row["ml_risk_score"]
    else:
        displayed_action = processed_row["recommended_action"]
        risk_label = "risk_score"
        risk_value = processed_row["risk_score"]

    action_color = ACTION_COLORS.get(displayed_action, "#f5f5f5")

    raw_chaser_x_values = event_observations["relative_position_r"].tolist()
    raw_chaser_y_values = event_observations["relative_position_t"].tolist()
    frame_count = len(event_observations)

    raw_start_x = raw_chaser_x_values[0]
    raw_start_y = raw_chaser_y_values[0]
    raw_end_x = raw_chaser_x_values[-1]
    raw_end_y = raw_chaser_y_values[-1]
    start_distance = (raw_start_x**2 + raw_start_y**2) ** 0.5
    end_distance = (raw_end_x**2 + raw_end_y**2) ** 0.5

    # The source rows are observation updates, not a clean plotted trajectory.
    # For presentation, smooth the visual path and orient it toward the target.
    if end_distance > start_distance:
        visual_start_x = raw_end_x
        visual_start_y = raw_end_y
        visual_end_x = raw_start_x
        visual_end_y = raw_start_y
    else:
        visual_start_x = raw_start_x
        visual_start_y = raw_start_y
        visual_end_x = raw_end_x
        visual_end_y = raw_end_y

    if frame_count == 1:
        chaser_x_values = [visual_end_x]
        chaser_y_values = [visual_end_y]
    else:
        chaser_x_values = [
            visual_start_x
            + (visual_end_x - visual_start_x) * index / (frame_count - 1)
            for index in range(frame_count)
        ]
        chaser_y_values = [
            visual_start_y
            + (visual_end_y - visual_start_y) * index / (frame_count - 1)
            for index in range(frame_count)
        ]

    span = max(
        max(abs(value) for value in chaser_x_values),
        max(abs(value) for value in chaser_y_values),
        1.0,
    )
    maneuver_offsets = {
        "no_action": 0.0,
        "monitor": 0.0,
        "small_maneuver": span * 0.12,
        "major_maneuver": span * 0.25,
    }
    max_offset = maneuver_offsets.get(displayed_action, 0.0)

    final_chaser_x = chaser_x_values[-1]
    final_chaser_y = chaser_y_values[-1]
    away_x = -final_chaser_x
    away_y = -final_chaser_y
    away_length = max((away_x**2 + away_y**2) ** 0.5, 1.0)
    away_x /= away_length
    away_y /= away_length
    target_end_x = away_x * max_offset
    target_end_y = away_y * max_offset

    margin = span * 0.35 + max_offset
    x_min = min(0, target_end_x, min(chaser_x_values)) - margin
    x_max = max(0, target_end_x, max(chaser_x_values)) + margin
    y_min = min(0, target_end_y, min(chaser_y_values)) - margin
    y_max = max(0, target_end_y, max(chaser_y_values)) + margin

    star_rng = random.Random(12000 + int(event_id))
    star_x = [star_rng.uniform(x_min, x_max) for _ in range(180)]
    star_y = [star_rng.uniform(y_min, y_max) for _ in range(180)]
    star_size = [star_rng.uniform(2, 12) for _ in range(180)]
    star_alpha = [star_rng.uniform(0.25, 0.85) for _ in range(180)]
    star_colors = [
        "#ffffff" if star_rng.random() > 0.35 else "#9aa6b2"
        for _ in range(180)
    ]

    fig, ax = plt.subplots(figsize=(9, 7), facecolor="#030711")

    # This animation is a visual decision-support aid, not a physical orbital
    # maneuver simulation.
    def _draw_space_background() -> None:
        ax.set_facecolor("#030711")
        ax.scatter(
            star_x,
            star_y,
            s=star_size,
            c=star_colors,
            alpha=star_alpha,
            linewidths=0,
            zorder=0,
        )

    def _draw_satellite(x_position: float, y_position: float) -> None:
        satellite_scale = span * 0.045
        body_width = satellite_scale * 0.9
        body_height = satellite_scale * 1.1
        panel_width = satellite_scale * 1.6
        panel_height = satellite_scale * 0.55

        ax.add_patch(
            Rectangle(
                (x_position - body_width / 2, y_position - body_height / 2),
                body_width,
                body_height,
                facecolor="#d8dee9",
                edgecolor="#ffffff",
                linewidth=1.0,
                zorder=5,
            )
        )
        ax.add_patch(
            Rectangle(
                (
                    x_position - body_width / 2 - panel_width,
                    y_position - panel_height / 2,
                ),
                panel_width,
                panel_height,
                facecolor="#4f8fd8",
                edgecolor="#b9d8ff",
                linewidth=0.8,
                zorder=4,
            )
        )
        ax.add_patch(
            Rectangle(
                (
                    x_position + body_width / 2,
                    y_position - panel_height / 2,
                ),
                panel_width,
                panel_height,
                facecolor="#4f8fd8",
                edgecolor="#b9d8ff",
                linewidth=0.8,
                zorder=4,
            )
        )
        ax.add_patch(
            Circle(
                (x_position, y_position),
                radius=satellite_scale * 0.18,
                facecolor="#ffd166",
                edgecolor="#fff4c2",
                linewidth=0.7,
                zorder=6,
            )
        )
        ax.annotate(
            "Target satellite",
            xy=(x_position, y_position),
            xytext=(12, 14),
            textcoords="offset points",
            color="#eef5ff",
            fontsize=10,
            weight="bold",
        )

    def _frame_target_position(frame_index: int) -> tuple[float, float]:
        frame_count = len(event_observations)
        maneuver_start = int(frame_count * 0.75)
        if frame_index < maneuver_start or max_offset == 0:
            return 0.0, 0.0

        denominator = max(frame_count - maneuver_start - 1, 1)
        progress = (frame_index - maneuver_start) / denominator
        offset = max_offset * progress
        return away_x * offset, away_y * offset

    def _update(frame_index: int) -> None:
        ax.clear()
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect("equal", adjustable="datalim")
        _draw_space_background()

        current_x = chaser_x_values[frame_index]
        current_y = chaser_y_values[frame_index]
        target_x, target_y = _frame_target_position(frame_index)

        ax.plot(
            chaser_x_values[: frame_index + 1],
            chaser_y_values[: frame_index + 1],
            color="#c9d6e3",
            linestyle="--",
            linewidth=1.4,
            alpha=0.55,
            zorder=1,
        )
        ax.plot(
            [target_x, current_x],
            [target_y, current_y],
            color="#c9d6e3",
            linestyle="--",
            linewidth=1.2,
            alpha=0.65,
            zorder=2,
        )

        _draw_satellite(target_x, target_y)

        if max_offset > 0 and (target_x != 0 or target_y != 0):
            ax.plot(
                [0, target_x],
                [0, target_y],
                color=action_color,
                linestyle="--",
                linewidth=1.4,
                alpha=0.65,
                zorder=3,
            )

        ax.scatter(
            current_x,
            current_y,
            s=900,
            color=action_color,
            alpha=0.16,
            linewidths=0,
            zorder=3,
        )
        ax.scatter(
            current_x,
            current_y,
            s=150,
            color="#ff6b35",
            edgecolor="#ffd1b3",
            linewidth=1.2,
            zorder=6,
        )
        ax.annotate(
            "Chaser object",
            xy=(current_x, current_y),
            xytext=(12, 14),
            textcoords="offset points",
            color="#ffd1b3",
            fontsize=10,
            weight="bold",
        )

        current_time_to_tca = event_observations.iloc[frame_index]["time_to_tca"]
        info_lines = [
            f"event_id: {event_id}",
            f"time_to_tca: {current_time_to_tca:.4f}",
            f"displayed_action: {displayed_action}",
            f"risk_score: {processed_row['risk_score']:.4f}",
            "Chaser path is smoothed for visualization",
        ]
        if use_ml_recommendation and "ml_risk_score" in processed_df.columns:
            info_lines.append(f"{risk_label}: {risk_value:.4f}")
        info_text = "\n".join(info_lines)
        ax.text(
            0.02,
            0.98,
            info_text,
            transform=ax.transAxes,
            va="top",
            color="#f4f7fb",
            fontsize=10,
            linespacing=1.45,
            bbox={
                "boxstyle": "round,pad=0.55",
                "facecolor": "#101826",
                "edgecolor": action_color,
                "alpha": 0.9,
            },
        )

        action_messages = {
            "no_action": "No maneuver",
            "monitor": "Monitoring event",
            "small_maneuver": "Small visual maneuver",
            "major_maneuver": "Major visual maneuver",
        }
        action_message = action_messages.get(displayed_action)
        if action_message:
            ax.text(
                0.5,
                0.08,
                action_message,
                transform=ax.transAxes,
                ha="center",
                color=action_color,
                fontsize=11,
                weight="bold",
            )

        ax.text(
            0.5,
            0.02,
            "Visual demo, not a physical orbital simulation",
            transform=ax.transAxes,
            ha="center",
            color="#c9d6e3",
            fontsize=9,
            alpha=0.85,
        )
        ax.set_title(
            f"Event {event_id} - Recommended action: {displayed_action}",
            color=action_color,
            fontsize=14,
            weight="bold",
            pad=14,
        )
        ax.set_xlabel("Relative position R", color="#d8dee9")
        ax.set_ylabel("Relative position T", color="#d8dee9")
        ax.tick_params(colors="#b8c2cc")
        for spine in ax.spines.values():
            spine.set_color("#415063")
        ax.grid(True, color="#2f3b4d", alpha=0.45, linestyle=":")

    animation = FuncAnimation(
        fig,
        _update,
        frames=len(event_observations),
        interval=130,
        repeat=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames_per_second = 1000 / frame_duration_ms
    animation.save(output_path, writer=PillowWriter(fps=frames_per_second), dpi=130)
    plt.close(fig)
