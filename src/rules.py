import pandas as pd


def detect_failed_login_attack(row: pd.Series) -> str:
    """
    Evaluates rule for failed login brute-force attempt.

    Parameters:
        row: Series or dict containing 'failed_logins'

    Returns:
        "Suspicious" if failed_logins >= 5, else "Normal"
    """
    failed = row.get("failed_logins", 0)
    if failed >= 5:
        return "Suspicious"
    return "Normal"


def calculate_risk(row: pd.Series) -> str:
    """
    Categorizes threat risk level based on failed login threshold.

    Parameters:
        row: Series or dict containing 'failed_logins'

    Returns:
        "HIGH" (failed_logins >= 10), "MEDIUM" (failed_logins >= 5), else "LOW"
    """
    failed = row.get("failed_logins", 0)
    if failed >= 10:
        return "HIGH"
    elif failed >= 5:
        return "MEDIUM"
    return "LOW"


def apply_rules(features: pd.DataFrame) -> pd.DataFrame:
    """
    Applies rule-based detection and risk level evaluation across all feature rows.

    Parameters:
        features: Aggregated features DataFrame per IP

    Returns:
        DataFrame with 'rule_result' and 'rule_risk' columns appended.
    """
    df = features.copy()
    if df.empty:
        df["rule_result"] = []
        df["rule_risk"] = []
        return df

    df["rule_result"] = df.apply(detect_failed_login_attack, axis=1)
    df["rule_risk"] = df.apply(calculate_risk, axis=1)
    return df
