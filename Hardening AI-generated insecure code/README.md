# 🛡️ Hardening AI-Generated Insecure Code

> *"AI can generate code in seconds, but secure code requires human judgment, validation, and defensive programming."*

---

# 📌 Overview

The **Hardening AI-Generated Insecure Code** lab demonstrates how artificial intelligence tools can produce functional yet vulnerable code and how cybersecurity professionals can identify, analyze, and remediate these security weaknesses.

This project focuses on three of the most dangerous application security vulnerabilities:

* SQL Injection
* Path Traversal
* Command Injection

Using Python, Bandit, and secure coding techniques, you'll learn how to transform insecure AI-generated scripts into production-ready secure implementations.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Identify security flaws commonly found in AI-generated code

✅ Understand why AI-generated code may introduce vulnerabilities

✅ Analyze code using static security analysis tools

✅ Implement secure coding best practices

✅ Apply input validation and sanitization techniques

✅ Refactor vulnerable code into secure implementations

---

# 🏗️ Environment Setup

## Step 1: Update the System

```bash
sudo apt update
```

---

## Step 2: Install Python Dependencies

```bash
sudo apt install -y python3 python3-pip python3-venv
```

---

## Step 3: Create Project Directory

```bash
mkdir ~/secure-code-lab
cd ~/secure-code-lab
```

---

## Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 5: Install Security Tools

```bash
pip install bandit safety pylint
```

---

# 📂 Project Structure

```text
secure-code-lab/
│
├── user_login.py
├── file_reader.py
├── command_executor.py
│
├── user_login_secure.py
├── file_reader_secure.py
├── command_executor_secure.py
│
├── bandit_report.txt
│
└── README.md
```

---

# 🔍 Task 1: Analyze AI-Generated Insecure Code

Modern AI coding assistants frequently generate code that works correctly but lacks security protections.

This lab demonstrates three common examples.

---

# 🚨 Vulnerability 1: SQL Injection

## Insecure Script

**File:** `user_login.py`

### Vulnerable Code

```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

### Why It's Dangerous

User input is directly inserted into a SQL statement.

Attackers can manipulate queries and bypass authentication.

### Example Attack

```text
Username:
admin' OR '1'='1

Password:
anything
```

Result:

```text
Authentication Bypass
```

---

# 🚨 Vulnerability 2: Path Traversal

## Insecure Script

**File:** `file_reader.py`

### Vulnerable Code

```python
file_path = base_path + filename
```

### Why It's Dangerous

No validation prevents users from navigating outside the intended directory.

### Example Attack

```text
../../etc/passwd
```

Result:

```text
Sensitive System Files Exposed
```

---

# 🚨 Vulnerability 3: Command Injection

## Insecure Script

**File:** `command_executor.py`

### Vulnerable Code

```python
command = f"ping -c 4 {hostname}"
os.system(command)
```

### Why It's Dangerous

User input is executed directly by the operating system shell.

### Example Attack

```text
google.com; cat /etc/passwd
```

Result:

```text
Arbitrary Command Execution
```

---

# 🔬 Security Analysis with Bandit

Bandit is a Python static analysis tool designed to identify security vulnerabilities.

---

## Run Security Scan

```bash
bandit -r . -f txt -o bandit_report.txt
```

---

## View Results

```bash
cat bandit_report.txt
```

---

## Expected Findings

Bandit should identify:

| Vulnerability     | Bandit ID |
| ----------------- | --------- |
| SQL Injection     | B608      |
| Command Injection | B605      |
| Shell Execution   | B607      |
| Unsafe Operations | Multiple  |

---

# 🔒 Task 2: Refactor and Harden the Code

---

# 🛡️ Secure Login Implementation

## File

```text
user_login_secure.py
```

---

## Security Improvements

### Parameterized Queries

Instead of:

```python
query = f"SELECT * FROM users WHERE username='{username}'"
```

Use:

```python
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, hashed_pwd))
```

---

### Password Hashing

```python
hashlib.sha256(password.encode()).hexdigest()
```

Benefits:

* Passwords are not stored in plaintext
* Reduced credential exposure risk

---

### Username Validation

```python
return username.replace('_', '').isalnum()
```

Allows:

```text
john_doe
admin1
user123
```

Blocks:

```text
admin';
<script>
```

---

# 🛡️ Secure File Reader

## File

```text
file_reader_secure.py
```

---

## Security Improvements

### Path Sanitization

```python
safe_filename = os.path.basename(filename)
```

Removes malicious path components.

---

### Path Resolution

```python
file_path = (base_path / safe_filename).resolve()
```

---

### Directory Boundary Validation

```python
file_path.relative_to(base_path)
```

Ensures files remain inside:

```text
/tmp/uploads/
```

---

### Example Attack Blocked

```text
../../etc/passwd
```

Response:

```text
Access denied - path traversal detected!
```

---

# 🛡️ Secure Command Executor

## File

```text
command_executor_secure.py
```

---

## Security Improvements

### Hostname Validation

Allowed:

```text
google.com
example.org
192.168.1.10
```

Blocked:

```text
google.com; rm -rf /
```

---

### Safe Process Execution

Instead of:

```python
os.system(command)
```

Use:

```python
subprocess.run(
    ['ping', '-c', '4', hostname]
)
```

Benefits:

* No shell interpretation
* Prevents command chaining
* Eliminates injection attacks

---

### Timeout Protection

```python
timeout=10
```

Prevents:

* Hanging processes
* Resource abuse

---

# 🔬 Verify Security Improvements

## Scan Secure Versions

```bash
bandit user_login_secure.py \
       file_reader_secure.py \
       command_executor_secure.py \
       -f txt
