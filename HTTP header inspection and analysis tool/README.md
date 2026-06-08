# 🌐 HTTP Header Inspection and Analysis Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/HTTP-Headers-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Web-Security-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Security-Audit-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/Cybersecurity-Header_Analysis-black?style=for-the-badge" />
</p>

---

# 📖 Overview

HTTP Security Headers provide an essential layer of defense for web applications. They help protect websites against common attacks such as:

* 🛡️ Cross-Site Scripting (XSS)
* 🖼️ Clickjacking
* 🔒 Protocol Downgrade Attacks
* 🕵️ MIME-Type Sniffing
* 📡 Information Leakage

In this lab, you will build a Python-based **HTTP Header Inspection and Analysis Tool** capable of:

* Extracting HTTP response headers
* Identifying missing security headers
* Detecting insecure configurations
* Generating security analysis reports

This project simulates a simplified security auditing tool used during penetration testing and web application assessments.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Extract HTTP headers from web servers

✅ Parse and analyze header information

✅ Detect missing security headers

✅ Identify insecure configurations

✅ Generate security assessment reports

✅ Understand HTTP security best practices

---

# 📋 Prerequisites

Before starting, ensure you have:

* Basic Understanding of HTTP Protocol
* Linux Command Line Knowledge
* Familiarity with Nano or Vim
* Basic Python Knowledge
* Understanding of Web Security Concepts

---

# 🛠️ Environment Setup

---

## 🚀 Install Required Tools

Update Package Manager:

```bash
sudo apt update
```

Install Python:

```bash
sudo apt install python3 python3-pip -y
```

Install Required Libraries:

```bash
pip3 install requests colorama
```

---

## ✅ Verify Installation

Check Python Version:

```bash
python3 --version
```

Verify Requests Library:

```bash
python3 -c "import requests; print('Requests library installed successfully')"
```

Expected Output:

```text
Requests library installed successfully
```

---

# 📂 Task 1 — Build HTTP Header Extraction Tool

---

## 📁 Step 1: Create Project Directory

```bash
mkdir ~/http-header-analyzer
cd ~/http-header-analyzer

touch header_analyzer.py
chmod +x header_analyzer.py
```

Verify:

```bash
ls -la
```

Expected:

```text
header_analyzer.py
```

---

## 📝 Step 2: Create Main Script

Open the file:

```bash
nano header_analyzer.py
```

Paste the starter code provided in the lab instructions.

---

## 🔍 Implement Header Extraction

Inside the `fetch_headers()` function:

```python
response = requests.get(
    url,
    timeout=10,
    allow_redirects=True
)

return response.headers
```

---

## 📋 Implement Header Display Function

Example:

```python
for header, value in headers.items():
    print(f"{header}: {value}")
```

Expected Output:

```text
Content-Type: text/html
Server: nginx
X-Content-Type-Options: nosniff
```

---

# 🛡️ Task 2 — Implement Security Header Analysis

---

## 🔒 Critical Security Headers

The analyzer checks for the following important security headers:

| Header                    | Purpose                      |
| ------------------------- | ---------------------------- |
| Strict-Transport-Security | Enforce HTTPS                |
| X-Frame-Options           | Prevent Clickjacking         |
| X-Content-Type-Options    | Prevent MIME Sniffing        |
| Content-Security-Policy   | Restrict Resource Loading    |
| X-XSS-Protection          | Browser XSS Filtering        |
| Referrer-Policy           | Referrer Privacy             |
| Permissions-Policy        | Browser Feature Restrictions |

---

## ⚠️ Insecure Header Values

The tool flags dangerous values such as:

### X-Frame-Options

Unsafe:

```http
X-Frame-Options: ALLOW
```

---

### X-XSS-Protection

Unsafe:

```http
X-XSS-Protection: 0
```

---

### HSTS Configuration

Unsafe:

```http
Strict-Transport-Security: max-age=300
```

Short expiration periods reduce protection effectiveness.

---

## 🔎 Implement Security Analysis Function

The analyzer should:

### Check Missing Headers

Example:

```python
for header in SECURITY_HEADERS:
    if header not in headers:
        missing.append(header)
```

---

### Check Insecure Values

Example:

```python
if headers.get('X-XSS-Protection') == '0':
    insecure.append('X-XSS-Protection disabled')
```

---

# 📊 Generate Security Reports

---

## Missing Security Headers

Example Output:

```text
Missing Security Headers (5)

- Strict-Transport-Security
- X-Frame-Options
- Content-Security-Policy
- Referrer-Policy
- Permissions-Policy
```

---

## Insecure Configurations

Example Output:

```text
Insecure Configurations Found (2)

- X-XSS-Protection disabled
- HSTS max-age too low
```

---

# ⚙️ Main Function Workflow

The application should:

### Step 1

Receive URL from command line

