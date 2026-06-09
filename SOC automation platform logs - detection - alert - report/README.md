# 🛡️ SOC Automation Platform

> *"Automation transforms security operations from reactive monitoring into proactive defense."*

---

# 📚 Lab Overview

Security Operations Centers (SOCs) rely on automation to process massive volumes of security events, identify threats, generate alerts, and produce actionable reports.

In this hands-on lab, you will build a **SOC Automation Platform** that:

- Generates simulated security logs
- Detects suspicious activities using threat signatures
- Creates automated alerts
- Produces security reports
- Demonstrates core SOC workflows

This project provides foundational experience with log analysis, threat detection, security automation, and reporting.

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Set up a SOC automation workflow

✅ Generate and ingest security logs

✅ Detect simulated threats using pattern matching

✅ Create automated alerts

✅ Build security reporting capabilities

✅ Understand SOC monitoring fundamentals

---

# 🛠️ Technologies Used

![Python](https://img.shields.io/badge/Python-3-blue)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)
![SOC](https://img.shields.io/badge/SOC-Automation-red)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Detection-green)
![Log Analysis](https://img.shields.io/badge/Log-Analysis-purple)

---

# 🖥️ Environment Setup

## Step 1: Update System

```bash
sudo apt update
```

---

## Step 2: Install Required Packages

```bash
sudo apt install -y python3 python3-pip
```

---

## Step 3: Install Python Dependencies

```bash
pip3 install watchdog
```

---

## Step 4: Create Project Structure

```bash
mkdir -p ~/soc-lab/{logs,scripts,alerts,reports}
cd ~/soc-lab
```

---

# 📂 Project Structure

```text
soc-lab/
│
├── logs/
│   └── security.log
│
├── alerts/
│   └── threats.txt
│
├── reports/
│   └── security_report.txt
│
└── scripts/
    ├── log_generator.py
    ├── threat_detector.py
    └── report_generator.py
```

---

# 🚩 Task 1 — Generate Security Logs

---

# 📄 File: scripts/log_generator.py

```python
#!/usr/bin/env python3

"""
Simple log generator for SOC simulation
Generates normal and suspicious security events
"""

import time
import random
from datetime import datetime

NORMAL_EVENTS = [
    "User login successful from 192.168.1.{} - user: employee{}",
    "File accessed: /home/user{}/documents/report.pdf",
    "Service started: web_server on port 80"
]

SUSPICIOUS_EVENTS = [
    "Failed login attempt from 10.0.0.{} - user: admin - attempt {}",
    "Port scan detected from 203.0.113.{} targeting ports 22,23,3389",
    "Unusual outbound connection to 198.51.100.{} on port 4444",
    "Multiple failed sudo attempts - user: guest{}"
]

def generate_log_entry(event_type):
    """
    Generate a log entry
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if event_type == "normal":

        template = random.choice(
            NORMAL_EVENTS
        )

    else:

        template = random.choice(
            SUSPICIOUS_EVENTS
        )

    event = template.format(
        random.randint(1, 254),
        random.randint(1, 50)
    )

    return f"[{timestamp}] {event}"

def main():

    log_file = "../logs/security.log"

    print(
        "Generating security logs..."
    )

    with open(log_file, "a") as f:

        while True:

            event_type = random.choices(
                ["normal", "suspicious"],
                weights=[80, 20]
            )[0]

            log = generate_log_entry(
                event_type
            )

            f.write(log + "\n")
            f.flush()

            print(log)

            time.sleep(
                random.uniform(1, 3)
            )

if __name__ == "__main__":
    main()
```

---

# ▶️ Run Log Generator

```bash
chmod +x scripts/log_generator.py

python3 scripts/log_generator.py &
```

Save PID:

```bash
echo $! > /tmp/log_generator.pid
```

Verify logs:

```bash
head -20 logs/security.log
```

---

# 🚩 Task 2 — Build Threat Detection Engine

---

# 📄 File: scripts/threat_detector.py

```python
#!/usr/bin/env python3

"""
SOC Threat Detection Engine
"""

import re
import time
from datetime import datetime

THREAT_PATTERNS = {
    "brute_force":
        r"Failed login attempt.*user: admin",

    "port_scan":
        r"Port scan detected",

    "suspicious_connection":
        r"Unusual outbound connection.*4444",

    "privilege_escalation":
        r"Multiple failed sudo attempts"
}

def analyze_log_line(line):

    for threat_type, pattern in THREAT_PATTERNS.items():

        if re.search(pattern, line):

            return {
                "threat_type": threat_type,
                "timestamp":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                "raw_log": line.strip()
            }

    return None

def monitor_logs(log_file, alert_file):

    print(
        f"Monitoring {log_file}"
    )

    with open(log_file, "r") as logfile:

        logfile.seek(0, 2)

        while True:

            line = logfile.readline()

            if not line:
                time.sleep(1)
                continue

            threat = analyze_log_line(line)

            if threat:

                alert = (
                    f"[{threat['timestamp']}] "
                    f"{threat['threat_type']} | "
                    f"{threat['raw_log']}"
                )

                with open(
                    alert_file,
                    "a"
                ) as af:

                    af.write(alert + "\n")

                print(
                    "[ALERT]",
                    alert
                )

def main():

    monitor_logs(
        "../logs/security.log",
        "../alerts/threats.txt"
    )

if __name__ == "__main__":
    main()
```

---

# ▶️ Run Threat Detector

```bash
chmod +x scripts/threat_detector.py

python3 scripts/threat_detector.py &
```

Save PID:

```bash
echo $! > /tmp/detector.pid
```

Check alerts:

```bash
sleep 60

cat alerts/threats.txt
```

---

# 🚩 Task 3 — Generate Security Reports

---

# 📄 File: scripts/report_generator.py

```python
#!/usr/bin/env python3

"""
SOC Report Generator
"""

from datetime import datetime
from collections import Counter

def parse_alerts(alert_file):

    threats = []

    try:

        with open(alert_file) as f:

            for line in f:

                if "|" in line:

                    parts = line.split("|")

                    threat_type = (
                        parts[0]
                        .split("]")
                        [-1]
                        .strip()
                    )

                    threats.append({
                        "type":
                            threat_type,
                        "raw":
                            line.strip()
                    })

    except FileNotFoundError:

        print(
            "Alert file not found."
        )

    return threats

def generate_summary(threats):

    counter = Counter(
        t["type"]
        for t in threats
    )

    summary = {
        "total_threats":
            len(threats),

        "threat_breakdown":
            dict(counter),

        "report_time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    return summary

def create_report(
    summary,
    output_file
):

    with open(
        output_file,
        "w"
    ) as report:

        report.write(
            "=" * 60 + "\n"
        )

        report.write(
            "SOC SECURITY REPORT\n"
        )

        report.write(
            "=" * 60 + "\n\n"
        )

        report.write(
            f"Generated: "
            f"{summary['report_time']}\n\n"
        )

        report.write(
            f"Total Threats: "
            f"{summary['total_threats']}\n\n"
        )

        report.write(
            "Threat Breakdown\n"
        )

        report.write(
            "-" * 30 + "\n"
        )

        for threat, count in \
            summary[
                "threat_breakdown"
            ].items():

            report.write(
                f"{threat}: {count}\n"
            )

        report.write(
            "\nRecommendations:\n"
        )

        report.write(
            "- Investigate brute force attempts\n"
        )

        report.write(
            "- Review suspicious outbound traffic\n"
        )

        report.write(
            "- Monitor privilege escalation events\n"
        )

        report.write(
            "- Harden exposed services\n"
        )

def main():

    alert_file = (
        "../alerts/threats.txt"
    )

    report_file = (
        "../reports/security_report.txt"
    )

    threats = parse_alerts(
        alert_file
    )

    summary = generate_summary(
        threats
    )

    create_report(
        summary,
        report_file
    )

    print(
        f"Report saved to "
        f"{report_file}"
    )

if __name__ == "__main__":
    main()
```

---

# ▶️ Generate Security Report

Stop background processes:

```bash
kill $(cat /tmp/log_generator.pid)

kill $(cat /tmp/detector.pid)
```

Generate report:

```bash
chmod +x scripts/report_generator.py

python3 scripts/report_generator.py
```

View report:

```bash
cat reports/security_report.txt
```

---

# 🧪 Verification

## Verify Logs

```bash
echo "=== Log Sample ==="

head -10 logs/security.log
```

---

## Verify Threat Detection

```bash
echo "=== Detected Threats ==="

cat alerts/threats.txt | wc -l

echo "threats detected"
```

---

## Verify Report

```bash
cat reports/security_report.txt
```

---

## Verify Lab Structure

```bash
tree ~/soc-lab
```

---

# 📊 Expected Results

You should observe:

✅ Continuous security logs

✅ Brute force detection

✅ Port scan alerts

✅ Suspicious outbound connections

✅ Privilege escalation detections

✅ Automated report generation

Example:

```text
[ALERT] brute_force
[ALERT] port_scan
[ALERT] suspicious_connection
[ALERT] privilege_escalation
```

---

# 🔐 Detection Workflow

```text
Security Events
        │
        ▼
Log Generator
        │
        ▼
Security Log File
        │
        ▼
Threat Detection Engine
        │
        ▼
Alert Generation
        │
        ▼
Security Reports
```

---

# 🚨 Threat Signatures Used

| Threat | Detection Logic |
|----------|----------------|
| Brute Force | Failed admin logins |
| Port Scan | Scan activity detected |
| Suspicious Connection | Port 4444 outbound traffic |
| Privilege Escalation | Failed sudo attempts |

---

# 🛠 Troubleshooting

## No Logs Generated

```bash
ps aux | grep log_generator
```

Check permissions:

```bash
ls -la logs/
```

---

## No Threats Detected

Verify suspicious events:

```bash
grep -i "failed\|scan\|unusual" logs/security.log
```

---

## Empty Report

```bash
cat alerts/threats.txt
```

Verify parser logic.

---

# 📈 Real-World SOC Applications

This lab demonstrates concepts used in:

- Security Operations Centers (SOC)
- SIEM Platforms
- Threat Hunting
- Managed Detection & Response (MDR)
- Security Monitoring
- Incident Response Automation

Examples:

- Splunk
- IBM QRadar
- Elastic Security
- Microsoft Sentinel
- Wazuh

---

# 🎯 Key Takeaways

✔ Log monitoring provides security visibility

✔ Threat detection automates analysis

✔ Alerts reduce incident response time

✔ Reports improve security awareness

✔ Automation scales security operations

✔ Signature detection forms the foundation of SOC monitoring

---

# 🚀 Next Steps

Enhance the platform by adding:

- Email Alerting
- Slack Notifications
- Threat Intelligence Feeds
- IOC Matching
- Machine Learning Detection
- Real-Time Dashboards
- SIEM Integration
- MITRE ATT&CK Mapping

---

# 🏆 Lab Completed

You have successfully built a **SOC Automation Platform** capable of:

✅ Log Generation

✅ Threat Detection

✅ Alerting

✅ Security Reporting

✅ SOC Workflow Automation

This project demonstrates the core building blocks used by modern Security Operations Centers to identify, investigate, and respond to security threats at scale.

---

**Author:** Muhammad Salman  
**Domain:** SOC Operations • Cyber Defense • Security Automation
