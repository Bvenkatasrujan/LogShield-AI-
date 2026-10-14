import pytest
import pandas as pd
from src.rules import detect_failed_login_attack, calculate_risk, apply_rules


def test_detect_failed_login_attack():
    row_normal = {"failed_logins": 2}
    row_suspicious = {"failed_logins": 6}

    assert detect_failed_login_attack(row_normal) == "Normal"
    assert detect_failed_login_attack(row_suspicious) == "Suspicious"


def test_calculate_risk():
    assert calculate_risk({"failed_logins": 1}) == "LOW"
    assert calculate_risk({"failed_logins": 6}) == "MEDIUM"
    assert calculate_risk({"failed_logins": 12}) == "HIGH"


def test_apply_rules_dataframe():
    df = pd.DataFrame([
        {"ip": "192.168.1.1", "failed_logins": 0},
        {"ip": "192.168.1.2", "failed_logins": 6},
        {"ip": "192.168.1.3", "failed_logins": 15},
    ])
    res = apply_rules(df)
    assert res.iloc[0]["rule_result"] == "Normal"
    assert res.iloc[0]["rule_risk"] == "LOW"
    assert res.iloc[1]["rule_result"] == "Suspicious"
    assert res.iloc[1]["rule_risk"] == "MEDIUM"
    assert res.iloc[2]["rule_result"] == "Suspicious"
    assert res.iloc[2]["rule_risk"] == "HIGH"
