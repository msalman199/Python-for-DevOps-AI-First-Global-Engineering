# 🔐 Encrypted Evidence Vault

> *"Protecting digital evidence requires confidentiality, integrity, accountability, and secure access control."*

---

## 📖 Overview

The **Encrypted Evidence Vault** project demonstrates how cybersecurity professionals securely store, manage, and verify sensitive forensic evidence using industry-standard encryption technologies.

This lab walks through the creation of a secure evidence storage solution using:

- 🔒 LUKS (Linux Unified Key Setup) encryption
- 🔑 Multi-key authentication
- 📂 Encrypted storage containers
- 🛡️ SHA-256 integrity verification
- 📜 Audit logging
- 🔐 GPG encrypted key backups

---

## 🎯 Learning Objectives

By completing this lab, you will:

- Understand encryption fundamentals for forensic evidence protection
- Create encrypted evidence storage containers
- Implement secure key management practices
- Control access to protected evidence repositories
- Verify evidence integrity using cryptographic hashes
- Maintain audit trails for chain-of-custody compliance

---

## 🛠️ Technology Stack

![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=linux)
![LUKS](https://img.shields.io/badge/LUKS-Disk%20Encryption-blue?style=for-the-badge)
![Cryptsetup](https://img.shields.io/badge/Cryptsetup-Security-red?style=for-the-badge)
![GPG](https://img.shields.io/badge/GPG-Encryption-green?style=for-the-badge)
![Bash](https://img.shields.io/badge/Bash-Scripting-black?style=for-the-badge&logo=gnu-bash)
![SHA256](https://img.shields.io/badge/SHA256-Integrity-purple?style=for-the-badge)

---

# 📋 Prerequisites

Before starting this lab, ensure you have:

- Basic Linux command-line knowledge
- Understanding of file permissions
- Familiarity with Nano or Vim editors
- Root or sudo access
- Ubuntu/Linux machine

---

# ⚙️ Environment Setup

## Step 1: Update Package Lists

```bash
sudo apt update
```

## Step 2: Install Required Tools

### Install LUKS Encryption Utility

```bash
sudo apt install -y cryptsetup
```

### Install Additional Utilities

```bash
sudo apt install -y tree gnupg2
```

---

## Step 3: Verify Installation

```bash
cryptsetup --version
gpg --version
```

Expected Output:

```text
cryptsetup 2.x.x
gpg (GnuPG) 2.x.x
```

---

# 🏗️ Task 1: Create an Encrypted Evidence Vault

---

## 📁 Step 1: Create Container File

Create a dedicated workspace:

```bash
mkdir -p ~/evidence-lab
cd ~/evidence-lab
```

Create a 100MB encrypted container:

```bash
dd if=/dev/zero of=evidence_vault.img bs=1M count=100
```

Verify creation:

```bash
ls -lh evidence_vault.img
```

---

## 🔒 Step 2: Initialize LUKS Encryption

Encrypt the container:

```bash
sudo cryptsetup luksFormat evidence_vault.img
```

When prompted:

```text
Type YES
Enter passphrase
Confirm passphrase
```

Example passphrase:

```text
ForensicEvidence2024!
```

---

## 🔓 Step 3: Open the Encrypted Vault

```bash
sudo cryptsetup luksOpen evidence_vault.img evidence_vault
```

Verify mapping:

```bash
ls -l /dev/mapper/evidence_vault
```

---

## 💾 Step 4: Create Filesystem

Create an EXT4 filesystem:

```bash
sudo mkfs.ext4 /dev/mapper/evidence_vault
```

Create mount point:

```bash
sudo mkdir -p /mnt/evidence_vault
```

Mount vault:

```bash
sudo mount /dev/mapper/evidence_vault /mnt/evidence_vault
```

Verify mount:

```bash
df -h | grep evidence_vault
```

---

## 📑 Step 5: Store Sample Evidence

Create Case File #001

```bash
sudo bash -c 'cat > /mnt/evidence_vault/case_001.txt << EOF
CASE ID: 001
DATE: 2024-01-15
INVESTIGATOR: J. Smith
DESCRIPTION: Network intrusion evidence
HASH: a1b2c3d4e5f6
EOF'
```

Create Case File #002

```bash
sudo bash -c 'cat > /mnt/evidence_vault/case_002.txt << EOF
CASE ID: 002
DATE: 2024-01-16
INVESTIGATOR: M. Johnson
DESCRIPTION: Malware sample analysis
HASH: f6e5d4c3b2a1
EOF'
```

Create Chain of Custody Log:

```bash
sudo bash -c 'cat > /mnt/evidence_vault/chain_of_custody.log << EOF
[2024-01-15 10:30] Evidence collected by J. Smith
[2024-01-15 11:00] Evidence stored in encrypted vault
[2024-01-16 09:15] Evidence collected by M. Johnson
[2024-01-16 09:45] Evidence stored in encrypted vault
EOF'
```

Verify files:

```bash
sudo ls -la /mnt/evidence_vault/
```

---

## 🔐 Step 6: Close Vault Securely

Unmount:

```bash
sudo umount /mnt/evidence_vault
```

Close vault:

```bash
sudo cryptsetup luksClose evidence_vault
```

Verify closure:

```bash
ls /dev/mapper/ | grep evidence_vault
```

---

# 🔑 Task 2: Key Management & Access Control

---

## 🗝️ Step 1: Add Additional Key Slot

Reopen vault:

```bash
sudo cryptsetup luksOpen evidence_vault.img evidence_vault
```

Add backup passphrase:

```bash
sudo cryptsetup luksAddKey evidence_vault.img
```

Example backup key:

```text
BackupKey2024!
```

---

## 📋 Step 2: View Key Slots

```bash
sudo cryptsetup luksDump evidence_vault.img | grep "Key Slot"
```

---

## 🔑 Step 3: Create Key File

Generate secure random key:

```bash
sudo dd if=/dev/urandom of=~/evidence-lab/vault.key bs=512 count=1
```

Secure permissions:

```bash
sudo chmod 400 ~/evidence-lab/vault.key
```

Add key file to LUKS:

```bash
sudo cryptsetup luksAddKey evidence_vault.img ~/evidence-lab/vault.key
```

---

## ⚡ Step 4: Test Key File Access

Close vault:

```bash
sudo cryptsetup luksClose evidence_vault
```

Open using key file:

```bash
sudo cryptsetup luksOpen evidence_vault.img evidence_vault \
--key-file ~/evidence-lab/vault.key
```

Mount:

```bash
sudo mount /dev/mapper/evidence_vault /mnt/evidence_vault
```

Verify:

```bash
sudo ls /mnt/evidence_vault/
```

---

# 🤖 Vault Management Script

Create:

```bash
nano ~/evidence-lab/vault_manager.sh
```

Features:

- Open vault
- Close vault
- Check status

Make executable:

```bash
chmod +x ~/evidence-lab/vault_manager.sh
```

---

## Usage

Check status:

```bash
~/evidence-lab/vault_manager.sh status
```

Open vault:

```bash
~/evidence-lab/vault_manager.sh open
```

Close vault:

```bash
~/evidence-lab/vault_manager.sh close
```

---

# 🛡️ Evidence Integrity Verification

Generate SHA-256 hashes:

```bash
sudo bash -c 'cd /mnt/evidence_vault && sha256sum *.txt > evidence_checksums.sha256'
```

View checksums:

```bash
sudo cat /mnt/evidence_vault/evidence_checksums.sha256
```

---

## Verification Script

Create:

```bash
nano ~/evidence-lab/verify_evidence.sh
```

Make executable:

```bash
chmod +x ~/evidence-lab/verify_evidence.sh
```

Run verification:

```bash
~/evidence-lab/verify_evidence.sh
```

Expected:

```text
All evidence files verified successfully
```

---

# 🧪 Integrity Tampering Test

Modify evidence:

```bash
sudo bash -c 'echo "tampered" >> /mnt/evidence_vault/case_001.txt'
```

Run verification:

```bash
~/evidence-lab/verify_evidence.sh
```

Expected:

```text
WARNING: Evidence integrity check FAILED
```

---

# 📜 Audit Logging System

Create:

```bash
nano ~/evidence-lab/audit_log.sh
```

Make executable:

```bash
chmod +x ~/evidence-lab/audit_log.sh
```

Example logs:

```bash
~/evidence-lab/audit_log.sh "VAULT_OPENED" "Evidence vault accessed"
~/evidence-lab/audit_log.sh "EVIDENCE_VERIFIED" "Integrity check passed"
~/evidence-lab/audit_log.sh "EVIDENCE_ADDED" "New case file added"
```

View audit trail:

```bash
cat ~/evidence-lab/vault_audit.log
```

---

# 🔐 Secure Key Backup with GPG

Encrypt key file:

```bash
gpg --symmetric --cipher-algo AES256 ~/evidence-lab/vault.key
```

Verify encrypted backup:

```bash
ls -l ~/evidence-lab/vault.key.gpg
```

Restore key:

```bash
gpg --decrypt ~/evidence-lab/vault.key.gpg > ~/evidence-lab/vault.key
```

---

# ✅ Verification Checklist

## Verify Vault Creation

```bash
ls -lh ~/evidence-lab/evidence_vault.img
```

```bash
sudo cryptsetup luksDump ~/evidence-lab/evidence_vault.img | head
```

---

## Verify Key Slots

```bash
sudo cryptsetup luksDump ~/evidence-lab/evidence_vault.img | grep "ENABLED"
```

Expected:

```text
3 or more active key slots
```

---

## Verify Integrity Checking

```bash
~/evidence-lab/verify_evidence.sh
```

Expected:

```text
All evidence files verified successfully
```

---

## Verify Audit Logs

```bash
cat ~/evidence-lab/vault_audit.log
```

Expected:

```text
Multiple audit entries recorded
```

---

# 🔬 Complete Security Test

Close vault:

```bash
~/evidence-lab/vault_manager.sh close
```

View raw encrypted data:

```bash
sudo head -c 100 ~/evidence-lab/evidence_vault.img | xxd | head
```

Reopen vault:

```bash
~/evidence-lab/vault_manager.sh open
```

Verify evidence:

```bash
sudo cat /mnt/evidence_vault/case_001.txt
```

---

# 📂 Project Structure

```text
evidence-lab/
│
├── evidence_vault.img
├── vault.key
├── vault.key.gpg
├── vault_manager.sh
├── verify_evidence.sh
├── audit_log.sh
├── vault_audit.log
│
└── /mnt/evidence_vault
    ├── case_001.txt
    ├── case_002.txt
    ├── chain_of_custody.log
    └── evidence_checksums.sha256
```

---

# 🎓 Key Skills Demonstrated

✅ LUKS Disk Encryption

✅ Evidence Protection

✅ Secure Key Management

✅ Chain of Custody Preservation

✅ SHA-256 Integrity Validation

✅ Audit Logging

✅ Access Control Automation

✅ GPG Key Backup

---

# 🚀 Real-World Applications

- Digital Forensics
- Incident Response
- Law Enforcement Investigations
- Malware Analysis Labs
- Compliance & Audit Programs
- Evidence Preservation Systems
- Secure Research Data Storage

---

# 🏁 Conclusion

In this lab, you built a professional-grade **Encrypted Evidence Vault** that provides:

- 🔒 Confidentiality through LUKS encryption
- 🔑 Secure multi-factor key management
- 🛡️ Integrity verification using SHA-256
- 📜 Comprehensive audit logging
- ⚡ Automated vault management
- 🔐 Secure GPG key backups

These techniques mirror real-world forensic evidence handling procedures used by cybersecurity teams, incident responders, digital forensics investigators, and law enforcement agencies to ensure evidence remains confidential, verifiable, and legally admissible.

---

⭐ **Security Principle:** Confidentiality + Integrity + Accountability = Trusted Digital Evidence
