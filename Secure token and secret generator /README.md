# 🔐 Secure Token and Secret Generator

> *"Strong security starts with strong secrets. Generate them securely, store them safely, and manage them responsibly."*

---

## 📖 Overview

The **Secure Token and Secret Generator** is a hands-on cybersecurity lab that demonstrates how to generate cryptographically secure tokens, API keys, passwords, and secrets using Python's built-in `secrets` module.

This project teaches best practices for secure randomness, credential generation, token management, and secure storage of sensitive information.

---

## 🎯 Learning Objectives

By completing this lab, you will learn how to:

* 🔑 Understand cryptographic randomness and why it matters
* 🎲 Generate secure random values using Python's `secrets` module
* 🛡️ Create API keys and secret credentials programmatically
* 🔒 Generate strong passwords and authentication tokens
* 📂 Store sensitive credentials securely
* ⚙️ Build a reusable token management utility
* 🚫 Avoid insecure randomness mechanisms

---

## 🛠️ Prerequisites

Before starting, ensure you have:

* Linux environment (Ubuntu recommended)
* Python 3.8+
* Basic Linux command-line knowledge
* Familiarity with Python basics
* Text editor (nano, vim, VS Code)

---

# 🏗️ Environment Setup

## Step 1: Update System

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

---

## Step 2: Create Lab Directory

```bash
mkdir -p ~/secure-token-lab
cd ~/secure-token-lab
```

---

## Step 3: Verify Python Installation

```bash
python3 --version
```

Expected Output:

```text
Python 3.8+
```

---

# 📚 Task 1: Understanding Cryptographic Randomness

## Why Cryptographic Randomness Matters

Secure random numbers are used for:

* Authentication tokens
* Session IDs
* Password reset links
* API keys
* Encryption keys
* Multi-factor authentication

### ❌ Never Use

```python
import random
```

for security-sensitive operations.

### ✅ Always Use

```python
import secrets
```

---

## Create Comparison Script

### File: `random_comparison.py`

```python
import random
import secrets

print("=== Insecure Random (for demonstration only) ===")

random.seed(42)

for i in range(3):
    print(f"Random number {i+1}: {random.randint(1000,9999)}")

print("\n=== Cryptographically Secure Random ===")

for i in range(3):
    print(
        f"Secure number {i+1}: {secrets.randbelow(9000)+1000}"
    )
```

---

## Run the Script

```bash
python3 random_comparison.py
```

Observe:

* `random` produces predictable output.
* `secrets` produces unpredictable output.

---

# 🔑 Task 2: Generate Secure Tokens

## Create Token Generator

### File: `token_generator.py`

```python
#!/usr/bin/env python3

import secrets
import string


def generate_hex_token(length=32):
    return secrets.token_hex(length)


def generate_url_safe_token(length=32):
    return secrets.token_urlsafe(length)


def generate_alphanumeric_token(length=16):
    alphabet = string.ascii_letters + string.digits

    return ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def main():

    print("=== Secure Token Generator ===\n")

    print("1. Hexadecimal Token")
    print(generate_hex_token())

    print("\n2. URL Safe Token")
    print(generate_url_safe_token())

    print("\n3. Alphanumeric Token")
    print(generate_alphanumeric_token())


if __name__ == "__main__":
    main()
```

---

## Execute

```bash
chmod +x token_generator.py
python3 token_generator.py
```

---

## Verify Uniqueness

```bash
for i in {1..3}
do
    echo "Run $i"
    python3 token_generator.py
    echo ""
done
```

Every execution should generate different values.

---

# 🔐 Task 3: API Key and Secret Generator

## Create Generator

### File: `api_key_generator.py`

```python
#!/usr/bin/env python3

import secrets
import string
import json
import os

from datetime import datetime


def generate_api_key(prefix="sk", length=32):

    alphabet = string.ascii_letters + string.digits

    random_part = ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )

    return f"{prefix}_{random_part}"


def generate_secret_key(length=64):
    return secrets.token_hex(length)


def generate_password(length=20, use_special=True):

    alphabet = string.ascii_letters + string.digits

    if use_special:
        alphabet += string.punctuation

    return ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def save_credentials(filename, credentials):

    with open(filename, "w") as f:
        json.dump(credentials, f, indent=2)

    os.chmod(filename, 0o600)


def main():

    credentials = {
        "generated_at": datetime.now().isoformat(),
        "api_key": generate_api_key(),
        "api_secret": generate_secret_key(),
        "webhook_secret": generate_secret_key(32),
        "admin_password": generate_password(),
        "database_password": generate_password(24)
    }

    for key, value in credentials.items():
        print(f"{key}: {value}")

    save_credentials(
        "credentials.json",
        credentials
    )

    print("\nSaved securely to credentials.json")


if __name__ == "__main__":
    main()
```

