# 🔐 Linux Authentication Log Analyzer

<div align="center">

# 🛡️ Linux Authentication Log Analysis Toolkit

### Detect Failed Logins • Track Successful Access • Identify Suspicious Activity

![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu)
![Bash](https://img.shields.io/badge/Bash-Scripting-black?style=for-the-badge\&logo=gnu-bash)
![Security](https://img.shields.io/badge/Cybersecurity-Log_Analysis-red?style=for-the-badge)
![Monitoring](https://img.shields.io/badge/Security-Monitoring-blue?style=for-the-badge)
![SIEM](https://img.shields.io/badge/SIEM-Foundations-green?style=for-the-badge)
![SOC](https://img.shields.io/badge/SOC-Operations-purple?style=for-the-badge)

---

### 🔍 Analyze Authentication Logs Like a Security Analyst

</div>

---

# 📚 Prerequisites

Before starting this lab, ensure you have:

✅ Basic Linux command line knowledge (`cd`, `ls`, `cat`)

✅ Understanding of text files and file paths

✅ Familiarity with text searching concepts

✅ SSH access to a Linux machine

---

# 🎯 Learning Objectives

By completing this lab, you will:

🔹 Understand Linux authentication log structure

🔹 Locate and analyze authentication logs

🔹 Detect failed login attempts

🔹 Track successful authentication events

🔹 Identify suspicious login activity

🔹 Build automated security monitoring scripts

🔹 Create a complete authentication log dashboard

---

# 🖥️ Environment Setup

---

## 🚀 Step 1: Access Your Lab Machine

Click **Start Lab** and connect to your Linux machine via SSH.

---

## 📂 Step 2: Verify Log Access

Authentication logs are usually stored in:

```bash
sudo ls -lh /var/log/auth.log*
```

Expected Output:

```text
auth.log
auth.log.1
auth.log.2.gz
```

---

## 🔧 Step 3: Verify Required Tools

```bash
which grep awk sed
```

Expected Output:

```text
/usr/bin/grep
/usr/bin/awk
/usr/bin/sed
```

---

## 📁 Step 4: Create Working Directory

```bash
mkdir ~/log-analysis

cd ~/log-analysis
```

---

# 🔍 Task 1: Understanding Authentication Logs

---

## 📖 Step 1: Examine Log Structure

View recent authentication events:

```bash
sudo tail -n 20 /var/log/auth.log
```

Example:

```text
Dec 15 10:23:45 server sshd[1234]:
Failed password for root from 192.168.1.100 port 55000 ssh2
```

### Log Components

| Component     | Example         |
| ------------- | --------------- |
| Timestamp     | Dec 15 10:23:45 |
| Hostname      | server          |
| Service       | sshd            |
| PID           | [1234]          |
| Event Message | Failed password |

---

## 🧪 Step 2: Generate Test Events

Create authentication activity:

```bash
# Intentional failed login
su - nonexistentuser

# Successful sudo authentication
sudo whoami
```

---

## 👀 Step 3: View Generated Events

```bash
sudo tail -n 5 /var/log/auth.log
```

Verify the events appear.

---

# 🚨 Task 2: Detecting Failed Login Attempts

---

## 🔍 Step 1: Find Failed Password Attempts

```bash
sudo grep "Failed password" /var/log/auth.log
```

---

## 📊 Step 2: Count Failed Attempts by Username

```bash
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-5)}' \
| sort \
| uniq -c \
| sort -rn
```

### Breakdown

| Command  | Purpose             |
| -------- | ------------------- |
| grep     | Find failed logins  |
| awk      | Extract username    |
| uniq -c  | Count occurrences   |
| sort -rn | Highest count first |

---

## 🌐 Step 3: Identify Attacking IP Addresses

```bash
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-3)}' \
| sort \
| uniq -c \
| sort -rn
```

---

## 🛠️ Step 4: Create Failed Login Report Script

Create file:

```bash
nano failed_logins.sh
```

Add:

```bash
#!/bin/bash

echo "=== Failed Login Attempts Report ==="
echo "Generated: $(date)"
echo ""

echo "Total Failed Attempts:"
sudo grep "Failed password" /var/log/auth.log | wc -l

echo ""
echo "Top 10 Usernames Targeted:"
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-5)}' \
| sort | uniq -c | sort -rn | head -10

echo ""
echo "Top 10 Source IPs:"
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-3)}' \
| sort | uniq -c | sort -rn | head -10
```

Run:

```bash
chmod +x failed_logins.sh

./failed_logins.sh
```

---

# ✅ Task 3: Analyzing Successful Logins

---

## 🔐 Step 1: Find Successful SSH Logins

```bash
sudo grep "Accepted password\|Accepted publickey" /var/log/auth.log
```

---

## 📋 Step 2: Extract Login Details

```bash
sudo grep "Accepted" /var/log/auth.log \
| awk '{print $1, $2, $3, $9, $11}'
```

Output:

```text
Dec 15 10:45:21 ubuntu 192.168.1.50
```

---

## 👤 Step 3: List Unique Users

```bash
sudo grep "Accepted" /var/log/auth.log \
| awk '{print $9}' \
| sort -u
```

---

## 📈 Step 4: Create Successful Login Report

Create:

```bash
nano successful_logins.sh
```

Add:

```bash
#!/bin/bash

echo "=== Successful Login Report ==="
echo "Generated: $(date)"
echo ""

echo "Total Successful Logins:"
sudo grep "Accepted" /var/log/auth.log | wc -l

echo ""
echo "Users Who Logged In:"
sudo grep "Accepted" /var/log/auth.log \
| awk '{print $9}' \
| sort -u

echo ""
echo "Recent 10 Successful Logins:"
sudo grep "Accepted" /var/log/auth.log \
| tail -10 \
| awk '{print $1, $2, $3, $9, "from", $11}'
```

Run:

```bash
chmod +x successful_logins.sh

./successful_logins.sh
```

---

# ⚠️ Task 4: Detecting Suspicious Activity

---

## 🚨 Step 1: Detect Brute Force Attacks

IPs with more than 5 failed attempts:

```bash
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-3)}' \
| sort \
| uniq -c \
| sort -rn \
| awk '$1 > 5'
```

---

## 👻 Step 2: Detect Invalid Users

```bash
sudo grep "Invalid user" /var/log/auth.log | head -20
```

Common attacker behavior:

```text
Invalid user admin
Invalid user test
Invalid user backup
```

---

## 👑 Step 3: Detect Root Login Attempts

```bash
sudo grep "Failed password for root" /var/log/auth.log
```

Root login attempts should be investigated immediately.

---

## 🕒 Step 4: Identify Unusual Login Hours

```bash
sudo grep "Accepted" /var/log/auth.log \
| awk '{print $3}' \
| cut -d: -f1 \
| sort \
| uniq -c
```

Example:

```text
5 08
15 09
20 10
1 03
```

A login at 03:00 may warrant investigation.

---

## 🚨 Step 5: Create Security Alert Script

Create:

```bash
nano security_alerts.sh
```

Add the full security alert analyzer from the lab instructions.

Run:

```bash
chmod +x security_alerts.sh

./security_alerts.sh
```

Expected Alerts:

```text
[ALERT] Brute Force Attempts
[ALERT] Invalid Users
[ALERT] Root Login Attempts
[ALERT] Failed Then Successful Logins
```

---

# 📊 Task 5: Build Complete Authentication Dashboard

---

## 🏗️ Step 1: Create Master Analyzer

Create:

```bash
nano auth_analyzer.sh
```

Add the complete analyzer script from the lab.

Run:

```bash
chmod +x auth_analyzer.sh

./auth_analyzer.sh
```

---

## 📈 Sample Dashboard Output

```text
========================================
AUTHENTICATION LOG ANALYSIS REPORT
========================================

Total Failed Attempts: 42
Total Successful Logins: 17
Total Invalid Users: 8

--- TOP ATTACKERS ---
12 203.0.113.10
9 198.51.100.5

--- TARGETED USERS ---
15 root
8 admin

--- SECURITY WARNINGS ---
[WARNING] Root login attempts detected
[WARNING] Brute force behavior detected
```

---

## 🗂️ Step 2: Analyze Older Logs

Check rotated logs:

```bash
sudo ls -lh /var/log/auth.log*
```

Analyze:

```bash
./auth_analyzer.sh /var/log/auth.log.1
```

---

# 📁 Project Structure

```text
log-analysis/
│
├── failed_logins.sh
├── successful_logins.sh
├── security_alerts.sh
└── auth_analyzer.sh
```

---

# ✅ Verification

---

## Check Failed Login Analyzer

```bash
./failed_logins.sh
```

Verify:

✔ Failed login count

✔ Top usernames

✔ Top source IPs

---

## Check Successful Login Analyzer

```bash
./successful_logins.sh
```

Verify:

✔ Successful login count

✔ User list

✔ Recent login events

---

## Check Security Alerts

```bash
./security_alerts.sh
```

Verify:

✔ Brute force detection

✔ Invalid users

✔ Root login attempts

✔ Failed → Successful login correlation

---

## Check Complete Dashboard

```bash
./auth_analyzer.sh
```

Verify:

✔ Summary statistics

✔ Attacker analysis

✔ Target analysis

✔ Security warnings

---

# 🧠 Knowledge Check

---

### How many unique attacker IPs?

```bash
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-3)}' \
| sort -u \
| wc -l
```

---

### Most common login hour?

```bash
sudo grep "Accepted\|Failed" /var/log/auth.log \
| awk '{print $3}' \
| cut -d: -f1 \
| sort | uniq -c | sort -rn | head -1
```

---

### Most targeted account?

```bash
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $(NF-5)}' \
| sort | uniq -c | sort -rn | head -1
```

---

# 🛠️ Troubleshooting

---

## ❌ Permission Denied

Use:

```bash
sudo grep "Failed password" /var/log/auth.log
```

Auth logs require elevated privileges.

---

## ❌ No Log Output

Check:

```bash
sudo ls -lh /var/log/auth.log
```

Some distributions use:

```text
/var/log/secure
```

---

## ❌ Script Won't Run

Make executable:

```bash
chmod +x scriptname.sh
```

Run:

```bash
./scriptname.sh
```

---

## ❌ Incorrect AWK Fields

Check total fields:

```bash
awk '{print NF}'
```

Different Linux distributions may use slightly different log formats.

---

## ❌ Empty Results

Generate activity:

```bash
sudo whoami

ssh localhost
```

Monitor logs:

```bash
sudo tail -f /var/log/auth.log
```

---

# 🎓 Skills Practiced

### 🔍 Log Analysis

* Authentication log parsing
* Event correlation
* Security monitoring

### 🛡️ Threat Detection

* Brute force attacks
* Invalid user attempts
* Root login attempts

### 🐧 Linux Security

* SSH monitoring
* Authentication auditing
* Security investigations

### 📊 Reporting

* Bash automation
* Dashboard creation
* Security alerting

---

# 🌍 Real-World Cybersecurity Applications

These techniques are used by:

🏢 SOC Analysts

🛡️ Security Engineers

🔍 Incident Responders

📈 SIEM Administrators

☁️ Cloud Security Teams

Authentication logs are often the first place investigators look when:

* Accounts are compromised
* Servers are attacked
* Brute force campaigns occur
* Unauthorized access is suspected

---

# 🏆 Conclusion

Congratulations! 🎉

You successfully built a Linux Authentication Log Analysis Toolkit capable of:

✅ Parsing authentication logs

✅ Detecting failed logins

✅ Tracking successful authentications

✅ Identifying brute force attacks

✅ Detecting root login attempts

✅ Generating automated security reports

✅ Building a complete authentication dashboard

---

# 🚀 Next Steps

Enhance the toolkit by adding:

🔹 Email alert notifications

🔹 Slack / Discord alerts

🔹 JSON report generation

🔹 SIEM integration

🔹 Real-time monitoring

🔹 GeoIP attacker analysis

🔹 Cron-based scheduled scans

🔹 Threat intelligence feeds

---

<div align="center">

# 🛡️ Lab Completed Successfully

### Authentication Logs ➜ Threat Detection ➜ Security Monitoring 🚀

⭐ Happy Hunting & Secure Logging ⭐

</div>
