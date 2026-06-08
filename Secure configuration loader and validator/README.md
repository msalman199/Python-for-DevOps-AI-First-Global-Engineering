# 🔐 Secure Configuration Loader and Validator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/YAML-Configuration-CB171E?style=for-the-badge&logo=yaml&logoColor=white" />
  <img src="https://img.shields.io/badge/JSON-Schema-black?style=for-the-badge&logo=json&logoColor=white" />
  <img src="https://img.shields.io/badge/Security-Validation-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/Cybersecurity-Configuration_Hardening-green?style=for-the-badge" />
</p>

---

# 📖 Overview

Configuration files are critical components of modern applications. Misconfigured applications can expose sensitive data, allow unauthorized access, and create significant security risks.

In this lab, you will build a **Secure Configuration Loader and Validator** using Python. The validator will securely load YAML configuration files, verify required fields, inspect file permissions, detect weak passwords, identify insecure protocols, and generate detailed security reports.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Load configuration files securely

✅ Parse YAML configuration data safely

✅ Validate required configuration schemas

✅ Detect missing configuration values

✅ Identify weak passwords

✅ Detect insecure protocols (HTTP)

✅ Validate SSL/TLS settings

✅ Check Linux file permissions

✅ Generate comprehensive security reports

---

# 📋 Prerequisites

Before starting, ensure you have:

* Linux System Access
* Basic Linux Command Line Knowledge
* Familiarity with Nano or Vim
* Basic Python Programming Skills
* Understanding of Linux File Permissions

---

# 🛠️ Environment Setup

---

## 🚀 Step 1: Update System and Install Python

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

Verify Installation:

```bash
python3 --version
pip3 --version
```

Expected Output:

```bash
Python 3.x.x
pip x.x.x
```

---

## 📁 Step 2: Create Lab Directory

```bash
mkdir -p ~/config-security-lab
cd ~/config-security-lab
```

Verify:

```bash
pwd
```

---

## 🐍 Step 3: Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Verify Environment:

```bash
which python
```

Expected:

```bash
~/config-security-lab/venv/bin/python
```

---

## 📦 Step 4: Install Required Libraries

```bash
pip install pyyaml jsonschema
```

Verify:

```bash
pip list
```

Expected Libraries:

* PyYAML
* jsonschema

---

# 🧪 Task 1 — Create Sample Configuration Files

---

## 🔒 Step 1: Create Secure Configuration File

```bash
nano config_secure.yaml
```

Add:

```yaml
database:
  host: localhost
  port: 5432
  username: app_user
  password: "StrongP@ssw0rd123!"
  ssl_enabled: true

api:
  endpoint: https://api.example.com
  timeout: 30
  max_retries: 3

logging:
  level: INFO
  file: /var/log/app.log
```

---

## ⚠️ Step 2: Create Insecure Configuration File

```bash
nano config_insecure.yaml
```

Add:

```yaml
database:
  host: localhost
  port: 5432
  username: root
  password: "123456"
  ssl_enabled: false

api:
  endpoint: http://api.example.com
  timeout: 30

logging:
  level: DEBUG
```

---

## ❌ Step 3: Create Incomplete Configuration File

```bash
nano config_incomplete.yaml
```

Add:

```yaml
database:
  host: localhost
  port: 5432

api:
  endpoint: https://api.example.com
```

---

# 🏗️ Task 2 — Build the Configuration Validator

---

## 📝 Step 1: Create Main Python Script

```bash
nano config_validator.py
```

Paste the complete validator code provided in the lab instructions.

---

## 🔓 Step 2: Make Script Executable

```bash
chmod +x config_validator.py
```

Verify:

```bash
ls -l config_validator.py
```

Expected:

```bash
-rwxr-xr-x
```

---

## ▶️ Step 3: Run the Validator

```bash
python3 config_validator.py
```

---

# 🔍 Understanding Security Checks

---

## 🔐 Weak Password Detection

The validator searches for:

* password
* passwd

And identifies:

```text
123456
password
admin
root
12345
```

as weak credentials.

Example Warning:

```text
Weak password: database.password: Common weak password
```

---

## 🌐 Insecure Protocol Detection

The validator checks for:

```text
http://
```

instead of:

```text
https://
```

Example Warning:

```text
Insecure protocol: api.endpoint: Using insecure HTTP protocol
```

---

## 🛡️ SSL/TLS Validation

The validator verifies:

```yaml
ssl_enabled: true
```

Unsafe Configuration:

```yaml
ssl_enabled: false
```

