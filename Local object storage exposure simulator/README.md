# 🔓 Local Object Storage Exposure Simulator

> *"One of the most common cloud security incidents isn't a sophisticated attack—it's accidentally making sensitive data public."*

<p align="center">
  <img src="https://img.shields.io/badge/Cybersecurity-Storage%20Security-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Cloud-Security-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/MinIO-S3%20Compatible-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Linux-Ubuntu-black?style=for-the-badge">
  <img src="https://img.shields.io/badge/Bash-Scripting-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/SOC-Exposure%20Detection-purple?style=for-the-badge">
</p>

---

# 📖 Overview

This lab demonstrates how **misconfigured object storage services** can unintentionally expose sensitive information to the public.

Using **MinIO**, an S3-compatible object storage platform, you'll simulate:

- Publicly exposed storage buckets
- Sensitive data leakage
- Bucket policy misconfigurations
- Exposure verification techniques
- Automated storage scanning
- Security reporting

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

✅ Understand object storage exposure risks

✅ Deploy a local S3-compatible storage service

✅ Configure secure and insecure bucket permissions

✅ Identify publicly accessible data

✅ Verify storage exposure using HTTP requests

✅ Create an automated exposure detection scanner

✅ Generate exposure assessment reports

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| MinIO | Object Storage Platform |
| MinIO Client (mc) | Storage Administration |
| Bash | Automation Scripts |
| curl | Exposure Verification |
| Linux | Lab Environment |

---

# 🏗️ Lab Architecture

```text
                ┌──────────────────┐
                │  Sensitive Files │
                └─────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │      MinIO       │
                │ Object Storage   │
                └─────────┬────────┘
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼

 Private Bucket      Public Bucket      Exposed Bucket
   (Secure)          (Misconfigured)   (Misconfigured)

       ▼                  ▼                  ▼

     403               HTTP 200          HTTP 200
   Forbidden          Accessible       Accessible
```

---

# ⚙️ Environment Setup

---

## 🔹 Step 1: Install MinIO Server

```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio

chmod +x minio

sudo mv minio /usr/local/bin/

minio --version
```

---

## 🔹 Step 2: Create Storage Directories

```bash
mkdir -p ~/minio-storage/data

mkdir -p ~/sensitive-data
```

---

# 📁 Creating Sensitive Data

---

## 🔐 Customer Database

```bash
cat > ~/sensitive-data/customer-data.txt << 'EOF'
Customer Database - CONFIDENTIAL
================================
ID: 1001, Name: John Doe, SSN: 123-45-6789, Email: john@example.com
ID: 1002, Name: Jane Smith, SSN: 987-65-4321, Email: jane@example.com
ID: 1003, Name: Bob Johnson, SSN: 555-12-3456, Email: bob@example.com
EOF
```

---

## 🔑 API Keys File

```bash
cat > ~/sensitive-data/api-keys.txt << 'EOF'
API Keys - DO NOT SHARE
=======================
AWS_ACCESS_KEY: AKIAIOSFODNN7EXAMPLE
AWS_SECRET_KEY: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
DATABASE_PASSWORD: SuperSecret123!
EOF
```

---

## 💰 Financial Report

```bash
cat > ~/sensitive-data/financial-report.txt << 'EOF'
Q4 Financial Report - INTERNAL ONLY
====================================
Revenue: $5,234,567
Expenses: $3,456,789
Net Profit: $1,777,778
Projected Growth: 23%
EOF
```

---

# 🚀 Start MinIO Server

```bash
MINIO_ROOT_USER=minioadmin \
MINIO_ROOT_PASSWORD=minioadmin \
minio server ~/minio-storage/data \
--console-address ":9001" &
```

Wait for startup:

```bash
sleep 5
```

Verify:

```bash
ps aux | grep minio
```

---

# 🌐 Access MinIO

```bash
echo "MinIO Console: http://localhost:9001"
echo "MinIO API: http://localhost:9000"
```

### Default Credentials

```text
Username: minioadmin
Password: minioadmin
```

---

# 🧰 Install MinIO Client

```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mc

chmod +x mc

sudo mv mc /usr/local/bin/

mc --version
```

---

# 🔗 Configure Connection

```bash
mc alias set localminio \
http://localhost:9000 \
minioadmin \
minioadmin
```

Verify:

```bash
mc admin info localminio
```

---

# 🪣 Create Buckets

---

## 🔒 Private Bucket

```bash
mc mb localminio/private-bucket
```

---

## ⚠️ Public Bucket

```bash
mc mb localminio/public-bucket
```

---

## 🚨 Exposed Data Bucket

```bash
mc mb localminio/exposed-data
```

---

# 📤 Upload Sensitive Files

## Secure Upload

```bash
mc cp ~/sensitive-data/customer-data.txt \
localminio/private-bucket/
```

---

## Misconfigured Uploads

```bash
mc cp ~/sensitive-data/api-keys.txt \
localminio/public-bucket/

mc cp ~/sensitive-data/financial-report.txt \
localminio/exposed-data/
```

---

# 🚨 Configure Dangerous Public Access

```bash
mc anonymous set download \
localminio/public-bucket
```

```bash
mc anonymous set download \
localminio/exposed-data
```

Verify:

```bash
mc anonymous list localminio/public-bucket

mc anonymous list localminio/exposed-data

mc anonymous list localminio/private-bucket
```

---

# 🔍 Exposure Verification

---

## List Buckets

```bash
mc ls localminio/
```

---

## Review Policies

```bash
for bucket in private-bucket public-bucket exposed-data
do
    echo "Bucket: $bucket"
    mc anonymous list localminio/$bucket
    echo "---"
done
```

---

