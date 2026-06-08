# 🔍 Plugin-Driven Log Analysis Engine

> *"Modern security monitoring isn't about reading logs manually—it's about building systems that can detect threats automatically."*

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge\&logo=python)
![Log Analysis](https://img.shields.io/badge/Log-Analysis-green?style=for-the-badge)
![Plugin Architecture](https://img.shields.io/badge/Plugin-Architecture-orange?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Monitoring-red?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Compatible-yellow?style=for-the-badge\&logo=linux)

---

# 📖 Overview

The **Plugin-Driven Log Analysis Engine** is a modular security monitoring framework that analyzes log files using dynamically loaded plugins.

Instead of hardcoding detection logic into a single application, this engine allows new analyzers to be added simply by dropping Python modules into a plugins directory.

This architecture is inspired by enterprise security platforms such as:

* 🔍 Splunk
* 📊 Elastic Stack (ELK)
* 🛡️ OSSEC
* 🚨 Security Information and Event Management (SIEM) Systems
* 📈 Threat Detection Platforms

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Understand plugin architecture design patterns

✅ Implement dynamic module loading in Python

✅ Create reusable security analyzers

✅ Process and analyze log files programmatically

✅ Generate structured security reports

✅ Build modular and scalable security tools

---

# 🛠️ Prerequisites

* Basic Python programming
* Linux command-line knowledge
* Understanding of file operations
* Familiarity with log file formats

---

# ⚙️ Environment Setup

## Step 1: Verify Python Installation

```bash
python3 --version
```

Expected Output:

```text
Python 3.8+
```

---

## Step 2: Create Project Structure

```bash
mkdir -p ~/log-analyzer/{plugins,logs,output}

cd ~/log-analyzer
```

---

## Step 3: Install Required Dependencies

```bash
pip3 install --user colorama
```

---

# 📁 Project Structure

```text
log-analyzer/
│
├── plugin_base.py
├── plugin_loader.py
├── log_analyzer.py
│
├── plugins/
│   ├── failed_login_analyzer.py
│   ├── error_pattern_analyzer.py
│   └── custom_analyzer.py
│
├── logs/
│   └── sample.log
│
└── output/
    └── report.json
```

---

# 🏗️ Task 1: Build the Plugin Architecture

---

# 🔌 Plugin Base Class

All analyzer plugins inherit from a common interface.

Create:

```bash
nano plugin_base.py
```

```python
"""
Base class for all log analyzer plugins.
"""

class PluginBase:

    def __init__(self):
        self.name = "Base Plugin"
        self.description = "Base plugin class"

    def analyze(self, log_line: str) -> dict:
        raise NotImplementedError(
            "Plugins must implement analyze() method"
        )

    def get_info(self) -> dict:
        return {
            'name': self.name,
            'description': self.description
        }
```

---

# 🔐 Failed Login Analyzer Plugin

Detects authentication failures in log files.

Create:

```bash
nano plugins/failed_login_analyzer.py
```

```python
import sys
sys.path.append('..')

from plugin_base import PluginBase
import re

class FailedLoginAnalyzer(PluginBase):

    def __init__(self):
        super().__init__()

        self.name = "Failed Login Analyzer"
        self.description = (
            "Detects failed authentication attempts"
        )

        self.patterns = [
            r'Failed password for .* from ([\d\.]+)',
            r'authentication failure.*rhost=([\d\.]+)',
            r'sudo.*authentication failure'
        ]

    def analyze(self, log_line: str) -> dict:

        for pattern in self.patterns:

            match = re.search(
                pattern,
                log_line,
                re.IGNORECASE
            )

            if match:

                return {
                    'severity': 'HIGH',
                    'message':
                        'Failed login attempt detected',
                    'details': {
                        'pattern_matched': pattern,
                        'log_line': log_line.strip()
                    }
                }

        return None

def get_plugin():
    return FailedLoginAnalyzer()
```

---

# 🚨 Error Pattern Analyzer Plugin

Detects critical errors and exceptions.

Create:

```bash
nano plugins/error_pattern_analyzer.py
```

```python
import sys
sys.path.append('..')

from plugin_base import PluginBase

class ErrorPatternAnalyzer(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "Error Pattern Analyzer"

        self.description = (
            "Detects common error keywords"
        )

        self.error_keywords = [
            'error',
            'critical',
            'fatal',
            'exception'
        ]

    def analyze(self, log_line: str) -> dict:

        log_lower = log_line.lower()

        for keyword in self.error_keywords:

            if keyword in log_lower:

                severity = (
                    'CRITICAL'
                    if keyword in ['critical', 'fatal']
                    else 'MEDIUM'
                )

                return {
                    'severity': severity,
                    'message':
                        f'Error keyword detected: {keyword}',
                    'details': {
                        'keyword': keyword,
                        'log_line': log_line.strip()
                    }
                }

        return None

def get_plugin():
    return ErrorPatternAnalyzer()
```

---

# ⚙️ Dynamic Plugin Loader

Create:

```bash
nano plugin_loader.py
```

```python
import os
import importlib.util

class PluginLoader:

    def __init__(self,
                 plugin_directory='plugins'):

        self.plugin_directory = plugin_directory
        self.plugins = []

    def load_plugins(self):

        if not os.path.exists(
            self.plugin_directory
        ):
            print(
                f"Plugin directory "
                f"'{self.plugin_directory}' not found"
            )
            return 0

        loaded_count = 0

        for filename in os.listdir(
            self.plugin_directory
        ):

            if filename.endswith(
                '_analyzer.py'
            ):

                plugin_path = os.path.join(
                    self.plugin_directory,
                    filename
                )

                try:

                    spec = importlib.util.spec_from_file_location(
                        filename[:-3],
                        plugin_path
                    )

                    module = importlib.util.module_from_spec(
                        spec
                    )

                    spec.loader.exec_module(module)

                    plugin = module.get_plugin()

                    self.plugins.append(plugin)

                    loaded_count += 1

                    print(
                        f"[+] Loaded plugin: "
                        f"{plugin.name}"
                    )

                except Exception as e:

                    print(
                        f"[-] Failed loading "
                        f"{filename}: {e}"
                    )

        return loaded_count

    def get_plugins(self):
        return self.plugins
```

---

# 🚀 Task 2: Build the Log Analysis Engine

---

# 🧠 Main Analysis Engine

Create:

```bash
nano log_analyzer.py
```

```python
from plugin_loader import PluginLoader
from datetime import datetime
import json

class LogAnalyzer:

    def __init__(self):

        self.loader = PluginLoader()
        self.results = []

    def initialize(self):

        print(
            "\n=== Initializing Log Analysis Engine ==="
        )

        count = self.loader.load_plugins()

        print(
            f"\nTotal plugins loaded: {count}\n"
        )

        return count > 0

    def analyze_file(self, log_file):

        print(
            f"[*] Analyzing log file: {log_file}"
        )

        try:

            with open(log_file, 'r') as f:

                line_number = 0

                for line in f:

                    line_number += 1

                    for plugin in self.loader.get_plugins():

                        result = plugin.analyze(line)

                        if result:

                            result['line_number'] = line_number
                            result['plugin'] = plugin.name
                            result['timestamp'] = (
                                datetime.now().isoformat()
                            )

                            self.results.append(result)

            print(
                f"[+] Analysis complete. "
                f"Found {len(self.results)} issues."
            )

        except FileNotFoundError:

            print(
                f"[-] Log file '{log_file}' not found"
            )

    def generate_report(
        self,
        output_file='output/report.json'
    ):

        report = {
            'analysis_date':
                datetime.now().isoformat(),
            'total_findings':
                len(self.results),
            'findings':
                self.results
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(
            f"\n[+] Report saved to: {output_file}"
        )

def main():

    analyzer = LogAnalyzer()

    if not analyzer.initialize():
        return

    analyzer.analyze_file(
        'logs/sample.log'
    )

    analyzer.generate_report()

if __name__ == "__main__":
    main()
```

---

# 📝 Sample Log File

Create:

```bash
nano logs/sample.log
```

```text
2024-01-15 10:23:45 INFO: System startup complete
2024-01-15 10:24:12 WARNING: High memory usage detected
2024-01-15 10:25:33 ERROR: Database connection failed
2024-01-15 10:26:01 Failed password for admin from 192.168.1.100 port 22 ssh2
2024-01-15 10:26:15 INFO: Service restarted successfully
2024-01-15 10:27:42 CRITICAL: Disk space below 5%
2024-01-15 10:28:19 Failed password for root from 10.0.0.50 port 22 ssh2
2024-01-15 10:29:05 authentication failure; rhost=172.16.0.25
2024-01-15 10:30:11 INFO: Backup completed
2024-01-15 10:31:28 FATAL: Application crashed unexpectedly
2024-01-15 10:32:45 sudo: authentication failure for user john
2024-01-15 10:33:12 ERROR: File not found exception
```

---

# ▶️ Run the Analyzer

```bash
cd ~/log-analyzer

python3 log_analyzer.py
```

---

# ✅ Expected Output

```text
=== Initializing Log Analysis Engine ===

[+] Loaded plugin: Error Pattern Analyzer
[+] Loaded plugin: Failed Login Analyzer

Total plugins loaded: 2

[*] Analyzing log file: logs/sample.log

[+] Analysis complete. Found 8 issues.

[+] Report saved to: output/report.json
```

---

# 📄 Verify the Report

```bash
cat output/report.json
```

Pretty-print JSON:

```bash
python3 -m json.tool output/report.json
```

---

# 🔍 View Findings by Severity

```bash
python3 -m json.tool output/report.json | grep -A 5 severity
```

---

# ➕ Add a Custom Plugin

Create:

```bash
nano plugins/custom_analyzer.py
```

```python
import sys
sys.path.append('..')

from plugin_base import PluginBase

class CustomAnalyzer(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "Custom Analyzer"

        self.description = (
            "Detects WARNING keywords"
        )

    def analyze(self, log_line: str):

        if 'WARNING' in log_line:

            return {
                'severity': 'LOW',
                'message':
                    'Warning detected',
                'details': {
                    'log_line':
                        log_line.strip()
                }
            }

        return None

def get_plugin():
    return CustomAnalyzer()
```

Run again:

```bash
python3 log_analyzer.py
```

The engine automatically discovers and loads the new analyzer.

---

# 🔬 Architecture Flow

```text
             Log File
                 │
                 ▼
      ┌────────────────────┐
      │  Log Analyzer      │
      └─────────┬──────────┘
                │
                ▼
      ┌────────────────────┐
      │  Plugin Loader     │
      └─────────┬──────────┘
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
 Failed     Error     Custom
 Login     Pattern    Plugin
 Plugin     Plugin
      │         │         │
      └─────────┼─────────┘
                ▼
      Security Findings
                ▼
         JSON Report
```

---

# 🧪 Verification Checklist

### Verify Plugins

```bash
ls plugins/
```

Expected:

```text
failed_login_analyzer.py
error_pattern_analyzer.py
custom_analyzer.py
```

---

### Verify Report Generation

```bash
ls output/
```

Expected:

```text
report.json
```

---

### Verify Findings Count

```bash
python3 -m json.tool output/report.json
```

Check:

```json
{
  "total_findings": 8
}
```

---

# 🚨 Troubleshooting

## Module Not Found

```text
No module named 'plugin_base'
```

Solution:

```bash
pwd
```

Ensure you are inside:

```text
~/log-analyzer
```

---

## Plugins Not Loading

Verify filenames:

```text
*_analyzer.py
```

Required:

```python
def get_plugin():
```

---

## No Findings

Verify:

```bash
cat logs/sample.log
```

Ensure patterns match plugin logic.

---

## Report Not Generated

Check:

```bash
ls output/
```

Create directory if missing:

```bash
mkdir -p output
```

---

# 🌍 Real-World Applications

This architecture is used in:

| Technology         | Purpose             |
| ------------------ | ------------------- |
| Splunk             | Security Analytics  |
| ELK Stack          | Log Management      |
| OSSEC              | Host-Based IDS      |
| SIEM Platforms     | Threat Detection    |
| SOC Tools          | Security Monitoring |
| Compliance Systems | Audit Monitoring    |

---

# 🎓 Key Takeaways

✅ Plugin architectures enable easy extensibility

✅ Dynamic loading avoids modifying core code

✅ Security detection logic can be modularized

✅ Structured JSON reporting supports automation

✅ Separation of concerns improves maintainability

✅ The same design pattern powers enterprise security platforms

---

# 🚀 Next Steps

Enhance the engine with:

* SQL Injection Detection Plugin
* Port Scan Detection Plugin
* Brute Force Detection Plugin
* Threat Scoring System
* HTML Dashboard
* Real-Time Log Monitoring
* Email Alerting
* SIEM Integration
* Machine Learning-Based Anomaly Detection

---

# 🏁 Conclusion

Congratulations! 🎉

You successfully built a **Plugin-Driven Log Analysis Engine** capable of:

* Dynamically loading analyzer modules
* Processing log files automatically
* Detecting security-relevant patterns
* Generating structured reports
* Supporting unlimited future plugins

This modular design pattern is widely used in professional security monitoring solutions and forms the foundation of scalable threat detection systems.