```bash
python3 header_analyzer.py github.com
```

---

### Step 2

Normalize URL

```python
if not url.startswith(('http://', 'https://')):
    url = 'https://' + url
```

---

### Step 3

Fetch Headers

```python
headers = fetch_headers(url)
```

---

### Step 4

Display Headers

```python
display_headers(headers)
```

---

### Step 5

Analyze Security

```python
missing, insecure = analyze_security_headers(headers)
```

---

### Step 6

Generate Report

```python
display_security_report(missing, insecure)
```

---

# 🧪 Testing the Tool

---

## Test Example.com

```bash
python3 header_analyzer.py https://example.com
```

---

## Test GitHub

```bash
python3 header_analyzer.py github.com
```

---

## Test Google

```bash
python3 header_analyzer.py https://www.google.com
```

---

# 📊 Sample Output

```text
Analyzing: https://example.com

==================================================
HTTP HEADERS FOUND
==================================================

Content-Type: text/html
Server: nginx
X-Content-Type-Options: nosniff

==================================================
SECURITY ANALYSIS REPORT
==================================================

Missing Security Headers (5)

- Strict-Transport-Security
- X-Frame-Options
- Content-Security-Policy
- Referrer-Policy
- Permissions-Policy

No insecure configurations detected!
```

---

# 🧪 Optional Test Server

Create:

```bash
nano test_server.py
```

Paste:

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header(
            'X-Content-Type-Options',
            'nosniff'
        )
        super().end_headers()

HTTPServer(
    ('', 8000),
    CustomHandler
).serve_forever()
```

---

## Run Test Server

```bash
python3 test_server.py
```

---

## Test Local Server

```bash
python3 header_analyzer.py http://localhost:8000
```

Expected:

Many missing security headers detected.

---

# ✅ Verification

---

## Verify Header Extraction

```bash
python3 header_analyzer.py https://www.google.com
```

Expected:

* Header list displayed
* Security report generated

---

## Verify Missing Header Detection

Test:

```bash
python3 header_analyzer.py http://localhost:8000
```

Expected:

5–6 missing headers identified.

---

## Verify Color-Coded Output

### 🟢 Green

Healthy Configurations

### 🔴 Red

Security Issues

### 🟡 Yellow

Report Sections

---

# 🎯 Expected Outcomes

After completing this lab, you should have:

✅ Working Header Extraction Tool

✅ Automated Security Header Analysis

✅ Security Audit Reporting

✅ Better Understanding of Web Security

✅ Practical HTTP Header Assessment Skills

---

# 🛠️ Troubleshooting

---

## ❌ Module Not Found

Install Dependencies:

```bash
pip3 install --user requests colorama
```

---

## ❌ Connection Timeout

Increase Timeout:

```python
requests.get(
    url,
    timeout=30
)
```

---

## ❌ SSL Certificate Errors

Testing Only:

```python
requests.get(
    url,
    verify=False
)
```

⚠️ Never disable SSL verification in production.

---

## ❌ Permission Denied

Make Script Executable:

```bash
chmod +x header_analyzer.py
```

---

# 🔐 Common Security Headers Explained

---

## Strict-Transport-Security (HSTS)

Protects against:

* Protocol Downgrade Attacks
* SSL Stripping

Example:

```http
Strict-Transport-Security: max-age=31536000
```

---

## Content-Security-Policy (CSP)

Protects against:

* XSS Attacks
* Malicious Resource Injection

Example:

```http
Content-Security-Policy: default-src 'self'
```

---

## X-Frame-Options

Protects against:

* Clickjacking

Example:

```http
X-Frame-Options: DENY
```

---

## X-Content-Type-Options

Protects against:

* MIME Sniffing

Example:

```http
X-Content-Type-Options: nosniff
```

---

# 🌍 Real-World Significance

Security teams use header analysis tools during:

* 🔎 Vulnerability Assessments
* 🛡️ Security Audits
* ☁️ Cloud Security Reviews
* 🧪 Penetration Testing
* 📋 Compliance Checks

Regular security header validation helps reduce attack surface and improve overall application security.

---

# 🚀 Key Takeaways

✔️ HTTP Security Headers provide critical protection layers

✔️ Missing headers expose applications to common attacks

✔️ Automated analysis improves security auditing efficiency

✔️ Regular header reviews should be part of DevSecOps practices

✔️ Security headers complement, not replace, secure coding practices

---

# 🏆 Lab Complete

Congratulations! 🎉

You successfully built an **HTTP Header Inspection and Analysis Tool** capable of:

✅ Extracting HTTP Response Headers

✅ Detecting Missing Security Headers

✅ Identifying Insecure Configurations

✅ Producing Actionable Security Reports

These skills are fundamental for cybersecurity professionals performing web application security assessments and compliance reviews.

**Happy Security Testing! 🔐🌐🚀**
