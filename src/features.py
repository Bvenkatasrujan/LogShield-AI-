import pandas as pd


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms clean event log records into IP-centric numerical features
    suitable for rule evaluation and machine learning models.

    Parameters:
        df: Cleaned pandas DataFrame of log events

    Returns:
        DataFrame aggregated per IP with numerical features:
        - total_events
        - failed_logins
        - successful_events
        - failure_ratio
        - unique_users
        - event_frequency (events per minute)
    """
    if df.empty:
        return pd.DataFrame(columns=[
            "ip", "total_events", "failed_logins", "successful_events",
            "failure_ratio", "unique_users", "event_frequency"
        ])

    df = df.copy()

    # Aggregate key metrics per IP
    grouped = df.groupby("ip")

    features = grouped.agg(
        total_events=("event", "count"),
        failed_logins=("status", lambda x: (x.astype(str).str.upper() == "FAILED").sum()),
        successful_events=("status", lambda x: (x.astype(str).str.upper() == "SUCCESS").sum()),
        unique_users=("user", "nunique") if "user" in df.columns else ("ip", lambda x: 1)
    ).reset_index()

    # Calculate failure ratio
    features["failure_ratio"] = (
        features["failed_logins"] / features["total_events"]
    ).fillna(0.0)

    # Calculate event frequency (events per minute for each IP)
    def calc_freq(group):
        if len(group) <= 1 or "timestamp" not in group.columns:
            return float(len(group))
        min_time = group["timestamp"].min()
        max_time = group["timestamp"].max()
        duration_minutes = (max_time - min_time).total_seconds() / 60.0
        if duration_minutes <= 0:
            duration_minutes = 1.0
        return round(len(group) / duration_minutes, 2)

    freq_df = df.groupby("ip").apply(calc_freq, include_groups=False).reset_index(name="event_frequency")
    features = pd.merge(features, freq_df, on="ip", how="left")
    features["event_frequency"] = features["event_frequency"].fillna(features["total_events"].astype(float))

    return features
