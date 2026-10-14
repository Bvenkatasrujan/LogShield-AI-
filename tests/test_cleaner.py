import pytest
import pandas as pd
from src.cleaner import clean_logs, prepare_timestamp


def test_clean_logs_removes_duplicates_and_missing():
    raw_data = pd.DataFrame([
        {"timestamp": "2026-09-21 10:00:00", "ip": "192.168.1.10", "event": "LOGIN", "status": "SUCCESS"},
        {"timestamp": "2026-09-21 10:00:00", "ip": "192.168.1.10", "event": "LOGIN", "status": "SUCCESS"},  # Duplicate
        {"timestamp": "2026-09-21 10:01:00", "ip": None, "event": "LOGIN", "status": "FAILED"},           # Missing IP
        {"timestamp": "invalid_date", "ip": "192.168.1.12", "event": "LOGIN", "status": "FAILED"},          # Invalid Timestamp
    ])

    cleaned = clean_logs(raw_data)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["ip"] == "192.168.1.10"


def test_prepare_timestamp_conversion():
    df = pd.DataFrame({"timestamp": ["2026-09-21 10:00:00", "bad_date"]})
    res = prepare_timestamp(df)
    assert len(res) == 1
    assert pd.api.types.is_datetime64_any_dtype(res["timestamp"])
