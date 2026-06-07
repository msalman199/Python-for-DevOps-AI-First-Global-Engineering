# 🛡️ Command-line Security Scanner

<div align="center">

# 🔍 Command-line Security Scanner

### Build a Python-Based Security Auditing Tool for Files & Directories

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=ubuntu)
![Security](https://img.shields.io/badge/Security-Scanner-red?style=for-the-badge\&logo=shield)
![Regex](https://img.shields.io/badge/Regex-Pattern_Matching-green?style=for-the-badge)
![CLI](https://img.shields.io/badge/CLI-Tool-purple?style=for-the-badge)
![Argparse](https://img.shields.io/badge/Argparse-Command_Line-success?style=for-the-badge)

---

### 🎯 Learn Security Scanning, Regex Detection & CLI Development

</div>

---

# 📚 Prerequisites

Before beginning this lab, ensure you have:

✅ Basic Linux command-line navigation (`cd`, `ls`, `cat`)

✅ Understanding of file permissions and text files

✅ Familiarity with Python 3 basics

✅ Ability to use a text editor (`nano`, `vim`, or `vi`)

---

# 🎯 Learning Objectives

By completing this lab, you will:

🔹 Build a command-line security scanning tool using Python

🔹 Parse and validate command-line arguments

🔹 Scan files and directories for security issues

🔹 Generate formatted terminal reports

🔹 Apply automated security validation techniques

🔹 Practice regex-based pattern detection

---

# 🖥️ Environment Setup

---

## 🚀 Step 1: Verify Python Installation

```bash
python3 --version
```

Expected Output:

```bash
Python 3.6+
```

---

## 📁 Step 2: Create Lab Directory

```bash
mkdir ~/security-scanner-lab

cd ~/security-scanner-lab
```

---

## 📦 Step 3: Install Required Package

```bash
pip3 install argparse --user
```

> Note: argparse is usually included with Python 3.

---

# 🔐 Task 1: Build the Security Scanner Tool

---

## 📝 Step 1: Create the Scanner Script

```bash
nano security_scanner.py
```

---

## 🏗️ Step 2: Add the Scanner Implementation

Paste the following complete code:

```python
#!/usr/bin/env python3

"""
Security Scanner - A simple CLI tool to scan files for security issues
"""

import argparse
import os
import re
import sys


class SecurityScanner:
    """Main security scanner class"""

    def __init__(self):

        self.patterns = {
            'hardcoded_password':
            r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',

            'api_key':
            r'(api_key|apikey|api-key)\s*=\s*["\'][^"\']+["\']',

            'private_key':
            r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',

            'ip_address':
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',

            'email':
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }

        self.findings = []


    def scan_file(self, filepath):

        if not os.path.isfile(filepath):
            print(
                f"Error: File '{filepath}' not found"
            )
            return

        try:
            with open(
                filepath,
                'r',
                encoding='utf-8',
                errors='ignore'
            ) as f:

                content = f.read()
                lines = content.split('\n')

        except Exception as e:
            print(f"Error reading file: {e}")
            return

        for line_num, line in enumerate(
            lines,
            start=1
        ):

            for issue_type, pattern in self.patterns.items():

                matches = re.finditer(
                    pattern,
                    line,
                    re.IGNORECASE
                )

                for match in matches:

                    self.findings.append({
                        'file': filepath,
                        'line': line_num,
                        'type': issue_type,
                        'content': line.strip(),
                        'match': match.group()
                    })


    def scan_directory(self, dirpath):

        if not os.path.isdir(dirpath):
            print(
                f"Error: Directory '{dirpath}' not found"
            )
            return

        for root, dirs, files in os.walk(dirpath):

            for filename in files:

                if filename.startswith('.'):
                    continue

                filepath = os.path.join(
                    root,
                    filename
                )

                self.scan_file(filepath)


    def generate_report(self):

        print("\n" + "=" * 70)
        print("SECURITY SCAN REPORT")
        print("=" * 70)

        if not self.findings:

            print(
                "\nNo security issues found!"
            )

            return

        print(
            f"\nTotal Issues Found: {len(self.findings)}\n"
        )

        by_type = {}

        for finding in self.findings:

            issue_type = finding['type']

            if issue_type not in by_type:
                by_type[issue_type] = []

            by_type[issue_type].append(
                finding
            )

        for issue_type, items in by_type.items():

            print(
                f"\n[{issue_type.upper().replace('_',' ')}]"
                f" - {len(items)} occurrence(s)"
            )

            print("-" * 70)

            for item in items:

                print(
                    f"  File: {item['file']}"
                )

                print(
                    f"  Line: {item['line']}"
                )

                print(
                    f"  Found: {item['match'][:50]}..."
                )

                print()


def main():

    parser = argparse.ArgumentParser(
        description=
        'Security Scanner - Scan files for common security issues',

        formatter_class=
        argparse.RawDescriptionHelpFormatter,

        epilog="""
Examples:
  python3 security_scanner.py -f config.txt
  python3 security_scanner.py -d /path/to/project
  python3 security_scanner.py --file secrets.env
"""
    )

    parser.add_argument(
        '-f',
        '--file',
        help='Scan a single file',
        type=str
    )

    parser.add_argument(
        '-d',
        '--directory',
        help='Scan all files in a directory',
        type=str
    )

    args = parser.parse_args()

    if not args.file and not args.directory:

        parser.print_help()
        sys.exit(1)

    scanner = SecurityScanner()

    if args.file:

        print(
            f"Scanning file: {args.file}"
        )

        scanner.scan_file(args.file)

    if args.directory:

        print(
            f"Scanning directory: {args.directory}"
        )

        scanner.scan_directory(
            args.directory
        )

    scanner.generate_report()


if __name__ == "__main__":
    main()
```

---

## ⚙️ Step 3: Make Script Executable

```bash
chmod +x security_scanner.py
```

---

# 🧪 Task 2: Test the Security Scanner

---

## 📄 Step 1: Create Test Files

### File 1: test_config.txt

```bash
cat > test_config.txt << 'EOF'
# Configuration File
database_host = 192.168.1.100
database_user = admin
password = "SuperSecret123"
api_key = "sk_live_abc123xyz789"
contact_email = admin@example.com

# SSH Key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----
EOF
```

---

### File 2: app_settings.py

```bash
cat > app_settings.py << 'EOF'
# Application Settings
DEBUG = True
SECRET_KEY = "django-insecure-key-12345"
DATABASE_PASSWORD = 'mypassword123'
API_ENDPOINT = "https://api.example.com"
ADMIN_EMAIL = "support@company.com"
SERVER_IP = "10.0.0.50"
EOF
```

---

## ▶️ Step 2: Run Scanner on a Single File

```bash
python3 security_scanner.py -f test_config.txt
```

Expected Findings:

✅ Password

✅ API Key

✅ Email Address

✅ IP Address

✅ RSA Private Key

---

## 📂 Step 3: Scan Entire Directory

```bash
python3 security_scanner.py -d ~/security-scanner-lab
```

Expected Result:

```text
SECURITY SCAN REPORT
======================================================
Total Issues Found: XX
```

---

## ❓ Step 4: Test Help Command

```bash
python3 security_scanner.py --help
```

Expected Output:

```text
usage: security_scanner.py [-h] [-f FILE] [-d DIRECTORY]
```

---

# ✅ Verification

---

## 🔍 Check 1: Verify Script Functionality

### Non-Existent File

```bash
python3 security_scanner.py -f nonexistent.txt
```

Expected:

```text
Error: File 'nonexistent.txt' not found
```

---

### No Arguments

```bash
python3 security_scanner.py
```

Expected:

```text
Usage information displayed
```

---

### Successful Scan

```bash
python3 security_scanner.py -f test_config.txt
```

Expected:

```text
Security findings displayed
```

---

## 🔍 Check 2: Verify Detection Capabilities

Your scanner should detect:

| Security Issue      | Expected Count |
| ------------------- | -------------- |
| Hardcoded Passwords | ≥ 1            |
| API Keys            | ≥ 1            |
| IP Addresses        | ≥ 2            |
| Email Addresses     | ≥ 2            |
| Private Key Header  | 1              |

---

## 📊 Check 3: Verify Report Format

Report should include:

✅ Security Scan Header

✅ Separator Lines

✅ Total Issue Count

✅ Findings Grouped by Type

✅ File Path Information

✅ Line Numbers

✅ Matched Content

---

# 📂 Example Project Structure

```text
security-scanner-lab/
│
├── security_scanner.py
├── test_config.txt
└── app_settings.py
```

---

# 🛠️ Troubleshooting

---

## ❌ Permission Denied

Solution:

```bash
chmod +x security_scanner.py
```

---

## ❌ No Module Named argparse

Solution:

```bash
pip3 install argparse --user
```

---

## ❌ Scanner Finds No Issues

Verify file contents:

```bash
cat test_config.txt
```

Ensure patterns exist in the file.

---

## ❌ Unicode Decode Errors

Already handled by:

```python
errors='ignore'
```

inside the file reader.

---

## ❌ Help Displays Instead of Scanning

Use one of:

```bash
python3 security_scanner.py -f filename

python3 security_scanner.py -d directory
```

---

# 🎓 Key Skills Practiced

### 🖥️ CLI Development

* Argument parsing
* User input validation
* Help documentation

### 📂 File Processing

* Reading files
* Directory traversal
* Recursive scanning

### 🔍 Security Analysis

* Credential detection
* Secret discovery
* Sensitive data identification

### 🧩 Regular Expressions

* Pattern matching
* Security signatures
* Content validation

### 📊 Reporting

* Structured output
* Finding aggregation
* User-friendly reporting

---

# 🏆 Conclusion

Congratulations! 🎉

You successfully built a **Command-line Security Scanner** capable of:

✅ Parsing CLI arguments

✅ Scanning files and directories

✅ Detecting security issues with regex

✅ Producing professional reports

✅ Handling errors gracefully

✅ Automating security reviews

---

# 🚀 Next-Level Enhancements

Expand your scanner with:

🔥 Severity Levels

📄 JSON Output

📊 CSV Reporting

🌐 URL Scanning

🔐 Secret Entropy Detection

☁️ CI/CD Integration

📦 Custom Rule Sets

⚡ Multi-threaded Scanning

---

<div align="center">

# 🎯 Lab Completed Successfully

### Keep Building Secure Automation Tools 🛡️

⭐ Happy Coding ⭐

</div>
