import pandas as pd


def prepare_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts timestamp column to pandas datetime object and drops invalid datetime rows.
    """
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
    return df


def clean_logs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw log DataFrame by:
    - Removing duplicate entries
    - Dropping missing values in essential columns (timestamp, ip, event, status)
    - Stripping trailing whitespace from text fields
    - Converting timestamps to valid datetime objects

    Parameters:
        df: Raw pandas DataFrame

    Returns:
        Cleaned pandas DataFrame
    """
    df = df.copy()

    # Drop duplicate records
    df = df.drop_duplicates()

    # Drop rows missing essential fields
    required_cols = ["timestamp", "ip", "event", "status"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns in log file: {missing_cols}")

    df = df.dropna(subset=required_cols)

    # Clean text columns
    for col in ["ip", "user", "event", "status"]:
        if col in df.columns and df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    # Ensure timestamp is parsed properly
    df = prepare_timestamp(df)

    return df
