# 📊 Log Line Parsing and Tokenization Utility Lab

## 📋 Prerequisites
* Basic Linux command line knowledge (navigating directories, creating files)
* Fundamental understanding of text files
* Basic Python programming (variables, functions, loops)
* Familiarity with string operations

---

## 🎯 Learning Objectives
By completing this lab, you will:
* Understand structured log file formats
* Parse log lines into individual components
* Extract timestamps, IP addresses, and message fields
* Tokenize log data for analysis
* Build a reusable log parsing utility

---

## ⚙️ Environment Setup

### 🧰 Step 1: Start Your Lab Environment
Click the **Start Lab** button to provision your Linux machine. Once ready, connect via SSH.

### 📥 Step 2: Install Required Tools
```bash
# Update package manager
sudo apt update

# Install Python 3 and pip (if not already installed)
sudo apt install -y python3 python3-pip

# Verify installation
python3 --version
```

### 🗂️ Step 3: Create Lab Directory
```bash
# Create and navigate to lab directory
mkdir -p ~/log-parser-lab
cd ~/log-parser-lab
```

### 📝 Step 4: Create Sample Log File
```bash
# Create a sample log file with various formats
cat > sample.log << 'EOF'
2024-01-15 10:23:45 192.168.1.100 INFO User login successful
2024-01-15 10:24:12 10.0.0.45 ERROR Failed authentication attempt
2024-01-15 10:25:33 172.16.0.88 WARNING High memory usage detected
2024-01-15 10:26:01 192.168.1.100 INFO User logout
2024-01-15 10:27:18 203.0.113.42 ERROR Connection timeout
2024-01-15 10:28:45 192.168.1.105 INFO File upload completed
2024-01-15 10:29:52 10.0.0.45 WARNING Disk space low
2024-01-15 10:30:15 172.16.0.88 INFO Database backup started
EOF

# View the log file
cat sample.log
```

---

## 🛠️ Task 1: Build Basic Log Parser

### 📝 Step 1: Create Parser Script
Create a Python script for parsing log lines:
```bash
nano log_parser.py
```
Add the following template starter code:
```python
#!/usr/bin/env python3
"""
Log Parser Utility
Parses structured log files and extracts key components
"""

import re
from datetime import datetime
from typing import Dict, List, Optional

def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """
    Parse a single log line into components.
    
    Expected format: YYYY-MM-DD HH:MM:SS IP_ADDRESS LEVEL MESSAGE
    """
    pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\s+(.+)'
    # TODO: Implement regex matching logic
    pass

def tokenize_message(message: str) -> List[str]:
    """Tokenize a log message into individual words."""
    # TODO: Split message into tokens
    pass

def extract_timestamp_components(timestamp_str: str) -> Dict[str, int]:
    """Extract date and time components from timestamp string."""
    # TODO: Parse timestamp string using datetime.strptime()
    pass

def validate_ip_address(ip: str) -> bool:
    """Validate if string is a valid IPv4 address."""
    # TODO: Create regex pattern for IPv4 validation
    pass

def parse_log_file(filename: str) -> List[Dict[str, str]]:
    """Parse entire log file and return list of parsed entries."""
    # TODO: Open and read file line by line
    pass

def filter_by_level(parsed_logs: List[Dict], level: str) -> List[Dict]:
    """Filter log entries by severity level."""
    # TODO: Filter logs where level matches
    pass

def main():
    print("=== Log Parser Utility ===\n")
    # TODO: Handle setup & execution demonstration

if __name__ == "__main__":
    main()
```

### ⚙️ Step 2: Implement Core Functions
Replace your template script by adding the fully completed logical implementation into `log_parser.py`:

