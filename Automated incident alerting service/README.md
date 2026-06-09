# 🚨 Automated Incident Alerting Service

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=linux)
![YAML](https://img.shields.io/badge/YAML-Configuration-red?style=for-the-badge\&logo=yaml)
![Cyber Security](https://img.shields.io/badge/Cyber%20Security-Incident%20Response-darkred?style=for-the-badge)
![SIEM](https://img.shields.io/badge/SIEM-Security%20Monitoring-green?style=for-the-badge)
![Automation](https://img.shields.io/badge/Security-Automation-purple?style=for-the-badge)

### 🔥 Real-Time Security Monitoring and Automated Incident Alerting System

</div>

---

# 📖 Overview

The **Automated Incident Alerting Service** is a hands-on cybersecurity project that demonstrates how modern Security Operations Centers (SOCs) automatically detect suspicious activities from security logs and generate alerts in real time.

The project implements a lightweight SIEM-inspired workflow capable of:

✅ Monitoring security logs continuously

✅ Detecting suspicious patterns using regular expressions

✅ Applying configurable alert thresholds

✅ Formatting incident notifications

✅ Logging security alerts

✅ Automating security monitoring workflows

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

* Understand automated security incident detection
* Configure alert triggers using security events
* Implement pattern-based monitoring
* Format and send security notifications
* Build a basic SIEM workflow
* Perform real-time log analysis
* Automate security operations

---

# 📋 Prerequisites

Before starting, ensure you have:

* Basic Linux command-line knowledge
* Understanding of file permissions and text editing
* Familiarity with log files
* Basic Python programming concepts

---

# 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │ Security Log File   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Incident Monitor    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Pattern Matching    │
                    │ Rule Engine         │
                    └──────────┬──────────┘
                               │
                      Threshold Reached
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Alert Formatter     │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
      ┌──────────────────┐         ┌──────────────────┐
      │ Console Alerts   │         │ Alert Log File   │
      └──────────────────┘         └──────────────────┘
```

---

# 📂 Project Structure

```text
incident-alerting/
│
├── logs/
│   └── security.log
│
├── alerts/
│   └── incidents.log
│
├── config/
│   └── alert_config.yaml
│
├── incident_monitor.py
├── alert_formatter.py
├── integrated_system.py
├── generate_test_logs.py
│
└── README.md
```

---

# ⚙️ Environment Setup

## 🟢 Step 1 — Update Package Manager

```bash
sudo apt update
```

---

## 🟢 Step 2 — Install Python and Pip

```bash
sudo apt install -y python3 python3-pip
```

---

## 🟢 Step 3 — Install Required Libraries

```bash
pip3 install watchdog pyyaml
```

---

## 🟢 Step 4 — Create Project Directory

```bash
mkdir -p ~/incident-alerting
cd ~/incident-alerting
```

---

## 🟢 Step 5 — Create Project Structure

```bash
mkdir -p logs alerts config
touch logs/security.log
```

---

# ⚙️ Configuration File

## 📄 config/alert_config.yaml

```yaml
# Alert configuration

alert_rules:
  - name: "Failed Login Attempt"
    pattern: "Failed password"
    severity: "medium"
    threshold: 3

  - name: "Root Access"
    pattern: "root login"
    severity: "high"
    threshold: 1

  - name: "Port Scan Detected"
    pattern: "port scan"
    severity: "high"
    threshold: 1

notification:
  email_enabled: false
  log_file: "alerts/incidents.log"
  console_enabled: true
```

---

# 🚨 incident_monitor.py

```python
#!/usr/bin/env python3

import time
import yaml
import re
from collections import defaultdict


class IncidentMonitor:

    def __init__(self, config_file):
        self.load_config(config_file)
        self.incident_counts = defaultdict(int)

    def load_config(self, config_file):

        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        self.rules = config["alert_rules"]
        self.notification = config["notification"]

    def check_pattern(self, log_line, rule):

        return bool(
            re.search(
                rule["pattern"],
                log_line,
                re.IGNORECASE
            )
        )

    def monitor_log(self, log_file):

        print(f"[*] Starting incident monitor on {log_file}")

        with open(log_file, "r") as f:

            f.seek(0, 2)

            while True:

                line = f.readline()

                if not line:
                    time.sleep(1)
                    continue

                for rule in self.rules:

                    if self.check_pattern(line, rule):

                        self.incident_counts[
                            rule["name"]
                        ] += 1

                        print(
                            f"[+] Match Found: {rule['name']}"
                        )

                        if (
                            self.incident_counts[
                                rule["name"]
                            ] >= rule["threshold"]
                        ):

                            print(
                                f"[ALERT] {rule['name']} Threshold Reached!"
                            )

                            self.incident_counts[
                                rule["name"]
                            ] = 0


if __name__ == "__main__":

    monitor = IncidentMonitor(
        "config/alert_config.yaml"
    )

    monitor.monitor_log(
        "logs/security.log"
    )
```

---

# 📢 alert_formatter.py

```python
#!/usr/bin/env python3

from datetime import datetime
import os


class AlertFormatter:

    def __init__(self, notification_config):

        self.notification = notification_config

        self.log_file = notification_config.get(
            "log_file",
            "alerts/incidents.log"
        )

        os.makedirs(
            os.path.dirname(
                self.log_file
            ),
            exist_ok=True
        )

    def format_alert(
        self,
        rule_name,
        severity,
        log_entry,
        count
    ):

        return f"""
============================================================
SECURITY ALERT
============================================================
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Rule: {rule_name}
Severity: {severity.upper()}
Occurrences: {count}
Log Entry: {log_entry.strip()}
============================================================
"""

    def send_alert(
        self,
        alert_message
    ):

        if self.notification.get(
            "console_enabled",
            True
        ):
            print(alert_message)

        self.write_to_log(
            alert_message
        )

    def write_to_log(
        self,
        message
    ):

        with open(
            self.log_file,
            "a"
        ) as f:

            f.write(message)
            f.write("\n")
            f.write("-" * 80)
            f.write("\n")


if __name__ == "__main__":

    config = {
        "log_file": "alerts/incidents.log",
        "console_enabled": True
    }

    formatter = AlertFormatter(config)

    test_alert = formatter.format_alert(
        "Failed Login Attempt",
        "medium",
        "Failed password for user admin",
        3
    )

    formatter.send_alert(
        test_alert
    )
```

---

# 🔔 integrated_system.py

```python
#!/usr/bin/env python3

import time
import yaml
import re
from collections import defaultdict

from alert_formatter import AlertFormatter


class IntegratedAlertSystem:

    def __init__(
        self,
        config_file
    ):

        with open(
            config_file,
            "r"
        ) as f:

            config = yaml.safe_load(f)

        self.rules = config["alert_rules"]

        self.formatter = AlertFormatter(
            config["notification"]
        )

        self.incident_counts = defaultdict(
            int
        )

    def process_log_line(
        self,
        line
    ):

        for rule in self.rules:

            if re.search(
                rule["pattern"],
                line,
                re.IGNORECASE
            ):

                self.incident_counts[
                    rule["name"]
                ] += 1

                count = self.incident_counts[
                    rule["name"]
                ]

                if count >= rule["threshold"]:

                    alert = (
                        self.formatter.format_alert(
                            rule["name"],
                            rule["severity"],
                            line,
                            count
                        )
                    )

                    self.formatter.send_alert(
                        alert
                    )

                    self.incident_counts[
                        rule["name"]
                    ] = 0

    def monitor(
        self,
        log_file
    ):

        print(
            f"[*] Monitoring {log_file}"
        )

        with open(
            log_file,
            "r"
        ) as f:

            f.seek(0, 2)

            while True:

                line = f.readline()

                if not line:
                    time.sleep(1)
                    continue

                self.process_log_line(
                    line
                )


if __name__ == "__main__":

    system = IntegratedAlertSystem(
        "config/alert_config.yaml"
    )

    system.monitor(
        "logs/security.log"
    )
```

---

# 🧪 generate_test_logs.py

```python
#!/usr/bin/env python3

import time
from datetime import datetime


def generate_log_entry(
    event_type
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    events = {

        "failed_login":
        f"{timestamp} sshd[1234]: Failed password for admin from 192.168.1.100",

        "root_access":
        f"{timestamp} su: root login on tty1",

        "port_scan":
        f"{timestamp} firewall: port scan detected from 10.0.0.50",

        "normal":
        f"{timestamp} sshd[5678]: Accepted publickey for user from 192.168.1.10"
    }

    return events.get(
        event_type,
        events["normal"]
    )


def generate_test_logs(
    log_file
):

    with open(
        log_file,
        "a"
    ) as f:

        for _ in range(5):

            f.write(
                generate_log_entry(
                    "failed_login"
                ) + "\n"
            )

            f.flush()
            time.sleep(1)

        f.write(
            generate_log_entry(
                "root_access"
            ) + "\n"
        )

        f.flush()
        time.sleep(1)

        for _ in range(2):

            f.write(
                generate_log_entry(
                    "port_scan"
                ) + "\n"
            )

            f.flush()
            time.sleep(1)

    print(
        "[+] Test logs generated successfully"
    )


if __name__ == "__main__":

    print(
        "[*] Generating Test Security Logs..."
    )

    generate_test_logs(
        "logs/security.log"
    )
```

---

# ✅ Verification

## 🖥️ Terminal 1

Start monitoring:

```bash
cd ~/incident-alerting
python3 integrated_system.py
```

---

## 🖥️ Terminal 2

Generate test logs:

```bash
cd ~/incident-alerting
python3 generate_test_logs.py
```

---

# 🎯 Expected Alerts

### Failed Login Attempt

```text
Threshold: 3
```

Alert generated after three failed logins.

---

### Root Access

```text
Threshold: 1
```

Alert generated immediately.

---

### Port Scan Detected

```text
Threshold: 1
```

Alert generated immediately.

---

# 📋 Check Alert Log

```bash
cat alerts/incidents.log
```

Expected output:

```text
============================================================
SECURITY ALERT
============================================================
Timestamp: 2025-01-01 12:00:00
Rule: Root Access
Severity: HIGH
Occurrences: 1
============================================================
```

---

# 🧪 Manual Testing

Add a custom failed login event:

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') sshd[9999]: Failed password for root from 1.2.3.4" >> logs/security.log
```

The monitoring service should immediately detect and process the event.

---

# 🛠️ Troubleshooting

## Monitor Not Detecting Logs

```bash
ls -l logs/security.log
```

```bash
chmod 644 logs/security.log
```

---

## Verify YAML Configuration

```bash
python3 -c "import yaml; yaml.safe_load(open('config/alert_config.yaml'))"
```

---

## Test Alert Formatter

```bash
python3 alert_formatter.py
```

---

## Test Regex Pattern

```bash
python3 -c "import re; print(re.search('Failed password','test Failed password log'))"
```

---

# 🔐 SIEM Concepts Demonstrated

| Feature             | Status |
| ------------------- | ------ |
| Log Monitoring      | ✅      |
| Event Analysis      | ✅      |
| Incident Detection  | ✅      |
| Pattern Matching    | ✅      |
| Threshold Alerting  | ✅      |
| Security Automation | ✅      |
| SOC Workflow        | ✅      |
| Alert Logging       | ✅      |

---

# 🚀 Future Enhancements

* 📧 Email Notifications using `smtplib`
* 💬 Slack Integration using Webhooks
* 🎫 Jira Ticket Automation
* 🌐 Flask Web Dashboard
* 📊 Grafana Visualization
* 🗄️ Elasticsearch Integration
* ☁️ Cloud Security Monitoring

---

# 🎓 Skills Acquired

✅ Real-Time Log Monitoring

✅ Security Event Analysis

✅ Incident Detection

✅ Pattern-Based Threat Identification

✅ Alert Threshold Management

✅ YAML Configuration Management

✅ Security Automation

✅ Python Security Engineering

✅ SIEM Fundamentals

✅ SOC Operations Concepts

---

# 🏆 Conclusion

You have successfully built an **Automated Incident Alerting Service** capable of monitoring security logs, detecting suspicious activities, generating alerts, and logging incidents automatically.

This project demonstrates the core concepts used by enterprise SIEM platforms and Security Operations Centers (SOCs), providing a strong foundation for cybersecurity automation, incident response, and threat detection engineering.

### ⭐ Happy Threat Hunting! 🚨🔍
