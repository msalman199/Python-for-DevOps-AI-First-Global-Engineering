# 🔐 Identity and Access Risk Scoring System

> *"Modern cybersecurity is not just about protecting systems—it's about understanding who has access, how they use it, and when that behavior becomes risky."*

---

## 📌 Overview

The **Identity and Access Risk Scoring System** is a hands-on cybersecurity project designed to simulate how modern Identity and Access Management (IAM) platforms evaluate user risk.

This lab demonstrates how security teams can:

* Quantify IAM risks using measurable factors
* Detect risky user behavior patterns
* Analyze permissions and privilege levels
* Identify anomalies through statistical analysis
* Generate actionable security reports

The project combines **Python**, **JSON**, **Pandas**, and **behavior analytics** to create a simplified version of enterprise IAM risk assessment solutions.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Understand Identity and Access Management (IAM) risk concepts

✅ Learn how security teams score users based on risk

✅ Analyze permissions and detect excessive privileges

✅ Identify anomalous user activities

✅ Build a practical risk scoring engine using Python

✅ Generate risk assessment reports for remediation

---

# 🛠️ Prerequisites

Before starting, ensure you have:

* Basic Linux command-line knowledge
* Understanding of user accounts and permissions
* Familiarity with Python fundamentals
* Basic JSON knowledge
* Python 3.x installed

---

# 🏗️ Environment Setup

## Step 1: Update System

```bash
sudo apt update
```

---

## Step 2: Install Python and Pip

```bash
sudo apt install -y python3 python3-pip
```

---

## Step 3: Install Required Libraries

```bash
pip3 install pandas numpy
```

---

## Step 4: Create Lab Directory

```bash
mkdir -p ~/iam-risk-lab
cd ~/iam-risk-lab
```

---

# 📂 Project Structure

```text
iam-risk-lab/
│
├── generate_data.py
├── iam_data.json
├── risk_scorer.py
├── anomaly_detector.py
├── risk_report.csv
│
└── README.md
```

---

# 📊 Task 1: Generate Sample IAM Data

## Create Data Generator

Create the file:

```bash
nano generate_data.py
```

This script generates:

* User identities
* Roles
* Permissions
* Activity logs
* Password age information

### Sample Users

| User    | Role       | Department  |
| ------- | ---------- | ----------- |
| alice   | admin      | IT          |
| bob     | developer  | Engineering |
| charlie | analyst    | Finance     |
| david   | user       | HR          |
| eve     | contractor | External    |

---

## Generate Dataset

```bash
python3 generate_data.py
```

### Expected Output

```text
Sample IAM data generated successfully!
Created data for 5 users
```

---

## Review Generated Data

```bash
cat iam_data.json
```

Example:

```json
{
  "username": "alice",
  "role": "admin",
  "permissions": [
    "read",
    "write",
    "delete",
    "admin"
  ]
}
```

---

# 🔎 Task 2: Build the IAM Risk Scoring Engine

## Create Risk Scorer

```bash
nano risk_scorer.py
```

The scoring engine evaluates risk using three categories:

| Category             | Maximum Score |
| -------------------- | ------------- |
| Permission Risk      | 30            |
| Behavioral Risk      | 40            |
| Account Hygiene Risk | 30            |

**Total Maximum Risk Score = 100**

---

# 🚨 Permission Risk Analysis

High-risk permissions increase exposure.

### High-Risk Permissions

```python
high_risk_perms = [
    "admin",
    "sudo",
    "config_change",
    "delete"
]
```

Each high-risk permission adds:

```text
+10 Risk Points
```

---

### Medium-Risk Permissions

```python
medium_risk_perms = [
    "deploy",
    "database_access"
]
```

Each medium-risk permission adds:

```text
+5 Risk Points
```

---

### Low-Risk Permissions

```python
read
write
report_access
```

Each low-risk permission adds:

```text
+1 Risk Point
```

---

# 👤 Behavioral Risk Analysis

The engine evaluates:

## Failed Logins

```python
failed_logins > 10
```

Risk:

```text
+15 Points
```

---

## Off-Hours Access

Access outside business hours may indicate:

* Compromised accounts
* Insider threats
* Suspicious automation

Risk:

```text
+12 Points
```

---

## Privilege Escalation Attempts

Each attempt adds:

```text
+5 Points
```

---

## Excessive Downloads

Large data downloads may indicate:

* Data exfiltration
* Unauthorized copying
* Insider activity

Risk:

```text
+8 Points
```

---

# 🔑 Account Hygiene Risk

Password age contributes to risk.

| Password Age | Risk |
| ------------ | ---- |
| >180 Days    | 30   |
| >90 Days     | 20   |
| >60 Days     | 10   |
| ≤60 Days     | 5    |

---

# 📈 Risk Classification

After combining all scores:

| Score  | Risk Level  |
| ------ | ----------- |
| 70-100 | 🔴 CRITICAL |
| 50-69  | 🟠 HIGH     |
| 30-49  | 🟡 MEDIUM   |
| 0-29   | 🟢 LOW      |

---

