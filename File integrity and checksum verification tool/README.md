# 🛡️ File Integrity and Checksum Verification Tool

> *"Trust, but verify. File integrity is one of the foundations of cybersecurity."*

<p align="center">

![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge\&logo=ubuntu\&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-Scripting-121011?style=for-the-badge\&logo=gnu-bash\&logoColor=white)
![SHA256](https://img.shields.io/badge/SHA256-Integrity-blue?style=for-the-badge)
![MD5](https://img.shields.io/badge/MD5-Hashing-green?style=for-the-badge)
![Security](https://img.shields.io/badge/Cybersecurity-File_Integrity-red?style=for-the-badge)
![Level](https://img.shields.io/badge/Level-Beginner-success?style=for-the-badge)

</p>

---

# 📖 Overview

In this lab, you will learn how to verify file integrity using cryptographic checksums. You will generate and compare SHA256 and MD5 hashes, detect unauthorized modifications, and build an automated Bash-based integrity verification tool.

Checksums are widely used in:

* 🔐 Cybersecurity Monitoring
* 📦 Software Distribution Verification
* 💾 Backup Validation
* 🌐 Secure File Transfers
* 🛡️ Incident Response Investigations

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Understand what checksums are and why they matter

✅ Generate SHA256 and MD5 hashes for files

✅ Verify file integrity using saved hashes

✅ Detect modified or corrupted files

✅ Build an automated checksum verification script

✅ Apply integrity validation techniques used by cybersecurity professionals

---

# 🛠️ Prerequisites

Before starting, ensure you have:

* Basic Linux command-line knowledge
* Understanding of file systems and file operations
* Familiarity with nano or vi text editor
* Access to a Linux terminal

---

# ⚙️ Environment Setup

## 🔹 Step 1: Verify Required Tools

Check if hashing utilities are installed:

```bash
which sha256sum
which md5sum
```

Expected output:

```bash
/usr/bin/sha256sum
/usr/bin/md5sum
```

---

## 🔹 Step 2: Install Missing Tools (If Needed)

```bash
sudo apt-get update
sudo apt-get install coreutils -y
```

---

# 📂 Task 1: Understanding Checksums and Generating Hashes

---

## 📝 What is a Checksum?

A checksum is a unique fingerprint generated from file contents.

### Key Properties

🔹 Same file → Same checksum

🔹 Tiny file change → Completely different checksum

🔹 Useful for detecting tampering or corruption

Example:

```text
Original File  -> SHA256 Hash A
Modified File  -> SHA256 Hash B
```

Even changing one character produces a different hash.

---

## 🔹 Step 1: Create Test Files

Create a working directory:

```bash
mkdir ~/checksum-lab
cd ~/checksum-lab
```

Create sample files:

```bash
echo "This is my original file content." > original.txt

echo "Important data for verification." > document.txt
```

Verify:

```bash
ls -l
```

Expected:

```text
original.txt
document.txt
```

---

## 🔹 Step 2: Generate SHA256 Checksums

Generate SHA256 hash:

```bash
sha256sum original.txt
```

Save checksum:

```bash
sha256sum original.txt > original.sha256
```

View checksum:

```bash
cat original.sha256
```

Example:

```text
f6b2a9d7f9b0c8c6d0a8...
original.txt
```

---

## 🔹 Step 3: Generate MD5 Checksums

Generate MD5 hash:

```bash
md5sum original.txt
```

Save output:

```bash
md5sum original.txt > original.md5
```

View:

```bash
cat original.md5
```

Example:

```text
5eb63bbbe01eeed093cb22bb8f5acdc3
original.txt
```

---

## 🔹 Step 4: Generate Hashes for Multiple Files

Create checksums for all text files:

```bash
sha256sum *.txt > all-files.sha256
```

Display:

```bash
cat all-files.sha256
```

Expected:

```text
HASH1 original.txt
HASH2 document.txt
```

---

# 🔍 Task 2: Verify File Integrity and Detect Changes

---

## 🔹 Step 1: Verify Files Using Saved Checksums

Check file integrity:

```bash
sha256sum -c original.sha256
```

Verify all files:

```bash
sha256sum -c all-files.sha256
```

Expected:

```text
original.txt: OK
document.txt: OK
```

---

## 🔹 Step 2: Detect File Modifications

Modify file:

```bash
echo "This file has been tampered with!" >> original.txt
```

Verify again:

```bash
sha256sum -c original.sha256
```

Expected:

```text
original.txt: FAILED
sha256sum: WARNING: 1 computed checksum did NOT match
```

🚨 Integrity violation detected!

---

## 🔹 Step 3: Compare Hashes Manually

Generate new checksum:

```bash
sha256sum original.txt
```

Compare with:

```bash
cat original.sha256
```

Observe:

✅ Completely different hashes

---

## 🔹 Step 4: Restore and Verify

Restore file:

```bash
echo "This is my original file content." > original.txt
```

Verify:

```bash
sha256sum -c original.sha256
```

Expected:

```text
original.txt: OK
```

---

# 🤖 Task 3: Build a Simple Integrity Checker Script

---

## 🔹 Step 1: Create Script Template

Create script:

```bash
nano integrity-checker.sh
```

---

## 🔹 Step 2: Complete Script

Paste the following:

```bash
#!/bin/bash

# File Integrity Checker Script

generate_checksums() {
    local directory="${1:-.}"
    local output_file="checksums.sha256"

    echo "Generating checksums for files in $directory..."

    find "$directory" -type f -name "*.txt" \
        -exec sha256sum {} \; > "$output_file"

    echo "Checksums saved to $output_file"
}

verify_checksums() {
    local checksum_file="${1:-checksums.sha256}"

    if [ ! -f "$checksum_file" ]; then
        echo "Error: Checksum file not found!"
        exit 1
    fi

    echo "Verifying file integrity..."
    sha256sum -c "$checksum_file"
}

case "$1" in
    generate)
        generate_checksums "$2"
        ;;
    verify)
        verify_checksums "$2"
        ;;
    *)
        echo "Usage: $0 {generate|verify} [path]"
        exit 1
        ;;
esac
```

Save and exit.

---

## 🔹 Step 3: Make Script Executable

```bash
chmod +x integrity-checker.sh
```

Verify:

```bash
ls -l integrity-checker.sh
```

Expected:

```text
-rwxr-xr-x
```

---

## 🔹 Step 4: Generate Checksums

```bash
./integrity-checker.sh generate
```

Expected:

```text
Generating checksums...
Checksums saved to checksums.sha256
```

---

## 🔹 Step 5: Verify Integrity

```bash
./integrity-checker.sh verify
```

Expected:

```text
original.txt: OK
document.txt: OK
```

---

## 🔹 Step 6: Simulate Tampering

Modify file:

```bash
echo "Modified" >> document.txt
```

Run verification:

```bash
./integrity-checker.sh verify
```

Expected:

```text
document.txt: FAILED
```

🚨 Modification successfully detected.

---

# ✅ Verification

---

## 🔎 Check 1: Verify Checksum Generation

```bash
sha256sum original.txt
md5sum original.txt
```

Expected:

```text
<Hash Value> original.txt
```

---

## 🔎 Check 2: Verify Modification Detection

Create test file:

```bash
echo "test" > test.txt
```

Generate checksum:

```bash
sha256sum test.txt > test.sha256
```

Modify file:

```bash
echo "changed" >> test.txt
```

Verify:

```bash
sha256sum -c test.sha256
```

Expected:

```text
FAILED
```

---

## 🔎 Check 3: Verify Script Functionality

Generate:

```bash
./integrity-checker.sh generate
```

Verify:

```bash
./integrity-checker.sh verify
```

Expected:

```text
Checksums generated successfully
Files verified successfully
```

---

# 🛠️ Troubleshooting

---

## ❌ Command Not Found

Install required utilities:

```bash
sudo apt-get install coreutils -y
```

---

## ❌ Permission Denied

Make executable:

```bash
chmod +x integrity-checker.sh
```

---

## ❌ Checksum File Missing

Check current directory:

```bash
pwd
ls -la
```

---

## ❌ All Files Show FAILED

Possible causes:

* Files were modified
* Paths changed
* Checksum file generated from a different location

Regenerate:

```bash
./integrity-checker.sh generate
```

---

# 🏆 Lab Completion Checklist

* [x] Created checksum-lab directory
* [x] Generated SHA256 hashes
* [x] Generated MD5 hashes
* [x] Verified file integrity
* [x] Detected modified files
* [x] Built integrity-checker.sh
* [x] Automated checksum verification
* [x] Successfully completed verification tests

---

# 🔐 Real-World Applications

### 📦 Software Distribution

Verify downloaded software hasn't been altered.

### 💾 Backup Validation

Ensure backups exactly match originals.

### 🛡️ Security Monitoring

Detect unauthorized modifications.

### 🌐 Secure Data Transfers

Validate transferred files remain intact.

### 🚨 Incident Response

Identify tampered files during investigations.

---

# 🎓 Key Takeaways

✅ Checksums provide reliable integrity validation

✅ SHA256 is stronger and more secure than MD5

✅ Even one character change produces a different hash

✅ Automated integrity checking improves security operations

✅ File integrity verification is a core cybersecurity skill

---

# 🚀 Next Steps

Enhance your tool by adding:

* 📧 Email alerts for failed checks
* 📊 HTML or JSON reporting
* ⏰ Scheduled cron-based monitoring
* 📁 Recursive directory integrity tracking
* 🔒 Support for SHA512 verification
* ☁️ Cloud storage integrity validation

---

# 🎉 Conclusion

Congratulations!

You successfully built a **File Integrity and Checksum Verification Tool** capable of generating, storing, and validating cryptographic hashes.

You learned how cybersecurity teams use integrity monitoring to:

🔹 Detect tampering

🔹 Validate backups

🔹 Verify software downloads

🔹 Protect critical systems

🔹 Maintain trust in digital assets

This foundational skill is widely used in **Security Operations (SOC)**, **Incident Response**, **Digital Forensics**, and **Compliance Monitoring** environments.
