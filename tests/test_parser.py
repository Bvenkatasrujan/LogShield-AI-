import pytest
import pandas as pd
import io
from src.parser import load_log_file


def test_load_log_file_from_csv_path():
    df = load_log_file("data/sample_logs.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "timestamp" in df.columns
    assert "ip" in df.columns


def test_load_log_file_from_buffer():
    csv_data = "timestamp,ip,user,event,status\n2026-09-21 10:00:00,192.168.1.1,user1,LOGIN,SUCCESS"
    buffer = io.StringIO(csv_data)
    df = load_log_file(buffer)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["ip"] == "192.168.1.1"
