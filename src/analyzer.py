import pandas as pd
from typing import Union, BinaryIO, Dict, Any

from src.parser import load_log_file
from src.cleaner import clean_logs
from src.features import extract_features
from src.rules import apply_rules
from src.anomaly_detector import detect_anomalies


def calculate_final_assessment(row: pd.Series) -> str:
    """
    Combines Rule Result and AI Result into unified assessment:
    - Suspicious + Anomaly => High Attention
    - Normal + Anomaly => Investigate
    - Suspicious + Normal => Suspicious
    - Normal + Normal => Normal
    """
    rule = row.get("rule_result", "Normal")
    ai = row.get("ai_result", "Normal")

    if rule == "Suspicious" and ai == "Anomaly":
        return "High Attention"
    elif rule == "Normal" and ai == "Anomaly":
        return "Investigate"
    elif rule == "Suspicious" and ai == "Normal":
        return "Suspicious"
    else:
        return "Normal"


def calculate_combined_risk(row: pd.Series) -> str:
    """
    Combines rule risk and final assessment into final risk level (HIGH, MEDIUM, LOW).
    """
    rule_risk = row.get("rule_risk", "LOW")
    assessment = row.get("final_assessment", "Normal")

    if rule_risk == "HIGH" or assessment == "High Attention":
        return "HIGH"
    elif rule_risk == "MEDIUM" or assessment in ["Investigate", "Suspicious"]:
        return "MEDIUM"
    else:
        return "LOW"


def analyze_logs(file_input: Union[str, BinaryIO, pd.DataFrame]) -> Dict[str, Any]:
    """
    End-to-end log analysis workflow pipeline:
    Log File -> Parser -> Cleaner -> Features -> Rules -> AI -> Final Assessment & Risk

    Parameters:
        file_input: File path, file-like buffer, or raw DataFrame

    Returns:
        Dict containing:
        - 'raw_logs': cleaned DataFrame of raw log entries
        - 'results': aggregated per-IP DataFrame with features, rule results, AI results, and final risk
        - 'total_events': int count of events processed
        - 'unique_ips': int count of unique IP addresses
        - 'anomaly_count': int count of detected anomalies
    """
    raw_df = load_log_file(file_input)
    cleaned_df = clean_logs(raw_df)
    features_df = extract_features(cleaned_df)
    features_with_rules = apply_rules(features_df)
    results_df = detect_anomalies(features_with_rules)

    if not results_df.empty:
        results_df["final_assessment"] = results_df.apply(calculate_final_assessment, axis=1)
        results_df["final_risk"] = results_df.apply(calculate_combined_risk, axis=1)
    else:
        results_df["final_assessment"] = []
        results_df["final_risk"] = []

    anomaly_count = (results_df["ai_result"] == "Anomaly").sum() if not results_df.empty else 0

    return {
        "raw_logs": cleaned_df,
        "results": results_df,
        "total_events": len(cleaned_df),
        "unique_ips": len(results_df),
        "anomaly_count": int(anomaly_count)
    }
