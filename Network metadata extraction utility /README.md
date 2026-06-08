# 🌐 Network Metadata Extraction Utility

> *"Transform raw network traffic into actionable intelligence through metadata extraction, enrichment, and analysis."*

---

## 📌 Overview

The **Network Metadata Extraction Utility** is a Python-based network analysis tool designed to extract, enrich, and analyze network intelligence from traffic logs and packet captures.

This lab demonstrates how cybersecurity analysts and network engineers can process network data, identify services, classify internal and external traffic, generate statistical reports, and export structured metadata for further investigation.

---

## 🎯 Learning Objectives

By completing this lab, you will:

* Extract network intelligence from log files and packet captures
* Parse IP addresses, ports, and protocols from network data
* Enrich metadata with service information and geolocation
* Classify internal and external network communications
* Generate statistical reports from network traffic
* Export structured metadata for future analysis

---

## 🛠️ Prerequisites

* Basic Linux command-line knowledge
* Understanding of IP addresses and ports
* Familiarity with text file operations
* Python 3 fundamentals (variables, loops, functions)

---

## 🏗️ Environment Setup

### Step 1: Update Package Repository

```bash
sudo apt update
```

### Step 2: Install Python and Network Tools

```bash
sudo apt install -y python3 python3-pip
sudo apt install -y tcpdump tshark
```

### Step 3: Install Python Dependencies

```bash
pip3 install geoip2-database maxminddb-geolite2 python-whois
```

### Step 4: Create Working Directory

```bash
mkdir ~/network-metadata-lab
cd ~/network-metadata-lab
```

---

# 📊 Task 1: Generate Sample Network Data

## Step 1: Create Sample Network Log File

Create a simulated network traffic log:

```bash
cat > network_traffic.log << 'EOF'
2024-01-15 10:23:45 TCP 192.168.1.100:45678 -> 8.8.8.8:53
2024-01-15 10:23:46 UDP 192.168.1.100:54321 -> 1.1.1.1:53
2024-01-15 10:24:12 TCP 192.168.1.105:49152 -> 93.184.216.34:80
2024-01-15 10:24:15 TCP 192.168.1.105:49153 -> 93.184.216.34:443
2024-01-15 10:25:01 TCP 192.168.1.110:51234 -> 140.82.121.4:443
2024-01-15 10:25:30 UDP 192.168.1.100:68 -> 192.168.1.1:67
2024-01-15 10:26:45 TCP 192.168.1.120:55678 -> 151.101.1.140:443
2024-01-15 10:27:10 TCP 192.168.1.100:60123 -> 172.217.14.206:443
EOF
```

---

## Step 2: Capture Live Network Traffic (Optional)

Capture real packets from the system:

```bash
sudo timeout 10 tcpdump -i any -c 20 -w capture.pcap 2>/dev/null
```

Convert PCAP to text:

```bash
tshark -r capture.pcap \
-T fields \
-e frame.time \
-e ip.proto \
-e ip.src \
-e tcp.srcport \
-e udp.srcport \
-e ip.dst \
-e tcp.dstport \
-e udp.dstport \
2>/dev/null > live_traffic.txt
```

---

# 🔍 Task 2: Build Network Metadata Extraction Utility

## Step 1: Create Main Python Script

Create:

```bash
nano network_metadata_extractor.py
```

---

### Complete Source Code

