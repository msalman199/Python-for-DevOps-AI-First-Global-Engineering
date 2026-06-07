# 🐞 Debugging and Refactoring a Flawed Script

<div align="center">

# 🔧 Debugging and Refactoring a Flawed Script

### Identify Bugs • Fix Security Vulnerabilities • Improve Code Quality

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Bash](https://img.shields.io/badge/Bash-Scripting-green?style=for-the-badge\&logo=gnu-bash)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=ubuntu)
![ShellCheck](https://img.shields.io/badge/ShellCheck-Static_Analysis-success?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Hardening-red?style=for-the-badge\&logo=shield)
![Refactoring](https://img.shields.io/badge/Code-Refactoring-purple?style=for-the-badge)

---

### 🎯 Learn Secure Coding Through Debugging & Refactoring

</div>

---

# 📚 Prerequisites

Before starting this lab, ensure you have:

✅ Basic Linux command-line knowledge

✅ Familiarity with text editors (`nano`, `vim`, `vi`)

✅ Basic Python programming knowledge

✅ Basic Bash scripting knowledge

✅ Understanding of Linux file permissions

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

🔹 Identify syntax, logic, and runtime bugs

🔹 Detect and remediate security vulnerabilities

🔹 Prevent command injection attacks

🔹 Remove hardcoded credentials

🔹 Refactor inefficient code

🔹 Improve maintainability and readability

🔹 Apply secure coding practices

---

# 🖥️ Environment Setup

---

## 🚀 Step 1: Provision Lab Machine

Click **Start Lab** and connect using SSH.

---

## 📦 Step 2: Install Required Packages

```bash
sudo apt update

sudo apt install -y python3 python3-pip shellcheck
```

---

## 📁 Step 3: Create Working Directory

```bash
mkdir ~/debug-lab

cd ~/debug-lab
```

---

# 🐍 Task 1: Debug and Fix a Flawed Python Script

---

# 📝 Step 1: Create the Flawed Script

Create:

```bash
nano user_manager.py
```

Paste the provided vulnerable code into the file.

---

# 🔍 Step 2: Identify the Bugs

## 🚨 Security Issues

### Hardcoded Credentials

```python
admin_password = "admin123"
```

Problem:

❌ Password stored in plaintext

Risk:

🔥 Credential exposure

---

### Command Injection

```python
command = "cat /etc/passwd | grep " + user_input
os.system(command)
```

Problem:

❌ User controls command execution

Example Attack:

```bash
; ls -la
```

Risk:

🔥 Arbitrary command execution

---

### Missing Input Validation

```python
add_user(username)
```

Problem:

❌ Accepts any input

Risk:

🔥 Invalid or malicious data

---

## 🧠 Logic Errors

### Authentication Bypass

```python
if username == "admin" or password == admin_password:
```

Problem:

❌ Uses OR instead of AND

Impact:

User gains access using:

```text
Username: admin
Password: wrong
```

---

### Missing Newline

```python
file.write(username)
```

Problem:

❌ Users stored on same line

---

## 🧹 Code Quality Problems

### Missing Error Handling

```python
open("/tmp/users.txt", "r")
```

Problem:

❌ Crashes if file missing

---

### No Context Managers

```python
file = open(...)
file.close()
```

Problem:

❌ Resource leaks possible

---

# 🛠️ Step 3: Create Fixed Version

Create:

```bash
nano user_manager_fixed.py
```

---

# 🔐 Secure Authentication

```python
import hashlib

ADMIN_PASSWORD_HASH = hashlib.sha256(
    "admin123".encode()
).hexdigest()
```

Benefits:

✅ No plaintext comparison

✅ Password hashing

---

# 🔒 Fixed Authentication Logic

```python
def authenticate_user(username, password):

    password_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    if (
        username == "admin"
        and
        password_hash == ADMIN_PASSWORD_HASH
    ):
        return True

    return False
```

Improvements:

✅ Uses AND

✅ Verifies hash securely

---

# 🛡️ Safe User Listing

```python
import subprocess

def list_users():

    try:

        result = subprocess.run(
            [
                "grep",
                "/bin/bash",
                "/etc/passwd"
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        print(result.stdout)

    except subprocess.TimeoutExpired:

        print("Command timed out")

    except Exception as e:

        print(
            f"Error listing users: {e}"
        )
```

Benefits:

✅ Prevents injection

✅ Timeout protection

✅ Exception handling

---

# ✔ Input Validation

```python
if (
    not username.isalnum()
    or len(username) < 3
    or len(username) > 20
):
    print(
        "Invalid username"
    )
```

Benefits:

✅ Blocks malicious input

✅ Enforces standards

---

# 📂 Secure File Writing

```python
with open(
    "/tmp/users.txt",
    "a"
) as file:

    file.write(
        username + "\n"
    )
```

Benefits:

✅ Context manager

✅ Automatic cleanup

✅ Proper formatting

---

# 📖 Safe File Reading

```python
try:

    with open(
        "/tmp/users.txt",
        "r"
    ) as file:

        users = file.read()

except FileNotFoundError:

    return (
        "User file not found"
    )
```

Benefits:

✅ Handles missing files

✅ Prevents crashes

---

# 🎛️ Menu Validation

```python
choice = input(
    "Enter choice (1-5): "
).strip()

if (
    not choice.isdigit()
    or int(choice) not in range(1,6)
):
    print("Invalid choice")
```

Benefits:

✅ Prevents invalid input

---

# 🧪 Step 4: Test Both Versions

---

## Run Vulnerable Script

```bash
chmod +x user_manager.py

python3 user_manager.py
```

---

### Authentication Bypass Test

Input:

```text
1
admin
wrong
```

Buggy Result:

```text
Access granted
```

❌ Security failure

---

### Command Injection Test

Input:

```text
2
; ls -la
```

Buggy Result:

```text
Directory listing displayed
```

❌ Command injection successful

---

## Run Fixed Version

```bash
chmod +x user_manager_fixed.py

python3 user_manager_fixed.py
```

Same tests now:

```text
Access denied
```

✅ Vulnerability fixed

---

# 🐚 Task 2: Debug and Refactor a Bash Script

---

# 📝 Step 1: Create Vulnerable Script

```bash
nano backup_script.sh
```

Paste provided backup script.

---

# 🔍 Step 2: Analyze with ShellCheck

Run:

```bash
shellcheck backup_script.sh
```

ShellCheck identifies:

⚠ Unquoted variables

⚠ Missing error checks

⚠ Unsafe command usage

⚠ Potential word splitting

⚠ Script reliability issues

---

# 🛠️ Step 3: Create Fixed Script

Create:

```bash
nano backup_script_fixed.sh
```

---

# 🚀 Enable Strict Mode

```bash
set -euo pipefail
```

Meaning:

| Option   | Purpose                      |
| -------- | ---------------------------- |
| -e       | Exit on error                |
| -u       | Error on undefined variables |
| pipefail | Detect pipeline failures     |

---

# ✔ Validate Input

```bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 <source_directory>"
    exit 1
fi
```

Benefits:

✅ Prevents incorrect execution

---

# ✔ Verify Source Directory

```bash
if [ ! -d "$SOURCE_DIR" ]; then

    echo "Directory does not exist"

    exit 1

fi
```

Benefits:

✅ Prevents backup failures

---

# ✔ Create Backup Directory Safely

```bash
mkdir -p "$BACKUP_DIR"
```

Benefits:

✅ Creates only when needed

---

# ✔ Quote Variables

Bad:

```bash
cp -r $SOURCE_DIR $BACKUP_DIR
```

Good:

```bash
cp -r "$SOURCE_DIR" "$BACKUP_DIR"
```

Benefits:

✅ Prevents word splitting

✅ Handles spaces safely

---

# ✔ Timestamp Validation

```bash
timestamp=$(date +%Y%m%d) || {

    echo "Failed"

    exit 1

}
```

Benefits:

✅ Error detection

---

# ✔ Safe Rename

```bash
source_basename=$(
    basename "$SOURCE_DIR"
)
```

Then:

```bash
mv \
"$BACKUP_DIR/$source_basename" \
"$BACKUP_DIR/backup_$timestamp"
```

Benefits:

✅ Safe path handling

---

# ✔ Secure Logging

```bash
echo \
"Backup completed at $(date)" \
>> "$BACKUP_DIR/backup.log"
```

Benefits:

✅ Removes hardcoded password

✅ Useful audit trail

---

# 🧪 Step 4: Test Fixed Script

---

## Make Executable

```bash
chmod +x backup_script.sh

chmod +x backup_script_fixed.sh
```

---

## Create Test Data

```bash
mkdir -p ~/test_backup

echo "test file" \
> ~/test_backup/test.txt
```

---

## Execute Backup

```bash
./backup_script_fixed.sh \
~/test_backup
```

Expected:

```text
Backup completed successfully
```

---

## Verify Backup

```bash
ls -la /tmp/backups/
```

---

## View Log

```bash
cat /tmp/backups/backup.log
```

---

## Test Error Handling

```bash
./backup_script_fixed.sh \
/nonexistent/directory
```

Expected:

```text
Error: Source directory does not exist
```

---

# ✅ Verification

---

# Python Improvements

### Authentication Test

```bash
echo -e \
"1\nadmin\nwrong" \
| python3 user_manager_fixed.py
```

Expected:

```text
Access denied
```

---

### Input Validation

```bash
echo -e \
"3\nuser@123" \
| python3 user_manager_fixed.py
```

Expected:

```text
Invalid username
```

---

# Bash Improvements

### Static Analysis

```bash
shellcheck backup_script_fixed.sh
```

Expected:

✅ No critical warnings

---

### Usage Validation

```bash
./backup_script_fixed.sh
```

Expected:

```text
Usage:
backup_script_fixed.sh
<source_directory>
```

---

### Backup Verification

```bash
ls /tmp/backups/backup_*/test.txt
```

Expected:

```text
test.txt
```

---

# 🛠️ Troubleshooting

---

## Python Import Errors

Verify:

```bash
python3 --version
```

---

## Permission Errors

Check:

```bash
ls -l /tmp/users.txt
```

---

## ShellCheck Missing

Install:

```bash
sudo apt install shellcheck
```

---

## Script Not Executable

Fix:

```bash
chmod +x script.sh
```

---

## Bash Debugging

Enable tracing:

```bash
set -x
```

---

## Python Debugging

Use debugger:

```bash
python3 -m pdb script.py
```

---

## System Diagnostics

```bash
journalctl -xe
```

or

```bash
dmesg
```

---

# 🎓 Key Skills Practiced

### 🔍 Vulnerability Discovery

* Hardcoded credentials
* Command injection
* Input validation failures

### 🔐 Secure Coding

* Password hashing
* Safe subprocess usage
* Secure file handling

### 🧹 Refactoring

* Context managers
* Error handling
* Cleaner logic

### 🐚 Bash Hardening

* Variable quoting
* Strict mode
* Safe path handling

### 📊 Static Analysis

* ShellCheck
* Code review techniques

---

# 🏆 Conclusion

Congratulations! 🎉

You successfully:

✅ Identified security vulnerabilities

✅ Fixed authentication bypasses

✅ Prevented command injection

✅ Implemented proper input validation

✅ Refactored Python code

✅ Hardened Bash scripts

✅ Applied secure coding best practices

✅ Used ShellCheck for automated analysis

---

# 🚀 Real-World Applications

These skills are directly applicable to:

🔐 Security Audits

🛡️ Vulnerability Assessments

💻 Secure Software Development

📜 Code Reviews

🚨 Incident Response

⚙️ DevSecOps Pipelines

🏢 Enterprise Security Operations

---

<div align="center">

# 🎯 Lab Completed Successfully

### Secure Code Starts with Good Debugging 🔐

⭐ Happy Debugging & Refactoring ⭐

</div>
