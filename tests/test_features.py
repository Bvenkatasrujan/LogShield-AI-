import pytest
import pandas as pd
from src.features import extract_features


def test_extract_features_grouping():
    logs = pd.DataFrame([
        {"timestamp": pd.to_datetime("2026-09-21 10:00:00"), "ip": "192.168.1.50", "user": "u1", "event": "LOGIN", "status": "FAILED"},
        {"timestamp": pd.to_datetime("2026-09-21 10:00:01"), "ip": "192.168.1.50", "user": "u1", "event": "LOGIN", "status": "FAILED"},
        {"timestamp": pd.to_datetime("2026-09-21 10:00:02"), "ip": "192.168.1.50", "user": "u1", "event": "LOGIN", "status": "SUCCESS"},
        {"timestamp": pd.to_datetime("2026-09-21 10:00:00"), "ip": "192.168.1.10", "user": "u2", "event": "LOGIN", "status": "SUCCESS"},
    ])

    features = extract_features(logs)
    assert len(features) == 2

    ip_50 = features[features["ip"] == "192.168.1.50"].iloc[0]
    assert ip_50["total_events"] == 3
    assert ip_50["failed_logins"] == 2
    assert ip_50["successful_events"] == 1
    assert pytest.approx(ip_50["failure_ratio"], 0.01) == 2 / 3
