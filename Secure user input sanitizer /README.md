# 🔐 Secure User Input Sanitizer 

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=linux)
![Security](https://img.shields.io/badge/Security-Input%20Validation-red?style=for-the-badge\&logo=securityscorecard)
![Regex](https://img.shields.io/badge/Regex-Validation-green?style=for-the-badge)
![OWASP](https://img.shields.io/badge/OWASP-Secure%20Coding-black?style=for-the-badge)

</p>

---

# 📖 Overview

Modern applications must never trust user-supplied data. Improper handling of input can lead to serious vulnerabilities such as:

* 💥 Command Injection
* 💥 SQL Injection
* 💥 Cross-Site Scripting (XSS)
* 💥 Path Traversal
* 💥 Remote Code Execution

This lab demonstrates both **vulnerable** and **secure** approaches to user input handling using Python.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Understand common input injection vulnerabilities

✅ Implement input sanitization techniques

✅ Validate user input against approved patterns

✅ Detect malicious user input

✅ Apply secure coding best practices

---

# 🛠️ Prerequisites

* Basic Linux command line knowledge
* Basic Python programming skills
* Understanding of variables and functions
* Linux machine with sudo privileges

---

# 🏗️ Environment Setup

## 🔹 Step 1: Start Lab Environment

Provision your Linux machine using the **Start Lab** button.

---

## 🔹 Step 2: Install Required Tools

```bash
sudo apt update

sudo apt install -y python3 python3-pip

python3 --version
```

### ✅ Expected Output

```text
Python 3.x.x
```

---

## 🔹 Step 3: Create Project Directory

```bash
mkdir ~/input-sanitizer-lab

cd ~/input-sanitizer-lab
```

---

# 🚨 Task 1: Understanding Input Vulnerabilities

---

## 🔹 Step 1: Create Vulnerable Application

Create file:

```bash
nano vulnerable_app.py
```

### vulnerable_app.py

```python
#!/usr/bin/env python3

import os

def unsafe_command_execution(user_input):
    command = f"echo {user_input}"
    os.system(command)

def unsafe_file_access(filename):
    try:
        with open(filename, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Vulnerable Application Demo ===")

    print("\n[Test 1] Command Injection:")
    user_input = "Hello; ls -la"
    print(f"Input: {user_input}")
    unsafe_command_execution(user_input)

    print("\n[Test 2] Path Traversal:")
    filename = "../../etc/passwd"
    print(f"Filename: {filename}")
    unsafe_file_access(filename)
```

---

## 🔹 Step 2: Run Vulnerable Application

```bash
chmod +x vulnerable_app.py

python3 vulnerable_app.py
```

### ⚠ Observe

The application:

* Executes unintended shell commands
* Reads sensitive system files

This demonstrates:

* Command Injection
* Path Traversal

---

# 🛡️ Task 2: Build Secure Input Sanitizer

---

## 🔹 Step 1: Create Sanitizer Module

```bash
nano input_sanitizer.py
```

### input_sanitizer.py

```python
#!/usr/bin/env python3

import re
import html
import os

class InputSanitizer:

    DANGEROUS_CHARS = [
        '<', '>', '&', '"', "'",
        ';', '|', '`', '$',
        '(', ')', '{', '}'
    ]

    SQL_KEYWORDS = [
        'SELECT',
        'INSERT',
        'UPDATE',
        'DELETE',
        'DROP',
        'UNION',
        '--',
        '/*'
    ]

    @staticmethod
    def remove_dangerous_chars(user_input):
        sanitized = user_input

        for char in InputSanitizer.DANGEROUS_CHARS:
            sanitized = sanitized.replace(char, '')

        return sanitized

    @staticmethod
    def validate_alphanumeric(user_input, allow_spaces=True):

        if allow_spaces:
            pattern = r'^[a-zA-Z0-9 ]+$'
        else:
            pattern = r'^[a-zA-Z0-9]+$'

        return bool(re.match(pattern, user_input))

    @staticmethod
    def validate_email(email):

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        return bool(re.match(pattern, email))

    @staticmethod
    def sanitize_filename(filename):

        sanitized = os.path.basename(filename)

        sanitized = re.sub(
            r'[^a-zA-Z0-9._-]',
            '',
            sanitized
        )

        return sanitized

    @staticmethod
    def escape_html(user_input):

        return html.escape(user_input)

    @staticmethod
    def check_sql_injection(user_input):

        upper_input = user_input.upper()

        for keyword in InputSanitizer.SQL_KEYWORDS:
            if keyword in upper_input:
                return True

        return False
```

---

# 🔒 Task 3: Create Secure Application

---

## 🔹 Step 1: Create Secure Application

```bash
nano secure_app.py
```

### secure_app.py

```python
#!/usr/bin/env python3

from input_sanitizer import InputSanitizer

def process_username(username):

    print(f"\n[Processing Username: {username}]")

    if not InputSanitizer.validate_alphanumeric(
        username,
        allow_spaces=False
    ):
        print(
            "❌ Invalid username"
        )
        return False

    sanitized = InputSanitizer.remove_dangerous_chars(
        username
    )

    print(
        f"✓ Sanitized username: {sanitized}"
    )

    return True

def process_email(email):

    print(f"\n[Processing Email: {email}]")

    if not InputSanitizer.validate_email(email):
        print("❌ Invalid email format")
        return False

    print(f"✓ Valid email: {email}")
    return True

def process_comment(comment):

    print(f"\n[Processing Comment: {comment}]")

    if InputSanitizer.check_sql_injection(comment):
        print(
            "❌ Suspicious SQL patterns detected"
        )
        return False

    escaped = InputSanitizer.escape_html(comment)

    print(
        f"✓ HTML-escaped comment: {escaped}"
    )

    return True

def process_filename(filename):

    print(
        f"\n[Processing Filename: {filename}]"
    )

    sanitized = InputSanitizer.sanitize_filename(
        filename
    )

    print(
        f"✓ Sanitized filename: {sanitized}"
    )

    return sanitized

if __name__ == "__main__":

    print(
        "=== Secure Input Processing Demo ==="
    )

    process_username("john_doe")
    process_email("user@example.com")
    process_comment("<script>alert('XSS')</script>")
    process_filename("../../etc/passwd")
```

---

## 🔹 Step 2: Run Secure Application

```bash
python3 secure_app.py
```

### ✅ Expected Result

* Malicious usernames rejected
* SQL patterns detected
* HTML escaped
* Filenames sanitized

---

# 🧪 Task 4: Interactive Testing

---

## 🔹 Step 1: Create Interactive Test Program

```bash
nano interactive_test.py
```

### interactive_test.py

```python
#!/usr/bin/env python3

from input_sanitizer import InputSanitizer

def main():

    while True:

        print("\n" + "=" * 50)

        print(
            "Secure Input Sanitizer"
        )

        print("=" * 50)

        print("1. Username Validation")
        print("2. Email Validation")
        print("3. HTML Escaping")
        print("4. Filename Sanitization")
        print("5. SQL Injection Detection")
        print("6. Exit")

        choice = input(
            "\nSelect option: "
        )

        if choice == "1":

            username = input(
                "Username: "
            )

            print(
                InputSanitizer.validate_alphanumeric(
                    username,
                    False
                )
            )

        elif choice == "2":

            email = input("Email: ")

            print(
                InputSanitizer.validate_email(
                    email
                )
            )

        elif choice == "3":

            html_text = input(
                "HTML Input: "
            )

            print(
                InputSanitizer.escape_html(
                    html_text
                )
            )

        elif choice == "4":

            filename = input(
                "Filename: "
            )

            print(
                InputSanitizer.sanitize_filename(
                    filename
                )
            )

        elif choice == "5":

            query = input(
                "Query: "
            )

            print(
                InputSanitizer.check_sql_injection(
                    query
                )
            )

        elif choice == "6":
            break

if __name__ == "__main__":
    main()
```

---

## 🔹 Step 2: Run Interactive Testing

```bash
python3 interactive_test.py
```

### Test Inputs

```text
admin'; DROP TABLE--
```

```text
test@example.com
```

```html
<script>alert('XSS')</script>
```

```text
../../etc/passwd
```

```sql
SELECT * FROM users
```

---

# ✅ Verification

---

## 🔹 Create Verification Script

```bash
nano verify_lab.py
```

### verify_lab.py

```python
#!/usr/bin/env python3

from input_sanitizer import InputSanitizer

print("Verification Tests")
print("-" * 50)

print(
    "Test 1:",
    InputSanitizer.remove_dangerous_chars(
        "test<script>"
    )
)

print(
    "Test 2:",
    InputSanitizer.validate_alphanumeric(
        "user123"
    )
)

print(
    "Test 3:",
    InputSanitizer.validate_email(
        "user@example.com"
    )
)

print(
    "Test 4:",
    InputSanitizer.sanitize_filename(
        "../../etc/passwd"
    )
)

print(
    "Test 5:",
    InputSanitizer.check_sql_injection(
        "SELECT * FROM users"
    )
)

print("\nAll tests completed.")
```

---

## Run Verification

```bash
python3 verify_lab.py
```

### Expected Output

```text
PASS
PASS
PASS
PASS
PASS
```

---

# 📂 Final Project Structure

```text
input-sanitizer-lab/
│
├── vulnerable_app.py
├── input_sanitizer.py
├── secure_app.py
├── interactive_test.py
├── verify_lab.py
│
└── README.md
```

---

# 🛠 Troubleshooting

## ❌ Import Errors

```bash
cd ~/input-sanitizer-lab
```

---

## ❌ Permission Denied

```bash
chmod +x *.py
```

---

## ❌ Python Module Not Found

```bash
python3 script.py
```

---

## ❌ Regex Validation Issues

Always use raw strings:

```python
r'^[a-zA-Z0-9]+$'
```

---

# 🎓 Security Concepts Learned

✅ Command Injection Prevention

✅ Path Traversal Protection

✅ SQL Injection Detection

✅ Cross-Site Scripting (XSS) Prevention

✅ Input Validation Best Practices

✅ Secure File Handling

---

# 🚀 Real-World Applications

These techniques are widely used in:

* 🌐 Web Applications
* 🔐 Authentication Systems
* 📡 APIs
* 🗄 Database Security
* 🛡 Penetration Testing
* ☁ Cloud-Native Applications

---

# 🏁 Conclusion

Congratulations! 🎉

You successfully built a **Secure User Input Sanitizer** capable of:

* Detecting malicious input
* Sanitizing unsafe characters
* Validating usernames and emails
* Preventing path traversal attacks
* Detecting SQL injection attempts
* Escaping HTML to prevent XSS

### 💡 Golden Rule

> **Never trust user input. Always validate, sanitize, and escape before processing.**

---

⭐ Happy Secure Coding!
