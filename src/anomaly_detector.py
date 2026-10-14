import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(features: pd.DataFrame, contamination: float = 0.1, random_state: int = 42) -> pd.DataFrame:
    """
    Uses unsupervised Machine Learning (Isolation Forest) to detect anomalies in log features.

    Parameters:
        features: Aggregated features DataFrame per IP
        contamination: Proportion of anomalies expected in dataset (default: 0.1)
        random_state: Random seed for reproducible results (default: 42)

    Returns:
        DataFrame with 'prediction' (-1 for anomaly, 1 for normal) and 'ai_result' columns.
    """
    df = features.copy()

    columns = [
        "total_events",
        "failed_logins",
        "successful_events",
        "failure_ratio"
    ]

    # Ensure all required feature columns exist
    for col in columns:
        if col not in df.columns:
            df[col] = 0

    if df.empty:
        df["prediction"] = []
        df["ai_result"] = []
        return df

    # Adjust contamination dynamically if dataset is small
    n_samples = len(df)
    if n_samples < 5:
        # For very small datasets, use simple heuristic boundary for IsolationForest or adjusted contamination
        effective_contamination = min(0.5, max(0.1, 1.0 / n_samples))
    else:
        effective_contamination = contamination

    model = IsolationForest(
        contamination=effective_contamination,
        random_state=random_state
    )

    df["prediction"] = model.fit_predict(df[columns])
    df["ai_result"] = df["prediction"].apply(
        lambda x: "Anomaly" if x == -1 else "Normal"
    )

    return df