# ▶️ Run Risk Analysis

```bash
python3 risk_scorer.py
```

---

# 📋 Example Output

```text
================================================================================
IAM RISK ASSESSMENT REPORT
================================================================================

 username   role       total_risk_score   risk_level
 alice      admin      72                 CRITICAL
 eve        contractor 68                 HIGH
 bob        developer  40                 MEDIUM
 charlie    analyst    28                 LOW
 david      user       18                 LOW
```

---

# 📄 CSV Report Generation

The engine automatically exports:

```text
risk_report.csv
```

View it:

```bash
cat risk_report.csv
```

---

# 🚨 Task 3: Implement Anomaly Detection

## Create Detector

```bash
nano anomaly_detector.py
```

The anomaly detector identifies unusual user behavior.

---

# 📊 Statistical Analysis

The detector calculates:

* Mean
* Standard Deviation

for:

* Login Count
* Failed Logins
* Off-Hours Access

---

# 🎯 Detection Logic

A user is flagged when activity exceeds:

```text
Mean + (2 × Standard Deviation)
```

This method helps identify outliers without machine learning.

---

## Detect Excessive Logins

Example:

```python
if login_count > mean + (2 * std):
```

---

## Detect Failed Login Spikes

Example:

```python
if failed_logins > mean + (2 * std):
```

---

## Detect Off-Hours Activity

Example:

```python
if off_hours_access > mean + (2 * std):
```

---

## Detect Privilege Escalation Attempts

Any escalation attempt is flagged.

Example:

```python
if privilege_escalation_attempts > 0:
```

---

# ▶️ Run Anomaly Detection

```bash
python3 anomaly_detector.py
```

---

# 📋 Sample Output

```text
================================================================================
ANOMALY DETECTION REPORT
================================================================================

USER: eve (contractor)

Department: External

Anomalies detected:

- Excessive logins: 89
- High failed logins: 24
- Unusual off-hours access: 31
- Privilege escalation attempts: 2
```

---

# 🧪 Verification

## Check All Files

```bash
ls -lh ~/iam-risk-lab/
```

Expected:

```text
generate_data.py
iam_data.json
risk_scorer.py
risk_report.csv
anomaly_detector.py
```

---

## View Risk Distribution

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('risk_report.csv')
print(df['risk_level'].value_counts())
"
```

---

## Display Highest Risk Users

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('risk_report.csv')
print(df.nlargest(3, 'total_risk_score'))
"
```

---

# 🔥 Test With High-Risk User

Add a simulated high-risk account:

```python
{
  "username": "test_user",
  "role": "admin",
  "permissions": [
    "admin",
    "sudo",
    "delete",
    "config_change"
  ]
}
```

Re-run:

```bash
python3 risk_scorer.py
```

Expected:

```text
Risk Level: CRITICAL
```

---

# 🐞 Troubleshooting

## Module Not Found

Install dependencies:

```bash
pip3 install --user pandas numpy
```

---

## Permission Denied

```bash
chmod +x *.py
```

---

## JSON Decode Error

Regenerate dataset:

```bash
python3 generate_data.py
```

---

# 🛡️ Security Concepts Demonstrated

This project introduces several real-world IAM security concepts:

* Identity Governance
* User Risk Scoring
* Behavioral Analytics
* Insider Threat Detection
* Privileged Access Monitoring
* Account Hygiene Assessment
* Statistical Anomaly Detection

---

# 🌍 Real-World Applications

Organizations use similar systems for:

### 🔐 IAM Security Platforms

* Microsoft Entra ID Protection
* Okta Identity Security
* CyberArk Identity
* Ping Identity

### 🛡️ Security Operations

* User behavior analytics
* Insider threat monitoring
* Risk-based authentication
* Access reviews

### ☁️ Cloud Security

* Privileged account monitoring
* IAM posture assessment
* Compliance validation

---

# 🚀 Future Enhancements

Potential improvements include:

* SIEM integration
* Real-time risk scoring
* Machine learning anomaly detection
* Time-series trend analysis
* Automated alerting
* Dashboard visualization
* MFA risk assessment
* Cloud IAM integrations

---

# 🎓 Key Takeaways

✅ Risk scoring combines multiple security indicators

✅ Permissions alone do not define risk

✅ Behavioral analytics help detect compromised accounts

✅ Statistical methods can identify anomalies effectively

✅ Continuous IAM monitoring improves security posture

✅ Automated risk assessment helps prioritize remediation efforts

---

# 🏆 Conclusion

The **Identity and Access Risk Scoring System** demonstrates how cybersecurity professionals assess user risk by combining permissions, behavior analysis, and account hygiene into a unified scoring model.

Through this project, you gained practical experience building an IAM security solution capable of:

* Quantifying risk
* Detecting anomalies
* Identifying privileged threats
* Generating actionable security reports

These same concepts are used in enterprise IAM, Zero Trust architectures, UEBA platforms, and modern security operations centers (SOCs) worldwide.

---

### ⭐ If you found this project useful, consider starring the repository and sharing it with fellow cybersecurity learners.
