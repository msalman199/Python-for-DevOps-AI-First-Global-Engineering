# 🌐 IP Address and Hostname Validator Lab

## 📋 Prerequisites
* Basic understanding of Linux command line
* Familiarity with text editors (`nano` or `vi`)
* Basic knowledge of IP addresses and hostnames
* Python 3.x installed (will verify during setup)

---

## 🎯 Learning Objectives
By completing this lab, you will:
* Understand IPv4 and IPv6 address formats
* Learn hostname validation rules
* Implement validation logic using Python
* Detect malformed network identifiers
* Use regular expressions for pattern matching

---

## ⚙️ Environment Setup

### 🧰 Step 1: Verify Python Installation
```bash
python3 --version
```
If Python is not installed, run:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### 🗂️ Step 2: Create Lab Directory
```bash
mkdir ~/ip-validator-lab
cd ~/ip-validator-lab
```

### 📦 Step 3: Install Required Python Module
```bash
pip3 install ipaddress
```

---

## 🛠️ Task 1: Build an IPv4 Validator

### 📖 Understanding IPv4 Format
IPv4 addresses consist of four octets (0-255) separated by dots.
* **Valid:** `192.168.1.1`, `10.0.0.1`
* **Invalid:** `256.1.1.1`, `192.168.1`, `192.168.1.1.1`

### 📝 Step 1: Create the IPv4 Validator Script
```bash
nano ipv4_validator.py
```
Add the following code template:
```python
#!/usr/bin/env python3
"""
IPv4 Address Validator
Validates IPv4 addresses using basic parsing logic
"""

def validate_ipv4(ip_address):
    """
    Validate an IPv4 address.
    
    Args:
        ip_address (str): The IP address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # TODO: Split the IP address by '.' into parts
    # Hint: Use ip_address.split('.')
    parts = None
    
    # TODO: Check if there are exactly 4 parts
    # Hint: Use len(parts)
    
    # TODO: Loop through each part and check:
    # 1. Each part is a digit
    # 2. Each part is between 0 and 255
    # Hint: Use part.isdigit() and int(part)
    
    return False  # Replace with your validation logic


def test_ipv4_addresses():
    """Test the IPv4 validator with sample addresses"""
    test_cases = [
        ("192.168.1.1", True),
        ("10.0.0.1", True),
        ("256.1.1.1", False),
        ("192.168.1", False),
        ("192.168.1.1.1", False),
        ("192.168.-1.1", False),
        ("192.168.1.a", False)
    ]
    
    print("IPv4 Validation Tests:")
    print("-" * 50)
    
    for ip, expected in test_cases:
        result = validate_ipv4(ip)
        status = "PASS" if result == expected else "FAIL"
        print(f"{ip:20} | Expected: {expected:5} | Got: {result:5} | {status}")


if __name__ == "__main__":
    test_ipv4_addresses()
```

### ⚙️ Step 2: Complete the IPv4 Validator
Edit the `validate_ipv4` function to implement the final validation logic:
```python
def validate_ipv4(ip_address):
    """
    Validate an IPv4 address.
    
    Args:
        ip_address (str): The IP address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Split the IP address into parts
    parts = ip_address.split('.')
    
    # Check if there are exactly 4 parts
    if len(parts) != 4:
        return False
    
    # Validate each part
    for part in parts:
        # Check if part is a digit
        if not part.isdigit():
            return False
        
        # Convert to integer and check range
        num = int(part)
        if num < 0 or num > 255:
            return False
    
    return True
```

### 🧪 Step 3: Test IPv4 Validator
```bash
python3 ipv4_validator.py
```
*Expected output shows PASS for all test cases.*

---

## 🛠️ Task 2: Build an IPv6 Validator

### 📖 Understanding IPv6 Format
IPv6 addresses consist of eight groups of four hexadecimal digits separated by colons.
* **Valid:** `2001:0db8:85a3:0000:0000:8a2e:0370:7334`, `2001:db8::1`
* **Invalid:** `2001:0db8:85a3::8a2e::7334`, `gggg::`

