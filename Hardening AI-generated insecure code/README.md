# 🔐 Hardening AI-Generated Insecure Code

> *"AI can generate code quickly, but secure software requires human security review, validation, and hardening."*

---

# 📚 Overview

This hands-on cybersecurity lab demonstrates how AI-generated code can introduce security vulnerabilities and how to systematically identify, analyze, and remediate those weaknesses using secure coding practices and static analysis tools.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Identify common security vulnerabilities in AI-generated code

✅ Understand why AI tools may generate insecure patterns

✅ Apply secure coding best practices

✅ Use static analysis tools to discover vulnerabilities

✅ Implement input validation and sanitization

✅ Verify remediation efforts using automated security scanners

---

# 🛠 Prerequisites

- Basic Linux command line knowledge
- Familiarity with Python programming
- Basic understanding of:
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Command Injection
  - Path Traversal
- Linux machine with sudo privileges

---

# 🏗 Environment Setup

## Step 1: Update System

```bash
sudo apt update
```

## Step 2: Install Python Environment

```bash
sudo apt install -y python3 python3-pip python3-venv
```

## Step 3: Create Working Directory

```bash
mkdir ~/secure-code-lab
cd ~/secure-code-lab
```

## Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

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
└── venv/
```

---

# 🚨 Task 1 — Analyze Insecure AI-Generated Code

AI coding assistants often generate code that works functionally but may violate secure coding practices.

---

# 🛑 Vulnerability #1: SQL Injection

## File: user_login.py

```python
import sqlite3

def authenticate_user(username, password):
    """
    Authenticate user against database.
    WARNING: This code contains security vulnerabilities!
    """

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # VULNERABLE: Direct string concatenation in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    cursor.execute(query)

    result = cursor.fetchone()

    conn.close()

    if result:
        return True

    return False


if __name__ == "__main__":
    user = input("Enter username: ")
    pwd = input("Enter password: ")

    if authenticate_user(user, pwd):
        print("Login successful!")
    else:
        print("Login failed!")
```

---

## ⚠ Exploit Example

```text
Username:
admin' OR '1'='1

Password:
anything
```

Generated SQL:

```sql
SELECT * FROM users
WHERE username='admin' OR '1'='1'
AND password='anything'
```

Result:

```text
Authentication bypass
```

---

# 🛑 Vulnerability #2: Path Traversal

## File: file_reader.py

```python
import os

def read_user_file(filename):
    """
    Read a file from uploads directory.
    WARNING: Vulnerable code.
    """

    base_path = "/tmp/uploads/"

    file_path = base_path + filename

    try:
        with open(file_path, 'r') as f:
            return f.read()

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    file = input("Enter filename to read: ")
    print(read_user_file(file))
```

---

## ⚠ Exploit Example

```text
../../etc/passwd
```

Application attempts to read:

```text
/tmp/uploads/../../etc/passwd
```

Result:

```text
Unauthorized file disclosure
```

---

# 🛑 Vulnerability #3: Command Injection

## File: command_executor.py

```python
import os

def ping_host(hostname):
    """
    WARNING: Vulnerable code.
    """

    command = f"ping -c 4 {hostname}"

    result = os.system(command)

    return result


if __name__ == "__main__":
    host = input("Enter hostname to ping: ")
    ping_host(host)
```

---

## ⚠ Exploit Example

```text
google.com; cat /etc/passwd
```

Executed command:

```bash
ping -c 4 google.com; cat /etc/passwd
```

Result:

```text
Arbitrary command execution
```

---

# 🔍 Task 2 — Security Analysis with Bandit

## Run Security Scan

```bash
bandit -r . -f txt -o bandit_report.txt
```

## View Report

```bash
cat bandit_report.txt
```

---

## Expected Findings

### SQL Injection

```text
B608: SQL Injection
```

### Command Injection

```text
B605: Starting a process with a shell
B607: Partial executable path
```

### Path Traversal

```text
Unsafe file handling
```

---

# 🔐 Task 3 — Harden the Code

---

# ✅ Secure Version 1: SQL Injection Prevention

## File: user_login_secure.py

```python
import sqlite3
import hashlib


def hash_password(password):
    """
    Hash password using SHA256.
    Production recommendation:
    bcrypt or argon2.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_username(username):

    if not username:
        return False

    if len(username) > 50:
        return False

    return username.replace("_", "").isalnum()


def authenticate_user(username, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM users
    WHERE username=?
    AND password=?
    """

    hashed_pwd = hash_password(password)

    cursor.execute(
        query,
        (username, hashed_pwd)
    )

    result = cursor.fetchone()

    conn.close()

    return bool(result)


if __name__ == "__main__":

    user = input("Enter username: ")

    if not validate_username(user):
        print("Invalid username")
        exit(1)

    pwd = input("Enter password: ")

    if authenticate_user(user, pwd):
        print("Login successful!")
    else:
        print("Login failed!")
```

---

# 🔐 Security Improvements

✔ Parameterized queries

✔ Password hashing

✔ Username validation

✔ Reduced attack surface

---

# ✅ Secure Version 2: Path Traversal Prevention

## File: file_reader_secure.py

```python
import os
from pathlib import Path


