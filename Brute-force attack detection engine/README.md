# 🚨 Brute-force Attack Detection Engine

> *"Every failed login attempt tells a story. Security monitoring helps identify when that story becomes an attack."*

---

# 📖 Overview

The **Brute-force Attack Detection Engine** is a Python-based security monitoring tool that analyzes authentication logs and detects suspicious login activity indicative of brute-force attacks.

This project demonstrates how security analysts and SOC teams identify malicious authentication attempts using threshold-based detection logic and automated alerting.

---

# 🎯 Learning Objectives

By completing this lab, you will:

* 🔍 Analyze authentication log files
* 🛡️ Detect brute-force attack patterns
* 📊 Monitor failed login attempts by IP address
* 🚨 Generate security alerts automatically
* 📝 Save alerts for auditing and investigation
* ⚙️ Understand basic security monitoring workflows

---

# 🛠️ Prerequisites

Before starting, ensure you have:

* Linux machine (Ubuntu recommended)
* Python 3.x installed
* Basic Linux command-line knowledge
* Understanding of authentication concepts
* Familiarity with Python fundamentals

---

# 🏗️ Environment Setup

## Step 1: Update System

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

---

## Step 2: Create Lab Directory

```bash
mkdir ~/brute-force-lab
cd ~/brute-force-lab
```

---

## Step 3: Create Sample Authentication Log

```bash
cat > auth.log << 'EOF'
2024-01-15 10:23:45 SUCCESS user=alice ip=192.168.1.100
2024-01-15 10:24:12 FAILED user=admin ip=203.0.113.45
2024-01-15 10:24:18 FAILED user=admin ip=203.0.113.45
2024-01-15 10:24:25 FAILED user=admin ip=203.0.113.45
2024-01-15 10:24:31 FAILED user=admin ip=203.0.113.45
2024-01-15 10:24:38 FAILED user=admin ip=203.0.113.45
2024-01-15 10:25:02 SUCCESS user=bob ip=192.168.1.101
2024-01-15 10:25:45 FAILED user=root ip=198.51.100.23
2024-01-15 10:25:52 FAILED user=root ip=198.51.100.23
2024-01-15 10:26:01 FAILED user=root ip=198.51.100.23
2024-01-15 10:26:08 FAILED user=root ip=198.51.100.23
2024-01-15 10:27:15 SUCCESS user=charlie ip=192.168.1.102
2024-01-15 10:28:33 FAILED user=admin ip=203.0.113.45
2024-01-15 10:28:40 FAILED user=admin ip=203.0.113.45
2024-01-15 10:28:47 FAILED user=admin ip=203.0.113.45
EOF
```

---

# 📚 Task 1: Build the Detection Engine

## Create Main Script

```bash
nano detector.py
```

---

## Detection Engine Source Code

```python
#!/usr/bin/env python3

"""
Brute-force Attack Detection Engine
Analyzes authentication logs to detect suspicious login patterns
"""

from datetime import datetime
from collections import defaultdict


class BruteForceDetector:

    def __init__(self, threshold=5, time_window=300):

        self.threshold = threshold
        self.time_window = time_window

        self.failed_attempts = defaultdict(list)
        self.alerts = []

    def parse_log_line(self, line):

        parts = line.strip().split()

        if len(parts) < 5:
            return None

        try:
            timestamp_str = f"{parts[0]} {parts[1]}"
            timestamp = datetime.strptime(
                timestamp_str,
                "%Y-%m-%d %H:%M:%S"
            )

            status = parts[2]
            user = parts[3].split("=")[1]
            ip = parts[4].split("=")[1]

            return {
                "timestamp": timestamp,
                "status": status,
                "user": user,
                "ip": ip
            }

        except Exception as e:
            print(f"Parse Error: {e}")
            return None

    def analyze_attempt(self, log_entry):

        if not log_entry:
            return

        if log_entry["status"] == "FAILED":

            ip = log_entry["ip"]

            self.failed_attempts[ip].append({
                "timestamp": log_entry["timestamp"],
                "user": log_entry["user"]
            })

            self.check_for_attack(ip)

    def check_for_attack(self, ip):

        attempts = self.failed_attempts[ip]

        if len(attempts) < self.threshold:
            return

        recent = attempts[-self.threshold:]

        first_time = recent[0]["timestamp"]
        last_time = recent[-1]["timestamp"]

        duration = (
            last_time - first_time
        ).total_seconds()

        if duration <= self.time_window:

            alert = {
                "ip": ip,
                "attempts": len(attempts),
                "users_targeted":
                    list(set(
                        a["user"]
                        for a in attempts
                    )),
                "first_attempt": first_time,
                "last_attempt": last_time
            }

            if not any(
                a["ip"] == ip
                for a in self.alerts
            ):
                self.alerts.append(alert)
                self.raise_alert(alert)

    def raise_alert(self, alert):

        print("\n" + "=" * 60)
        print("SECURITY ALERT: Brute-force Attack Detected!")
        print("=" * 60)
        print(f"Source IP: {alert['ip']}")
        print(f"Failed Attempts: {alert['attempts']}")
        print(
            f"Targeted Users: "
            f"{', '.join(alert['users_targeted'])}"
        )
        print(
            f"Attack Duration: "
            f"{alert['first_attempt']} "
            f"to "
            f"{alert['last_attempt']}"
        )
        print("=" * 60)

    def process_log_file(self, filename):

        print(f"Analyzing: {filename}")

        with open(filename, "r") as file:

            for line in file:

                log_entry = self.parse_log_line(line)

                self.analyze_attempt(log_entry)

        self.print_summary()

    def print_summary(self):

        print("\n" + "=" * 60)
        print("DETECTION SUMMARY")
        print("=" * 60)

        print(
            f"Total IPs analyzed: "
            f"{len(self.failed_attempts)}"
        )

        print(
            f"Attacks detected: "
            f"{len(self.alerts)}"
        )

        if self.alerts:

            print("\nSuspicious IP Addresses:")

            for alert in self.alerts:
                print(
                    f"- {alert['ip']} "
                    f"({alert['attempts']} attempts)"
                )

        else:
            print("No attacks detected.")

        print("=" * 60)


def main():

    detector = BruteForceDetector(
        threshold=5,
        time_window=300
    )

    detector.process_log_file("auth.log")


if __name__ == "__main__":
    main()
```

