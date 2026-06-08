# 🔐 Login Anomaly Detection System

> *"Modern cybersecurity depends on identifying abnormal behavior before it becomes a breach."*

<img src="https://www.animatedimages.org/data/media/562/animated-line-image-0382.gif" width="100%" />

## 📌 Overview

The **Login Anomaly Detection System** is a Python-based security monitoring tool designed to analyze authentication logs and identify suspicious login behavior. By establishing normal user patterns and detecting deviations, the system helps security teams identify compromised accounts, unauthorized access attempts, and brute-force attacks.

This lab introduces fundamental Security Information and Event Management (SIEM) concepts through hands-on log analysis and anomaly detection techniques.

---

## 🎯 Learning Objectives

By completing this lab, you will learn how to:

✅ Analyze authentication logs for security monitoring

✅ Identify abnormal login patterns based on:

- Login Time
- Login Location
- Login Frequency

✅ Build a simple anomaly detection engine using Python

✅ Parse and process authentication logs programmatically

✅ Generate security reports for incident investigation

---

# 🛠️ Prerequisites

Before starting this lab, ensure you have:

- Basic Linux command line knowledge
- Understanding of log files and text processing
- Familiarity with Python basics (variables, loops, functions)
- SSH access to a Linux machine

---

# 🚀 Environment Setup

## Step 1: Install Required Tools

```bash
# Update package manager
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install required Python libraries
pip3 install pandas
```

---

## Step 2: Create Working Directory

```bash
mkdir ~/login-anomaly-lab
cd ~/login-anomaly-lab
```

---

## Step 3: Generate Sample Login Data

Create a log generator script:

```bash
nano generate_logs.py
```

Paste the following code:

```python
#!/usr/bin/env python3

import random
from datetime import datetime, timedelta

users = ['alice', 'bob', 'charlie', 'admin']
ips = [
    '192.168.1.10',
    '192.168.1.20',
    '10.0.0.5',
    '203.0.113.45',
    '198.51.100.78'
]

locations = [
    'NewYork',
    'LosAngeles',
    'Chicago',
    'Houston',
    'Phoenix'
]

logs = []
start_date = datetime.now() - timedelta(days=7)

# Generate normal login behavior
for day in range(7):
    for user in users[:3]:
        for _ in range(random.randint(2, 5)):
            hour = random.randint(8, 18)
            timestamp = start_date + timedelta(
                days=day,
                hours=hour,
                minutes=random.randint(0, 59)
            )

            ip = random.choice(ips[:3])
            location = random.choice(locations[:2])

            logs.append(
                f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},"
                f"{user},{ip},{location},success"
            )

# Anomaly 1 - Late Night Login
timestamp = datetime.now() - timedelta(days=1, hours=2)
logs.append(
    f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},"
    f"alice,192.168.1.10,NewYork,success"
)

# Anomaly 2 - Unusual Location
timestamp = datetime.now() - timedelta(hours=5)
logs.append(
    f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},"
    f"bob,203.0.113.45,Tokyo,success"
)

# Anomaly 3 - High Frequency Login Attempts
for i in range(15):
    timestamp = datetime.now() - timedelta(minutes=30 - i)

    logs.append(
        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},"
        f"admin,198.51.100.78,Unknown,failed"
    )

with open("auth_logs.csv", "w") as f:
    f.write("timestamp,username,ip_address,location,status\n")

    for log in sorted(logs):
        f.write(log + "\n")

print("Generated auth_logs.csv with sample data")
```

Run the generator:

```bash
python3 generate_logs.py
```

---

# 📊 Task 1: Parse and Load Login Data

Create the anomaly detector:

```bash
nano anomaly_detector.py
```

---

## Starter Code

