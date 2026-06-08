# 🔐 Password Hashing and Verification System

> *"Passwords should never be stored — only verified."*

---

## 🎯 Overview

The **Password Hashing and Verification System** demonstrates how modern applications securely store and verify user passwords using the industry-standard **bcrypt** hashing algorithm.

This lab contrasts insecure plain-text password storage with secure password hashing and salting techniques, helping learners understand the importance of protecting user credentials against data breaches, rainbow table attacks, and unauthorized access.

---

## 🏷️ Technology Stack

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=linux)
![bcrypt](https://img.shields.io/badge/bcrypt-Password%20Hashing-green?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data%20Storage-black?style=for-the-badge)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Authentication-red?style=for-the-badge)

---

# 📚 Learning Objectives

By completing this lab, you will learn how to:

✅ Understand why storing passwords in plain text is dangerous

✅ Implement secure password hashing using bcrypt

✅ Apply cryptographic salts automatically

✅ Verify passwords securely without storing original passwords

✅ Build an interactive password management system

✅ Understand real-world password security practices

---

# 📋 Prerequisites

Before starting, ensure you have:

- Basic Linux command-line knowledge
- Familiarity with Python programming
- Understanding of passwords and authentication
- Internet connectivity
- Python 3.x installed

---

# 🛠️ Environment Setup

## Step 1: Update System Packages

```bash
sudo apt update
```

---

## Step 2: Install Python and Pip

```bash
sudo apt install python3 python3-pip -y
```

---

## Step 3: Install bcrypt

```bash
pip3 install bcrypt
```

---

## Step 4: Create Working Directory

```bash
mkdir ~/password-lab
cd ~/password-lab
```

---

# 🚨 Task 1: Understanding Insecure Password Storage

## Why Plain Text Passwords Are Dangerous

When passwords are stored as plain text:

❌ Attackers can read all passwords immediately

❌ Users often reuse passwords across websites

❌ One breach can compromise multiple accounts

❌ Compliance regulations may be violated

---

## Create Demonstration Script

### File: `plain_text_demo.py`

```python
# plain_text_demo.py
# This demonstrates INSECURE password storage (DO NOT USE IN PRODUCTION)

def store_password_insecure(username, password):
    """
    BAD PRACTICE: Storing passwords in plain text
    """
    with open('insecure_passwords.txt', 'a') as f:
        f.write(f"{username}:{password}\n")
    print(f"[INSECURE] Stored password for {username}")

def verify_password_insecure(username, password):
    """
    BAD PRACTICE: Checking plain text passwords
    """
    try:
        with open('insecure_passwords.txt', 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split(':')
                if stored_user == username and stored_pass == password:
                    return True
        return False
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    print("=== INSECURE PASSWORD STORAGE DEMO ===")

    store_password_insecure("alice", "password123")
    store_password_insecure("bob", "qwerty456")

    print("\nVerifying passwords:")
    print(f"Alice login: {verify_password_insecure('alice', 'password123')}")
    print(f"Bob wrong password: {verify_password_insecure('bob', 'wrong')}")

    print("\n[WARNING] Check insecure_passwords.txt to see the danger!")
```

---

## Execute Demo

```bash
python3 plain_text_demo.py
```

---

## Inspect Stored Passwords

```bash
cat insecure_passwords.txt
```

### Example Output

```text
alice:password123
bob:qwerty456
```

⚠️ Anyone who can access this file can see all user passwords.

---

# 🔒 Task 2: Implement Secure Password Hashing

## Create Secure Password Manager

### File: `secure_password_manager.py`

```python
import bcrypt
import json
import os

class SecurePasswordManager:
    """
    A secure password manager using bcrypt
    """

    def __init__(self, storage_file='secure_passwords.json'):
        self.storage_file = storage_file
        self.users = self._load_users()

    def _load_users(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.users, f, indent=2)

    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def register_user(self, username, password):

        if username in self.users:
            print(f"[ERROR] User '{username}' already exists")
            return False

        hashed_password = self.hash_password(password)

        self.users[username] = hashed_password

        self._save_users()

        print(f"[SUCCESS] User '{username}' registered successfully")
        return True

    def verify_password(self, username, password):

        if username not in self.users:
            print(f"[ERROR] User '{username}' not found")
            return False

        stored_hash = self.users[username].encode('utf-8')
        password_bytes = password.encode('utf-8')

        result = bcrypt.checkpw(password_bytes, stored_hash)

        if result:
            print(f"[SUCCESS] Password verified for '{username}'")
        else:
            print(f"[FAILED] Invalid password for '{username}'")

        return result

    def list_users(self):
        return list(self.users.keys())


if __name__ == "__main__":

    print("=== SECURE PASSWORD MANAGER ===\n")

    manager = SecurePasswordManager()

    print("--- Registering Users ---")

    manager.register_user("alice", "SecurePass123!")
    manager.register_user("bob", "MyP@ssw0rd")
    manager.register_user("alice", "duplicate")

    print("\n--- Verifying Passwords ---")

    manager.verify_password("alice", "SecurePass123!")
    manager.verify_password("alice", "WrongPassword")
    manager.verify_password("bob", "MyP@ssw0rd")
    manager.verify_password("charlie", "anything")

    print("\n--- Registered Users ---")
    print(f"Users: {manager.list_users()}")
```

---

## Run Secure Password Manager

```bash
python3 secure_password_manager.py
```

---

## View Hashed Passwords

```bash
cat secure_passwords.json
```

### Example Output

```json
{
  "alice": "$2b$12$Pb3ZPzM9...",
  "bob": "$2b$12$D1skL3v..."
}
```

✅ Passwords are no longer readable.

---

# 💻 Task 3: Interactive Password CLI

## File: `password_cli.py`

```python
from secure_password_manager import SecurePasswordManager
import getpass

def main():

    manager = SecurePasswordManager()

    print("=" * 50)
    print("SECURE PASSWORD MANAGEMENT SYSTEM")
    print("=" * 50)

    while True:

        print("\nOptions:")
        print("1. Register new user")
        print("2. Login")
        print("3. List users")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":

            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")

            manager.register_user(username, password)

        elif choice == "2":

            username = input("Enter username: ").strip()
            password = getpass.getpass("Enter password: ")

            if manager.verify_password(username, password):
                print(f"\nWelcome, {username}!")
            else:
                print("\nAccess denied!")

        elif choice == "3":

            users = manager.list_users()

            print(
                f"\nRegistered users: {', '.join(users) if users else 'None'}"
            )

        elif choice == "4":

            print("\nGoodbye!")
            break

        else:

            print("\n[ERROR] Invalid choice")

if __name__ == "__main__":
    main()
```

---

## Launch Interactive CLI

```bash
python3 password_cli.py
```

---

# 🧪 Verification

## Test Salt Functionality

### File: `test_salt.py`

```python
import bcrypt

password = "SamePassword123"

print("Hashing the same password 3 times:\n")

for i in range(3):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    print(f"Hash {i+1}: {hashed.decode()}")

print("\nEach hash is different because bcrypt generates a unique salt.")
```

---

## Run Test

```bash
python3 test_salt.py
```

### Example Output

```text
Hash 1: $2b$12$...
Hash 2: $2b$12$...
Hash 3: $2b$12$...
```

✅ Same password

✅ Different hashes

✅ Rainbow table resistant

---

# 🔍 Security Comparison

## Insecure Storage

```text
alice:password123
bob:qwerty456
```

---

## Secure Storage

```json
{
  "alice": "$2b$12$...",
  "bob": "$2b$12$..."
}
```

---

# ✅ Verification Checklist

- [x] Plain text storage demonstrated
- [x] bcrypt installed successfully
- [x] Password hashing implemented
- [x] Salt generation verified
- [x] Password verification works
- [x] Incorrect passwords rejected
- [x] Interactive CLI functional
- [x] Passwords stored securely

---

# 🌍 Real-World Applications

This technology is used in:

🔐 User Authentication Systems

🔐 Enterprise Identity Management

🔐 Banking Applications

🔐 Cloud Platforms

🔐 Healthcare Systems

🔐 Government Security Infrastructure

🔐 E-Commerce Websites

---

# 🎓 Key Skills Demonstrated

### Authentication Security

- Password Hashing
- Password Verification
- User Authentication

### Cryptography

- Salting
- One-Way Hash Functions
- bcrypt Implementation

### Secure Coding

- Input Handling
- Data Storage Security
- Credential Protection

### Python Development

- Object-Oriented Programming
- JSON Data Handling
- File Management

---

# 📈 Next Steps

Enhance the project by adding:

- Multi-Factor Authentication (MFA)
- Password Strength Enforcement
- Password Expiration Policies
- Account Lockout Protection
- Login Attempt Tracking
- Secure Database Storage
- Argon2 Password Hashing Support
- Web-Based Authentication Interface

---

# 🏆 Conclusion

You successfully built a **Password Hashing and Verification System** that follows modern cybersecurity best practices.

The project demonstrates:

✅ Secure password hashing with bcrypt

✅ Automatic salt generation

✅ Password verification without storing plaintext passwords

✅ Interactive authentication workflows

✅ Protection against common password attacks

These concepts are fundamental in cybersecurity, secure software development, identity management, and modern authentication systems used across the technology industry.

---

### 🔐 Remember

> **Never store passwords. Store password hashes.**
>
> **Never trust passwords. Verify them securely.**
>
> **Security starts with proper credential protection.**

---
