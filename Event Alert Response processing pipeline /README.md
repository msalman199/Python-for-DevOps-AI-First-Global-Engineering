# 🔔 Event Alert Response Processing Pipeline

> *Build a rule-based security monitoring pipeline that processes events, detects threats, generates alerts, and executes automated responses.*

---

## 📌 Overview

The **Event Alert Response Processing Pipeline** is a lightweight Security Information and Event Management (SIEM)-style project that monitors security logs, applies detection rules, generates alerts, and performs automated response actions.

This lab demonstrates how cybersecurity teams automate threat detection and incident response using event-driven architectures.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Build an event-driven security workflow

✅ Process security events from log files

✅ Apply rule-based threat detection logic

✅ Generate security alerts automatically

✅ Execute automated response actions

✅ Understand SIEM and incident response fundamentals

---

# 🛠 Prerequisites

* Linux Command Line Basics
* Python 3.x Fundamentals
* File Operations
* YAML Configuration Files
* Basic Security Concepts
* Understanding of Logs & Alerts

---

# 🏗 Environment Setup

## Step 1: Update System

```bash
sudo apt update
```

---

## Step 2: Install Python & Pip

```bash
sudo apt install -y python3 python3-pip
```

---

## Step 3: Install Required Libraries

```bash
pip3 install pyyaml watchdog
```

---

## Step 4: Create Lab Workspace

```bash
mkdir -p ~/security-pipeline
cd ~/security-pipeline
```

---

# 📂 Project Structure

```text
security-pipeline/
│
├── logs/
│   └── security_events.log
│
├── rules/
│   └── security_rules.yaml
│
├── alerts/
│
├── responses/
│
├── event_processor.py
│
└── generate_events.py
```

---

# 🚀 Task 1: Create Event Processing Components

## Step 1: Create Required Directories

```bash
mkdir -p logs rules alerts responses
touch logs/security_events.log
```

---

# 📜 Step 2: Create Security Rules

Create:

```bash
nano rules/security_rules.yaml
```

Add:

```yaml
rules:
  - id: 1
    name: "Failed Login Attempts"
    pattern: "FAILED_LOGIN"
    threshold: 3
    severity: "HIGH"
    response: "block_ip"

  - id: 2
    name: "Suspicious File Access"
    pattern: "UNAUTHORIZED_ACCESS"
    threshold: 1
    severity: "CRITICAL"
    response: "alert_admin"

  - id: 3
    name: "Port Scan Detected"
    pattern: "PORT_SCAN"
    threshold: 5
    severity: "MEDIUM"
    response: "log_only"
```

Save and exit.

---

# ⚙️ Step 3: Create Event Processor

Create:

```bash
nano event_processor.py
```

---

## Complete Event Processor Source Code

```python
#!/usr/bin/env python3

import yaml
import json
import time
from datetime import datetime
from collections import defaultdict


class EventProcessor:
    def __init__(self, rules_file):
        self.rules = self.load_rules(rules_file)
        self.event_counter = defaultdict(lambda: defaultdict(int))

    def load_rules(self, rules_file):
        with open(rules_file, 'r') as f:
            data = yaml.safe_load(f)
            return data['rules']

    def parse_event(self, log_line):
        try:
            parts = log_line.strip().split('|')

            if len(parts) >= 4:
                return {
                    'timestamp': parts[0].strip(),
                    'source_ip': parts[1].strip(),
                    'event_type': parts[2].strip(),
                    'details': parts[3].strip()
                }

        except Exception as e:
            print(f"Error parsing event: {e}")

        return None

    def check_rules(self, event):
        triggered = []

        for rule in self.rules:
            if rule['pattern'] in event['event_type']:

                key = f"{event['source_ip']}_{rule['id']}"

                self.event_counter[key]['count'] += 1

                if self.event_counter[key]['count'] >= rule['threshold']:
                    triggered.append(rule)

        return triggered

    def generate_alert(self, event, rule):

        alert = {
            'alert_time': datetime.now().isoformat(),
            'rule_id': rule['id'],
            'rule_name': rule['name'],
            'severity': rule['severity'],
            'source_ip': event['source_ip'],
            'event_type': event['event_type'],
            'details': event['details']
        }

        filename = f"alerts/alert_{rule['id']}_{int(time.time())}.json"

        with open(filename, 'w') as f:
            json.dump(alert, f, indent=2)

        print(
            f"[ALERT] {rule['severity']} - {rule['name']} from {event['source_ip']}"
        )

    def execute_response(self, event, rule):

        response_action = rule['response']

        response_log = {
            'timestamp': datetime.now().isoformat(),
            'action': response_action,
            'source_ip': event['source_ip'],
            'rule_id': rule['id']
        }

        filename = f"responses/response_{int(time.time())}.json"

        with open(filename, 'w') as f:
            json.dump(response_log, f, indent=2)

        if response_action == 'block_ip':
            print(f"[RESPONSE] Blocking IP: {event['source_ip']}")

        elif response_action == 'alert_admin':
            print(
                f"[RESPONSE] Alerting administrator about {event['source_ip']}"
            )

        elif response_action == 'log_only':
            print(
                f"[RESPONSE] Logging event from {event['source_ip']}"
            )

    def process_event(self, log_line):

        event = self.parse_event(log_line)

        if not event:
            return

        triggered_rules = self.check_rules(event)

        for rule in triggered_rules:
            self.generate_alert(event, rule)
            self.execute_response(event, rule)


def main():

    print("=== Security Event Processing Pipeline ===")
    print("Initializing processor...")

    processor = EventProcessor(
        'rules/security_rules.yaml'
    )

    print("Monitoring logs/security_events.log for events...")
    print("Press Ctrl+C to stop\n")

    try:

        with open('logs/security_events.log', 'r') as f:

            for line in f:
                if line.strip():
                    processor.process_event(line)

            while True:

                line = f.readline()

                if line:
                    processor.process_event(line)
                else:
                    time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down processor...")

    except FileNotFoundError:
        print("Log file not found!")


if __name__ == "__main__":
    main()
```