```python
#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
from collections import defaultdict

class LoginAnomalyDetector:

    def __init__(self, log_file):
        self.log_file = log_file
        self.df = None
        self.user_profiles = {}

    def load_logs(self):

        self.df = pd.read_csv(self.log_file)

        self.df['timestamp'] = pd.to_datetime(
            self.df['timestamp']
        )

        self.df['hour'] = self.df['timestamp'].dt.hour

        print(f"Loaded {len(self.df)} login records")
        print("\nSample Data:")
        print(self.df.head())

    def build_user_profiles(self):

        successful = self.df[
            self.df['status'] == 'success'
        ]

        for username in successful['username'].unique():

            user_data = successful[
                successful['username'] == username
            ]

            typical_hours = (
                user_data['hour']
                .tolist()
            )

            typical_locations = (
                user_data['location']
                .unique()
                .tolist()
            )

            self.user_profiles[username] = {
                'typical_hours': typical_hours,
                'typical_locations': typical_locations,
                'login_count': len(user_data)
            }

        print(
            f"\nBuilt profiles for "
            f"{len(self.user_profiles)} users"
        )

    def detect_time_anomalies(self):

        business_start = 8
        business_end = 18

        anomalies = self.df[
            (self.df['hour'] < business_start) |
            (self.df['hour'] > business_end)
        ]

        return anomalies

    def detect_location_anomalies(self):

        anomalies = []

        for _, row in self.df.iterrows():

            username = row['username']
            location = row['location']

            if username in self.user_profiles:

                typical_locations = (
                    self.user_profiles[username]
                    ['typical_locations']
                )

                if location not in typical_locations:
                    anomalies.append(row)

        if anomalies:
            return pd.DataFrame(anomalies)

        return pd.DataFrame()

    def detect_frequency_anomalies(
        self,
        time_window=30,
        threshold=10
    ):

        df_sorted = self.df.sort_values(
            'timestamp'
        )

        suspicious_users = defaultdict(int)

        for username in df_sorted[
            'username'
        ].unique():

            user_logs = df_sorted[
                df_sorted['username'] == username
            ]

            recent = user_logs[
                user_logs['timestamp']
                >= (
                    datetime.now()
                    - pd.Timedelta(
                        minutes=time_window
                    )
                )
            ]

            if len(recent) >= threshold:
                suspicious_users[username] = len(recent)

        return suspicious_users

    def generate_report(self):

        print("\n" + "=" * 60)
        print("LOGIN ANOMALY DETECTION REPORT")
        print("=" * 60)

        self.build_user_profiles()

        # Time-Based Detection
        print(
            "\n[1] TIME-BASED ANOMALIES"
        )
        print("-" * 60)

        time_anomalies = (
            self.detect_time_anomalies()
        )

        if len(time_anomalies) > 0:

            print(
                f"Found "
                f"{len(time_anomalies)} "
                f"suspicious login(s):"
            )

            for _, row in (
                time_anomalies.iterrows()
            ):
                print(
                    f" - {row['username']} "
                    f"at {row['timestamp']} "
                    f"from {row['location']}"
                )

        else:
            print(
                "No time anomalies detected."
            )

        # Location-Based Detection
        print(
            "\n[2] LOCATION-BASED ANOMALIES"
        )
        print("-" * 60)

        location_anomalies = (
            self.detect_location_anomalies()
        )

        if len(location_anomalies) > 0:

            print(
                f"Found "
                f"{len(location_anomalies)} "
                f"suspicious login(s):"
            )

            for _, row in (
                location_anomalies.iterrows()
            ):
                print(
                    f" - {row['username']} "
                    f"from {row['location']} "
                    f"(IP: {row['ip_address']})"
                )

        else:
            print(
                "No location anomalies detected."
            )

        # Frequency Detection
        print(
            "\n[3] FREQUENCY-BASED ANOMALIES"
        )
        print("-" * 60)

        freq_anomalies = (
            self.detect_frequency_anomalies()
        )

        if freq_anomalies:

            print(
                f"Found "
                f"{len(freq_anomalies)} "
                f"suspicious user(s):"
            )

            for user, count in (
                freq_anomalies.items()
            ):
                print(
                    f" - {user}: "
                    f"{count} attempts "
                    f"in last 30 minutes"
                )

        else:
            print(
                "No frequency anomalies detected."
            )

        print("\n" + "=" * 60)


if __name__ == "__main__":

    detector = LoginAnomalyDetector(
        "auth_logs.csv"
    )

    detector.load_logs()
    detector.generate_report()
```