```python
#!/usr/bin/env python3
"""
Network Metadata Extraction Utility
Extracts and enriches network intelligence from logs
"""

import re
import json
from collections import defaultdict
from datetime import datetime

try:
    from geolite2 import geolite2
    GEOIP_AVAILABLE = True
except ImportError:
    GEOIP_AVAILABLE = False
    print("Note: GeoIP not available.")

class NetworkMetadataExtractor:

    def __init__(self):
        self.connections = []
        self.stats = defaultdict(int)

        self.port_services = {
            20: "FTP-DATA",
            21: "FTP",
            22: "SSH",
            23: "TELNET",
            25: "SMTP",
            53: "DNS",
            67: "DHCP",
            68: "DHCP",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt"
        }

        self.protocols = {
            1: "ICMP",
            6: "TCP",
            17: "UDP"
        }

    def parse_log_line(self, line):

        pattern = (
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
            r'\s+(\w+)'
            r'\s+([\d.]+):(\d+)'
            r'\s+->\s+([\d.]+):(\d+)'
        )

        match = re.search(pattern, line)

        if not match:
            return None

        timestamp, protocol, src_ip, src_port, dst_ip, dst_port = match.groups()

        return {
            'timestamp': timestamp,
            'protocol': protocol,
            'src_ip': src_ip,
            'src_port': int(src_port),
            'dst_ip': dst_ip,
            'dst_port': int(dst_port)
        }

    def enrich_metadata(self, metadata):

        metadata['service'] = self.port_services.get(
            metadata['dst_port'],
            f"Unknown-{metadata['dst_port']}"
        )

        if GEOIP_AVAILABLE:
            try:
                reader = geolite2.reader()
                geo_data = reader.get(metadata['dst_ip'])

                if geo_data:
                    metadata['dst_country'] = geo_data.get(
                        'country',
                        {}
                    ).get(
                        'iso_code',
                        'Unknown'
                    )

                    metadata['dst_city'] = geo_data.get(
                        'city',
                        {}
                    ).get(
                        'names',
                        {}
                    ).get(
                        'en',
                        'Unknown'
                    )
            except:
                metadata['dst_country'] = "Unknown"

        metadata['dst_type'] = self._classify_ip(
            metadata['dst_ip']
        )

        return metadata

    def _classify_ip(self, ip):

        octets = ip.split('.')

        if octets[0] == '10':
            return 'Internal'

        elif octets[0] == '172' and 16 <= int(octets[1]) <= 31:
            return 'Internal'

        elif octets[0] == '192' and octets[1] == '168':
            return 'Internal'

        return 'External'

    def process_log_file(self, filename):

        print(f"[*] Processing {filename}")

        with open(filename, 'r') as file:

            for line in file:

                metadata = self.parse_log_line(line)

                if metadata:

                    enriched = self.enrich_metadata(metadata)

                    self.connections.append(enriched)

                    self.stats['total_connections'] += 1
                    self.stats[f"protocol_{enriched['protocol']}"] += 1
                    self.stats[f"service_{enriched['service']}"] += 1

        print(
            f"[+] Processed "
            f"{self.stats['total_connections']} connections"
        )

    def generate_report(self):

        print("\n" + "=" * 60)
        print("NETWORK METADATA EXTRACTION REPORT")
        print("=" * 60)

        print(
            f"\n[*] Total Connections: "
            f"{self.stats['total_connections']}"
        )

        print("\n[*] Protocol Distribution:")

        for key, value in self.stats.items():

            if key.startswith("protocol_"):
                protocol = key.replace(
                    "protocol_",
                    ""
                )

                print(f"    {protocol}: {value}")

        print("\n[*] Top Services:")

        services = [
            (
                k.replace("service_", ""),
                v
            )
            for k, v in self.stats.items()
            if k.startswith("service_")
        ]

        services.sort(
            key=lambda x: x[1],
            reverse=True
        )

        for service, count in services[:5]:
            print(f"    {service}: {count}")

        unique_ips = set(
            conn['dst_ip']
            for conn in self.connections
        )

        print(
            f"\n[*] Unique Destination IPs: "
            f"{len(unique_ips)}"
        )

        external = sum(
            1 for conn in self.connections
            if conn['dst_type'] == 'External'
        )

        internal = sum(
            1 for conn in self.connections
            if conn['dst_type'] == 'Internal'
        )

        print("\n[*] Traffic Distribution:")
        print(f"    External: {external}")
        print(f"    Internal: {internal}")

    def export_json(self, output_file):

        with open(output_file, 'w') as file:

            json.dump(
                {
                    "metadata": self.connections,
                    "statistics": dict(self.stats),
                    "generated_at": datetime.now().isoformat()
                },
                file,
                indent=2
            )

        print(
            f"\n[+] Exported metadata to "
            f"{output_file}"
        )

def main():

    print("Network Metadata Extraction Utility")
    print("-" * 60)

    extractor = NetworkMetadataExtractor()

    extractor.process_log_file(
        "network_traffic.log"
    )

    extractor.generate_report()

    extractor.export_json(
        "network_metadata.json"
    )

    print("\n[+] Analysis complete!")

if __name__ == "__main__":
    main()
```

