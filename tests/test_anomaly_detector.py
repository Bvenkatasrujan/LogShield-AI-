import pytest
import pandas as pd
from src.anomaly_detector import detect_anomalies


def test_detect_anomalies_isolation_forest():
    # Synthetic feature dataset with obvious normal baseline + 1 anomaly
    normal_data = [
        {"ip": f"192.168.1.{i}", "total_events": 5, "failed_logins": 0, "successful_events": 5, "failure_ratio": 0.0}
        for i in range(10, 20)
    ]
    anomaly_data = [
        {"ip": "192.168.1.99", "total_events": 100, "failed_logins": 80, "successful_events": 20, "failure_ratio": 0.8}
    ]

    features = pd.DataFrame(normal_data + anomaly_data)
    results = detect_anomalies(features, contamination=0.1)

    assert "prediction" in results.columns
    assert "ai_result" in results.columns
    assert len(results) == 11
    
    # Check that anomaly output values are either 'Normal' or 'Anomaly'
    assert set(results["ai_result"].unique()).issubset({"Normal", "Anomaly"})