def read_user_file(filename):

    base_path = Path("/tmp/uploads").resolve()

    safe_filename = os.path.basename(filename)

    file_path = (base_path / safe_filename).resolve()

    try:
        file_path.relative_to(base_path)

    except ValueError:
        return "Error: Path traversal detected!"

    if not file_path.exists():
        return "Error: File not found"

    if not file_path.is_file():
        return "Error: Invalid file"

    try:
        with open(file_path, "r") as f:
            return f.read()

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    file = input("Enter filename: ")
    print(read_user_file(file))
```

---

# 🔐 Security Improvements

✔ Path canonicalization

✔ Directory boundary enforcement

✔ Filename sanitization

✔ File existence validation

---

# ✅ Secure Version 3: Command Injection Prevention

## File: command_executor_secure.py

```python
import subprocess
import re


def validate_hostname(hostname):

    pattern = r'^[a-zA-Z0-9.-]+$'

    if not re.match(pattern, hostname):
        return False

    if len(hostname) > 253:
        return False

    return True


def ping_host(hostname):

    if not validate_hostname(hostname):
        print("Invalid hostname")
        return 1

    try:

        result = subprocess.run(
            [
                "ping",
                "-c",
                "4",
                hostname
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )

        print(result.stdout)

        return result.returncode

    except subprocess.TimeoutExpired:
        print("Ping timeout")
        return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    host = input("Enter hostname: ")
    ping_host(host)
```

---

# 🔐 Security Improvements

✔ No shell execution

✔ Argument list execution

✔ Input validation

✔ Timeout protection

✔ Safe subprocess usage

---

# 🧪 Verification

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

Valid Input:

```text
test.txt
```

Expected:

```text
This is a safe test file
```

---

Malicious Input:

```text
../../etc/passwd
```

Expected:

```text
Error: Path traversal detected!
```

---

# 🔎 Re-Scan Secure Files

```bash
bandit user_login_secure.py \
       file_reader_secure.py \
       command_executor_secure.py \
       -f txt
```

---

## Compare Results

```bash
echo "Original Issues:"
grep "Issue:" bandit_report.txt | wc -l

echo "Secure Issues:"
bandit *_secure.py 2>&1 | grep "Issue:" | wc -l
```

Expected:

```text
Original Issues: Multiple

Secure Issues: Significantly Reduced
```

---

# 📋 Security Improvements Summary

| Vulnerability | Insecure Practice | Secure Practice |
|--------------|------------------|----------------|
| SQL Injection | String Concatenation | Parameterized Queries |
| Path Traversal | Direct Path Usage | Path Validation |
| Command Injection | Shell Commands | Safe Subprocess API |
| Authentication | Plain Passwords | Hashed Passwords |
| User Input | No Validation | Strict Validation |

---

# 🛠 Troubleshooting

## Bandit Not Found

```bash
source ~/secure-code-lab/venv/bin/activate

pip install bandit
```

---

## Permission Denied

```bash
sudo mkdir -p /tmp/uploads
sudo chmod 755 /tmp/uploads
```

---

## Python Version Issues

```bash
python3 --version

which python3
```

---

# ✅ Verification Checklist

### Security Scan Completed

```bash
ls -lh bandit_report.txt
```

### Secure Files Exist

```bash
ls -1 *_secure.py
```

### Security Scan Passed

```bash
bandit *_secure.py -ll
```

### Functional Testing Completed

```bash
echo "test content" > /tmp/uploads/valid.txt

echo "valid.txt" | python3 file_reader_secure.py
```

---

# 🎓 Key Takeaways

- AI-generated code should never be trusted without review.
- Functionality does not equal security.
- Parameterized queries prevent SQL injection.
- Path validation prevents directory traversal attacks.
- Subprocess argument lists prevent command injection.
- Input validation is essential.
- Static analysis tools accelerate vulnerability discovery.
- Defense-in-depth improves overall security posture.

---

# 🚀 Real-World Applications

- Secure Software Development Lifecycle (SSDLC)
- DevSecOps Pipelines
- Application Security Testing
- Code Review Automation
- Secure AI-Assisted Development
- CI/CD Security Gates

---

# 📈 Next Steps

- Learn **Semgrep**
- Learn **OWASP Top 10**
- Explore **SAST** and **DAST**
- Integrate **Bandit** into GitHub Actions
- Study secure coding standards
- Implement automated security checks in CI/CD

---

# 🏁 Conclusion

Congratulations! 🎉

You successfully:

✔ Analyzed insecure AI-generated code

✔ Identified SQL Injection vulnerabilities

✔ Identified Path Traversal vulnerabilities

✔ Identified Command Injection vulnerabilities

✔ Used Bandit for static analysis

✔ Refactored insecure code into secure implementations

✔ Applied input validation and sanitization

✔ Verified improvements through automated testing

This lab demonstrates a critical cybersecurity skill: **reviewing and hardening AI-generated code before deployment into production environments.**

---
**Author:** Cybersecurity Hands-On Lab  
**Topic:** Secure Coding & AI Security  
**Difficulty:** Beginner → Intermediate  
**Platform:** Linux + Python + Bandit