---

## Step 2: Make Script Executable

```bash
chmod +x network_metadata_extractor.py
```

---

## Step 3: Run the Utility

```bash
python3 network_metadata_extractor.py
```

Expected output:

```text
Network Metadata Extraction Utility
------------------------------------------------------------

[*] Processing network_traffic.log
[+] Processed 8 connections

============================================================
NETWORK METADATA EXTRACTION REPORT
============================================================

[*] Total Connections: 8

[*] Protocol Distribution:
    TCP: 6
    UDP: 2

[*] Top Services:
    HTTPS: 4
    DNS: 2
    HTTP: 1
    DHCP: 1
```

---

# 📁 Examine Exported Metadata

Pretty-print JSON:

```bash
cat network_metadata.json | python3 -m json.tool
```

View first 30 lines:

```bash
cat network_metadata.json | python3 -m json.tool | head -30
```

---

# ✅ Verification

## Verify JSON Output

```bash
ls -lh network_metadata.json
```

---

## Verify Connection Counts

```bash
python3 << 'EOF'
import json

with open('network_metadata.json') as f:
    data = json.load(f)

print(
    f"Total Connections: "
    f"{len(data['metadata'])}"
)

print(
    f"Unique Services: "
    f"{len(set(m['service']
    for m in data['metadata']))}"
)
EOF
```

---

## Test with Custom Input

```bash
echo "2024-01-15 11:00:00 TCP 10.0.0.5:12345 -> 142.250.185.46:443" > test_input.log
```

Run test:

```bash
python3 << 'EOF'
from network_metadata_extractor import NetworkMetadataExtractor

extractor = NetworkMetadataExtractor()

extractor.process_log_file('test_input.log')
extractor.generate_report()
EOF
```

---

# 📈 Expected Results

After completing this lab:

✅ Network logs successfully parsed

✅ Services automatically identified

✅ Internal and external traffic classified

✅ Statistical report generated

✅ JSON metadata exported

✅ Ready for SIEM and security analytics integration

---

# 🛠️ Troubleshooting

## GeoIP Library Not Working

Install:

```bash
pip3 install --user maxminddb-geolite2
```

GeoIP enrichment is optional.

---

## No Connections Parsed

Verify:

```bash
cat network_traffic.log
```

Ensure entries follow:

```text
TIMESTAMP PROTOCOL SRC_IP:SRC_PORT -> DST_IP:DST_PORT
```

---

## JSON File Empty

Check:

```bash
ls -l network_traffic.log
```

Ensure the log contains valid entries.

---

## Import Errors

Reinstall dependencies:

```bash
pip3 install --user maxminddb-geolite2 python-whois
```

---

# 🎯 Real-World Applications

This utility can be used for:

* Security monitoring
* Threat hunting
* Network traffic analysis
* Incident response investigations
* Digital forensics
* Compliance reporting
* SOC operations

---

# 🔐 Key Skills Demonstrated

### Network Log Parsing

* Regular Expressions
* Structured Data Extraction

### Metadata Enrichment

* Service Identification
* IP Classification
* Geolocation Mapping

### Traffic Analytics

* Protocol Analysis
* Service Distribution
* Connection Statistics

### Data Export

* JSON Serialization
* Security Data Pipelines

---

# 🏁 Conclusion

In this lab, you successfully built a **Network Metadata Extraction Utility** capable of transforming raw network logs into actionable security intelligence.

You learned how to:

* Parse network traffic records
* Extract IPs, ports, and protocols
* Enrich data with service metadata
* Classify internal and external communications
* Generate network activity reports
* Export structured JSON datasets

These techniques form the foundation of many enterprise-grade monitoring, threat detection, and incident response platforms used by cybersecurity professionals every day.

---

## 💡 Key Takeaways

* Network metadata provides valuable security insights.
* Port-to-service mapping helps identify traffic behavior.
* Internal vs External classification improves visibility.
* Structured JSON output enables automation.
* Metadata enrichment increases investigative value.

**Happy Learning & Secure Monitoring! 🚀**
