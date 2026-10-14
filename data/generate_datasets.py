import csv
import random
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_brute_force_logs():
    """Generates a dataset simulating a brute-force attack from multiple attacker IPs."""
    filepath = os.path.join(DATA_DIR, "brute_force_logs.csv")
    base_time = datetime(2026, 9, 21, 10, 0, 0)
    
    rows = [["timestamp", "ip", "user", "event", "status"]]
    
    # Normal users
    normal_ips = [f"192.168.1.{i}" for i in range(10, 20)]
    for i in range(50):
        t = base_time + timedelta(seconds=i * 10)
        ip = random.choice(normal_ips)
        user = f"user_{ip.split('.')[-1]}"
        event = random.choice(["LOGIN", "FILE_ACCESS", "API_REQUEST"])
        rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), ip, user, event, "SUCCESS"])

    # Attacker 1: 15 rapid failed logins (High Risk)
    attacker1_ip = "192.168.1.150"
    for i in range(15):
        t = base_time + timedelta(seconds=100 + i * 2)
        rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), attacker1_ip, "admin", "LOGIN", "FAILED"])

    # Attacker 2: 7 failed logins (Medium Risk)
    attacker2_ip = "192.168.1.160"
    for i in range(7):
        t = base_time + timedelta(seconds=150 + i * 3)
        rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), attacker2_ip, "root", "LOGIN", "FAILED"])

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Generated {filepath} ({len(rows)-1} records)")


def generate_high_frequency_logs():
    """Generates a dataset simulating API flooding / DDoS high request rate per IP."""
    filepath = os.path.join(DATA_DIR, "high_frequency_logs.csv")
    base_time = datetime(2026, 9, 21, 11, 0, 0)
    
    rows = [["timestamp", "ip", "user", "event", "status"]]
    
    # Normal activity
    for i in range(30):
        t = base_time + timedelta(seconds=i * 15)
        rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), "192.168.1.12", "user_12", "API_REQUEST", "SUCCESS"])

    # High frequency bot activity: 150 requests in 1 minute
    bot_ip = "192.168.1.200"
    for i in range(150):
        t = base_time + timedelta(seconds=i % 60)
        rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), bot_ip, "bot_client", "API_REQUEST", "SUCCESS"])

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Generated {filepath} ({len(rows)-1} records)")


def generate_benchmark_10k():
    """Generates 10,000 synthetic log records for speed and scalability testing."""
    filepath = os.path.join(DATA_DIR, "benchmark_10k.csv")
    base_time = datetime(2026, 9, 21, 0, 0, 0)
    
    rows = [["timestamp", "ip", "user", "event", "status"]]
    
    ips = [f"192.168.1.{i}" for i in range(1, 101)]
    users = [f"user_{i}" for i in range(1, 51)]
    events = ["LOGIN", "LOGOUT", "FILE_ACCESS", "API_REQUEST", "PASSWORD_RESET"]
    statuses = ["SUCCESS"] * 8 + ["FAILED"] * 2  # 80% success, 20% failed overall

    for i in range(10000):
        t = base_time + timedelta(seconds=i * 3)
        ip = random.choice(ips)
        user = random.choice(users)
        event = random.choice(events)
        status = random.choice(statuses)
        rows.append([t.strftime("%Y-%m-%d %H:%M:%S"), ip, user, event, status])

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Generated {filepath} ({len(rows)-1} records)")


if __name__ == "__main__":
    generate_brute_force_logs()
    generate_high_frequency_logs()
    generate_benchmark_10k()