---

## Run

```bash
python3 api_key_generator.py
```

---

## Verify Permissions

```bash
ls -l credentials.json
```

Expected:

```text
-rw------- 1 user user
```

---

# 🚀 Task 4: Complete Token Management Tool

## Features

The Token Manager can generate:

| Token Type         | Purpose                     |
| ------------------ | --------------------------- |
| Session Token      | User sessions               |
| CSRF Token         | CSRF protection             |
| Reset Token        | Password resets             |
| API Key Pair       | API authentication          |
| OTP Secret         | 2FA/MFA                     |
| Complete Token Set | Full application deployment |

---

## Create Token Manager

### File: `token_manager.py`

```python
#!/usr/bin/env python3

import secrets
import string
import json
import os

from datetime import datetime


class TokenManager:

    def __init__(self):
        self.tokens = {}

    def generate_session_token(self):
        return secrets.token_urlsafe(32)

    def generate_csrf_token(self):
        return secrets.token_hex(32)

    def generate_reset_token(self):
        return secrets.token_urlsafe(48)

    def generate_api_key_pair(self, prefix="app"):

        key_id = ''.join(
            secrets.choice(
                string.ascii_uppercase +
                string.digits
            )
            for _ in range(16)
        )

        return {
            "api_key": f"{prefix}_{key_id}",
            "api_secret": secrets.token_hex(32)
        }

    def generate_otp_secret(self):

        import base64

        random_bytes = secrets.token_bytes(20)

        return base64.b32encode(
            random_bytes
        ).decode()

    def create_token_set(self, name):

        token_set = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "session_token": self.generate_session_token(),
            "csrf_token": self.generate_csrf_token(),
            "reset_token": self.generate_reset_token(),
            "api_credentials": self.generate_api_key_pair(name),
            "otp_secret": self.generate_otp_secret()
        }

        self.tokens[name] = token_set

        return token_set

    def save_tokens(self):

        with open("tokens.json", "w") as f:
            json.dump(self.tokens, f, indent=2)

        os.chmod("tokens.json", 0o600)
```

---

## Execute

```bash
chmod +x token_manager.py
python3 token_manager.py
```

---

# ✅ Verification

## Verify Token Uniqueness

### File: `verify_tokens.py`

```python
#!/usr/bin/env python3

import secrets

tokens = set()

count = 1000

for _ in range(count):
    tokens.add(
        secrets.token_hex(32)
    )

print(f"Generated: {count}")
print(f"Unique: {len(tokens)}")

if len(tokens) == count:
    print("SUCCESS")
else:
    print("Duplicates Found")
```

Run:

```bash
python3 verify_tokens.py
```

Expected:

```text
Generated: 1000
Unique: 1000
SUCCESS
```

---

## Check JSON Security

```bash
ls -la *.json
```

Expected:

```text
-rw------- credentials.json
-rw------- tokens.json
```

---

## Check Entropy

```bash
python3 -c "import secrets; print(len(secrets.token_hex(32))*4)"
```

Expected:

```text
256
```

Meaning:

```text
256-bit entropy
```

---

# 📂 Project Structure

```text
secure-token-lab/
│
├── random_comparison.py
├── token_generator.py
├── api_key_generator.py
├── token_manager.py
├── verify_tokens.py
│
├── credentials.json
├── tokens.json
│
└── README.md
```

---

# 🔒 Security Best Practices

### ✅ Do

* Use `secrets` module
* Rotate tokens regularly
* Restrict file permissions (600)
* Use HTTPS
* Store secrets securely
* Audit credential access

### ❌ Don't

* Use `random` for security
* Commit secrets to Git repositories
* Store secrets in plaintext logs
* Share credentials over insecure channels
* Reuse API keys indefinitely

---

# 🌍 Real-World Applications

This project demonstrates techniques used in:

* Web Authentication Systems
* OAuth Providers
* API Gateways
* Password Reset Workflows
* JWT Infrastructure
* Session Management
* Cloud Security Platforms
* DevSecOps Pipelines

---

# 📈 Key Takeaways

* Cryptographic randomness is essential for security.
* Python's `secrets` module should be used for all sensitive token generation.
* API credentials must be securely stored and protected.
* Strong entropy prevents guessing and brute-force attacks.
* File permissions are an important part of secret management.

---

# 🎉 Lab Complete

You have successfully built a **Secure Token and Secret Generator** capable of generating:

* 🔑 API Keys
* 🔒 Secret Keys
* 🌐 Session Tokens
* 🛡️ CSRF Tokens
* 🔄 Password Reset Tokens
* 🔐 OTP Secrets

These are the same foundational techniques used in modern authentication and cybersecurity systems.
