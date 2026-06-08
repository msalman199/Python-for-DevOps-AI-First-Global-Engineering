# 🔒 Integrity Monitoring and Tamper Detection Tool

> *"Trust is good, but verification is better. File Integrity Monitoring helps detect unauthorized system changes before they become security incidents."*

---

## 📌 Overview

The **Integrity Monitoring and Tamper Detection Tool** lab demonstrates how cybersecurity professionals use **AIDE (Advanced Intrusion Detection Environment)** to monitor critical files and detect unauthorized modifications.

This project walks through:

* Creating a file integrity baseline
* Monitoring critical files and directories
* Detecting file tampering attempts
* Generating security alerts
* Automating integrity verification

---

## 🎯 Learning Objectives

By completing this lab, you will:

* Understand file integrity monitoring concepts
* Install and configure AIDE
* Create integrity baselines
* Detect unauthorized file modifications
* Generate and interpret security alerts
* Automate integrity monitoring workflows

---

## 🛠️ Technologies Used

![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu)
![AIDE](https://img.shields.io/badge/AIDE-Integrity%20Monitoring-blue?style=for-the-badge)
![Bash](https://img.shields.io/badge/Bash-Scripting-4EAA25?style=for-the-badge\&logo=gnubash)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-File%20Integrity-red?style=for-the-badge)

---

# 📋 Prerequisites

Before starting, ensure you have:

* Basic Linux command-line knowledge
* Understanding of file permissions
* Familiarity with nano or vi text editors
* Access to a Linux machine with sudo privileges

---

# 🏗️ Environment Setup

## Step 1: Update System and Install AIDE

```bash
sudo apt update
sudo apt install aide -y
```

### Verify Installation

```bash
aide --version
```

Expected Output:

```text
AIDE x.x.x
```

---

# 🚀 Task 1: Initialize AIDE and Create Baseline Database

## Step 1.1: Review AIDE Configuration

```bash
sudo cat /etc/aide/aide.conf | grep -v "^#" | grep -v "^$" | head -20
```

### Important Directories Monitored

| Directory | Purpose                 |
| --------- | ----------------------- |
| `/bin`    | System binaries         |
| `/sbin`   | Administrative binaries |
| `/etc`    | Configuration files     |

---

## Step 1.2: Create Initial Baseline

```bash
sudo aideinit
```

This process scans configured files and generates a baseline integrity database.

⏱️ Expected Duration: 2–5 minutes

---

## Step 1.3: Activate Database

```bash
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

---

## Step 1.4: Verify Database Creation

```bash
ls -lh /var/lib/aide/aide.db
```

Expected:

```text
-rw------- 1 root root XXM aide.db
```

---

# 🧪 Task 2: Monitor Files and Detect Tampering

## Step 2.1: Create Critical Files

```bash
sudo mkdir -p /opt/critical_files

sudo bash -c 'echo "Original content - Configuration file" > /opt/critical_files/config.txt'

sudo bash -c 'echo "Original content - Data file" > /opt/critical_files/data.txt'

sudo bash -c 'echo "#!/bin/bash" > /opt/critical_files/script.sh'

sudo chmod +x /opt/critical_files/script.sh
```

Verify:

```bash
ls -la /opt/critical_files/
```

---

## Step 2.2: Add Custom Monitoring Rule

### Backup Configuration

```bash
sudo cp /etc/aide/aide.conf /etc/aide/aide.conf.backup
```

### Add Monitoring Rule

```bash
sudo bash -c 'echo "" >> /etc/aide/aide.conf'
sudo bash -c 'echo "# Custom monitoring for lab" >> /etc/aide/aide.conf'
sudo bash -c 'echo "/opt/critical_files R" >> /etc/aide/aide.conf'
```

### Rule Explanation

```text
R = Monitor:
✔ Permissions
✔ Ownership
✔ File Type
✔ File Content
```

---

## Step 2.3: Update Database

```bash
sudo aide --update

sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

---

## Step 2.4: Initial Integrity Check

```bash
sudo aide --check
```

Expected:

```text
AIDE found NO differences between database and filesystem.
```

---

# ⚠️ Simulate File Tampering

## Modify File Content

```bash
sudo bash -c 'echo "TAMPERED - Malicious content added" >> /opt/critical_files/config.txt'
```

---

## Change Permissions

```bash
sudo chmod 777 /opt/critical_files/script.sh
```

---

## Delete File

```bash
sudo rm /opt/critical_files/data.txt
```

---

## Add Unauthorized File

```bash
sudo bash -c 'echo "Backdoor script" > /opt/critical_files/backdoor.sh'
```

---

## Detect Tampering

```bash
sudo aide --check
```

Expected Detection:

* Modified Files
* Permission Changes
* Deleted Files
* Added Files

---

## Generate Detailed Report

```bash
sudo aide --check > /tmp/aide_report.txt 2>&1
```

View Report:

```bash
cat /tmp/aide_report.txt
```

---

## View Summary Section

```bash
grep -A 20 "^Summary:" /tmp/aide_report.txt
```

Example:

```text
Summary:
Total entries: XXXX
Added files: 1
Removed files: 1
Changed files: 2
```

---

# 🚨 Task 3: Create Automated Alerting System

## Step 3.1: Create Monitoring Script

```bash
sudo nano /usr/local/bin/integrity_monitor.sh
```

Add:

```bash
#!/bin/bash

REPORT_FILE="/var/log/aide_check_$(date +%Y%m%d_%H%M%S).log"
ALERT_FILE="/var/log/aide_alerts.log"

echo "Running integrity check at $(date)" | sudo tee -a $ALERT_FILE

sudo aide --check > $REPORT_FILE 2>&1

if grep -q "found differences" $REPORT_FILE; then

    echo "ALERT: File integrity violations detected!" | sudo tee -a $ALERT_FILE

    echo "Report saved to: $REPORT_FILE" | sudo tee -a $ALERT_FILE

    grep -A 10 "^Summary:" $REPORT_FILE | sudo tee -a $ALERT_FILE

    echo "---" | sudo tee -a $ALERT_FILE
else
    echo "No integrity violations detected." | sudo tee -a $ALERT_FILE
fi
```

---

## Step 3.2: Make Script Executable

```bash
sudo chmod +x /usr/local/bin/integrity_monitor.sh
```

---

## Step 3.3: Run Monitoring Script

```bash
sudo /usr/local/bin/integrity_monitor.sh
```

---

## Step 3.4: View Alert Log

```bash
cat /var/log/aide_alerts.log
```

Example:

```text
Running integrity check...
ALERT: File integrity violations detected!
Report saved to: /var/log/aide_check_xxx.log
```

---

## Step 3.5: View Generated Reports

```bash
ls -lh /var/log/aide_check_*.log
```

View Latest:

```bash
sudo cat $(ls -t /var/log/aide_check_*.log | head -1)
```

---

# ✅ Verification

## Verify Database

```bash
sudo aide --check --config=/etc/aide/aide.conf | head -20
```

---

## Verify Tampering Detection

```bash
grep -c "changed" /tmp/aide_report.txt
```

Expected:

```text
Number > 0
```

---

## Verify Alert Generation

```bash
test -f /var/log/aide_alerts.log && echo "Alert log exists"
```

Count Alerts:

```bash
grep -c "ALERT" /var/log/aide_alerts.log
```

---

# 🧹 Complete Verification Test

## Restore Files

```bash
sudo bash -c 'echo "Original content - Configuration file" > /opt/critical_files/config.txt'

sudo chmod 755 /opt/critical_files/script.sh

sudo bash -c 'echo "Original content - Data file" > /opt/critical_files/data.txt'

sudo rm /opt/critical_files/backdoor.sh
```

---

## Update Baseline

```bash
sudo aide --update

sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

---

## Final Integrity Check

```bash
sudo aide --check | grep -i "found NO differences"
```

Expected:

```text
AIDE found NO differences
```

---

# 🛠️ Troubleshooting

## AIDE Initialization Takes Too Long

**Cause**

Large filesystem scan.

**Solution**

Wait 5–10 minutes for completion.

---

## Permission Denied Errors

**Solution**

Use:

```bash
sudo
```

for all AIDE commands.

---

## Database Not Found

```bash
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
```

---

## No Changes Detected

Verify rule exists:

```bash
grep "/opt/critical_files" /etc/aide/aide.conf
```

---

# 🌍 Real-World Applications

File Integrity Monitoring is used for:

* Malware Detection
* Rootkit Detection
* Security Incident Investigation
* Compliance Monitoring
* Configuration Protection
* Insider Threat Detection

---

# 🔐 Security Benefits

| Security Control        | Benefit                       |
| ----------------------- | ----------------------------- |
| Integrity Monitoring    | Detects unauthorized changes  |
| Baseline Comparison     | Identifies anomalies          |
| Alerting                | Provides immediate visibility |
| Audit Trail             | Supports investigations       |
| Continuous Verification | Improves security posture     |

---

# 📚 Key Takeaways

✅ Created an AIDE integrity baseline

✅ Monitored critical files and directories

✅ Detected file modifications and deletions

✅ Detected unauthorized file additions

✅ Automated integrity checks

✅ Generated security alerts

✅ Learned a core cybersecurity defensive control

---

# 🎓 Conclusion

In this lab, you successfully built a **File Integrity Monitoring (FIM)** solution using **AIDE**, one of the most widely used open-source integrity monitoring tools.

You learned how to:

* Establish a trusted baseline
* Detect unauthorized modifications
* Generate forensic reports
* Automate security monitoring
* Investigate potential tampering incidents

These techniques are commonly used by SOC analysts, system administrators, incident responders, and forensic investigators to protect critical systems and maintain trust in computing environments.

---

## ⭐ Next Steps

Enhance this project by:

* Scheduling checks with Cron
* Sending alerts to SIEM platforms
* Monitoring additional directories
* Integrating email notifications
* Storing AIDE databases on read-only media
* Automating incident response workflows

---

### 🔥 Cybersecurity Skills Demonstrated

* File Integrity Monitoring (FIM)
* Linux Security Administration
* AIDE Configuration
* Incident Detection
* Security Automation
* Threat Monitoring
* Defensive Security Operations
* Compliance Monitoring

**Secure systems start with knowing when something changes.**
