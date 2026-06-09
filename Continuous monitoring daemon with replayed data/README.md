# 🔄 Continuous Monitoring Daemon with Replayed Data

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge\&logo=linux)
![Monitoring](https://img.shields.io/badge/Monitoring-Real_Time-green?style=for-the-badge)
![Daemon](https://img.shields.io/badge/Daemon-Background_Service-red?style=for-the-badge)
![Logs](https://img.shields.io/badge/Log-Analysis-purple?style=for-the-badge)
![Automation](https://img.shields.io/badge/Automation-Python-black?style=for-the-badge)

### 🚀 Build a Continuous Monitoring Service Using Historical Log Replay

</div>

---

# 📖 Overview

This project demonstrates how monitoring daemons work by replaying historical log data and processing it as if it were being generated in real time.

The monitoring daemon continuously:

✅ Reads log entries

✅ Parses log events

✅ Detects critical conditions

✅ Generates alerts

✅ Stores alerts for later analysis

✅ Produces monitoring statistics

This lab simulates functionality commonly found in:

* Security Information and Event Management (SIEM)
* Infrastructure Monitoring Systems
* Application Monitoring Platforms
* Security Operations Centers (SOC)

---

# 🎯 Learning Objectives

By completing this lab, you will:

* Understand daemon processes
* Learn background execution techniques
* Simulate real-time monitoring
* Parse log entries
* Detect critical events
* Generate alerts automatically
* Analyze monitoring statistics
* Build continuous monitoring workflows

---

# 📋 Prerequisites

Before beginning:

* Basic Linux command-line knowledge
* Understanding of file operations
* Familiarity with nano or vi
* Basic understanding of processes
* Basic Python knowledge

---

# 🏗️ Monitoring Architecture

```text
Historical Log File
         │
         ▼
 ┌─────────────────┐
 │ Monitoring      │
 │ Daemon          │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Log Parser      │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Alert Detection │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Alert Generator │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ alerts.log      │
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │ Statistics      │
 │ Analysis        │
 └─────────────────┘
```

---

# 📂 Project Structure

```text
monitoring-lab/
│
├── logs/
│   └── access.log
│
├── output/
│   ├── alerts.log
│   ├── daemon.log
│   └── daemon.pid
│
├── monitor_daemon.py
├── analyze_alerts.py
│
└── README.md
```

---

# ⚙️ Environment Setup

## 🟢 Step 1: Update Package Repository

```bash
sudo apt update
```

---

## 🟢 Step 2: Install Python

```bash
sudo apt install -y python3 python3-pip
```

---

## 🟢 Step 3: Verify Installation

```bash
python3 --version
```

---

## 🟢 Step 4: Create Lab Directory

```bash
mkdir -p ~/monitoring-lab

cd ~/monitoring-lab
```

---

## 🟢 Step 5: Create Directories

```bash
mkdir logs output
```

---

# 📄 Sample Log Data

Create:

```text
logs/access.log
```

```log
2024-01-15 10:23:45 INFO User login successful - user: alice
2024-01-15 10:24:12 INFO Page accessed - /dashboard
2024-01-15 10:25:33 WARNING High memory usage - 85%
2024-01-15 10:26:01 INFO User login successful - user: bob
2024-01-15 10:27:15 ERROR Database connection failed
2024-01-15 10:28:22 INFO Page accessed - /reports
2024-01-15 10:29:45 WARNING Disk space low - 90%
2024-01-15 10:30:11 ERROR Authentication failed - user: charlie
2024-01-15 10:31:28 INFO User logout - user: alice
2024-01-15 10:32:50 CRITICAL System overload detected
2024-01-15 10:33:15 INFO Page accessed - /settings
2024-01-15 10:34:42 WARNING CPU usage high - 92%
2024-01-15 10:35:19 ERROR File not found - /data/report.pdf
2024-01-15 10:36:33 INFO User login successful - user: david
2024-01-15 10:37:55 CRITICAL Security breach attempt detected
```

---

# 🚀 monitor_daemon.py

```python
#!/usr/bin/env python3

"""
Continuous Monitoring Daemon
Replays log data and monitors for critical events
"""

import time
import sys
from datetime import datetime


class LogMonitor:

    def __init__(
        self,
        log_file,
        output_file,
        replay_speed=1.0
    ):
        self.log_file = log_file
        self.output_file = output_file
        self.replay_speed = replay_speed
        self.alert_count = 0

    def parse_log_line(self, line):

        parts = line.strip().split(' ', 3)

        if len(parts) < 4:
            return None

        return {
            'date': parts[0],
            'time': parts[1],
            'level': parts[2],
            'message': parts[3]
        }

    def check_alert_conditions(
        self,
        log_entry
    ):

        level = log_entry.get(
            'level',
            ''
        )

        return level in [
            'ERROR',
            'CRITICAL'
        ]

    def write_alert(
        self,
        log_entry
    ):

        timestamp = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        alert_msg = (
            f"[ALERT {timestamp}] "
            f"{log_entry['level']}: "
            f"{log_entry['message']}\n"
        )

        with open(
            self.output_file,
            'a'
        ) as f:
            f.write(alert_msg)

        self.alert_count += 1

        print(
            f"ALERT: "
            f"{log_entry['level']} - "
            f"{log_entry['message']}"
        )

    def run(self):

        print("Starting monitoring daemon...")
        print(f"Reading from: {self.log_file}")
        print(f"Writing alerts to: {self.output_file}")
        print(f"Replay speed: {self.replay_speed}x")

        print("-" * 60)

        try:

            with open(
                self.log_file,
                'r'
            ) as f:
                lines = f.readlines()

            for line in lines:

                log_entry = self.parse_log_line(
                    line
                )

                if log_entry is None:
                    continue

                print(
                    f"[{log_entry['date']} "
                    f"{log_entry['time']}] "
                    f"{log_entry['level']}: "
                    f"{log_entry['message']}"
                )

                if self.check_alert_conditions(
                    log_entry
                ):
                    self.write_alert(
                        log_entry
                    )

                time.sleep(
                    0.5 / self.replay_speed
                )

            print("-" * 60)

            print(
                f"Monitoring complete. "
                f"Total alerts: {self.alert_count}"
            )

        except FileNotFoundError:

            print(
                f"ERROR: Log file not found: "
                f"{self.log_file}"
            )

            sys.exit(1)

        except KeyboardInterrupt:

            print(
                "\nMonitoring stopped by user"
            )

            print(
                f"Total alerts generated: "
                f"{self.alert_count}"
            )

            sys.exit(0)


def main():

    log_file = "logs/access.log"

    output_file = "output/alerts.log"

    replay_speed = 2.0

    monitor = LogMonitor(
        log_file,
        output_file,
        replay_speed
    )

    monitor.run()


if __name__ == "__main__":
    main()
```

---

# 📊 analyze_alerts.py

```python
#!/usr/bin/env python3

"""
Analyze alerts generated by monitoring daemon
"""


def analyze_alerts(
    alert_file
):

    try:

        with open(
            alert_file,
            'r'
        ) as f:

            lines = f.readlines()

        error_count = 0
        critical_count = 0

        for line in lines:

            if 'ERROR:' in line:
                error_count += 1

            elif 'CRITICAL:' in line:
                critical_count += 1

        print("=" * 50)
        print("ALERT STATISTICS")
        print("=" * 50)

        print(
            f"Total Alerts: "
            f"{len(lines)}"
        )

        print(
            f"ERROR Alerts: "
            f"{error_count}"
        )

        print(
            f"CRITICAL Alerts: "
            f"{critical_count}"
        )

        print("=" * 50)

    except FileNotFoundError:

        print(
            f"Alert file not found: "
            f"{alert_file}"
        )


if __name__ == "__main__":

    analyze_alerts(
        "output/alerts.log"
    )
```

---

# ▶️ Running the Monitoring Daemon

## Foreground Mode

```bash
chmod +x monitor_daemon.py

python3 monitor_daemon.py
```

---

## Background Daemon Mode

```bash
nohup python3 monitor_daemon.py > output/daemon.log 2>&1 &
```

Save Process ID:

```bash
echo $! > output/daemon.pid
```

---

# 🔍 Check Daemon Status

View running process:

```bash
ps aux | grep monitor_daemon.py
```

Monitor daemon output:

```bash
tail -f output/daemon.log
```

Press:

```text
Ctrl + C
```

to stop viewing logs.

---

# 🚨 View Generated Alerts

```bash
cat output/alerts.log
```

Count alerts:

```bash
wc -l output/alerts.log
```

Expected:

```text
5 alerts
```

* 3 ERROR
* 2 CRITICAL

---

# 📈 Analyze Alert Statistics

```bash
chmod +x analyze_alerts.py

python3 analyze_alerts.py
```

Expected Output:

```text
==================================================
ALERT STATISTICS
==================================================
Total Alerts: 5
ERROR Alerts: 3
CRITICAL Alerts: 2
==================================================
```

---

# ✅ Verification Checklist

## Check 1

```bash
ls -lh logs/access.log
```

Expected:

```text
15 log entries
```

---

## Check 2

```bash
test -f output/alerts.log && echo "SUCCESS" || echo "FAIL"
```

---

## Check 3

```bash
wc -l output/alerts.log
```

Expected:

```text
5
```

---

## Check 4

Stop daemon:

```bash
if [ -f output/daemon.pid ]; then
    kill $(cat output/daemon.pid)
fi
```

---

# 🛠 Troubleshooting

## Permission Denied

```bash
chmod +x monitor_daemon.py
```

---

## Log File Not Found

```bash
ls logs/access.log
```

---

## No Alerts Generated

Verify:

```bash
mkdir -p output
```

Check alert condition:

```python
return level in ['ERROR', 'CRITICAL']
```

---

## Force Kill Daemon

Find PID:

```bash
ps aux | grep monitor_daemon.py
```

Kill:

```bash
kill -9 PID
```

---

# 🎓 Skills Acquired

✅ Continuous Monitoring

✅ Daemon Processes

✅ Background Services

✅ Log Replay Simulation

✅ Log Parsing

✅ Alert Generation

✅ Statistics Analysis

✅ Process Management

✅ Linux Monitoring

✅ Python Automation

---

# 🏆 Conclusion

Congratulations! You have successfully built a Continuous Monitoring Daemon that replays historical logs, detects critical events, generates alerts, runs as a background service, and produces monitoring statistics.

These concepts are widely used in:

* SIEM Platforms
* SOC Monitoring
* Cloud Operations
* Infrastructure Monitoring
* Incident Response Systems
* Application Performance Monitoring

This project provides a solid foundation for building enterprise-grade monitoring and cybersecurity automation solutions.

### ⭐ Happy Monitoring & Threat Hunting! 🚀🔍
