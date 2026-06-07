# 🤖 Natural-Language Requirement Functional Python Tool

<div align="center">

# 🧠 Natural-Language Requirement → Functional Python Tool

### Convert Human Requirements into Executable Python Function Templates

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=ubuntu)
![Automation](https://img.shields.io/badge/Automation-Code_Generation-green?style=for-the-badge)
![NLP](https://img.shields.io/badge/NLP-Requirement_Parsing-purple?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Automation-red?style=for-the-badge\&logo=shield)
![Developer](https://img.shields.io/badge/Developer-Productivity-success?style=for-the-badge)

---

### 🎯 Transform Natural Language Requirements into Python Code

</div>

---

# 📚 Prerequisites

Before starting this lab, ensure you have:

✅ Basic Python programming knowledge

✅ Familiarity with Linux command line

✅ Understanding of Python string manipulation

✅ Access to a Linux machine with internet access

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

🔹 Parse natural language requirements

🔹 Extract structured information from human-readable text

🔹 Generate Python function templates automatically

🔹 Build a requirement-to-code conversion tool

🔹 Implement generated functions with real logic

🔹 Bridge communication between requirements and implementation

---

# 🖥️ Environment Setup

---

## 🚀 Step 1: Access Lab Environment

Click **Start Lab** and connect to your Linux machine using SSH.

---

## 📦 Step 2: Install Required Tools

```bash
# Update package manager
sudo apt update

# Install Python
sudo apt install -y python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

Expected Output:

```bash
Python 3.x.x
pip 23.x.x
```

---

## 📁 Step 3: Create Lab Directory

```bash
mkdir ~/nlp-requirement-tool

cd ~/nlp-requirement-tool
```

---

# 🧠 Task 1: Build a Natural Language Requirement Parser

---

## 📖 Overview

In this task, you will create a Python tool capable of converting simple natural language requirements into executable Python function templates.

Example:

```text
validate user password strength
```

Becomes:

```python
def validate_user_password_strength(input_data):
    pass
```

This simulates how security professionals translate requirements into code.

---

# 📝 Step 1: Create Main Script

```bash
nano requirement_parser.py
```

---

# ⚙️ Step 2: Implement Requirement Parser

Paste the following code:

```python
#!/usr/bin/env python3
"""
Natural Language Requirement to Python Function Converter
Parses simple requirements and generates function templates
"""

import re
import sys


class RequirementParser:
    """
    Parses natural language requirements into
    function specifications.
    """

    def __init__(self):

        self.action_verbs = [
            "validate",
            "check",
            "verify",
            "scan",
            "analyze",
            "filter",
            "encrypt",
            "decrypt",
            "authenticate"
        ]


    def parse_requirement(
        self,
        requirement: str
    ) -> dict:

        requirement = (
            requirement
            .lower()
            .strip()
        )

        action = None

        for verb in self.action_verbs:

            if verb in requirement:

                action = verb
                break

        target = (
            requirement
            .replace(action, "")
            .strip()
            if action
            else requirement
        )

        function_name = (
            requirement
            .replace(" ", "_")
        )

        return {

            "function_name":
            function_name,

            "action":
            action,

            "target":
            target,

            "original":
            requirement
        }


    def generate_function_template(
        self,
        parsed_req: dict
    ) -> str:

        function_name = parsed_req[
            "function_name"
        ]

        action = parsed_req[
            "action"
        ]

        target = parsed_req[
            "target"
        ]

        template = f'''
def {function_name}(input_data):
    """
    {action.capitalize()} {target}.

    Args:
        input_data: Data to process

    Returns:
        bool: True if successful
    """

    result = False

    # TODO:
    # Implement {action} logic

    return result
'''

        return template


def main():

    parser = RequirementParser()

    print("=" * 60)

    print(
        "Natural Language Requirement "
        "to Python Function Converter"
    )

    print("=" * 60)

    sample_requirements = [

        "validate user password strength",

        "check file permissions",

        "scan network ports",

        "encrypt sensitive data"
    ]

    print(
        "\nProcessing Requirements:\n"
    )

    for req in sample_requirements:

        print(
            f"Requirement: '{req}'"
        )

        parsed = parser.parse_requirement(
            req
        )

        print(
            f"  Function Name: "
            f"{parsed['function_name']}"
        )

        print(
            f"  Action: "
            f"{parsed['action']}"
        )

        print(
            f"  Target: "
            f"{parsed['target']}"
        )

        template = (
            parser
            .generate_function_template(
                parsed
            )
        )

        filename = (
            f"{parsed['function_name']}.py"
        )

        with open(
            filename,
            "w"
        ) as f:

            f.write(template)

        print(
            f"  Generated: {filename}\n"
        )

    print("=" * 60)

    print(
        "Function templates generated "
        "successfully!"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

# 🔐 Step 3: Make Script Executable

```bash
chmod +x requirement_parser.py
```

---

# ▶️ Step 4: Run Parser

```bash
python3 requirement_parser.py
```

Expected Output:

```text
============================================================
Natural Language Requirement to Python Function Converter
============================================================

Requirement: 'validate user password strength'

Function Name:
validate_user_password_strength

Action:
validate

Target:
user password strength

Generated:
validate_user_password_strength.py
```

---

# 🧩 Task 2: Implement Generated Functions

---

# 📂 Step 1: Review Generated Templates

List files:

```bash
ls -la *.py
```

View generated template:

```bash
cat validate_user_password_strength.py
```

---

# 🛠️ Step 2: Implement Password Validation Function

Edit generated file:

```bash
nano validate_user_password_strength.py
```

Replace contents with:

```python
def validate_user_password_strength(
    input_data
):
    """
    Validate password strength.
    """

    password = str(input_data)

    has_length = (
        len(password) >= 8
    )

    has_upper = any(
        c.isupper()
        for c in password
    )

    has_lower = any(
        c.islower()
        for c in password
    )

    has_digit = any(
        c.isdigit()
        for c in password
    )

    has_special = any(
        not c.isalnum()
        for c in password
    )

    return all([
        has_length,
        has_upper,
        has_lower,
        has_digit,
        has_special
    ])


if __name__ == "__main__":

    test_passwords = [

        "weak",

        "StrongPass1!",

        "NoSpecial123",

        "MySecureP@ssw0rd"
    ]

    for pwd in test_passwords:

        is_valid = (
            validate_user_password_strength(
                pwd
            )
        )

        print(
            f"Password: '{pwd}' "
            f"- Valid: {is_valid}"
        )
```

---

# 🧪 Step 3: Test Implementation

Run:

```bash
python3 validate_user_password_strength.py
```

Expected Output:

```text
Password: 'weak' - Valid: False

Password: 'StrongPass1!' - Valid: True

Password: 'NoSpecial123' - Valid: False

Password: 'MySecureP@ssw0rd' - Valid: True
```

---

# ✅ Verification

---

## 🔍 Step 1: Verify Parser

Run parser again:

```bash
python3 requirement_parser.py
```

Verify files:

```bash
ls -1 *.py | wc -l
```

Expected:

```text
5
```

Files:

```text
requirement_parser.py

validate_user_password_strength.py

check_file_permissions.py

scan_network_ports.py

encrypt_sensitive_data.py
```

---

## 🔍 Step 2: Verify Password Validation

Run:

```bash
python3 validate_user_password_strength.py
```

Confirm valid passwords return:

```text
True
```

Weak passwords return:

```text
False
```

---

## 🧪 Step 3: Create Custom Requirement

Create:

```bash
nano test_custom_requirement.py
```

Add:

```python
#!/usr/bin/env python3

from requirement_parser import (
    RequirementParser
)

parser = RequirementParser()

custom_req = (
    "verify email format"
)

parsed = parser.parse_requirement(
    custom_req
)

template = (
    parser.generate_function_template(
        parsed
    )
)

print(
    f"Custom Requirement: "
    f"{custom_req}"
)

print(
    "\nGenerated Function:\n"
)

print(template)
```

---

Run:

```bash
python3 test_custom_requirement.py
```

Expected:

```python
def verify_email_format(
    input_data
):
    """
    Verify email format.
    """
```

---

# 📂 Project Structure

Expected layout:

```text
nlp-requirement-tool/
│
├── requirement_parser.py
├── validate_user_password_strength.py
├── check_file_permissions.py
├── scan_network_ports.py
├── encrypt_sensitive_data.py
└── test_custom_requirement.py
```

---

# 🛠️ Troubleshooting

---

## ❌ Module Not Found

Verify location:

```bash
pwd
```

Expected:

```text
~/nlp-requirement-tool
```

---

## ❌ Permission Denied

Fix:

```bash
chmod +x *.py
```

---

## ❌ No Output Generated

Check action verbs list:

```python
self.action_verbs
```

Ensure requirements contain supported verbs.

---

## ❌ Templates Generated But Don't Work

Remember:

Generated functions are templates only.

You must implement the actual business logic.

---

## ❌ File Creation Errors

Verify write permissions:

```bash
ls -la
```

Check ownership:

```bash
whoami
```

---

# 🎓 Key Skills Practiced

### 🧠 Requirement Analysis

* Natural language parsing
* Requirement extraction
* Structured data creation

### ⚙️ Automation

* Automatic file generation
* Template creation
* Development acceleration

### 🐍 Python Development

* Classes
* Functions
* Dictionaries
* String manipulation

### 🔐 Security Engineering Relevance

Examples:

```text
validate input sanitization

verify authentication token

check password strength

scan open network ports
```

These are common cybersecurity requirements.

---

# 🌍 Real-World Cybersecurity Applications

Security engineers frequently receive requirements such as:

```text
Validate user credentials

Verify access tokens

Scan systems for vulnerabilities

Encrypt sensitive records
```

This tool helps bridge:

```text
Business Requirement
        ↓
Structured Requirement
        ↓
Python Function Template
        ↓
Implementation
```

---

# 🏆 Conclusion

Congratulations! 🎉

You successfully created a:

✅ Natural Language Requirement Parser

✅ Function Template Generator

✅ Automated Code Creation Tool

✅ Password Validation Implementation

✅ Requirement-to-Code Workflow

---

# 🚀 Next Steps

Expand the project by adding:

🔹 Parameter extraction

🔹 Multiple function arguments

🔹 AI-assisted requirement analysis

🔹 JSON/YAML requirement support

🔹 Security requirement templates

🔹 Compliance rule generation

🔹 Unit test generation

🔹 Automatic documentation creation

---

<div align="center">

# 🎯 Lab Completed Successfully

### From Human Requirements ➜ Working Python Code 🚀

⭐ Happy Coding & Automation ⭐

</div>
