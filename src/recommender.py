"""Action scoring utilities for satellite collision-avoidance support."""

from __future__ import annotations

import pandas as pd


def add_action_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Add candidate action scores without selecting a final recommendation.

    The score definitions encode simple operational preferences:

    - ``no_action`` should dominate low-risk cases.
    - ``monitor`` should dominate medium cases.
    - ``small_maneuver`` should be competitive for medium-high risk when fuel
      cost is not too high.
    - ``major_maneuver`` should be reserved for the most severe cases, where
      risk, urgency, and mission priority are high.

    Parameters
    ----------
    df:
        Input dataset. It must contain ``risk_score``, ``fuel_cost``,
        ``mission_priority``, and ``urgency`` columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with four action-score columns added.
    """
    required_columns = {"risk_score", "fuel_cost", "mission_priority", "urgency"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_scores = df.copy()

    # No action falls off quickly as risk rises, so it dominates only low-risk
    # cases.
    df_with_scores["no_action_score"] = 1 - (
        1.4 * df_with_scores["risk_score"]
    )

    # Monitoring is centered around low-medium to medium risk.
    df_with_scores["monitor_score"] = 1 - (
        abs(df_with_scores["risk_score"] - 0.45) * 1.6
    )

    # A small maneuver is intended for medium-high risk cases where an
    # intervention is useful, but a major maneuver is not yet justified.
    df_with_scores["small_maneuver_score"] = (
        0.82 * df_with_scores["risk_score"]
        + 0.22 * df_with_scores["urgency"]
        - 0.16 * df_with_scores["fuel_cost"]
    )

    # A major maneuver is reserved for the most severe cases. The extra
    # threshold-like term makes it competitive mainly when risk_score is high.
    df_with_scores["major_maneuver_score"] = (
        0.75 * df_with_scores["risk_score"]
        + 0.18 * df_with_scores["urgency"]
        + 0.20 * df_with_scores["mission_priority"]
        - 0.18 * df_with_scores["fuel_cost"]
        + 0.15 * (df_with_scores["risk_score"] > 0.80).astype(float)
    )

    score_columns = [
        "no_action_score",
        "monitor_score",
        "small_maneuver_score",
        "major_maneuver_score",
    ]
    df_with_scores[score_columns] = df_with_scores[score_columns].clip(0, 1)

    return df_with_scores


def add_recommended_action(df: pd.DataFrame) -> pd.DataFrame:
    """Select the recommended action from candidate action scores.

    Action scores estimate the suitability of each candidate action.
    ``recommended_action`` is selected as the action with the highest score.
    If two or more actions have exactly the same highest score, ties are
    resolved by choosing the least aggressive option to avoid unnecessary
    maneuvers.

    Parameters
    ----------
    df:
        Input dataset. It must contain the four action-score columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with ``recommended_action`` added.
    """
    action_score_columns = {
        "no_action_score": "no_action",
        "monitor_score": "monitor",
        "small_maneuver_score": "small_maneuver",
        "major_maneuver_score": "major_maneuver",
    }
    missing_columns = set(action_score_columns).difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_action = df.copy()

    # Columns are ordered from least to most aggressive. Pandas idxmax returns
    # the first maximum, so exact ties choose the least aggressive action.
    ordered_score_columns = list(action_score_columns)
    best_score_column = df_with_action[ordered_score_columns].idxmax(axis=1)
    df_with_action["recommended_action"] = best_score_column.map(
        action_score_columns
    )

    return df_with_action


def add_ml_action_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Add ML-based candidate action scores.

    These scores mirror ``add_action_scores`` but use ``ml_risk_score`` in
    place of ``risk_score``. The original rule-based action scores and
    ``recommended_action`` are kept unchanged for side-by-side comparison.
    """
    required_columns = {"ml_risk_score", "fuel_cost", "mission_priority", "urgency"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")
    score_columns = [
        "ml_no_action_score",
        "ml_monitor_score",
        "ml_small_maneuver_score",
        "ml_major_maneuver_score",
    ]
    existing_score_columns = set(score_columns).intersection(df.columns)
    if existing_score_columns:
        existing = ", ".join(sorted(existing_score_columns))
        raise ValueError(f"Column(s) already exist: {existing}")

    df_with_scores = df.copy()

    df_with_scores["ml_no_action_score"] = 1 - (
        1.4 * df_with_scores["ml_risk_score"]
    )

    df_with_scores["ml_monitor_score"] = 1 - (
        abs(df_with_scores["ml_risk_score"] - 0.45) * 1.6
    )

    df_with_scores["ml_small_maneuver_score"] = (
        0.82 * df_with_scores["ml_risk_score"]
        + 0.22 * df_with_scores["urgency"]
        - 0.16 * df_with_scores["fuel_cost"]
    )

    df_with_scores["ml_major_maneuver_score"] = (
        0.75 * df_with_scores["ml_risk_score"]
        + 0.18 * df_with_scores["urgency"]
        + 0.20 * df_with_scores["mission_priority"]
        - 0.18 * df_with_scores["fuel_cost"]
        + 0.15 * (df_with_scores["ml_risk_score"] > 0.80).astype(float)
    )

    df_with_scores[score_columns] = df_with_scores[score_columns].clip(0, 1)

    return df_with_scores


def add_ml_recommended_action(df: pd.DataFrame) -> pd.DataFrame:
    """Select the ML-based recommended action from ML action scores.

    ``ml_recommended_action`` uses the model-predicted risk layer, while the
    original ``recommended_action`` remains the rule-based baseline using the
    dataset risk. Exact ties are resolved by choosing the least aggressive
    action.
    """
    action_score_columns = {
        "ml_no_action_score": "no_action",
        "ml_monitor_score": "monitor",
        "ml_small_maneuver_score": "small_maneuver",
        "ml_major_maneuver_score": "major_maneuver",
    }
    missing_columns = set(action_score_columns).difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")
    if "ml_recommended_action" in df.columns:
        raise ValueError("Column already exists: ml_recommended_action")

    df_with_action = df.copy()

    ordered_score_columns = list(action_score_columns)
    best_score_column = df_with_action[ordered_score_columns].idxmax(axis=1)
    df_with_action["ml_recommended_action"] = best_score_column.map(
        action_score_columns
    )

    return df_with_action
