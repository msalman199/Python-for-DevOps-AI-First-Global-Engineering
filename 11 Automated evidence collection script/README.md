# 🔍 Automated Evidence Collection Script

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/Bash-Scripting-121011?style=for-the-badge&logo=gnubash&logoColor=white" />
  <img src="https://img.shields.io/badge/Digital-Forensics-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Security-Incident_Response-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Hashing-SHA256-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/MD5-Verification-orange?style=for-the-badge" />
</p>

---

# 📖 Overview

This lab demonstrates how to build an **Automated Evidence Collection Script** using Bash scripting on Linux.

The script automates forensic evidence gathering by collecting:

* 🖥️ System Information
* 👤 User Activity
* ⚙️ Running Processes
* 🌐 Network Configuration
* 📜 System Logs
* 🔐 Cryptographic Hashes

The collected evidence is stored securely with timestamps and integrity verification to maintain the **Chain of Custody** required during forensic investigations.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Understand forensic evidence collection fundamentals

✅ Create an automated Bash collection script

✅ Collect system information and logs

✅ Preserve evidence using timestamps

✅ Generate MD5 and SHA256 integrity hashes

✅ Create secure evidence archives

✅ Learn chain-of-custody best practices

---

# 📋 Prerequisites

Before starting, ensure you have:

* Linux System Access
* Basic Linux Command Knowledge
* Understanding of File Navigation (`cd`, `ls`, `pwd`)
* Familiarity with Nano or Vim
* Basic Bash Scripting Knowledge
* Root or Sudo Privileges

---

# 🛠️ Environment Setup

## 🚀 Start Lab Environment

Al Nafi provides a Linux cloud machine.

Click:

**Start Lab**

to access your environment.

---

## 📦 Install Required Packages

```bash
# Update repositories
sudo apt update

# Install required tools
sudo apt install -y coreutils util-linux net-tools

# Verify installation
which md5sum sha256sum date hostname
```

Expected Output:

```bash
/usr/bin/md5sum
/usr/bin/sha256sum
/usr/bin/date
/usr/bin/hostname
```

---

# 🧪 Task 1 — Create the Evidence Collection Script

---

## 📁 Step 1: Create Working Directories

```bash
mkdir -p ~/forensic-tools
cd ~/forensic-tools

mkdir -p ~/evidence-collection
```

Verify:

```bash
ls -la ~
```

---

## ✍️ Step 2: Create Collection Script

```bash
nano collect_evidence.sh
```

Paste the following complete script:

```bash
#!/bin/bash

# Automated Evidence Collection Script

EVIDENCE_DIR=~/evidence-collection/evidence_$(date +%Y%m%d_%H%M%S)
CASE_NAME="Lab11_Evidence_Collection"
COLLECTOR="Student_$(whoami)"

mkdir -p "$EVIDENCE_DIR"

cat > "$EVIDENCE_DIR/case_info.txt" << EOF
Case Name: $CASE_NAME
Collector: $COLLECTOR
Collection Date: $(date)
Hostname: $(hostname)
EOF

echo "Evidence collection started..."

collect_system_info() {

    echo "Collecting system information..."

    hostname > "$EVIDENCE_DIR/hostname.txt"
    uptime > "$EVIDENCE_DIR/uptime.txt"
    cat /etc/os-release > "$EVIDENCE_DIR/os_info.txt"
    uname -a > "$EVIDENCE_DIR/kernel_info.txt"
    date > "$EVIDENCE_DIR/collection_time.txt"
}

collect_user_process_info() {

    echo "Collecting user and process information..."

    w > "$EVIDENCE_DIR/logged_users.txt"
    cat /etc/passwd > "$EVIDENCE_DIR/user_accounts.txt"
    ps aux > "$EVIDENCE_DIR/running_processes.txt"
}

collect_network_info() {

    echo "Collecting network information..."

    ip addr > "$EVIDENCE_DIR/network_interfaces.txt"
    netstat -tuln > "$EVIDENCE_DIR/network_connections.txt" 2>/dev/null
    ip route > "$EVIDENCE_DIR/routing_table.txt"
}

collect_logs() {

    echo "Collecting system logs..."

    mkdir -p "$EVIDENCE_DIR/logs"

    sudo cp /var/log/auth.log* "$EVIDENCE_DIR/logs/" 2>/dev/null
    sudo cp /var/log/syslog* "$EVIDENCE_DIR/logs/" 2>/dev/null

    last > "$EVIDENCE_DIR/last_logins.txt"
    sudo lastb > "$EVIDENCE_DIR/failed_logins.txt" 2>/dev/null
}

create_hashes() {

    echo "Creating hash values..."

    find "$EVIDENCE_DIR" -type f -exec md5sum {} \; > "$EVIDENCE_DIR/evidence_md5.txt"

    find "$EVIDENCE_DIR" -type f -exec sha256sum {} \; > "$EVIDENCE_DIR/evidence_sha256.txt"
}

create_summary() {

    echo "Creating summary..."

    cat > "$EVIDENCE_DIR/summary.txt" << EOF
Collection End Time: $(date)
Total Files: $(find "$EVIDENCE_DIR" -type f | wc -l)
Directory Size: $(du -sh "$EVIDENCE_DIR" | awk '{print $1}')
EOF
}

collect_system_info
collect_user_process_info
collect_network_info
collect_logs
create_hashes
create_summary

echo "Evidence collection completed!"
echo "Evidence stored in: $EVIDENCE_DIR"
```

