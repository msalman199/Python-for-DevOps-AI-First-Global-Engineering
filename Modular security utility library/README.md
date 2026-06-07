# 🛡️ Modular Security Utility Library

<div align="center">

# 🔐 Modular Security Utility Library

### Build Reusable Security Modules with Python

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=ubuntu)
![Security](https://img.shields.io/badge/Security-Utilities-red?style=for-the-badge\&logo=shield)
![Hashing](https://img.shields.io/badge/SHA--256-Hashing-green?style=for-the-badge)
![Testing](https://img.shields.io/badge/Testing-Validation-success?style=for-the-badge)
![CLI](https://img.shields.io/badge/CLI-Demo-purple?style=for-the-badge)

---

### 🎯 Learn Modular Programming Through Security Utilities

</div>

---

# 📚 Prerequisites

Before starting this lab, ensure you have:

✅ Basic Python programming knowledge (variables, functions, loops)

✅ Familiarity with Linux command line

✅ Understanding of file operations in Python

✅ Basic knowledge of text encoding concepts

---

# 🎯 Learning Objectives

By completing this lab, you will learn how to:

🔹 Build reusable secure code modules in Python

🔹 Organize security functions into logical modules

🔹 Implement basic security utilities for common tasks

🔹 Apply modular programming principles

🔹 Test and verify security utility functions

🔹 Create a reusable security package

---

# 🖥️ Environment Setup

## 🚀 Step 1: Prepare the Lab Environment

```bash
# Update package manager
sudo apt update

# Install Python 3 and pip
sudo apt install -y python3 python3-pip

# Create lab directory
mkdir -p ~/security-lab5
cd ~/security-lab5

# Verify Python installation
python3 --version
```

Expected Output:

```bash
Python 3.x.x
```

---

# 🔐 Task 1: Design and Implement Password Validation Module

---

## 📁 Step 1: Create the Module Structure

Navigate to the project directory:

```bash
cd ~/security-lab5
```

Create package folders:

```bash
mkdir -p securitylib/password
mkdir -p securitylib/hash
mkdir -p tests
```

Create package initialization files:

```bash
touch securitylib/__init__.py
touch securitylib/password/__init__.py
touch securitylib/hash/__init__.py
```

---

## 🏗️ Step 2: Build Password Validation Module

Create the validator module:

```bash
nano securitylib/password/validator.py
```

### ✨ Complete Password Validator

```python
"""
Password validation module for security library.
Provides functions to check password strength and compliance.
"""

import re

def check_length(password, min_length=8):
    return len(password) >= min_length


def has_uppercase(password):
    return any(char.isupper() for char in password)


def has_lowercase(password):
    return any(char.islower() for char in password)


def has_digit(password):
    return any(char.isdigit() for char in password)


def has_special_char(password):
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return any(char in special_chars for char in password)


def validate_password(password, min_length=8):

    errors = []

    if not check_length(password, min_length):
        errors.append(
            f"Password must be at least {min_length} characters"
        )

    if not has_uppercase(password):
        errors.append(
            "Password must contain an uppercase letter"
        )

    if not has_lowercase(password):
        errors.append(
            "Password must contain a lowercase letter"
        )

    if not has_digit(password):
        errors.append(
            "Password must contain a digit"
        )

    if not has_special_char(password):
        errors.append(
            "Password must contain a special character"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
```

---

# 🔑 Step 3: Build Hash Utility Module

Create:

```bash
nano securitylib/hash/hasher.py
```

### ✨ Complete Hash Utility

```python
"""
Hashing utilities for secure password storage and data integrity.
"""

import hashlib


def hash_sha256(data):
    return hashlib.sha256(
        data.encode()
    ).hexdigest()


def hash_file(filepath):

    with open(filepath, "rb") as file:
        file_data = file.read()

    return hashlib.sha256(
        file_data
    ).hexdigest()


def verify_hash(data, expected_hash):

    generated_hash = hash_sha256(data)

    return generated_hash == expected_hash
```

---

# 📦 Step 4: Create Package Initialization

Create:

```bash
nano securitylib/__init__.py
```

Add:

```python
"""
Security Utility Library
A modular collection of security functions.
"""

from securitylib.password import validator
from securitylib.hash import hasher

__version__ = "1.0.0"

__all__ = [
    "validator",
    "hasher"
]
```

---

# 🧪 Task 2: Test and Verify Security Utilities

---

## 🔬 Step 1: Create Test Script

Create:

```bash
nano tests/test_security.py
```

Add:

```python
"""
Test script for security utility library.
"""

import sys

sys.path.insert(
    0,
    "/home/ubuntu/security-lab5"
)

from securitylib.password import validator
from securitylib.hash import hasher


def test_password_validation():

    print(
        "=== Testing Password Validation ===\n"
    )

    test_passwords = [
        "weak",
        "StrongPass123!",
        "noupppercase123!",
        "NOLOWERCASE123!",
        "NoDigitsHere!",
        "NoSpecialChar123"
    ]

    for pwd in test_passwords:

        result = validator.validate_password(
            pwd
        )

        print(f"Password: {pwd}")
        print(f"Valid: {result['valid']}")

        if not result["valid"]:
            print(
                f"Errors: {', '.join(result['errors'])}"
            )

        print()


def test_hashing():

    print(
        "=== Testing Hash Functions ===\n"
    )

    test_data = "SecureData123"

    hash_result = hasher.hash_sha256(
        test_data
    )

    print(f"Data: {test_data}")
    print(f"SHA-256: {hash_result}\n")

    is_valid = hasher.verify_hash(
        test_data,
        hash_result
    )

    print(
        f"Hash verification: {is_valid}\n"
    )

    with open(
        "/tmp/test_file.txt",
        "w"
    ) as f:

        f.write(
            "Test file content for hashing"
        )

    file_hash = hasher.hash_file(
        "/tmp/test_file.txt"
    )

    print(
        f"File hash: {file_hash}\n"
    )


if __name__ == "__main__":

    test_password_validation()

    test_hashing()

    print(
        "=== All Tests Complete ==="
    )
```

---

## ▶️ Step 2: Run Tests

```bash
cd ~/security-lab5

python3 tests/test_security.py
```

### Expected Results

✅ Password validation output

✅ SHA-256 hash generation

✅ Hash verification result

✅ File hashing output

---

# 🎮 Step 3: Create Interactive Demo Tool

Create:

```bash
nano demo_tool.py
```

Add:

```python
#!/usr/bin/env python3

"""
Interactive demo of security utility library.
"""

from securitylib.password import validator
from securitylib.hash import hasher


def main():

    print(
        "Security Utility Library Demo\n"
    )

    print("1. Validate Password")
    print("2. Hash Data")
    print("3. Exit")

    choice = input(
        "\nEnter choice (1-3): "
    )

    if choice == "1":

        password = input(
            "Enter password to validate: "
        )

        result = validator.validate_password(
            password
        )

        if result["valid"]:
            print(
                "\n✓ Password is strong!"
            )
        else:
            print(
                "\n✗ Password is weak:"
            )

            for error in result["errors"]:
                print(
                    f"  - {error}"
                )

    elif choice == "2":

        data = input(
            "Enter data to hash: "
        )

        hash_value = hasher.hash_sha256(
            data
        )

        print(
            f"\nSHA-256 Hash: {hash_value}"
        )

    elif choice == "3":
        print("Goodbye!")

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
```

---

## 🚀 Execute Demo

```bash
chmod +x demo_tool.py

python3 demo_tool.py
```

---

# ✅ Verification

---

## 📂 Verify Module Structure

```bash
cd ~/security-lab5

tree -L 3
```

Expected Structure:

```text
.
├── securitylib/
│   ├── __init__.py
│   ├── password/
│   │   ├── __init__.py
│   │   └── validator.py
│   └── hash/
│       ├── __init__.py
│       └── hasher.py
├── tests/
│   └── test_security.py
└── demo_tool.py
```

---

## 🔍 Verify Password Module

```bash
python3 -c "
from securitylib.password import validator
print(
validator.validate_password('Test123!')
)
"
```

Expected:

```python
{
 'valid': True,
 'errors': []
}
```

---

## 🔍 Verify Hash Module

```bash
python3 -c "
from securitylib.hash import hasher
print(
hasher.hash_sha256('test')
)
"
```

Expected:

```text
9f86d081884c7d659a2fe...
```

---

## 📦 Verify Import System

```bash
python3 << EOF

import sys

sys.path.insert(
    0,
    '/home/ubuntu/security-lab5'
)

from securitylib import validator, hasher

print(
    'Modules imported successfully!'
)

print(
    f'Validator functions: {dir(validator)}'
)

print(
    f'Hasher functions: {dir(hasher)}'
)

EOF
```

---

# 🛠️ Troubleshooting

## ❌ Import Errors

### Solution

```bash
ls securitylib
```

Ensure:

```text
__init__.py
```

exists in every package directory.

---

## ❌ Module Not Found

Add project path:

```python
import sys

sys.path.insert(
    0,
    "/home/ubuntu/security-lab5"
)
```

---

## ❌ Function Returns None

Check for unfinished code:

```python
pass
```

Replace all placeholder code with actual implementations.

---

## ❌ Hash Function Errors

Correct:

```python
data.encode()
```

File hashing:

```python
open(file, "rb")
```

Never use text mode for hashing files.

---

# 🎓 Key Concepts Learned

### 🔐 Password Security

* Length validation
* Uppercase checks
* Lowercase checks
* Digit validation
* Special character enforcement

### 🔑 Cryptographic Hashing

* SHA-256 hashing
* Data integrity verification
* File hashing
* Hash comparison

### 📦 Modular Python Design

* Package structure
* Reusable modules
* Import systems
* Clean architecture

### 🧪 Testing

* Unit-style validation
* Functional verification
* CLI demonstration

---

# 🏆 Conclusion

Congratulations! 🎉

You successfully created a **Modular Security Utility Library** featuring:

✅ Password validation module

✅ Secure SHA-256 hashing utilities

✅ Python package architecture

✅ Automated testing framework

✅ Interactive CLI demonstration

✅ Reusable security components

---

## 🚀 Benefits of Modular Design

✔ Reusable across projects

✔ Easier maintenance

✔ Better scalability

✔ Team collaboration

✔ Cleaner code organization

✔ Faster development

---

# 🌟 Next Steps

Expand your security library with:

🔐 Encryption Utilities

👤 Authentication Modules

📜 Audit Logging

🛡️ Access Control Functions

🌐 Secure API Helpers

🔑 Key Management Tools

---

<div align="center">

### 🎯 Lab Complete Successfully

**Keep Building Secure Software! 🔐**

⭐ Happy Coding ⭐

</div>
