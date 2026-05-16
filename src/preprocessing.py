"""Preprocessing utilities for satellite conjunction event data."""

from __future__ import annotations

import pandas as pd


def create_event_level_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Create one representative row per conjunction event.

    The original dataset contains multiple observations for the same
    ``event_id``. Each observation describes the same event at a different
    ``time_to_tca`` value.

    This event-level dataset keeps one representative observation per event:
    the row with the smallest non-negative ``time_to_tca``. In operational
    terms, this is the closest available observation before the time of
    closest approach.

    Parameters
    ----------
    df:
        Input observation-level dataset. It must contain ``event_id`` and
        ``time_to_tca`` columns.

    Returns
    -------
    pandas.DataFrame
        Event-level DataFrame containing one row per ``event_id`` that has at
        least one non-negative ``time_to_tca`` observation.
    """
    required_columns = {"event_id", "time_to_tca"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    # Keep only observations before or at closest approach.
    non_negative_tca = df[df["time_to_tca"] >= 0].copy()

    # Sort so the first row for each event is the closest available
    # observation before the time of closest approach.
    event_level_df = (
        non_negative_tca.sort_values(["event_id", "time_to_tca"])
        .groupby("event_id", as_index=False)
        .first()
    )

    return event_level_df


def add_probability_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add probability-like features derived from log10 risk columns.

    The ``risk`` and ``max_risk_estimate`` columns are represented on a log10
    scale. This function converts them into probability-like features for
    easier interpretation:

    - ``collision_probability = 10 ** risk``
    - ``max_collision_probability = 10 ** max_risk_estimate``

    Parameters
    ----------
    df:
        Input dataset. It must contain ``risk`` and ``max_risk_estimate``
        columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with the two derived probability columns.
    """
    required_columns = {"risk", "max_risk_estimate"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_probabilities = df.copy()
    df_with_probabilities["collision_probability"] = (
        10.0 ** df_with_probabilities["risk"]
    )
    df_with_probabilities["max_collision_probability"] = (
        10.0 ** df_with_probabilities["max_risk_estimate"]
    )

    return df_with_probabilities


def add_operational_risk_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add distance and urgency risk features for operational interpretation.

    ``distance_risk`` is an inverted min-max normalization of
    ``miss_distance``. The direction is inverted because smaller miss
    distances represent closer approaches and therefore higher operational
    risk.

    ``urgency`` is an inverted min-max normalization of ``time_to_tca``. The
    direction is inverted because smaller time-to-closest-approach values mean
    less time remains to act and therefore higher urgency.

    Parameters
    ----------
    df:
        Input dataset. It must contain ``miss_distance`` and ``time_to_tca``
        columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with ``distance_risk`` and ``urgency``
        columns added.
    """
    required_columns = {"miss_distance", "time_to_tca"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_operational_risk = df.copy()

    min_miss_distance = df_with_operational_risk["miss_distance"].min()
    max_miss_distance = df_with_operational_risk["miss_distance"].max()
    if max_miss_distance == min_miss_distance:
        df_with_operational_risk["distance_risk"] = 0.0
    else:
        # Invert the normalized distance so closer approaches receive
        # higher scores.
        df_with_operational_risk["distance_risk"] = 1 - (
            (
                df_with_operational_risk["miss_distance"] - min_miss_distance
            )
            / (max_miss_distance - min_miss_distance)
        )

    min_time_to_tca = df_with_operational_risk["time_to_tca"].min()
    max_time_to_tca = df_with_operational_risk["time_to_tca"].max()
    if max_time_to_tca == min_time_to_tca:
        df_with_operational_risk["urgency"] = 0.0
    else:
        # Invert the normalized time so events closer to TCA receive
        # higher urgency scores.
        df_with_operational_risk["urgency"] = 1 - (
            (df_with_operational_risk["time_to_tca"] - min_time_to_tca)
            / (max_time_to_tca - min_time_to_tca)
        )

    return df_with_operational_risk


def add_normalized_velocity_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add a normalized relative speed feature.

    ``relative_speed`` is min-max normalized into ``relative_speed_norm`` so
    velocity information is comparable with the other engineered 0-1 risk
    features.

    Parameters
    ----------
    df:
        Input dataset. It must contain a ``relative_speed`` column.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with ``relative_speed_norm`` added.
    """
    required_columns = {"relative_speed"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_velocity = df.copy()

    min_relative_speed = df_with_velocity["relative_speed"].min()
    max_relative_speed = df_with_velocity["relative_speed"].max()
    if max_relative_speed == min_relative_speed:
        df_with_velocity["relative_speed_norm"] = 0.0
    else:
        # Normalize relative speed to the same 0-1 range as the other
        # engineered risk features.
        df_with_velocity["relative_speed_norm"] = (
            df_with_velocity["relative_speed"] - min_relative_speed
        ) / (max_relative_speed - min_relative_speed)

    return df_with_velocity


def add_normalized_risk_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add a normalized log-scale collision risk feature.

    ``risk`` is represented on a log10 scale. Higher values, meaning values
    closer to zero, indicate higher collision risk. ``risk_norm`` converts
    this log-scale risk into a 0-1 feature suitable for scoring while
    preserving that ordering.

    Parameters
    ----------
    df:
        Input dataset. It must contain a ``risk`` column.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with ``risk_norm`` added.
    """
    required_columns = {"risk"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_risk = df.copy()

    min_risk = df_with_risk["risk"].min()
    max_risk = df_with_risk["risk"].max()
    if max_risk == min_risk:
        df_with_risk["risk_norm"] = 0.0
    else:
        # Min-max normalization maps higher log10 risk values, which are
        # closer to zero and therefore riskier, to higher 0-1 scores.
        df_with_risk["risk_norm"] = (
            df_with_risk["risk"] - min_risk
        ) / (max_risk - min_risk)

    return df_with_risk


def add_synthetic_decision_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add synthetic decision-support features for fuel cost and priority.

    The original dataset does not contain explicit fuel cost or mission
    priority variables. This function creates synthetic decision-support
    features for those concepts so the later recommendation system can model
    a more realistic operational trade-off.

    Because these variables are synthetic assumptions rather than observed
    measurements, this assumption must be documented in the project report.

    Parameters
    ----------
    df:
        Input dataset. It must contain ``relative_speed_norm``, ``urgency``,
        and ``mission_id`` columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with ``fuel_cost`` and
        ``mission_priority`` added.
    """
    required_columns = {"relative_speed_norm", "urgency", "mission_id"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_synthetic_features = df.copy()

    # Fuel cost is synthetic because the source data has no explicit
    # maneuver cost, delta-v, or propellant usage column.
    df_with_synthetic_features["fuel_cost"] = (
        0.6 * df_with_synthetic_features["relative_speed_norm"]
        + 0.4 * df_with_synthetic_features["urgency"]
    ).clip(0, 1)

    # Mission priority is synthetic because the source data has only a
    # mission identifier, not an explicit priority or criticality score.
    df_with_synthetic_features["mission_priority"] = 0.5 + 0.5 * (
        (df_with_synthetic_features["mission_id"] % 5) / 4
    )

    return df_with_synthetic_features


def add_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """Add an overall conjunction-event severity score.

    ``risk_score`` represents the overall physical severity of the conjunction
    event based on normalized risk, distance, urgency, velocity, and mission
    priority features.

    ``fuel_cost`` is intentionally not included in ``risk_score`` because fuel
    cost affects action desirability, not physical collision severity. It will
    be used later in action scoring.

    Parameters
    ----------
    df:
        Input dataset. It must contain ``risk_norm``, ``distance_risk``,
        ``urgency``, ``relative_speed_norm``, and ``mission_priority`` columns.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame with ``risk_score`` added.
    """
    required_columns = {
        "risk_norm",
        "distance_risk",
        "urgency",
        "relative_speed_norm",
        "mission_priority",
    }
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required column(s): {missing}")

    df_with_score = df.copy()

    # This score combines severity-related features only. Fuel cost is kept
    # separate for later action desirability scoring.
    df_with_score["risk_score"] = (
        0.35 * df_with_score["risk_norm"]
        + 0.25 * df_with_score["distance_risk"]
        + 0.20 * df_with_score["urgency"]
        + 0.10 * df_with_score["relative_speed_norm"]
        + 0.10 * df_with_score["mission_priority"]
    ).clip(0, 1)

    return df_with_score