```python
#!/usr/bin/env python3
"""
Log Parser Utility
Parses structured log files and extracts key components
"""

import re
from datetime import datetime
from typing import Dict, List, Optional

def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """
    Parse a single log line into components.
    
    Expected format: YYYY-MM-DD HH:MM:SS IP_ADDRESS LEVEL MESSAGE
    """
    pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)\s+(.+)'
    match = re.match(pattern, line.strip())
    if match:
        return {
            'timestamp': f"{match.group(1)} {match.group(2)}",
            'ip_address': match.group(3),
            'level': match.group(4),
            'message': match.group(5)
        }
    return None


def tokenize_message(message: str) -> List[str]:
    """Tokenize a log message into individual words."""
    tokens = message.split()
    return [token for token in tokens if token]


def extract_timestamp_components(timestamp_str: str) -> Dict[str, int]:
    """Extract date and time components from timestamp string."""
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.hour,
        'minute': dt.minute,
        'second': dt.second
    }


def validate_ip_address(ip: str) -> bool:
    """Validate if string is a valid IPv4 address."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False


def parse_log_file(filename: str) -> List[Dict[str, str]]:
    """Parse entire log file and return list of parsed entries."""
    parsed_logs = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed:
                    parsed_logs.append(parsed)
    except FileNotFoundError:
        print(f"Error: The file {filename} could not be found.")
    return parsed_logs


def filter_by_level(parsed_logs: List[Dict], level: str) -> List[Dict]:
    """Filter log entries by severity level."""
    return [log for log in parsed_logs if log['level'].upper() == level.upper()]


def main():
    """Main function to demonstrate log parsing functionality."""
    print("=== Log Parser Utility ===\n")
    
    # Parse the sample log file
    logs = parse_log_file("sample.log")
    print(f"Total entries successfully parsed: {len(logs)}\n")
    
    # Display the first 3 parsed entries
    print("--- First 3 Log Entries ---")
    for log in logs[:3]:
        print(log)
    print()
    
    # Filter and display ERROR entries
    print("--- Error Severity Logs ---")
    error_logs = filter_by_level(logs, "ERROR")
    for log in error_logs:
        print(f"[{log['timestamp']}] IP: {log['ip_address']} - Msg: {log['message']}")
    print()
        
    # Display tokenization extraction
    print("--- Message Tokenization Example ---")
    for log in logs[:2]:
        tokens = tokenize_message(log['message'])
        print(f"Original: '{log['message']}'")
        print(f"Tokens  : {tokens}")


if __name__ == "__main__":
    main()
```

### 🧪 Step 3: Test Your Parser
Make the engine executable and fire it against your local workspace context logs:
```bash
# Make script executable
chmod +x log_parser.py

# Run the parser
python3 log_parser.py
```
*Expected output shows cleanly parsed objects, filtered operational scopes, and segmented message tokens.*

---

## 🛠️ Task 2: Advanced Parsing Features

### 📝 Step 1: Create Enhanced Parser
To accumulate counts and historical interaction analytics, run:
```bash
nano advanced_parser.py
```
Paste this completed extension tracking matrix script inside:
```python
#!/usr/bin/env python3
"""
Advanced Log Parser with Statistics
"""

import re
from collections import Counter
from datetime import datetime
from typing import Dict, List
from log_parser import parse_log_file, validate_ip_address

def generate_statistics(parsed_logs: List[Dict]) -> Dict:
    """
    Generate statistics from parsed logs.
    
    Returns:
        Dictionary containing:
        - total_entries: Total number of log entries
        - level_counts: Count of each log level
        - unique_ips: Number of unique IP addresses
        - top_ips: Most frequent IP addresses
    """
    total_entries = len(parsed_logs)
    
    # Count occurrences of log levels
    levels = [log['level'] for log in parsed_logs]
    level_counts = dict(Counter(levels))
    
    # Filter valid IPs and track uniqueness/frequency
    ips = [log['ip_address'] for log in parsed_logs if validate_ip_address(log['ip_address'])]
    unique_ips = len(set(ips))
    top_ips = Counter(ips).most_common(3)
    
    return {
        'total_entries': total_entries,
        'level_counts': level_counts,
        'unique_ips': unique_ips,
        'top_ips': top_ips
    }

def main():
    print("=== Advanced Analytics Engine ===\n")
    logs = parse_log_file("sample.log")
    stats = generate_statistics(logs)
    
    print(f"Total Logs Processed   : {stats['total_entries']}")
    print(f"Unique IP Targets      : {stats['unique_ips']}")
    
    print("\nLog Levels Distribution:")
    for level, count in stats['level_counts'].items():
        print(f" - {level:<8}: {count}")
        
    print("\nTop Active IP Contacts:")
    for ip, count in stats['top_ips']:
        print(f" - {ip:<15}: seen {count} time(s)")

if __name__ == "__main__":
    main()
```

### 🧪 Step 2: Test Advanced Metric Parser
```bash
chmod +x advanced_parser.py
python3 advanced_parser.py
```
