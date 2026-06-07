# 🔐 Password Strength Validation Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=linux)
![Security](https://img.shields.io/badge/Cybersecurity-Password%20Validation-red?style=for-the-badge&logo=hackaday)
![Regex](https://img.shields.io/badge/Regex-Pattern%20Matching-green?style=for-the-badge)
![CLI](https://img.shields.io/badge/CLI-Terminal-black?style=for-the-badge)

# 🔒 Password Strength Validation Tool 

### Build a Security-Focused Password Validation System with Python

</div>

---

# 📚 Overview

Modern applications require strong password policies to protect users against brute-force attacks, credential stuffing, and dictionary attacks.

In this lab, you'll build a complete Password Strength Validation Tool that:

✅ Validates password length

✅ Checks password complexity

✅ Detects weak patterns

✅ Calculates strength scores

✅ Provides actionable user feedback

✅ Supports batch password testing

---

# 🎯 Learning Objectives

By completing this lab, you will:

- 🔐 Understand password security best practices
- 📏 Implement password length validation
- 🔤 Enforce password complexity requirements
- 🚨 Detect weak password patterns
- 📊 Create password strength scoring
- 🧠 Apply regular expressions for security validation
- 📂 Implement dictionary attack prevention
- ⚡ Build reusable security tooling

---

# 🛠️ Prerequisites

- Linux command-line knowledge
- Python basics
- Familiarity with text editors
- Python 3 installed

---

# 🏗️ Environment Setup

## Step 1: Verify Python Installation

```bash
python3 --version
```

Expected Output:

```text
Python 3.x.x
```

---

## Step 2: Create Project Directory

```bash
mkdir ~/password-validator-lab
cd ~/password-validator-lab
```

---

## Step 3: Create Project File

```bash
touch password_validator.py
chmod +x password_validator.py
```

---

# 📁 Project Structure

```text
password-validator-lab/
│
├── password_validator.py
├── common_passwords.txt
├── test_passwords.txt
└── README.md
```

---

# 🚀 Task 1 — Build the Password Validator

---

## 🔹 Step 1: Import Required Libraries

### password_validator.py

```python
#!/usr/bin/env python3

import re
import sys

COMMON_PASSWORDS = [
    'password',
    '123456',
    '12345678',
    'qwerty',
    'abc123',
    'monkey',
    '1234567',
    'letmein',
    'trustno1',
    'dragon',
    'baseball',
    'iloveyou',
    'master',
    'sunshine',
    'ashley',
    'bailey',
    'passw0rd',
    'shadow',
    '123123',
    '654321'
]
```

---

## 🔹 Step 2: Length Validation Function

```python
def check_length(password):
    """
    Validate password length.
    """

    min_length = 8
    max_length = 128

    if min_length <= len(password) <= max_length:
        return (True, "Length is adequate")

    return (
        False,
        f"Password must be {min_length}-{max_length} characters"
    )
```

---

## 🔹 Step 3: Complexity Validation

```python
def check_complexity(password):

    score = 0
    missing = []

    if re.search(r'[a-z]', password):
        score += 1
    else:
        missing.append("Lowercase letter")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        missing.append("Uppercase letter")

    if re.search(r'\d', password):
        score += 1
    else:
        missing.append("Digit")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        missing.append("Special character")

    return score, missing
```

---

## 🔹 Step 4: Weak Pattern Detection

```python
def check_common_patterns(password):

    issues = []

    if password.lower() in COMMON_PASSWORDS:
        issues.append("Common password detected")

    if re.search(r'123|234|345|456|567|678|789|abc|bcd|cde', password.lower()):
        issues.append("Sequential pattern detected")

    if re.search(r'(.)\1{2,}', password):
        issues.append("Repeated characters detected")

    return len(issues) > 0, issues
```

---

## 🔹 Step 5: Strength Calculation

```python
def calculate_strength(password):

    total_score = 0
    feedback = []

    length_valid, length_msg = check_length(password)

    if not length_valid:
        feedback.append(length_msg)

        return {
            "score": 0,
            "strength": "Invalid",
            "feedback": feedback
        }

    total_score += 20

    complexity_score, missing = check_complexity(password)

    total_score += complexity_score * 15

    if missing:
        feedback.extend(
            [f"Missing: {item}" for item in missing]
        )

    weak, issues = check_common_patterns(password)

    if weak:
        total_score -= 30
        feedback.extend(issues)

    if len(password) > 12:
        total_score += 10

    if len(password) > 16:
        total_score += 10

    total_score = max(0, min(100, total_score))

    if total_score <= 30:
        strength = "Weak"
    elif total_score <= 60:
        strength = "Fair"
    elif total_score <= 80:
        strength = "Good"
    else:
        strength = "Strong"

    return {
        "score": total_score,
        "strength": strength,
        "feedback": feedback
    }
```

---

## 🔹 Step 6: Dictionary Password Loader

```python
def load_common_passwords(
        filename='common_passwords.txt'
):

    try:
        with open(filename, 'r') as f:
            return {
                line.strip().lower()
                for line in f
            }

    except FileNotFoundError:
        return set()
```

---

## 🔹 Step 7: Batch Password Testing

```python
def batch_test(filename):

    total = 0
    strong = 0
    weak = 0

    try:
        with open(filename) as f:

            for password in f:

                password = password.strip()

                if not password:
                    continue

                total += 1

                result = calculate_strength(password)

                print(
                    f"{password:<25}"
                    f"{result['strength']}"
                )

                if result["strength"] == "Strong":
                    strong += 1

                if result["strength"] == "Weak":
                    weak += 1

        print("\nSummary")
        print("-" * 30)
        print(f"Total Tested : {total}")
        print(f"Strong       : {strong}")
        print(f"Weak         : {weak}")

    except FileNotFoundError:
        print("Password file not found")
```

---

## 🔹 Step 8: Main Program

```python
def main():

    print("=" * 50)
    print("Password Strength Validator")
    print("=" * 50)

    password = input(
        "Enter password to validate: "
    )

    result = calculate_strength(password)

    print("\nResults")
    print("-" * 50)

    print(
        f"Strength : {result['strength']}"
    )

    print(
        f"Score    : {result['score']}/100"
    )

    if result["feedback"]:
        print("\nFeedback:")

        for item in result["feedback"]:
            print(f" - {item}")


if __name__ == "__main__":
    main()
```

---

# 🛡️ Task 2 — Dictionary Attack Prevention

---

## Create Password Dictionary

```bash
cat > common_passwords.txt << EOF
password
123456
12345678
qwerty
abc123
EOF
```

---

# ⚡ Batch Testing

Create test file:

```bash
cat > test_passwords.txt << EOF
password
MyP@ss123
Str0ng!Pass2024
abc123
TestP@ssw0rd!2024
EOF
```

Run:

```python
batch_test("test_passwords.txt")
```

---

# 🧪 Verification

## Test 1

```bash
python3 password_validator.py
```

### Input

```text
pass
```

Expected:

```text
Invalid
```

---

## Test 2

```text
password123
```

Expected:

```text
Weak
```

---

## Test 3

```text
MyP@ssw0rd
```

Expected:

```text
Fair / Good
```

---

## Test 4

```text
Tr0ng!P@ssw0rd2024
```

Expected:

```text
Strong
```

---

# 🧪 Automated Test Function

```python
def run_tests():

    test_cases = [
        ("abc123", "Sequential Pattern"),
        ("Password123", "Common Word"),
        ("aaa111", "Repetition"),
        ("Tr0ng!P@ss#2024", "Strong Password")
    ]

    for password, description in test_cases:

        result = calculate_strength(password)

        print("\n" + "=" * 50)

        print(description)

        print(
            f"Password : {password}"
        )

        print(
            f"Result   : {result}"
        )
```

---

# 📊 Expected Outcomes

After completing this lab, you will have:

✅ Password Length Validation

✅ Character Complexity Checks

✅ Weak Pattern Detection

✅ Dictionary Attack Prevention

✅ Strength Scoring Engine

✅ Batch Validation System

✅ Security Feedback Mechanism

---

# 🛠️ Troubleshooting

## Issue: Python Module Error

```bash
python3 --version
```

Verify Python installation.

---

## Issue: Password Visible on Screen

Use:

```python
import getpass

password = getpass.getpass()
```

---

## Issue: Dictionary File Missing

```bash
ls -la common_passwords.txt
```

---

## Issue: Regex Not Matching

Test regex interactively:

```bash
python3
```

```python
import re

re.search(r'[a-z]', 'Test')
```

---

# 🎓 Conclusion

Congratulations! 🎉

You have successfully built a complete Password Strength Validation Tool that demonstrates:

🔐 Password Security Enforcement

📏 Length Validation

🔤 Complexity Validation

🚨 Weak Pattern Detection

📂 Dictionary Attack Protection

📊 Security Scoring Algorithms

⚡ Automated Security Assessment

These concepts are widely used in:

- Identity & Access Management (IAM)
- Application Security
- Authentication Systems
- Cybersecurity Operations
- Security Compliance Programs

---

<div align="center">

## 🏆 Lab Complete

**Secure Passwords = Stronger Security**

🔐 Happy Coding & Stay Secure!

</div>
