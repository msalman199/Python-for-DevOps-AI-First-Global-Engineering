# 🌐 DNS Resolution and Anomaly Simulator

> *"DNS is the phonebook of the internet. Understanding its behavior is critical for identifying threats, detecting anomalies, and securing modern networks."*

<p align="center">
<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=ubuntu" />
<img src="https://img.shields.io/badge/DNS-Dnspython-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/Security-Network%20Monitoring-red?style=for-the-badge" />
<img src="https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-purple?style=for-the-badge" />
</p>

---

# 📖 Overview

This lab introduces practical DNS resolution techniques and demonstrates how cybersecurity professionals detect suspicious DNS activities.

You will learn how to:

✅ Query DNS records using Linux tools

✅ Build a Python DNS resolver

✅ Simulate common DNS anomalies

✅ Detect suspicious domains using entropy analysis

✅ Identify potential malware communication patterns

---

# 🎯 Learning Objectives

After completing this lab, you will be able to:

* 🌍 Understand how DNS resolution works
* 🔍 Query DNS records using command-line tools
* ⚠️ Simulate DNS anomalies and security threats
* 🛡️ Detect suspicious DNS behavior
* 📊 Build a basic DNS monitoring and anomaly detection system

---

# 🛠️ Prerequisites

Before starting, ensure you have:

* Basic Linux command line knowledge
* Understanding of IP addresses and domain names
* Familiarity with nano or vi editor
* Basic Python programming knowledge

---

# ⚙️ Environment Setup

## 🔹 Step 1: Update System

```bash
sudo apt update
```

---

## 🔹 Step 2: Install DNS Utilities

```bash
sudo apt install -y dnsutils bind9-host
```

---

## 🔹 Step 3: Install Python & Pip

```bash
sudo apt install -y python3 python3-pip
```

---

## 🔹 Step 4: Install DNS Python Library

```bash
pip3 install dnspython
```

---

## 🔹 Step 5: Verify Installation

### Check Dig

```bash
dig -v
```

### Check Python DNS Library

```bash
python3 -c "import dns.resolver; print('DNS library ready')"
```

Expected Output:

```text
DNS library ready
```

---

# 🧪 Task 1: DNS Resolution Basics

---

## 📌 Step 1: Explore DNS Query Tools

### Basic DNS Lookup

```bash
dig google.com
```

### Query Specific Record Types

```bash
dig google.com A
dig google.com AAAA
dig google.com MX
dig google.com NS
dig google.com TXT
```

### Short Output Format

```bash
dig +short google.com
```

### Query Specific DNS Server

```bash
dig @8.8.8.8 google.com
```

---

## 📌 Step 2: Analyze DNS Responses

```bash
dig example.com
```

### Key Sections

| Section    | Purpose          |
| ---------- | ---------------- |
| QUESTION   | Requested Record |
| ANSWER     | DNS Response     |
| SERVER     | DNS Server Used  |
| QUERY TIME | Resolution Speed |

---

## 📌 Step 3: Create DNS Query Logger

Create workspace:

```bash
mkdir ~/dns-lab
cd ~/dns-lab
```

Create log file:

```bash
touch dns_queries.log
```

---

### Create Query Script

```bash
nano query_domains.sh
```

```bash
#!/bin/bash

DOMAINS=("google.com" "github.com" "stackoverflow.com" "example.com")
LOGFILE="dns_queries.log"

echo "=== DNS Query Log - $(date) ===" >> $LOGFILE

for domain in "${DOMAINS[@]}"
do
    echo "Querying: $domain" >> $LOGFILE
    dig +short $domain >> $LOGFILE
    echo "---" >> $LOGFILE
done
```

Make executable:

```bash
chmod +x query_domains.sh
```

Run:

```bash
./query_domains.sh
```

View logs:

```bash
cat dns_queries.log
```

---

# 🧪 Task 2: Build DNS Resolver

---

## 📌 Step 1: Create DNS Resolver Script

```bash
nano dns_resolver.py
```

### Features

* DNS lookups
* Error handling
* Multi-domain checking
* A-record resolution

Run:

```bash
python3 dns_resolver.py
```

Expected Output:

```text
============================================================
DNS Resolution Check
============================================================

Checking: google.com
 -> 142.250.x.x

Checking: github.com
 -> 140.82.x.x
```

---

# 🚨 Task 3: DNS Anomaly Simulator

---

## 📌 Step 1: Create Simulator

```bash
nano dns_anomaly_simulator.py
```

This simulator demonstrates:

### ✅ Normal DNS Queries

Legitimate domain lookups.

### ❌ NXDOMAIN Simulation

Example:

```text
nonexistent1234.invalid
```

---

### ⚠️ Fast Flux DNS

Rapid IP rotation:

```text
Query 1 → 192.0.2.55
Query 2 → 192.0.2.91
Query 3 → 192.0.2.144
```

Commonly seen in:

* Botnets
* Malware infrastructure
* Phishing campaigns

---

### ⚠️ DGA (Domain Generation Algorithm)

Generated domains:

```text
aksjdhfkajshdfkjhaskdf.com
```

Characteristics:

* High entropy
* Random characters
* Difficult to predict

Run:

```bash
python3 dns_anomaly_simulator.py
```

---

# 🔍 Task 4: DNS Anomaly Detector

---

## 📌 Step 1: Create Detector

```bash
nano dns_anomaly_detector.py
```

The detector performs:

### 📏 Domain Length Analysis

Checks:

```text
Very Long Domains
Very Short Domains
```

---

### 🔢 Numeric Ratio Analysis

Example:

```text
abc123456789xyz.com
```

High numeric ratios are suspicious.

---

### 📊 Entropy Analysis

Used to identify:

* DGA domains
* Randomly generated names
* Malware communication domains

---

## 📌 Risk Assessment Levels

| Risk      | Description                 |
| --------- | --------------------------- |
| 🟢 LOW    | No anomalies                |
| 🟡 MEDIUM | One anomaly detected        |
| 🔴 HIGH   | Multiple anomalies detected |

---

### Run Detector

```bash
python3 dns_anomaly_detector.py
```

---

# 🧪 Verification

---

## Verify DNS Resolution

```bash
dig +short google.com
```

---

## Verify Python DNS Library

```bash
python3 -c "import dns.resolver; r = dns.resolver.Resolver(); print(r.resolve('google.com','A')[0])"
```

---

## Verify Scripts

```bash
ls -lh ~/dns-lab/
```

Expected:

```text
dns_resolver.py
dns_anomaly_simulator.py
dns_anomaly_detector.py
query_domains.sh
dns_queries.log
```

---

## Run All Components

```bash
python3 dns_resolver.py

python3 dns_anomaly_simulator.py

python3 dns_anomaly_detector.py
```

---

# 📊 Expected Results

### DNS Resolver

```text
google.com -> IP Address
github.com -> IP Address
localhost -> 127.0.0.1
```

---

### Anomaly Simulator

Shows:

✅ Normal DNS Queries

❌ NXDOMAIN Events

⚠️ Fast Flux Activity

⚠️ DGA Domains

---

### Anomaly Detector

Produces:

```text
[OK] Domain Length

[SUSPICIOUS] Entropy

[SUSPICIOUS] Numeric Ratio

Overall:
HIGH RISK
```

---

# 🔧 Troubleshooting

---

## ❌ dig Command Not Found

Install DNS utilities:

```bash
sudo apt install -y dnsutils
```

---

## ❌ Python DNS Import Error

```bash
pip3 install --user dnspython
```

---

## ❌ Permission Denied

```bash
chmod +x dns_resolver.py
chmod +x dns_anomaly_detector.py
chmod +x dns_anomaly_simulator.py
```

---

## ❌ DNS Timeout

Check connectivity:

```bash
ping 8.8.8.8
```

Verify DNS:

```bash
cat /etc/resolv.conf
```

---

# 🔒 Security Concepts Covered

### DNS Resolution

Convert:

```text
google.com
```

into

```text
142.250.x.x
```

---

### Fast Flux

Attackers constantly rotate IP addresses to evade detection.

---

### DGA Domains

Malware generates thousands of random domains daily.

Example:

```text
kjashdfkjahsdjkhaskjdh.com
```

---

### NXDOMAIN Monitoring

Excessive NXDOMAIN requests may indicate:

* Malware
* Misconfigured systems
* Command-and-control traffic

---

# 📚 Real-World Applications

This lab reflects techniques used by:

* 🔐 SOC Analysts
* 🛡️ Threat Hunters
* 🌐 Network Security Engineers
* 🚨 Incident Responders
* 🕵️ Digital Forensics Teams

Common use cases:

* Malware detection
* DNS abuse monitoring
* Threat intelligence analysis
* Command-and-control discovery
* Security investigations

---

# 🎓 Conclusion

Congratulations! 🎉

You have successfully:

✅ Performed DNS queries using Linux tools

✅ Built a Python DNS resolver

✅ Simulated DNS anomalies

✅ Implemented DGA detection logic

✅ Created a DNS anomaly detector

✅ Learned how security teams identify suspicious DNS activity

---

## 🚀 Next Steps

Enhance the project by adding:

* Typosquatting detection
* DNS tunneling detection
* Threat intelligence feeds
* Real-time monitoring dashboards
* SIEM integration
* Automated alerting

---

<p align="center">
<b>🛡️ Cybersecurity • DNS Analysis • Threat Detection • Network Monitoring 🛡️</b>
</p>