# 🌍 Test Anonymous Access

---

## Public Bucket

```bash
curl -I \
http://localhost:9000/public-bucket/api-keys.txt
```

```bash
curl \
http://localhost:9000/public-bucket/api-keys.txt
```

---

## Exposed Bucket

```bash
curl \
http://localhost:9000/exposed-data/financial-report.txt
```

Expected:

```text
HTTP/1.1 200 OK
```

---

# 🔒 Verify Private Bucket

```bash
curl -I \
http://localhost:9000/private-bucket/customer-data.txt
```

Expected:

```text
HTTP/1.1 403 Forbidden
```

---

# 🛡️ Storage Exposure Scanner

Create:

```bash
nano ~/storage-scanner.sh
```

---

## Scanner Script

```bash
#!/bin/bash

echo "==================================="
echo "Storage Exposure Detection Scanner"
echo "==================================="

MINIO_HOST="http://localhost:9000"

BUCKETS=(
private-bucket
public-bucket
exposed-data
)

for bucket in "${BUCKETS[@]}"
do
    echo "Scanning bucket: $bucket"

    mc ls localminio/$bucket/ 2>/dev/null | while read -r line
    do
        filename=$(echo $line | awk '{print $NF}')

        file_response=$(curl -s \
        -o /dev/null \
        -w "%{http_code}" \
        "$MINIO_HOST/$bucket/$filename")

        if [ "$file_response" == "200" ]
        then
            echo "  [EXPOSED] $filename is publicly accessible!"
        else
            echo "  [SECURE] $filename is protected"
        fi
    done

    echo ""
done

echo "==================================="
echo "Scan Complete"
echo "==================================="
```

---

## Make Executable

```bash
chmod +x ~/storage-scanner.sh
```

---

## Execute

```bash
~/storage-scanner.sh
```

---

# 📊 Exposure Report Generator

Create:

```bash
nano ~/generate-report.sh
```

---

## Report Script

```bash
#!/bin/bash

REPORT_FILE=~/exposure-report.txt

echo "Object Storage Exposure Report" > $REPORT_FILE
echo "Generated: $(date)" >> $REPORT_FILE
echo "================================" >> $REPORT_FILE

for bucket in private-bucket public-bucket exposed-data
do
    echo "Bucket: $bucket" >> $REPORT_FILE

    policy=$(mc anonymous list localminio/$bucket)

    if echo "$policy" | grep -q "download"
    then
        echo "  Status: EXPOSED" >> $REPORT_FILE
        echo "  Risk Level: HIGH" >> $REPORT_FILE
    else
        echo "  Status: SECURE" >> $REPORT_FILE
        echo "  Risk Level: LOW" >> $REPORT_FILE
    fi

    echo "" >> $REPORT_FILE
done

cat $REPORT_FILE
```

---

## Run Report

```bash
chmod +x ~/generate-report.sh

~/generate-report.sh
```

---

# ✅ Verification

---

## Check MinIO Health

```bash
curl -I \
http://localhost:9000/minio/health/live
```

Expected:

```text
HTTP/1.1 200 OK
```

---

## Verify Buckets

```bash
mc ls localminio/
```

Expected:

```text
private-bucket
public-bucket
exposed-data
```

---

## Verify Exposure

```bash
curl -s \
http://localhost:9000/public-bucket/api-keys.txt \
| head -n 3
```

Expected:

```text
API Keys - DO NOT SHARE
```

---

## Verify Protection

```bash
curl -I \
http://localhost:9000/private-bucket/customer-data.txt
```

Expected:

```text
HTTP/1.1 403 Forbidden
```

---

# 🧹 Cleanup

Stop MinIO:

```bash
pkill minio
```

Remove data:

```bash
rm -rf ~/minio-storage

rm -rf ~/sensitive-data
```

---

# 🛠️ Troubleshooting

## MinIO Won't Start

```bash
netstat -tuln | grep 900
```

```bash
pkill minio
```

---

## mc Cannot Connect

```bash
mc alias list
```

```bash
ps aux | grep minio
```

---

## Upload Failures

```bash
ls ~/sensitive-data/
```

```bash
mc ls localminio/
```

---

## Connection Refused

```bash
curl http://localhost:9000
```

Verify MinIO is running and listening.

---

# 📈 Security Findings

| Bucket | Access Level | Risk |
|----------|-------------|-------|
| private-bucket | Private | 🟢 Low |
| public-bucket | Public Download | 🔴 High |
| exposed-data | Public Download | 🔴 High |

---

# 🎓 Skills Gained

✅ Object Storage Security

✅ MinIO Administration

✅ S3-Compatible Storage Management

✅ Exposure Detection

✅ Security Assessment

✅ Cloud Misconfiguration Analysis

✅ Data Exposure Verification

✅ Bash Security Automation

---

# 🌎 Real-World Relevance

Object storage misconfigurations are among the most common causes of cloud data breaches.

Examples include:

- Public S3 Buckets
- Exposed Backup Archives
- Leaked API Keys
- Public Financial Reports
- Open Customer Databases

Understanding how to identify and remediate these issues is a critical skill for:

- Cloud Security Engineers
- SOC Analysts
- DevSecOps Engineers
- Security Auditors
- Incident Responders

---

# 🏆 Lab Completed

You successfully:

✔ Installed MinIO Object Storage

✔ Created secure and insecure buckets

✔ Simulated real-world storage exposure

✔ Verified public accessibility

✔ Built an exposure scanner

✔ Generated a security assessment report

✔ Practiced cloud storage security fundamentals

---

### ⭐ If this lab helped you learn cloud security concepts, consider starring the repository and sharing it with other cybersecurity learners.
