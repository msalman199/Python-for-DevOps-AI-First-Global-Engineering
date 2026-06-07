#!/bin/bash
# Failed Login Analyzer
# TODO: Add date parameter support

echo "=== Failed Login Attempts Report ==="
echo "Generated: $(date)"
echo ""

# TODO: Count total failed attempts
echo "Total Failed Attempts:"
sudo grep "Failed password" /var/log/auth.log | wc -l

echo ""
echo "Top 10 Usernames Targeted:"
# TODO: Extract and count usernames from failed attempts
sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-5)}' | sort | uniq -c | sort -rn | head -10

echo ""
echo "Top 10 Source IPs:"
# TODO: Extract and count source IPs
sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -10