---

## 🔓 Step 3: Make Script Executable

```bash
chmod +x collect_evidence.sh
```

Verify:

```bash
ls -l collect_evidence.sh
```

---

## ▶️ Step 4: Run the Script

```bash
sudo ./collect_evidence.sh
```

Expected Output:

```bash
Evidence collection started...
Collecting system information...
Collecting user and process information...
Collecting network information...
Collecting system logs...
Creating hash values...
Creating summary...
Evidence collection completed!
```

---

# 🔐 Task 2 — Verify and Secure Evidence

---

## 📂 Step 1: Review Collected Evidence

```bash
ls -lh ~/evidence-collection/

cd ~/evidence-collection/evidence_*

ls -lR
```

---

## 🧾 Step 2: Create Verification Script

```bash
cd ~/forensic-tools

nano verify_evidence.sh
```

Paste:

```bash
#!/bin/bash

EVIDENCE_DIR=~/evidence-collection/evidence_*

echo "Starting evidence verification..."

md5sum -c $EVIDENCE_DIR/evidence_md5.txt

sha256sum -c $EVIDENCE_DIR/evidence_sha256.txt

echo "Verification completed!"
```

---

### 🔓 Make Executable

```bash
chmod +x verify_evidence.sh
```

---

### ▶️ Run Verification

```bash
./verify_evidence.sh
```

Expected:

```bash
hostname.txt: OK
uptime.txt: OK
os_info.txt: OK
...
Verification completed!
```

---

## 📦 Step 3: Create Secure Evidence Archive

```bash
cd ~/evidence-collection

tar -czf evidence_archive_$(date +%Y%m%d_%H%M%S).tar.gz evidence_*/
```

Verify:

```bash
ls -lh evidence_archive_*.tar.gz
```

Create Archive Hash:

```bash
sha256sum evidence_archive_*.tar.gz > evidence_archive.sha256
```

---

## 🔒 Step 4: Secure Evidence Permissions

```bash
chmod -R 444 ~/evidence-collection/evidence_*
```

Verify:

```bash
ls -la ~/evidence-collection/evidence_*
```

---

# ✅ Verification Checklist

## 🖥️ System Information

```bash
ls -1 hostname.txt uptime.txt os_info.txt kernel_info.txt collection_time.txt
```

---

## 👤 User Information

```bash
ls -1 logged_users.txt user_accounts.txt running_processes.txt
```

---

## 🌐 Network Information

```bash
ls -1 network_interfaces.txt network_connections.txt routing_table.txt
```

---

## 📜 Logs

```bash
ls -1 logs/
```

---

## 🔐 Hash Files

```bash
ls -1 evidence_md5.txt evidence_sha256.txt
```

---

## 📄 Case Information

```bash
cat case_info.txt
```

---

# 🔍 Integrity Validation

Count Files:

```bash
find ~/evidence-collection/evidence_*/ -type f | wc -l
```

Check Hash Files:

```bash
wc -l ~/evidence-collection/evidence_*/evidence_*.txt
```

Verify Archive Integrity:

```bash
sha256sum -c ~/evidence-collection/evidence_archive.sha256
```

Expected:

```bash
evidence_archive.tar.gz: OK
```

---

# 🎯 Expected Results

After successful completion:

✅ Timestamped evidence directory created

✅ System information collected

✅ User activity gathered

✅ Network information captured

✅ Logs preserved

✅ MD5 hashes generated

✅ SHA256 hashes generated

✅ Archive created

✅ Archive integrity verified

✅ Read-only permissions applied

---

# 🛠️ Troubleshooting

## ❌ Permission Denied

```bash
sudo ./collect_evidence.sh
```

Ensure sudo privileges are available.

---

## ❌ netstat Missing

Install:

```bash
sudo apt install net-tools
```

Or use:

```bash
ss -tuln
```

---

## ❌ Empty Log Files

Some systems use systemd journals.

Alternative:

```bash
sudo journalctl > logs/journal.log
```

---

## ❌ Hash Verification Failure

Possible causes:

* Files modified after collection
* Corrupted archive
* Incorrect evidence path

Regenerate hashes:

```bash
sha256sum *
md5sum *
```

---

# 🌍 Real-World Significance

Automated evidence collection is widely used in:

* 🚨 Incident Response
* 🔍 Digital Forensics
* 🛡️ Cybersecurity Investigations
* ⚖️ Legal Evidence Preservation
* 🏢 Enterprise Security Operations

Hash values provide cryptographic proof that evidence has not been altered, helping maintain the integrity and admissibility of evidence.

---

# 🚀 Next Steps

Enhance your forensic toolkit by collecting:

* 🌐 Browser History
* ⏰ Cron Jobs
* 💾 Memory Dumps
* 🔑 SSH Keys
* 📦 Installed Packages
* 📂 File Metadata
* 🔥 Firewall Rules
* 📊 Audit Logs

---

# 🏆 Lab Complete

You have successfully built an **Automated Evidence Collection and Verification Framework** capable of collecting, preserving, validating, and archiving forensic evidence using industry-standard techniques.

**Happy Investigating! 🔍🛡️**