Example Warning:

```text
SSL/TLS is disabled
```

---

## 👑 Privileged Account Detection

The validator flags:

```text
root
admin
administrator
```

Example Warning:

```text
Using privileged username: root
```

---

## 🐞 Debug Logging Detection

Production systems should avoid:

```yaml
level: DEBUG
```

Because debug logs may expose:

* Credentials
* Tokens
* Session IDs
* Internal Application Details

Example Warning:

```text
Debug logging enabled
```

---

## 🔒 File Permission Validation

The validator checks whether configuration files are world-readable.

Secure:

```bash
chmod 600 config_secure.yaml
```

Unsafe:

```bash
chmod 644 config_secure.yaml
```

Example Warning:

```text
Configuration file is world-readable
```

---

# ✅ Verification

---

## 📄 Verify All Configurations

Run:

```bash
python3 config_validator.py
```

Expected Results:

### 🔒 config_secure.yaml

Should produce:

```text
Configuration passed all security checks
```

or minimal warnings.

---

### ⚠️ config_insecure.yaml

Should report:

* Weak Password
* HTTP Usage
* SSL Disabled
* Debug Logging
* Privileged Username

---

### ❌ config_incomplete.yaml

Should report:

```text
Missing required field
Missing required section
```

errors.

---

# 🧪 Additional Permission Testing

---

## Make Configuration World-Readable

```bash
chmod 644 config_secure.yaml
```

Run:

```bash
python3 config_validator.py
```

Expected Warning:

```text
Configuration file is world-readable
```

---

## Fix Permissions

```bash
chmod 600 config_secure.yaml
```

Verify:

```bash
ls -l config_secure.yaml
```

Expected:

```bash
-rw-------
```

---

# 🎯 Create Your Own Test Configuration

Create:

```bash
nano config_test.yaml
```

Example:

```yaml
database:
  username: admin
  password: password

api:
  endpoint: http://internal-api.local

logging:
  level: DEBUG
```

Run Validator:

```bash
python3 config_validator.py
```

Verify detection of:

* Weak Passwords
* HTTP Protocol
* Debug Logging
* Privileged Username

---

# 📊 Expected Outcomes

Upon completion, you will have a validator capable of:

✅ Loading YAML safely

✅ Checking file permissions

✅ Validating schemas

✅ Detecting weak passwords

✅ Identifying insecure protocols

✅ Validating SSL/TLS settings

✅ Detecting dangerous configuration choices

✅ Generating security reports

---

# 🛠️ Troubleshooting

---

## ❌ YAML Parsing Errors

Cause:

Improper indentation.

Solution:

```yaml
database:
  host: localhost
```

Use spaces only.

Never use tabs.

---

## ❌ Module Not Found

Activate Virtual Environment:

```bash
source venv/bin/activate
```

Reinstall Packages:

```bash
pip install pyyaml jsonschema
```

---

## ❌ Permission Denied

Check Ownership:

```bash
ls -l config_*.yaml
```

Fix:

```bash
chmod 600 config_*.yaml
```

---

## ❌ Validator Not Detecting Issues

Verify configuration files match the sample content exactly.

Check YAML formatting.

Run:

```bash
cat config_insecure.yaml
```

---

# 🔐 Security Best Practices

Always:

✅ Validate configuration files before deployment

✅ Restrict permissions to 600 or 640

✅ Use HTTPS for all communications

✅ Enable SSL/TLS

✅ Store secrets securely

✅ Use least-privilege accounts

✅ Disable DEBUG mode in production

---

# 🌍 Real-World Significance

Configuration vulnerabilities are one of the most common causes of security breaches.

Organizations use automated validators to:

* Prevent insecure deployments
* Enforce compliance standards
* Detect weak passwords
* Ensure encryption is enabled
* Reduce human configuration errors

This technique is widely used in:

* DevSecOps
* Cloud Security
* Security Auditing
* Application Hardening
* Compliance Validation

---

# 🚀 Key Takeaways

✔️ Configuration files should always be validated before use

✔️ Weak passwords create major attack opportunities

✔️ HTTPS and SSL/TLS are mandatory for secure communications

✔️ Configuration files should never be world-readable

✔️ Debug logging should be disabled in production

✔️ Automated validation reduces deployment risks

---

# 🏆 Lab Complete

You have successfully built a **Secure Configuration Loader and Validator** capable of analyzing configuration files, identifying security weaknesses, validating schemas, checking permissions, and generating comprehensive security reports.

**Happy Secure Coding! 🔐🐍🚀**
