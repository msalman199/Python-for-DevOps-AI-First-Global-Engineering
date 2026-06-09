# 🔍 Secure Evidence Collection and Reporting System

![Digital Forensics](https://img.shields.io/badge/Digital-Forensics-blue)
![Incident Response](https://img.shields.io/badge/Incident%20Response-Security-red)
![Python](https://img.shields.io/badge/Python-3.x-green)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)
![Evidence Integrity](https://img.shields.io/badge/Evidence-Integrity-purple)
![Hashing](https://img.shields.io/badge/Hashing-SHA256%20%7C%20MD5-yellow)

---

# 📌 Overview

The **Secure Evidence Collection and Reporting System** demonstrates the core principles of digital forensics and incident response by implementing a structured evidence collection workflow.

This lab focuses on:

* Secure evidence acquisition
* Evidence preservation
* Cryptographic integrity verification
* Chain of custody documentation
* Automated forensic reporting
* Integrity validation procedures

The workflow mirrors real-world forensic investigation practices used by:

* Incident Responders
* Digital Forensics Analysts
* SOC Analysts
* Cybercrime Investigators
* Law Enforcement Agencies

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

✅ Build a forensic evidence collection framework

✅ Preserve evidence integrity using cryptographic hashes

✅ Create forensic working copies

✅ Generate MD5 and SHA256 hash manifests

✅ Implement chain of custody documentation

✅ Generate automated forensic reports

✅ Verify evidence integrity throughout investigations

---

# 🛠 Technologies Used

| Technology | Purpose                 |
| ---------- | ----------------------- |
| Linux      | Investigation Platform  |
| Python 3   | Report Automation       |
| dcfldd     | Forensic Copying        |
| md5deep    | Hash Verification       |
| SHA256     | Evidence Integrity      |
| Tree       | Directory Visualization |
| Bash       | Automation Scripts      |

---

# 📂 Project Structure

```text
forensics_lab/
│
├── evidence/
│   ├── original/
│   ├── working/
│   ├── reports/
│   ├── logs/
│   └── hashes/
│
├── suspicious_doc.txt
├── system.log
├── app.conf
│
├── generate_report.py
├── verify_integrity.sh
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

## Step 2: Install Required Tools

```bash
sudo apt install -y dcfldd md5deep python3 python3-pip tree
```

---

## Step 3: Verify Installation

```bash
dcfldd --version

md5deep -v

python3 --version
```

---

# 🗂 Task 1 — Create Evidence Collection Framework

---

## Create Lab Directory

```bash
mkdir -p ~/forensics_lab

cd ~/forensics_lab
```

---

## Create Evidence Structure

```bash
mkdir -p evidence/{original,working,reports}

mkdir -p evidence/logs

mkdir -p evidence/hashes
```

---

## Set Secure Permissions

```bash
chmod 755 evidence

chmod 700 evidence/original

chmod 755 evidence/working

chmod 755 evidence/reports
```

---

# 🧪 Task 2 — Create Sample Evidence

---

## Suspicious Document

```bash
echo "Confidential Project Data - Access Log" > suspicious_doc.txt

echo "User: jdoe - Access Time: 2024-01-15 14:23:45" >> suspicious_doc.txt

echo "Action: Downloaded sensitive files" >> suspicious_doc.txt
```

---

## System Log

### File: `system.log`

```text
2024-01-15 14:20:12 LOGIN jdoe from 192.168.1.105
2024-01-15 14:23:45 FILE_ACCESS jdoe accessed /secure/data.db
2024-01-15 14:24:01 FILE_DOWNLOAD jdoe downloaded data.db
2024-01-15 14:25:33 LOGOUT jdoe
```

---

## Application Configuration

### File: `app.conf`

```ini
[database]
host=192.168.1.50
user=admin
last_modified=2024-01-15
```

---

# 🔐 Task 3 — Collect Evidence Securely

---

## Forensic Copy Using dcfldd

```bash
dcfldd if=suspicious_doc.txt \
of=evidence/original/suspicious_doc.txt \
hash=md5,sha256 \
hashlog=evidence/hashes/suspicious_doc.hash
```

```bash
dcfldd if=system.log \
of=evidence/original/system.log \
hash=md5,sha256 \
hashlog=evidence/hashes/system.log.hash
```

```bash
dcfldd if=app.conf \
of=evidence/original/app.conf \
hash=md5,sha256 \
hashlog=evidence/hashes/app.conf.hash
```

---

## Protect Original Evidence

```bash
chmod 444 evidence/original/*
```

---

## Create Working Copies

```bash
cp -p evidence/original/* evidence/working/
```

---

# 🔑 Task 4 — Generate Hash Manifest

---

## Generate MD5 Manifest

```bash
cd evidence/original

md5deep -r . > ../hashes/md5_manifest.txt
```

---

## Generate SHA256 Manifest

```bash
sha256sum * > ../hashes/sha256_manifest.txt
```

---

## View Hashes

```bash
cat ../hashes/sha256_manifest.txt
```

---

# 📋 Task 5 — Chain of Custody Documentation

---

## Create Chain of Custody Log

```bash
cat > evidence/logs/chain_of_custody.log << 'EOF'
CHAIN OF CUSTODY LOG
====================
Case ID: CASE-2024-001
Collected By: Lab Student
EOF
```

---

## Add Evidence Metadata

```bash
for file in *; do
echo "Item: $file" >> ../logs/chain_of_custody.log

echo "Collected: $(date)" >> ../logs/chain_of_custody.log

echo "SHA256: $(sha256sum "$file" | awk '{print $1}')" >> ../logs/chain_of_custody.log

echo "" >> ../logs/chain_of_custody.log
done
```

---

## View Chain of Custody

```bash
cat ../logs/chain_of_custody.log
```

---

# 🐍 Task 6 — Automated Forensic Report Generator

## Create Python Script

### File: `generate_report.py`

```python
#!/usr/bin/env python3

import hashlib
import datetime
from pathlib import Path

class ForensicReporter:

    def __init__(self, evidence_dir):
        self.evidence_dir = Path(evidence_dir)
        self.report_data = []

    def calculate_hash(self, filepath, algorithm='sha256'):

        hash_obj = hashlib.new(algorithm)

        with open(filepath, 'rb') as f:
            hash_obj.update(f.read())

        return hash_obj.hexdigest()

    def analyze_evidence(self):

        original_dir = self.evidence_dir / "original"

        for filepath in original_dir.iterdir():

            if filepath.is_file():

                file_info = {
                    "filename": filepath.name,
                    "size": filepath.stat().st_size,
                    "md5": self.calculate_hash(filepath, "md5"),
                    "sha256": self.calculate_hash(filepath, "sha256")
                }

                self.report_data.append(file_info)

    def generate_report(self, output_file):

        with open(output_file, "w") as f:

            f.write("FORENSIC EVIDENCE REPORT\n")
            f.write("=" * 60 + "\n\n")

            for item in self.report_data:

                f.write(f"File: {item['filename']}\n")
                f.write(f"Size: {item['size']} bytes\n")
                f.write(f"MD5: {item['md5']}\n")
                f.write(f"SHA256: {item['sha256']}\n\n")

def main():

    evidence_path = Path.home() / "forensics_lab" / "evidence"

    report_path = evidence_path / "reports" / "forensic_report.txt"

    reporter = ForensicReporter(evidence_path)

    reporter.analyze_evidence()

    reporter.generate_report(report_path)

if __name__ == "__main__":
    main()
```

---

## Execute Report Generator

```bash
chmod +x generate_report.py

python3 generate_report.py
```

---

## View Report

```bash
cat evidence/reports/forensic_report.txt
```

---

# 📄 Executive Summary

### File: `executive_summary.txt`

```text
EXECUTIVE SUMMARY

Case ID: CASE-2024-001

Evidence Items Collected:
1. suspicious_doc.txt
2. system.log
3. app.conf

Integrity Status:
- MD5 Verified
- SHA256 Verified
- Chain of Custody Recorded
- Read-only Evidence Protected

Next Steps:
- Timeline Reconstruction
- Log Correlation
- User Activity Analysis
```

---

# 🛡 Integrity Verification Script

### File: `verify_integrity.sh`

```bash
#!/bin/bash

echo "=== Evidence Integrity Verification ==="

cd ~/forensics_lab/evidence/original

sha256sum -c ../hashes/sha256_manifest.txt

echo ""

echo "Verification Complete"
```

---

## Run Verification

```bash
chmod +x verify_integrity.sh

./verify_integrity.sh
```

---

# ✅ Verification Checklist

## Directory Structure

```bash
tree ~/forensics_lab -L 2
```

---

## Evidence Files

```bash
ls -lh evidence/original/
```

---

## Hash Files

```bash
ls -lh evidence/hashes/
```

---

## Reports

```bash
ls -lh evidence/reports/
```

---

## Verify Read-Only Protection

```bash
stat -c "%A %n" evidence/original/*
```

Expected:

```text
-r--r--r-- suspicious_doc.txt
-r--r--r-- system.log
-r--r--r-- app.conf
```

---

# 🔍 Evidence Integrity Validation

```bash
cd evidence/original

sha256sum -c ../hashes/sha256_manifest.txt
```

Expected:

```text
suspicious_doc.txt: OK
system.log: OK
app.conf: OK
```

---

# 🚨 Troubleshooting

## dcfldd Missing

```bash
sudo apt install -y dcfldd
```

---

## Permission Errors

```bash
chmod +x *.sh

chmod +x *.py
```

---

## Python Issues

```bash
python3 --version
```

---

## Hash Verification Failure

Verify original evidence was not modified:

```bash
ls -l evidence/original/
```

---

# 🎓 Key Digital Forensics Concepts

### Evidence Preservation

Original evidence must never be altered.

### Hash Verification

Cryptographic hashes prove integrity.

### Chain of Custody

Every action must be documented.

### Working Copies

Analysis should occur only on copies.

### Automated Reporting

Reduces human error and improves consistency.

---

# 🌎 Real-World Applications

This workflow is used in:

* Digital Forensics Investigations
* Incident Response
* Malware Analysis
* Insider Threat Investigations
* Security Operations Centers (SOC)
* Law Enforcement Cybercrime Units
* Regulatory Compliance Audits

---

# 🏆 Lab Completion Checklist

* [x] Installed forensic tools
* [x] Created evidence framework
* [x] Collected evidence securely
* [x] Generated MD5 hashes
* [x] Generated SHA256 hashes
* [x] Preserved original evidence
* [x] Created chain of custody
* [x] Automated report generation
* [x] Verified evidence integrity

---

# 🎯 Conclusion

In this lab, you built a complete **Secure Evidence Collection and Reporting System** that follows core digital forensics principles.

You successfully:

* Collected evidence using forensically sound methods
* Preserved evidence integrity using MD5 and SHA256
* Implemented chain of custody procedures
* Protected original evidence from modification
* Generated automated forensic reports
* Verified integrity throughout the investigation lifecycle

These are foundational skills required for careers in **Digital Forensics, Incident Response, Cybersecurity Operations, and Threat Investigations**.

**Key Takeaway:** Evidence is only valuable if its integrity can be proven. Proper collection, hashing, documentation, and preservation ensure forensic findings remain trustworthy and admissible.