---

# 🚀 Execute the Detection Engine

```bash
chmod +x detector.py
python3 detector.py
```

---

# 📊 Expected Output

```text
Analyzing log file: auth.log
Detection threshold: 5 failed attempts
Time window: 300 seconds

============================================================
SECURITY ALERT: Brute-force Attack Detected!
============================================================
Source IP: 203.0.113.45
Total Failed Attempts: 8
Targeted Users: admin
Attack Duration:
2024-01-15 10:24:12
to
2024-01-15 10:28:47
============================================================

============================================================
DETECTION SUMMARY
============================================================
Total IPs analyzed: 2
Attacks detected: 1
============================================================
```

---

# 📁 Task 2: Alert Logging

## Add Alert Saving Function

```python
def save_alerts_to_file(
    self,
    filename="alerts.log"
):

    with open(filename, "w") as f:

        f.write(
            "BRUTE-FORCE ATTACK REPORT\n"
        )

        f.write("=" * 60 + "\n\n")

        for i, alert in enumerate(
            self.alerts,
            start=1
        ):

            f.write(
                f"Alert #{i}\n"
            )

            f.write(
                f"IP Address: "
                f"{alert['ip']}\n"
            )

            f.write(
                f"Failed Attempts: "
                f"{alert['attempts']}\n"
            )

            f.write(
                f"Targeted Users: "
                f"{', '.join(alert['users_targeted'])}\n"
            )

            f.write(
                f"Time Range: "
                f"{alert['first_attempt']} "
                f"to "
                f"{alert['last_attempt']}\n"
            )

            f.write(
                "-" * 60 + "\n"
            )

    print(
        f"Alerts saved to {filename}"
    )
```

---

## Update Main Function

```python
def main():

    detector = BruteForceDetector(
        threshold=5,
        time_window=300
    )

    detector.process_log_file(
        "auth.log"
    )

    if detector.alerts:
        detector.save_alerts_to_file(
            "alerts.log"
        )
```

---

# 📄 View Saved Alerts

```bash
cat alerts.log
```

---

# ✅ Verification

## Verify Attack Source

```bash
grep "203.0.113.45" auth.log | wc -l
```

Expected:

```text
8
```

---

## Test Different Threshold

```python
detector = BruteForceDetector(
    threshold=3,
    time_window=300
)
```

Lower thresholds will detect attacks more aggressively.

---

## Create Custom Test Log

```bash
cat > test.log << 'EOF'
2024-01-15 11:00:00 FAILED user=testuser ip=10.0.0.1
2024-01-15 11:00:05 FAILED user=testuser ip=10.0.0.1
2024-01-15 11:00:10 FAILED user=testuser ip=10.0.0.1
2024-01-15 11:00:15 FAILED user=testuser ip=10.0.0.1
2024-01-15 11:00:20 FAILED user=testuser ip=10.0.0.1
EOF
```

Update:

```python
detector.process_log_file(
    "test.log"
)
```

Run again and verify detection.

---

# 📂 Project Structure

```text
brute-force-lab/
│
├── auth.log
├── test.log
├── alerts.log
├── detector.py
│
└── README.md
```

---

# 🔍 Troubleshooting

## File Not Found

```bash
pwd
ls -l auth.log
```

---

## No Alerts Generated

Lower the threshold:

```python
threshold=3
```

Verify log format is correct.

---

## Permission Denied

```bash
chmod +x detector.py
```

---

## Parsing Errors

Ensure entries follow:

```text
DATE TIME STATUS user=username ip=address
```

Example:

```text
2024-01-15 10:24:12 FAILED user=admin ip=203.0.113.45
```

---

# 🌍 Real-World Applications

This project demonstrates techniques used by:

* Security Information and Event Management (SIEM)
* Intrusion Detection Systems (IDS)
* Security Operations Centers (SOC)
* Cloud Authentication Services
* Identity and Access Management Platforms

Examples include:

* Fail2Ban
* Splunk
* Elastic Security
* Microsoft Sentinel
* IBM QRadar

---

# 📈 Key Takeaways

* Failed login monitoring is a critical security control.
* Threshold-based detection is simple but effective.
* Automated alerting improves incident response.
* Security logs provide valuable threat intelligence.
* Brute-force attacks often target privileged accounts such as `admin` and `root`.

---

# 🎉 Lab Complete

You have successfully built a **Brute-force Attack Detection Engine** capable of:

* 🔍 Parsing authentication logs
* 🚨 Detecting brute-force attacks
* 📊 Monitoring failed login attempts
* 📝 Generating security alerts
* 📁 Saving audit reports

These foundational techniques are widely used in modern cybersecurity monitoring, SOC operations, and incident response workflows.
