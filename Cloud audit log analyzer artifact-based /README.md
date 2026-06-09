# ☁️ Cloud Audit Log Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Cloud Security](https://img.shields.io/badge/Cloud-Security-orange?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Log%20Analysis-black?style=for-the-badge\&logo=json)
![Audit Logs](https://img.shields.io/badge/Audit-Logs-green?style=for-the-badge)
![Threat Detection](https://img.shields.io/badge/Threat-Detection-red?style=for-the-badge)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Analysis-purple?style=for-the-badge)

### 🔍 Analyze Cloud Audit Logs for Security Risks, Misconfigurations & Suspicious Activities

</div>

---

# 📖 Overview

The **Cloud Audit Log Analyzer** is a Python-based security monitoring tool designed to analyze cloud audit logs and identify potentially dangerous activities within cloud environments.

The analyzer performs:

✅ Audit Log Parsing

✅ Risky Action Detection

✅ Security Misconfiguration Identification

✅ Suspicious Activity Analysis

✅ Automated Security Reporting

✅ Cloud Security Monitoring

This project simulates security analysis techniques used by:

* Cloud Security Engineers
* SOC Analysts
* Security Consultants
* Incident Response Teams
* DevSecOps Engineers

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

* Parse JSON audit logs
* Analyze cloud activity records
* Detect risky administrative actions
* Identify security misconfigurations
* Detect suspicious user behavior
* Generate security reports
* Understand cloud security threats

---

# 📋 Prerequisites

Before beginning this lab:

* Basic Linux command-line knowledge
* Understanding of file operations
* Familiarity with nano or vi
* Basic JSON knowledge
* Python 3.x fundamentals

---

# 🏗️ Analyzer Architecture

```text
Cloud Audit Logs (JSON)
            │
            ▼
 ┌────────────────────┐
 │ Log Loader         │
 └─────────┬──────────┘
           │
           ▼
 ┌────────────────────┐
 │ Risky Action       │
 │ Detection Engine   │
 └─────────┬──────────┘
           │
           ▼
 ┌────────────────────┐
 │ Misconfiguration   │
 │ Detection Engine   │
 └─────────┬──────────┘
           │
           ▼
 ┌────────────────────┐
 │ Suspicious Activity│
 │ Detection Engine   │
 └─────────┬──────────┘
           │
           ▼
 ┌────────────────────┐
 │ Security Report    │
 └────────────────────┘
```

---

# 📂 Project Structure

```text
cloud-audit-lab/
│
├── sample_audit_logs.json
├── test_logs.json
├── audit_analyzer.py
│
└── README.md
```

---

# ⚙️ Environment Setup

## 🟢 Step 1: Verify Python Installation

```bash
python3 --version
```

Expected:

```text
Python 3.8+
```

---

## 🟢 Step 2: Install Required Library

```bash
pip3 install --user colorama
```

---

## 🟢 Step 3: Create Working Directory

```bash
mkdir -p ~/cloud-audit-lab

cd ~/cloud-audit-lab
```

---

# 📄 Sample Audit Logs

Create:

```text
sample_audit_logs.json
```

```json
[
  {
    "timestamp": "2024-01-15T10:23:45Z",
    "user": "admin@company.com",
    "action": "CreateUser",
    "resource": "IAM",
    "source_ip": "203.0.113.45",
    "status": "SUCCESS",
    "details": {
      "username": "newuser",
      "permissions": "Administrator"
    }
  },
  {
    "timestamp": "2024-01-15T10:25:12Z",
    "user": "developer@company.com",
    "action": "ModifySecurityGroup",
    "resource": "Network",
    "source_ip": "198.51.100.23",
    "status": "SUCCESS",
    "details": {
      "rule": "Allow 0.0.0.0/0 on port 22"
    }
  },
  {
    "timestamp": "2024-01-15T10:30:00Z",
    "user": "admin@company.com",
    "action": "DisableEncryption",
    "resource": "Storage",
    "source_ip": "203.0.113.45",
    "status": "SUCCESS",
    "details": {
      "bucket": "sensitive-data-bucket"
    }
  }
]
```

---

# 🚀 audit_analyzer.py

```python
#!/usr/bin/env python3

"""
Cloud Audit Log Analyzer
Analyzes cloud audit logs for security issues
"""

import json
import sys
from collections import defaultdict

try:
    from colorama import Fore, Style, init

    init(autoreset=True)

    COLORS_AVAILABLE = True

except ImportError:

    COLORS_AVAILABLE = False

    print(
        "Note: Install colorama for colored output"
    )


RISKY_ACTIONS = [
    'DisableEncryption',
    'ModifyLogging',
    'DeleteBackup',
    'CreateAccessKey',
    'DisableMFA'
]

MISCONFIGURATION_PATTERNS = {
    'open_ssh':
    '0.0.0.0/0 on port 22',

    'open_rdp':
    '0.0.0.0/0 on port 3389',

    'public_access':
    'public-read',

    'no_encryption':
    'encryption: false'
}


def load_audit_logs(filename):

    try:

        with open(
            filename,
            'r'
        ) as f:

            logs = json.load(f)

        print(
            f"[+] Loaded "
            f"{len(logs)} log entries "
            f"from {filename}"
        )

        return logs

    except FileNotFoundError:

        print(
            f"[!] Error: "
            f"File '{filename}' not found"
        )

        sys.exit(1)

    except json.JSONDecodeError:

        print(
            f"[!] Error: "
            f"Invalid JSON format"
        )

        sys.exit(1)


def analyze_risky_actions(logs):

    findings = []

    for log in logs:

        action = log.get(
            'action',
            ''
        )

        if action in RISKY_ACTIONS:

            findings.append({

                'severity': 'HIGH',

                'type': 'Risky Action',

                'timestamp':
                log.get('timestamp'),

                'user':
                log.get('user'),

                'action':
                action,

                'resource':
                log.get('resource'),

                'details':
                log.get('details', {})
            })

    return findings


def detect_misconfigurations(logs):

    findings = []

    for log in logs:

        details_str = json.dumps(
            log.get('details', {})
        )

        for (
            config_name,
            pattern
        ) in MISCONFIGURATION_PATTERNS.items():

            if pattern in details_str:

                findings.append({

                    'severity':
                    'CRITICAL',

                    'type':
                    'Misconfiguration',

                    'timestamp':
                    log.get('timestamp'),

                    'user':
                    log.get('user'),

                    'action':
                    log.get('action'),

                    'issue':
                    config_name.replace(
                        '_',
                        ' '
                    ).title(),

                    'details':
                    log.get('details', {})
                })

    return findings


def detect_suspicious_activity(logs):

    findings = []

    for log in logs:

        if log.get(
            'status'
        ) == 'FAILED':

            findings.append({

                'severity':
                'MEDIUM',

                'type':
                'Suspicious Activity',

                'timestamp':
                log.get('timestamp'),

                'user':
                log.get('user'),

                'action':
                log.get('action'),

                'issue':
                'Failed Access Attempt',

                'source_ip':
                log.get('source_ip')
            })

        timestamp = log.get(
            'timestamp',
            ''
        )

        if (
            'T02:' in timestamp or
            'T03:' in timestamp or
            'T04:' in timestamp
        ):

            findings.append({

                'severity':
                'MEDIUM',

                'type':
                'Suspicious Activity',

                'timestamp':
                timestamp,

                'user':
                log.get('user'),

                'action':
                log.get('action'),

                'issue':
                'Unusual Access Time'
            })

        user = log.get(
            'user',
            ''
        )

        if (
            'external' in user or
            'unknown' in user
        ):

            findings.append({

                'severity':
                'HIGH',

                'type':
                'Suspicious Activity',

                'timestamp':
                log.get('timestamp'),

                'user':
                user,

                'action':
                log.get('action'),

                'issue':
                'External User Activity',

                'source_ip':
                log.get('source_ip')
            })

    return findings


def generate_report(
    logs,
    risky_actions,
    misconfigs,
    suspicious
):

    print("\n" + "=" * 70)

    print(
        " CLOUD AUDIT SECURITY REPORT "
    )

    print("=" * 70)

    print(
        f"\nTotal Logs: {len(logs)}"
    )

    print(
        f"Risky Actions: "
        f"{len(risky_actions)}"
    )

    print(
        f"Misconfigurations: "
        f"{len(misconfigs)}"
    )

    print(
        f"Suspicious Activity: "
        f"{len(suspicious)}"
    )

    total = (
        len(risky_actions)
        + len(misconfigs)
        + len(suspicious)
    )

    print(
        f"\nTotal Security Issues: "
        f"{total}"
    )

    print("\n" + "=" * 70)

    print(
        "[RECOMMENDATIONS]"
    )

    print("=" * 70)

    print(
        "- Enable MFA"
    )

    print(
        "- Restrict public access"
    )

    print(
        "- Review IAM privileges"
    )

    print(
        "- Rotate access keys"
    )

    print(
        "- Monitor suspicious activity"
    )


def main():

    print(
        "\n=== Cloud Audit Log Analyzer ===\n"
    )

    if len(sys.argv) < 2:

        print(
            "Usage: "
            "python3 audit_analyzer.py "
            "<log_file.json>"
        )

        sys.exit(1)

    log_file = sys.argv[1]

    logs = load_audit_logs(
        log_file
    )

    print(
        "\n[*] Analyzing logs..."
    )

    risky_actions = (
        analyze_risky_actions(logs)
    )

    misconfigs = (
        detect_misconfigurations(logs)
    )

    suspicious = (
        detect_suspicious_activity(logs)
    )

    generate_report(
        logs,
        risky_actions,
        misconfigs,
        suspicious
    )


if __name__ == "__main__":
    main()
```

---

# ▶️ Make Script Executable

```bash
chmod +x audit_analyzer.py
```

---

# 🔍 Run Analyzer

```bash
python3 audit_analyzer.py sample_audit_logs.json
```

---

# 🧪 Create Test Dataset

Create:

```text
test_logs.json
```

```json
[
  {
    "timestamp": "2024-01-16T03:00:00Z",
    "user": "testuser@company.com",
    "action": "DisableMFA",
    "resource": "IAM",
    "source_ip": "10.0.0.1",
    "status": "SUCCESS",
    "details": {
      "account": "admin-account"
    }
  }
]
```

---

# 🔍 Test Detection Engine

Run:

```bash
python3 audit_analyzer.py test_logs.json
```

Expected detections:

✅ Risky Action → DisableMFA

✅ Unusual Access Time → 03:00 AM

✅ Proper Severity Assignment

---

# ✅ Verification Checklist

## Verify JSON Syntax

```bash
python3 -m json.tool sample_audit_logs.json
```

---

## Verify Analyzer Execution

```bash
python3 audit_analyzer.py sample_audit_logs.json
```

Expected:

* Risky Actions Found
* Misconfigurations Found
* Suspicious Activities Found
* Recommendations Generated

---

# 🚨 Security Findings Categories

| Detection Type         | Severity |
| ---------------------- | -------- |
| Disable Encryption     | HIGH     |
| Delete Backup          | HIGH     |
| Modify Logging         | HIGH     |
| Create Access Key      | HIGH     |
| Disable MFA            | HIGH     |
| Open SSH Rule          | CRITICAL |
| Failed Access Attempt  | MEDIUM   |
| Unusual Access Time    | MEDIUM   |
| External User Activity | HIGH     |

---

# 🛠 Troubleshooting

## Colorama Module Missing

Install:

```bash
pip3 install --user colorama
```

---

## JSON Syntax Error

Validate JSON:

```bash
python3 -m json.tool sample_audit_logs.json
```

---

## File Not Found

Check location:

```bash
pwd

ls
```

---

## No Findings Detected

Verify log fields:

```json
{
  "timestamp": "",
  "user": "",
  "action": "",
  "resource": "",
  "source_ip": "",
  "status": "",
  "details": {}
}
```

---

# 🔐 Cloud Security Concepts Demonstrated

✅ Audit Logging

✅ Threat Detection

✅ IAM Security Monitoring

✅ Security Misconfiguration Analysis

✅ Access Monitoring

✅ Cloud Compliance Visibility

✅ Security Reporting

✅ Risk Assessment

---

# 🎓 Skills Acquired

* JSON Parsing
* Security Log Analysis
* Cloud Security Monitoring
* Threat Detection Engineering
* Security Reporting
* Python Automation
* Risk Assessment
* Security Operations (SOC)

---

# 🏆 Conclusion

Congratulations! You have successfully built a **Cloud Audit Log Analyzer** capable of parsing audit logs, detecting risky administrative actions, identifying security misconfigurations, flagging suspicious activities, and generating comprehensive security reports.

This project demonstrates practical cloud security monitoring techniques used by cloud security engineers, SOC analysts, incident responders, and DevSecOps teams to secure modern cloud environments.

### ⭐ Happy Cloud Threat Hunting! ☁️🔍🛡️