```

---

## Compare Results

```bash
echo "=== Comparison ==="

echo "Original vulnerabilities:"
grep "Issue:" bandit_report.txt | wc -l

echo "Secure vulnerabilities:"
bandit *_secure.py 2>&1 | grep "Issue:" | wc -l
```

Expected:

```text
Significantly fewer findings
```

---

# 🧪 Functional Testing

---

## Create Test Environment

```bash
mkdir -p /tmp/uploads
echo "This is a safe test file" > /tmp/uploads/test.txt
```

---

## Test Secure File Reader

```bash
python3 file_reader_secure.py
```

Input:

```text
test.txt
```

Expected:

```text
This is a safe test file
```

---

## Test Traversal Attack

Input:

```text
../../etc/passwd
```

Expected:

```text
Access denied - path traversal detected!
```

---

# ✅ Verification Checklist

## Verify Bandit Report

```bash
ls -lh bandit_report.txt
```

---

## Verify Secure Files

```bash
ls -1 *_secure.py
```

Expected:

```text
user_login_secure.py
file_reader_secure.py
command_executor_secure.py
```

---

## Run Final Security Scan

```bash
bandit *_secure.py -ll
```

Expected:

```text
No High-Severity Findings
```

---

# 📊 Vulnerability Remediation Summary

| Vulnerability     | Insecure Implementation | Secure Implementation      |
| ----------------- | ----------------------- | -------------------------- |
| SQL Injection     | String Concatenation    | Parameterized Queries      |
| Password Storage  | Plaintext               | SHA-256 Hashing            |
| Path Traversal    | Unvalidated Paths       | Path Resolution Validation |
| Command Injection | os.system()             | subprocess.run()           |
| Input Validation  | None                    | Whitelisting & Validation  |

---

# 🔐 Security Principles Demonstrated

This project applies several industry-standard secure coding principles:

### Input Validation

Validate all user-supplied data before processing.

---

### Least Privilege

Grant only the minimum required permissions.

---

### Defense in Depth

Multiple layers of security controls.

---

### Secure APIs

Prefer safe APIs over dangerous alternatives.

Examples:

```text
subprocess.run()  >  os.system()
Parameterized SQL > String Concatenation
```

---

### Fail Securely

Reject malicious input safely.

---

# 🌍 Real-World Applications

These techniques are used in:

### Secure Software Development

* Web Applications
* APIs
* Authentication Systems

### DevSecOps Pipelines

* CI/CD Security Scanning
* Secure Code Reviews

### Security Engineering

* Threat Modeling
* Vulnerability Management
* Secure Architecture Reviews

---

# 🚀 Future Enhancements

Enhance the project by integrating:

* Semgrep
* OWASP Dependency Check
* Trivy
* SonarQube
* GitHub CodeQL
* Automated CI/CD Security Testing

---

# 📚 Additional Learning Resources

Topics to study next:

* OWASP Top 10
* Secure Authentication Design
* Secure Password Storage (bcrypt, Argon2)
* Secure File Upload Handling
* Secure API Development
* DevSecOps Practices

---

# 🎓 Key Takeaways

✅ AI-generated code should never be trusted blindly

✅ Security reviews are mandatory for AI-produced software

✅ Static analysis tools quickly identify common vulnerabilities

✅ Input validation is one of the strongest defenses

✅ Secure APIs reduce attack surface

✅ Defense-in-depth creates resilient applications

---

# 🏆 Conclusion

The **Hardening AI-Generated Insecure Code** lab demonstrates how cybersecurity professionals transform vulnerable code into secure, production-ready software.

Through this project, you learned to:

* Detect critical vulnerabilities
* Analyze code using Bandit
* Refactor insecure implementations
* Apply secure coding practices
* Validate and sanitize user input
* Verify improvements using security tooling

As AI-generated code becomes increasingly common, the ability to review, secure, and harden generated software will become one of the most valuable skills for security engineers, developers, and DevSecOps professionals.

---

### ⭐ If you found this project useful, consider starring the repository and sharing it with fellow cybersecurity learners.