### 📝 Step 1: Create the IPv6 Validator Script
```bash
nano ipv6_validator.py
```
Add the complete code:
```python
#!/usr/bin/env python3
"""
IPv6 Address Validator
Uses Python's ipaddress module for validation
"""

import ipaddress

def validate_ipv6(ip_address):
    """
    Validate an IPv6 address using ipaddress module.
    
    Args:
        ip_address (str): The IPv6 address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Use ipaddress.IPv6Address() to validate
        # Wrap in try-except to catch ValueError
        ipaddress.IPv6Address(ip_address)
        return True
    except ValueError:
        return False


def test_ipv6_addresses():
    """Test the IPv6 validator with sample addresses"""
    test_cases = [
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
        ("2001:db8::1", True),
        ("::1", True),
        ("fe80::1", True),
        ("2001:0db8:85a3::8a2e::7334", False),
        ("gggg::", False),
        ("192.168.1.1", False)
    ]
    
    print("IPv6 Validation Tests:")
    print("-" * 70)
    
    for ip, expected in test_cases:
        result = validate_ipv6(ip)
        status = "PASS" if result == expected else "FAIL"
        print(f"{ip:45} | Expected: {expected:5} | Got: {result:5} | {status}")


if __name__ == "__main__":
    test_ipv6_addresses()
```

### 🧪 Step 2: Test IPv6 Validator
```bash
python3 ipv6_validator.py
```

---

## 🛠️ Task 3: Build a Hostname Validator

### 📖 Understanding Hostname Rules
Valid hostnames must follow these criteria:
* Contain only alphanumeric characters, hyphens, and dots
* Not start or end with a hyphen
* Each label (between dots) must be 1-63 characters long
* Total length must not exceed 253 characters

### 📝 Step 1: Create the Hostname Validator Script
```bash
nano hostname_validator.py
```
Add the complete code:
```python
#!/usr/bin/env python3
"""
Hostname Validator
Validates hostnames according to RFC standards
"""

import re

def validate_hostname(hostname):
    """
    Validate a hostname according to RFC standards.
    
    Args:
        hostname (str): The hostname to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Check total length (max 253 characters)
    if len(hostname) > 253:
        return False
    
    # Check if hostname ends with a dot (allowed but remove it)
    if hostname.endswith('.'):
        hostname = hostname[:-1]
    
    # Split hostname into labels by '.'
    labels = hostname.split('.')
    
    # Validate each label:
    # 1. Length between 1 and 63 characters
    # 2. Only alphanumeric and hyphens
    # 3. Cannot start or end with hyphen
    # Pattern: ^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$
    
    label_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$')
    
    for label in labels:
        if not label_pattern.match(label):
            return False
    
    return True


def test_hostnames():
    """Test the hostname validator with sample hostnames"""
    test_cases = [
        ("example.com", True),
        ("://example.com", True),
        ("://example.com", True),
        ("://example.com", True),
        ("-invalid.com", False),
        ("invalid-.com", False),
        ("inv@lid.com", False),
        ("a" * 64 + ".com", False),
        ("valid.example.", True)
    ]
    
    print("Hostname Validation Tests:")
    print("-" * 60)
    
    for hostname, expected in test_cases:
        result = validate_hostname(hostname)
        status = "PASS" if result == expected else "FAIL"
        print(f"{hostname:30} | Expected: {expected:5} | Got: {result:5} | {status}")


if __name__ == "__main__":
    test_hostnames()
```

### 🧪 Step 2: Test Hostname Validator
```bash
python3 hostname_validator.py
```

---

## 🛠️ Task 4: Create a Combined Network Identifier Validator

### 📝 Step 1: Create the Combined Validator
```bash
nano network_validator.py
```
Add the completed combined validation engine:
```python
#!/usr/bin/env python3
"""
Combined Network Identifier Validator
Detects and validates IPv4, IPv6, and hostnames
"""

import ipaddress
import re

def validate_hostname(hostname):
    """Helper to validate hostname structure."""
    if len(hostname) > 253:
        return False
    if hostname.endswith('.'):
        hostname = hostname[:-1]
    labels = hostname.split('.')
    label_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$')
    for label in labels:
        if not label_pattern.match(label):
            return False
    return True

def detect_and_validate(identifier):
    """
    Detect the type of network identifier and validate it.
    
    Args:
        identifier (str): The network identifier to validate
    
    Returns:
        tuple: (type, is_valid) where type is 'IPv4', 'IPv6', 'Hostname', or 'Unknown'
    """
    # Try IPv4 detection
    if '.' in identifier and ':' not in identifier:
        # Simple character check to distinguish from general hostname domains
        if any(c.isalpha() for c in identifier):
            if validate_hostname(identifier):
                return ('Hostname', True)
            return ('Hostname', False)
        
        try:
            ipaddress.IPv4Address(identifier)
            return ('IPv4', True)
        except ValueError:
