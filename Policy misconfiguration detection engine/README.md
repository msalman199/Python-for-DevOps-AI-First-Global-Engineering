# 🛡️ Policy Misconfiguration Detection Engine

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=linux)
![JSON](https://img.shields.io/badge/JSON-Policy%20Analysis-black?style=for-the-badge\&logo=json)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Policy%20Auditing-red?style=for-the-badge)
![Firewall](https://img.shields.io/badge/Firewall-Rule%20Analysis-green?style=for-the-badge)
![Access Control](https://img.shields.io/badge/Access-Control-purple?style=for-the-badge)

### 🔍 Detect Security Policy Misconfigurations Automatically

</div>

---

# 📖 Overview

The **Policy Misconfiguration Detection Engine** is a Python-based security auditing tool that analyzes firewall and access control policies to identify weak, conflicting, or dangerous security configurations.

The engine automatically detects:

✅ Overly Permissive Firewall Rules

✅ Conflicting Security Policies

✅ Wildcard Access Permissions

✅ Sensitive Resource Exposure

✅ Policy Security Gaps

✅ Access Control Weaknesses

This project demonstrates security auditing techniques commonly used in:

* Security Operations Centers (SOC)
* DevSecOps Pipelines
* Compliance Audits
* Cloud Security Assessments
* Network Security Reviews

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

* Understand policy misconfigurations
* Analyze firewall rules
* Detect conflicting security controls
* Audit access control permissions
* Build automated security scanners
* Generate security findings reports

---

# 📋 Prerequisites

Before starting:

* Basic Linux command-line knowledge
* Understanding of JSON files
* Familiarity with firewall concepts
* Basic access control knowledge
* Text editor experience (nano, vim, vi)

---

# 🏗️ Detection Engine Architecture

```text
                Security Policies
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
 Firewall Policy                Access Control Policy
        │                               │
        ▼                               ▼
┌─────────────────┐          ┌─────────────────┐
│ Firewall Rule   │          │ Access Rule     │
│ Analyzer        │          │ Analyzer        │
└────────┬────────┘          └────────┬────────┘
         │                            │
         ▼                            ▼
  Misconfiguration             Permission Issues
     Detection                   Detection
         │                            │
         └──────────────┬─────────────┘
                        ▼
              Security Findings
                        │
                        ▼
                 Final Report
```

---

# 📂 Project Structure

```text
policy-lab/
│
├── firewall_policy.json
├── access_policy.json
├── secure_policy.json
├── policy_detector.py
│
└── README.md
```

---

# ⚙️ Environment Setup

## 🟢 Step 1: Update System

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

---

## 🟢 Step 2: Create Working Directory

```bash
mkdir ~/policy-lab

cd ~/policy-lab
```

---

## 🟢 Step 3: Install Dependencies

```bash
pip3 install pyyaml
```

---

# 🔥 Firewall Policy File

## 📄 firewall_policy.json

```json
{
  "firewall_rules": [
    {
      "rule_id": "FW-001",
      "action": "ALLOW",
      "source": "0.0.0.0/0",
      "destination": "10.0.0.5",
      "port": "22",
      "protocol": "TCP",
      "description": "SSH access from anywhere"
    },
    {
      "rule_id": "FW-002",
      "action": "ALLOW",
      "source": "192.168.1.0/24",
      "destination": "10.0.0.10",
      "port": "443",
      "protocol": "TCP",
      "description": "HTTPS from internal network"
    },
    {
      "rule_id": "FW-003",
      "action": "DENY",
      "source": "0.0.0.0/0",
      "destination": "10.0.0.5",
      "port": "22",
      "protocol": "TCP",
      "description": "Block SSH from anywhere"
    },
    {
      "rule_id": "FW-004",
      "action": "ALLOW",
      "source": "0.0.0.0/0",
      "destination": "10.0.0.20",
      "port": "3389",
      "protocol": "TCP",
      "description": "RDP access from anywhere"
    },
    {
      "rule_id": "FW-005",
      "action": "ALLOW",
      "source": "0.0.0.0/0",
      "destination": "10.0.0.30",
      "port": "*",
      "protocol": "*",
      "description": "Allow all traffic to database server"
    }
  ]
}
```

---

# 👥 Access Control Policy

## 📄 access_policy.json

```json
{
  "access_rules": [
    {
      "rule_id": "AC-001",
      "user": "admin",
      "resource": "/etc/passwd",
      "permission": "write",
      "description": "Admin can modify password file"
    },
    {
      "rule_id": "AC-002",
      "user": "*",
      "resource": "/var/log/secure",
      "permission": "read",
      "description": "Everyone can read security logs"
    },
    {
      "rule_id": "AC-003",
      "user": "guest",
      "resource": "/root",
      "permission": "read",
      "description": "Guest can read root directory"
    },
    {
      "rule_id": "AC-004",
      "user": "developer",
      "resource": "/home/developer",
      "permission": "read",
      "description": "Developer can read own directory"
    }
  ]
}
```

---

# 🚀 policy_detector.py

```python
#!/usr/bin/env python3

"""
Policy Misconfiguration Detection Engine
"""

import json


class PolicyDetector:

    def __init__(self):
        self.findings = []

    def load_policy(self, filename):

        try:
            with open(filename, 'r') as f:
                return json.load(f)

        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return None

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {filename}")
            return None

    def check_overly_permissive_source(self, rule):

        if (
            rule.get('source') == '0.0.0.0/0'
            and rule.get('action') == 'ALLOW'
        ):

            return (
                f"CRITICAL: Rule "
                f"{rule['rule_id']} allows "
                f"traffic from anywhere "
                f"to port {rule['port']}"
            )

        return None

    def check_conflicting_rules(self, rules):

        conflicts = []

        for i, rule1 in enumerate(rules):

            for rule2 in rules[i + 1:]:

                if (
                    rule1['source'] ==
                    rule2['source']
                    and
                    rule1['destination'] ==
                    rule2['destination']
                    and
                    rule1['port'] ==
                    rule2['port']
                    and
                    rule1['protocol'] ==
                    rule2['protocol']
                ):

                    if (
                        rule1['action']
                        !=
                        rule2['action']
                    ):

                        conflicts.append(
                            f"CONFLICT: Rules "
                            f"{rule1['rule_id']} "
                            f"and "
                            f"{rule2['rule_id']} "
                            f"have conflicting "
                            f"actions for same traffic"
                        )

        return conflicts

    def check_wildcard_permissions(self, rule):

        if rule.get('user') == '*':

            return (
                f"HIGH: Rule "
                f"{rule['rule_id']} grants "
                f"{rule['permission']} "
                f"to everyone"
            )

        return None

    def check_sensitive_resource_access(self, rule):

        sensitive_resources = [
            '/etc/passwd',
            '/etc/shadow',
            '/root',
            '/var/log/secure'
        ]

        resource = rule.get('resource')
        user = rule.get('user')

        if (
            resource in sensitive_resources
            and
            user not in ['admin', 'root']
        ):

            return (
                f"HIGH: Rule "
                f"{rule['rule_id']} allows "
                f"{user} access to "
                f"sensitive resource "
                f"{resource}"
            )

        return None

    def analyze_firewall_policy(self, policy_data):

        if not policy_data:
            return

        rules = policy_data.get(
            'firewall_rules',
            []
        )

        print(
            f"\nAnalyzing "
            f"{len(rules)} firewall rules..."
        )

        for rule in rules:

            finding = (
                self.check_overly_permissive_source(
                    rule
                )
            )

            if finding:
                self.findings.append(
                    finding
                )

        conflicts = (
            self.check_conflicting_rules(
                rules
            )
        )

        self.findings.extend(
            conflicts
        )

    def analyze_access_policy(
        self,
        policy_data
    ):

        if not policy_data:
            return

        rules = policy_data.get(
            'access_rules',
            []
        )

        print(
            f"Analyzing "
            f"{len(rules)} access control rules..."
        )

        for rule in rules:

            finding = (
                self.check_wildcard_permissions(
                    rule
                )
            )

            if finding:
                self.findings.append(
                    finding
                )

            finding = (
                self.check_sensitive_resource_access(
                    rule
                )
            )

            if finding:
                self.findings.append(
                    finding
                )

    def generate_report(self):

        print("\n" + "=" * 60)

        print(
            "SECURITY FINDINGS REPORT"
        )

        print("=" * 60)

        if not self.findings:

            print(
                "\nNo issues found."
            )

            return

        print(
            f"\nTotal Issues Found: "
            f"{len(self.findings)}\n"
        )

        for i, finding in enumerate(
            self.findings,
            1
        ):

            print(
                f"{i}. {finding}"
            )

        critical = sum(
            1
            for f in self.findings
            if "CRITICAL" in f
        )

        high = sum(
            1
            for f in self.findings
            if "HIGH" in f
        )

        print(
            "\n" + "-" * 60
        )

        print(
            f"Summary: "
            f"{critical} Critical, "
            f"{high} High severity issues"
        )

        print("=" * 60)


def main():

    print("=" * 60)
    print(
        "Policy Misconfiguration "
        "Detection Engine"
    )
    print("=" * 60)

    detector = PolicyDetector()

    firewall_policy = (
        detector.load_policy(
            'firewall_policy.json'
        )
    )

    detector.analyze_firewall_policy(
        firewall_policy
    )

    access_policy = (
        detector.load_policy(
            'access_policy.json'
        )
    )

    detector.analyze_access_policy(
        access_policy
    )

    detector.generate_report()

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
```

---

# ▶️ Make Executable

```bash
chmod +x policy_detector.py
```

---

# 🚀 Run Detection Engine

```bash
python3 policy_detector.py
```

---

# 📊 Expected Findings

```text
Total Issues Found: 7

CRITICAL: Rule FW-001 allows traffic from anywhere to port 22

CONFLICT: Rules FW-001 and FW-003 have conflicting actions

CRITICAL: Rule FW-004 allows traffic from anywhere to port 3389

CRITICAL: Rule FW-005 allows traffic from anywhere to port *

HIGH: Rule AC-002 grants read to everyone

HIGH: Rule AC-003 allows guest access to sensitive resource /root

HIGH: Rule AC-002 allows * access to sensitive resource /var/log/secure

Summary: 3 Critical, 4 High severity issues
```

---

# 🔒 Secure Policy Test

## 📄 secure_policy.json

```json
{
  "firewall_rules": [
    {
      "rule_id": "FW-100",
      "action": "ALLOW",
      "source": "192.168.1.0/24",
      "destination": "10.0.0.5",
      "port": "22",
      "protocol": "TCP",
      "description": "SSH from internal network only"
    }
  ]
}
```

---

# ✅ Verification

## Check Files

```bash
ls -lh ~/policy-lab/
```

Expected:

```text
firewall_policy.json
access_policy.json
secure_policy.json
policy_detector.py
```

---

## Test JSON Syntax

```bash
python3 -m json.tool firewall_policy.json
```

---

## Execute Detector

```bash
python3 policy_detector.py
```

Expected:

* Critical findings detected
* High severity findings detected
* Security report generated

---

# 🛠 Troubleshooting

## File Not Found

```bash
pwd
ls -la
```

---

## JSON Parsing Error

```bash
python3 -m json.tool firewall_policy.json
```

---

## Package Issues

```bash
pip3 install pyyaml
```

---

## Debug Rules

Add:

```python
print(f"Checking rule: {rule}")
```

inside analysis functions.

---

# 🔐 Security Concepts Demonstrated

✅ Firewall Rule Auditing

✅ Access Control Validation

✅ Security Policy Analysis

✅ Misconfiguration Detection

✅ Conflict Detection

✅ Least Privilege Enforcement

✅ Compliance Verification

---

# 🎓 Skills Acquired

* Security Policy Analysis
* Firewall Auditing
* Access Control Review
* Python Security Automation
* Threat Exposure Detection
* Security Compliance Validation
* DevSecOps Fundamentals

---

# 🏆 Conclusion

Congratulations! You have successfully built a **Policy Misconfiguration Detection Engine** capable of auditing firewall rules and access control policies for security weaknesses.

This project demonstrates foundational security engineering practices used by SOC analysts, cloud security engineers, DevSecOps teams, compliance auditors, and penetration testers to identify and remediate dangerous policy configurations before they become exploitable vulnerabilities.

### ⭐ Happy Security Auditing & Policy Hardening! 🛡️🔍🚀
