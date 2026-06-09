# ☁️ Cloud Security Audit Engine Using Artifacts

![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Cloud%20Security-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)
![Audit](https://img.shields.io/badge/Security-Audit-red)
![Compliance](https://img.shields.io/badge/Compliance-Reporting-purple)

---

# 📌 Overview

The **Cloud Security Audit Engine Using Artifacts** project demonstrates how cybersecurity professionals analyze configuration files, inspect logs, identify security weaknesses, and generate compliance reports using Python and open-source tools.

This hands-on lab simulates a real-world cloud security auditing workflow by examining infrastructure artifacts such as:

* SSH configurations
* Firewall rules
* User permission files
* Authentication logs
* Access logs

The audit engine automatically detects security misconfigurations, suspicious activities, compliance violations, and generates detailed reports.

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

✅ Understand cloud security auditing fundamentals

✅ Analyze configuration files for security weaknesses

✅ Parse authentication and access logs

✅ Detect brute-force attacks and unauthorized access

✅ Build automated compliance checks

✅ Generate security audit reports

✅ Calculate compliance scores

✅ Apply basic cloud security best practices

---

# 🛠️ Technologies Used

| Technology | Purpose               |
| ---------- | --------------------- |
| Python 3   | Automation & Analysis |
| Linux      | Lab Environment       |
| JSON       | Configuration Storage |
| YAML       | User Configuration    |
| JQ         | JSON Parsing          |
| Git        | Version Control       |
| Requests   | HTTP Operations       |
| PyYAML     | YAML Processing       |

---

# 📂 Project Structure

```text
security-audit-lab/
│
├── configs/
│   ├── sshd_config.sample
│   ├── firewall_rules.json
│   └── users.yaml
│
├── logs/
│   ├── auth.log
│   └── access.log
│
├── reports/
│   ├── config_audit.json
│   ├── log_audit.json
│   └── compliance_report.html
│
├── audit_configs.py
├── audit_logs.py
├── generate_report.py
│
└── README.md
```

---

# ⚙️ Environment Setup

## Step 1: Update System

```bash
sudo apt update
```

---

## Step 2: Install Python & Utilities

```bash
sudo apt install -y python3 python3-pip
sudo apt install -y jq
sudo apt install -y curl git
```

---

## Step 3: Create Lab Directory

```bash
mkdir -p ~/security-audit-lab
cd ~/security-audit-lab

mkdir -p configs logs artifacts reports
```

---

## Step 4: Install Python Libraries

```bash
pip3 install pyyaml requests
```

---

# 🔍 Task 1 — Create Security Artifacts

---

## SSH Configuration

### File: `configs/sshd_config.sample`

```text
Port 22
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords no
X11Forwarding yes
MaxAuthTries 6
```

---

## Firewall Rules

### File: `configs/firewall_rules.json`

```json
{
  "rules": [
    {
      "id": "rule-001",
      "protocol": "tcp",
      "port": "22",
      "source": "0.0.0.0/0",
      "action": "allow"
    },
    {
      "id": "rule-002",
      "protocol": "tcp",
      "port": "3389",
      "source": "0.0.0.0/0",
      "action": "allow"
    },
    {
      "id": "rule-003",
      "protocol": "tcp",
      "port": "443",
      "source": "0.0.0.0/0",
      "action": "allow"
    }
  ]
}
```

---

## User Permissions

### File: `configs/users.yaml`

```yaml
users:
  - username: admin
    uid: 1000
    sudo: true
    password_age: 365

  - username: developer
    uid: 1001
    sudo: true
    password_age: 180

  - username: guest
    uid: 1002
    sudo: false
    password_age: 90
```

---

# 📋 Task 2 — Generate Security Logs

---

## Authentication Log

### File: `logs/auth.log`

```text
2024-01-15 10:23:45 INFO: User admin logged in from 192.168.1.100
2024-01-15 10:45:12 WARNING: Failed login attempt for user root from 203.0.113.45
2024-01-15 11:02:33 WARNING: Failed login attempt for user root from 203.0.113.45
2024-01-15 11:15:22 WARNING: Failed login attempt for user admin from 198.51.100.23
2024-01-15 12:30:11 INFO: User developer logged in from 192.168.1.105
2024-01-15 13:45:00 ERROR: Brute force attack detected from 203.0.113.45
2024-01-15 14:20:15 INFO: User admin logged out
```

---

## Access Log

### File: `logs/access.log`

```text
2024-01-15 10:25:00 GET /api/users 200 admin
2024-01-15 10:30:15 POST /api/config 200 admin
2024-01-15 11:45:30 GET /api/secrets 403 guest
2024-01-15 12:00:45 DELETE /api/users/1001 200 admin
2024-01-15 13:15:20 GET /admin/panel 200 developer
```

---

# 🛡️ Task 3 — Configuration Security Analyzer

## Run Audit

```bash
python3 audit_configs.py
```

---

## Security Checks Performed

### SSH Configuration

* Root Login Enabled
* Password Authentication Enabled
* Excessive Authentication Attempts

### Firewall Rules

* Open Internet Access (0.0.0.0/0)
* Exposed Administrative Ports
* Unrestricted RDP Access

### User Permissions

* Excessive Password Age
* Unnecessary Sudo Privileges
* Weak Access Controls

---

# 🔎 Task 4 — Log Security Analyzer

## Run Log Audit

```bash
python3 audit_logs.py
```

---

## Security Events Detected

### Authentication Events

* Failed Logins
* Brute Force Attacks
* Suspicious IP Activity

### Access Events

* Unauthorized Access Attempts
* Sensitive Endpoint Access
* Administrative Actions
* Delete Operations

---

# 📊 Task 5 — Compliance Report Generator

Generate final compliance report:

```bash
python3 generate_report.py
```

---

## Generated Reports

```text
reports/
├── config_audit.json
├── log_audit.json
└── compliance_report.html
```

---

# 📈 Compliance Scoring Model

| Severity | Penalty |
| -------- | ------- |
| Critical | 10      |
| High     | 5       |
| Medium   | 2       |
| Low      | 1       |

---

### Formula

```text
Compliance Score = 100 - Total Penalties
```

---

## Example

```text
Score: 74/100

Issues Found:
- 1 Critical
- 3 High
- 4 Medium
- 2 Low
```

---

# 🚀 Running the Complete Audit

Execute all phases:

```bash
python3 audit_configs.py

python3 audit_logs.py

python3 generate_report.py
```

---

# 🔍 Verification Commands

## Check Reports

```bash
ls -lh reports/
```

---

## View Configuration Findings

```bash
cat reports/config_audit.json
```

---

## View Log Findings

```bash
cat reports/log_audit.json
```

---

## Count Findings

```bash
jq '. | length' reports/config_audit.json

jq '. | length' reports/log_audit.json
```

---

# ⚠️ Sample Findings

## Critical

```text
Brute force attack detected
```

---

## High

```text
PermitRootLogin enabled
```

```text
Firewall rule open to internet
```

---

## Medium

```text
Password authentication enabled
```

```text
Unauthorized access attempts
```

---

## Low

```text
Developer has sudo privileges
```

---

# 🛠 Troubleshooting

## PyYAML Missing

```bash
pip3 install pyyaml
```

---

## Permission Denied

```bash
chmod +x *.py
```

---

## Report Files Missing

Verify:

```bash
ls configs/
ls logs/
```

---

## Script Errors

Confirm directory:

```bash
pwd
```

Expected:

```text
/home/user/security-audit-lab
```

---

# 🎓 Key Security Concepts Learned

### Configuration Auditing

Identify insecure settings before attackers do.

### Log Analysis

Detect active threats using authentication and access logs.

### Compliance Monitoring

Measure security posture using standardized checks.

### Security Automation

Reduce manual effort through automated auditing.

### Risk Prioritization

Focus remediation efforts on critical findings first.

---

# 📚 Real-World Applications

This project reflects techniques used in:

* Cloud Security Audits
* Security Operations Centers (SOC)
* Compliance Monitoring
* Governance, Risk & Compliance (GRC)
* DevSecOps Pipelines
* Incident Response
* Threat Hunting

---

# 🏆 Lab Completion Checklist

* [x] Installed required tools
* [x] Created security artifacts
* [x] Generated authentication logs
* [x] Built configuration analyzer
* [x] Built log analyzer
* [x] Generated compliance reports
* [x] Calculated security score
* [x] Verified audit results

---

# 🎯 Conclusion

In this lab, you successfully built a **Cloud Security Audit Engine Using Artifacts** capable of analyzing configurations, auditing logs, detecting security risks, generating compliance reports, and calculating security scores.

The techniques demonstrated mirror foundational practices used by cloud security engineers, SOC analysts, compliance auditors, and cybersecurity professionals to continuously assess and improve infrastructure security.

**Key Takeaway:** Automated security auditing improves visibility, reduces human error, identifies vulnerabilities faster, and strengthens overall cloud security posture.