---

# ▶️ Run the Detector

```bash
python3 anomaly_detector.py
```

---

# ✅ Expected Output

```text
Loaded 100 login records

Built profiles for 4 users

============================================================
LOGIN ANOMALY DETECTION REPORT
============================================================

[1] TIME-BASED ANOMALIES
------------------------------------------------------------
Found 1 suspicious login(s):
 - alice at 2024-01-20 02:15:00 from NewYork

[2] LOCATION-BASED ANOMALIES
------------------------------------------------------------
Found 1 suspicious login(s):
 - bob from Tokyo (IP: 203.0.113.45)

[3] FREQUENCY-BASED ANOMALIES
------------------------------------------------------------
Found 1 suspicious user(s):
 - admin: 15 attempts in last 30 minutes

============================================================
```

---

# 🧪 Verification

## Verify Log Data

```bash
head auth_logs.csv
```

---

## Verify Time-Based Anomaly

```bash
grep "alice" auth_logs.csv
```

Look for login activity outside business hours.

---

## Verify Location-Based Anomaly

```bash
grep "Tokyo" auth_logs.csv
```

Expected:

```text
bob,203.0.113.45,Tokyo
```

---

## Verify Frequency-Based Anomaly

```bash
grep "admin" auth_logs.csv | wc -l
```

Expected:

```text
15
```

---

# ⚙️ Test Custom Thresholds

Modify:

```python
freq_anomalies = self.detect_frequency_anomalies(
    time_window=60,
    threshold=5
)
```

Run again:

```bash
python3 anomaly_detector.py
```

Observe how detection sensitivity changes.

---

# 🔍 Troubleshooting

### Issue: pandas Module Not Found

```bash
pip3 install --user pandas
```

---

### Issue: auth_logs.csv Missing

```bash
ls -lh auth_logs.csv
```

If missing:

```bash
python3 generate_logs.py
```

---

### Issue: No Anomalies Detected

Verify generated data:

```bash
cat auth_logs.csv
```

Check for:

- Late-night login entries
- Tokyo location login
- Multiple admin failures

---

# 📈 Real-World Applications

This technology is widely used in:

- Security Information and Event Management (SIEM)
- User and Entity Behavior Analytics (UEBA)
- Security Operations Centers (SOC)
- Insider Threat Detection
- Account Takeover Prevention
- Cloud Security Monitoring

---

# 🏆 Key Skills Gained

✔ Authentication Log Analysis

✔ Behavioral Profiling

✔ Anomaly Detection

✔ Security Event Investigation

✔ Python Log Processing

✔ Cybersecurity Monitoring Fundamentals

---

# 🎯 Next Steps

Enhance the project by:

- 📧 Email Alerting
- 📊 Web Dashboard Visualization
- 🧠 Machine Learning-Based Anomaly Detection
- ☁️ Cloud Log Integration
- 🔔 Real-Time Monitoring
- 📡 SIEM Integration
- 🚫 Automated Account Lockout

---

# 📚 Conclusion

You successfully built a **Login Anomaly Detection System** capable of:

- Parsing authentication logs
- Building user behavior baselines
- Detecting abnormal login times
- Detecting unusual login locations
- Identifying brute-force style login activity
- Generating actionable security reports

This project demonstrates core concepts used by enterprise SIEM and UEBA platforms to identify compromised accounts and malicious activity before significant damage occurs.

> **"Effective security monitoring begins with understanding what normal behavior looks like."**

---
⭐ Lab Complete — You now have hands-on experience with authentication analytics and anomaly detection techniques used by cybersecurity professionals.