---

# 🎲 Step 4: Create Security Event Generator

Create:

```bash
nano generate_events.py
```

---

## Complete Event Generator Source Code

```python
#!/usr/bin/env python3

import time
from datetime import datetime


def generate_event(event_type, source_ip, details):

    timestamp = datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    return (
        f"{timestamp} | "
        f"{source_ip} | "
        f"{event_type} | "
        f"{details}\n"
    )


def main():

    events = [
        ("FAILED_LOGIN", "192.168.1.100", "User: admin"),
        ("FAILED_LOGIN", "192.168.1.100", "User: root"),
        ("FAILED_LOGIN", "192.168.1.100", "User: admin"),
        ("UNAUTHORIZED_ACCESS", "10.0.0.50", "File: /etc/shadow"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 22,80,443"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 8080,8443"),
        ("NORMAL_LOGIN", "192.168.1.10", "User: john"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 21,23,25"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 3389,5900"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 1433,5432")
    ]

    print("Generating security events...")

    with open(
        'logs/security_events.log',
        'a'
    ) as f:

        for event_type, ip, details in events:

            log_entry = generate_event(
                event_type,
                ip,
                details
            )

            f.write(log_entry)

            print(
                f"Generated: {event_type} from {ip}"
            )

            time.sleep(1)

    print("\nEvent generation complete!")


if __name__ == "__main__":
    main()
```

---

# 🧪 Task 2: Run the Pipeline

## Make Scripts Executable

```bash
chmod +x event_processor.py generate_events.py
```

---

## Terminal 1: Start Event Processor

```bash
python3 event_processor.py
```

Expected:

```text
=== Security Event Processing Pipeline ===
Initializing processor...
Monitoring logs/security_events.log for events...
Press Ctrl+C to stop
```

---

## Terminal 2: Generate Events

```bash
python3 generate_events.py
```

---

# 🚨 Expected Alert Output

```text
[ALERT] HIGH - Failed Login Attempts from 192.168.1.100
[RESPONSE] Blocking IP: 192.168.1.100

[ALERT] CRITICAL - Suspicious File Access from 10.0.0.50
[RESPONSE] Alerting administrator about 10.0.0.50

[ALERT] MEDIUM - Port Scan Detected from 172.16.0.25
[RESPONSE] Logging event from 172.16.0.25
```

---

# ✅ Verification

## Check Alerts

```bash
ls -lh alerts/
```

---

## View Alert Content

```bash
cat alerts/alert_*.json
```

---

## Check Responses

```bash
ls -lh responses/
```

---

## View Response Logs

```bash
cat responses/response_*.json
```

---

## Count Processed Events

```bash
wc -l logs/security_events.log
```

---

## View All Events

```bash
cat logs/security_events.log
```

---

# 🔬 Custom Testing

Add a manual failed login event:

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') | 203.0.113.50 | FAILED_LOGIN | User: test" >> logs/security_events.log
```

Run the processor again and verify detection.

---

# 🐞 Troubleshooting

## YAML Module Error

```bash
pip3 install pyyaml
```

---

## Processor Not Detecting Events

Verify:

```bash
ls logs/
```

Ensure:

```text
security_events.log
```

exists.

---

## No Alerts Generated

Verify:

* Event type matches YAML rule pattern
* Threshold has been reached
* Rules file loads successfully

---

## Permission Errors

```bash
chmod +x *.py
```

---

# 📊 Expected Outcomes

After completing this lab, you will have:

✅ A real-time security event processing engine

✅ YAML-based detection rules

✅ Automated alert generation

✅ Automated response execution

✅ Structured JSON alert storage

✅ Understanding of SIEM workflows

---

# 🌍 Real-World Applications

* Security Information and Event Management (SIEM)
* SOC Monitoring Platforms
* Threat Detection Systems
* Incident Response Automation
* Compliance Monitoring
* Security Operations Centers

---

# 🔑 Key Takeaways

* Event-driven systems react to security incidents automatically.
* Detection rules convert raw logs into actionable alerts.
* Automated responses reduce reaction time during attacks.
* YAML provides flexible and maintainable rule configuration.
* Security automation is a core component of modern cybersecurity operations.

---

# 🚀 Next Steps

Enhance the project by adding:

* 📧 Email notifications
* 🗄 Database storage
* 🌐 Web dashboard
* 🔥 Firewall integration
* 📈 Threat scoring
* 🤖 Machine-learning based anomaly detection
* ☁️ Cloud SIEM integration

---

# 🎉 Conclusion

You have successfully built a **Security Event Alert Response Processing Pipeline** capable of:

* Monitoring security events
* Applying threat detection rules
* Generating security alerts
* Executing automated responses
* Producing structured incident records

This project provides a practical introduction to the event processing concepts used by enterprise SIEM and Security Operations Center (SOC) platforms.
