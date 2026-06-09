# 🔐 Identity and Access Risk Analysis Framework

> *A hands-on cybersecurity lab focused on Identity and Access Management (IAM) risk assessment, user behavior analytics, permission correlation, and risk scoring automation using Python.*


![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)

![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=linux)

![JSON](https://img.shields.io/badge/JSON-Data-green?style=for-the-badge\&logo=json)

![Pandas](https://img.shields.io/badge/Pandas-Analysis-purple?style=for-the-badge\&logo=pandas)

![Cybersecurity](https://img.shields.io/badge/Cybersecurity-IAM-red?style=for-the-badge)
---

## 📌 Overview

The **Identity and Access Risk Analysis Framework** is a practical cybersecurity project that demonstrates how organizations can identify risky user accounts by correlating identity information, permissions, and behavioral activity.

This project simulates a real-world IAM risk assessment workflow by:

* Collecting user identity information
* Mapping user permissions across critical resources
* Analyzing behavioral activity logs
* Calculating permission-based and behavior-based risk scores
* Generating comprehensive risk reports

The framework provides a foundation for **Identity Governance**, **Access Reviews**, **Insider Threat Detection**, and **Zero Trust Security** initiatives.

---

# 🎯 Learning Objectives

By completing this project, you will:

✅ Understand IAM risk analysis fundamentals

✅ Correlate user identities with permissions

✅ Analyze user behavior for anomalies

✅ Identify excessive privileges

✅ Detect suspicious account activities

✅ Build a weighted risk-scoring engine

✅ Generate actionable IAM security reports



# 📂 Project Structure

```text
iam-risk-lab/
│
├── data/
│   ├── users.json
│   ├── permissions.json
│   └── behavior_logs.json
│
├── scripts/
│   └── iam_risk_analyzer.py
│
├── reports/
│   └── iam_risk_report.txt
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

## Step 2: Install Required Packages

```bash
sudo apt install -y python3 python3-pip git jq
```

---

## Step 3: Create Project Structure

```bash
mkdir -p ~/iam-risk-lab/{data,scripts,reports}

cd ~/iam-risk-lab
```

---

## Step 4: Install Python Libraries

```bash
pip3 install pandas numpy
```

---

# 📋 Sample Identity Data

## users.json

```json
{
  "users": [
    {
      "id": "U001",
      "name": "Alice Johnson",
      "department": "Engineering",
      "role": "Developer",
      "hire_date": "2020-01-15"
    },
    {
      "id": "U002",
      "name": "Bob Smith",
      "department": "Finance",
      "role": "Analyst",
      "hire_date": "2019-06-20"
    },
    {
      "id": "U003",
      "name": "Carol White",
      "department": "Engineering",
      "role": "Admin",
      "hire_date": "2018-03-10"
    },
    {
      "id": "U004",
      "name": "David Brown",
      "department": "HR",
      "role": "Manager",
      "hire_date": "2021-09-01"
    },
    {
      "id": "U005",
      "name": "Eve Davis",
      "department": "Engineering",
      "role": "Developer",
      "hire_date": "2022-02-14"
    }
  ]
}
```

---

# 🔑 Permissions Dataset

## permissions.json

```json
{
  "permissions": [
    {
      "user_id": "U001",
      "resource": "database_prod",
      "access_level": "read"
    },
    {
      "user_id": "U001",
      "resource": "code_repo",
      "access_level": "write"
    },
    {
      "user_id": "U003",
      "resource": "database_prod",
      "access_level": "admin"
    },
    {
      "user_id": "U003",
      "resource": "server_config",
      "access_level": "admin"
    }
  ]
}
```

---

# 📊 User Activity Dataset

## behavior_logs.json

```json
{
  "activities": [
    {
      "user_id": "U003",
      "action": "login",
      "timestamp": "2024-01-15 22:45:00",
      "success": true
    },
    {
      "user_id": "U003",
      "action": "modify_config",
      "timestamp": "2024-01-15 23:00:00",
      "success": true
    },
    {
      "user_id": "U005",
      "action": "login",
      "timestamp": "2024-01-15 10:00:00",
      "success": false
    },
    {
      "user_id": "U005",
      "action": "delete_records",
      "timestamp": "2024-01-15 11:30:00",
      "success": true
    }
  ]
}
```

---

# 🧠 IAM Risk Analysis Engine

## Main Script

### iam_risk_analyzer.py

```python
#!/usr/bin/env python3

import json
from datetime import datetime

class IAMRiskAnalyzer:

    def __init__(self, users_file, permissions_file, behavior_file):

        self.users = self.load_json(users_file)["users"]
        self.permissions = self.load_json(permissions_file)["permissions"]
        self.activities = self.load_json(behavior_file)["activities"]

    def load_json(self, filepath):

        with open(filepath, "r") as f:
            return json.load(f)

    def correlate_user_data(self, user_id):

        user_info = next(
            (u for u in self.users if u["id"] == user_id),
            None
        )

        permissions = [
            p for p in self.permissions
            if p["user_id"] == user_id
        ]

        activities = [
            a for a in self.activities
            if a["user_id"] == user_id
        ]

        return {
            "identity": user_info,
            "permissions": permissions,
            "activities": activities
        }

    def analyze_permission_risk(self, permissions):

        risk_score = 0

        for permission in permissions:

            if permission["access_level"] == "admin":
                risk_score += 30

            elif permission["access_level"] == "write":
                risk_score += 15

            else:
                risk_score += 5

        return min(risk_score, 100)

    def analyze_behavior_risk(self, activities):

        risk_score = 0

        failed_logins = 0

        for activity in activities:

            if (
                activity["action"] == "login"
                and not activity.get("success", True)
            ):
                failed_logins += 1

        risk_score += failed_logins * 20

        for activity in activities:

            timestamp = activity.get("timestamp")

            if timestamp:

                hour = int(
                    timestamp.split()[1].split(":")[0]
                )

                if hour >= 22 or hour <= 6:
                    risk_score += 15

        high_risk_actions = [
            "delete_records",
            "modify_config",
            "privilege_escalation"
        ]

        for activity in activities:

            if activity["action"] in high_risk_actions:
                risk_score += 25

        return min(risk_score, 100)

    def calculate_composite_risk(self, user_id):

        data = self.correlate_user_data(user_id)

        permission_risk = self.analyze_permission_risk(
            data["permissions"]
        )

        behavior_risk = self.analyze_behavior_risk(
            data["activities"]
        )

        composite = (
            permission_risk * 0.4
            +
            behavior_risk * 0.6
        )

        if composite >= 70:
            level = "HIGH"

        elif composite >= 40:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "user": data["identity"]["name"],
            "risk_score": round(composite, 2),
            "risk_level": level
        }

    def analyze_all_users(self):

        results = []

        for user in self.users:

            results.append(
                self.calculate_composite_risk(user["id"])
            )

        return sorted(
            results,
            key=lambda x: x["risk_score"],
            reverse=True
        )

def main():

    analyzer = IAMRiskAnalyzer(
        "data/users.json",
        "data/permissions.json",
        "data/behavior_logs.json"
    )

    results = analyzer.analyze_all_users()

    print("=" * 60)
    print("IAM RISK ANALYSIS REPORT")
    print("=" * 60)

    for result in results:

        print(
            f"{result['user']:20} | "
            f"{result['risk_level']:6} | "
            f"{result['risk_score']}"
        )

if __name__ == "__main__":
    main()
```

---

# ▶️ Execute the Framework

```bash
cd ~/iam-risk-lab

python3 scripts/iam_risk_analyzer.py
```

---

# 📄 Example Output

```text
============================================================
IAM RISK ANALYSIS REPORT
============================================================

Carol White          | HIGH   | 81.0
Eve Davis            | HIGH   | 74.0
Alice Johnson        | LOW    | 20.0
Bob Smith            | LOW    | 10.0
David Brown          | LOW    | 15.0
```

---

# 🔍 Risk Scoring Methodology

| Factor               | Score |
| -------------------- | ----- |
| Admin Access         | +30   |
| Write Access         | +15   |
| Read Access          | +5    |
| Failed Login         | +20   |
| After-Hours Activity | +15   |
| Modify Config        | +25   |
| Delete Records       | +25   |

---

# 📈 Composite Risk Formula

```text
Composite Risk =
(Permission Risk × 40%)
+
(Behavior Risk × 60%)
```

---

# 🧪 Verification Commands

Verify JSON files:

```bash
jq . data/users.json
jq . data/permissions.json
jq . data/behavior_logs.json
```

Check report:

```bash
cat reports/iam_risk_report.txt
```

Find high-risk users:

```bash
grep "HIGH" reports/iam_risk_report.txt
```

---

# 🚨 Security Risks Identified

The framework can detect:

* Excessive administrative privileges
* Privilege creep
* Failed login attempts
* Suspicious after-hours activity
* Destructive actions
* Potential insider threats
* High-value resource exposure

---

# 📚 Real-World Applications

This framework mirrors workflows used by:

* Identity Governance Teams
* Security Operations Centers (SOC)
* Insider Threat Programs
* Privileged Access Management (PAM)
* Zero Trust Implementations
* Compliance Audits
* Risk Management Teams

---

# 🎯 Key Takeaways

✔ Identity alone does not determine risk

✔ Permissions must be correlated with behavior

✔ High privileges require continuous monitoring

✔ Risk scoring enables prioritization

✔ Behavioral analytics improve threat detection

✔ IAM is a foundational pillar of Zero Trust Security

---

# 🚀 Future Enhancements

* Role-Based Access Control (RBAC) analysis
* Machine Learning risk prediction
* Privileged Access Monitoring
* User Entity Behavior Analytics (UEBA)
* SIEM Integration
* Risk Dashboards
* Automated Access Reviews
* Insider Threat Detection Engine

---

# 👨‍💻 Author

**Muhammad Salman**

Cybersecurity | SOC Analyst | Threat Detection | IAM Security | Python Automation | Risk Management

---

> *"The greatest security risk is not always an attacker—it is often excessive access that nobody noticed."*
