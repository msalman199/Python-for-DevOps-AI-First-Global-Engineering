#!/bin/bash
# Security Alert Analyzer
# Detects suspicious authentication patterns

THRESHOLD=5  # Failed attempts threshold

echo "=== SECURITY ALERTS ==="
echo "Generated: $(date)"
echo ""

# Alert 1: Brute Force Detection
echo "[ALERT] IPs with more than $THRESHOLD failed attempts:"
# TODO: Find IPs exceeding threshold
sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | awk -v t=$THRESHOLD '$1 > t {print $1, "attempts from", $2}'

echo ""

# Alert 2: Invalid User Attempts
echo "[ALERT] Invalid user login attempts:"
# TODO: Count invalid user attempts
INVALID_COUNT=$(sudo grep "Invalid user" /var/log/auth.log | wc -l)
echo "Total: $INVALID_COUNT"
if [ $INVALID_COUNT -gt 0 ]; then
    echo "Top targeted invalid usernames:"
    sudo grep "Invalid user" /var/log/auth.log | awk '{print $8}' | sort | uniq -c | sort -rn | head -5
fi

echo ""

# Alert 3: Root Login Attempts
echo "[ALERT] Root login attempts:"
# TODO: Count root login attempts
ROOT_ATTEMPTS=$(sudo grep "Failed password for root" /var/log/auth.log | wc -l)
echo "Failed root attempts: $ROOT_ATTEMPTS"

echo ""

# Alert 4: Successful Logins After Failed Attempts
echo "[ALERT] IPs with both failed and successful logins:"
# TODO: Find IPs that eventually succeeded after failures
FAILED_IPS=$(sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort -u)
for ip in $FAILED_IPS; do
    SUCCESS=$(sudo grep "Accepted.*$ip" /var/log/auth.log | wc -l)
    if [ $SUCCESS -gt 0 ]; then
        echo "IP $ip: Had failures but eventually succeeded"
    fi
done

echo ""
echo "=== END OF REPORT ==="
