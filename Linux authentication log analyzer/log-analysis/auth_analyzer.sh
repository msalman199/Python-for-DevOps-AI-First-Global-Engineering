#!/bin/bash
# Complete Authentication Log Analyzer
# Usage: ./auth_analyzer.sh [logfile]

LOGFILE=${1:-/var/log/auth.log}

echo "========================================"
echo "  AUTHENTICATION LOG ANALYSIS REPORT"
echo "========================================"
echo "Log File: $LOGFILE"
echo "Generated: $(date)"
echo ""

# Section 1: Summary Statistics
echo "--- SUMMARY STATISTICS ---"
TOTAL_FAILED=$(sudo grep "Failed password" $LOGFILE | wc -l)
TOTAL_SUCCESS=$(sudo grep "Accepted" $LOGFILE | wc -l)
TOTAL_INVALID=$(sudo grep "Invalid user" $LOGFILE | wc -l)

echo "Total Failed Attempts: $TOTAL_FAILED"
echo "Total Successful Logins: $TOTAL_SUCCESS"
echo "Total Invalid User Attempts: $TOTAL_INVALID"
echo ""

# Section 2: Top Attackers
echo "--- TOP 5 ATTACKING IPs ---"
# TODO: List top 5 IPs by failed attempts
sudo grep "Failed password" $LOGFILE | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -5
echo ""

# Section 3: Targeted Accounts
echo "--- TOP 5 TARGETED ACCOUNTS ---"
# TODO: List top 5 usernames targeted
sudo grep "Failed password" $LOGFILE | awk '{print $(NF-5)}' | sort | uniq -c | sort -rn | head -5
echo ""

# Section 4: Successful Logins
echo "--- RECENT SUCCESSFUL LOGINS (Last 5) ---"
# TODO: Show last 5 successful logins
sudo grep "Accepted" $LOGFILE | tail -5 | awk '{print $1, $2, $3, "-", $9, "from", $11}'
echo ""

# Section 5: Security Warnings
echo "--- SECURITY WARNINGS ---"
# TODO: Check for root attempts
ROOT_FAIL=$(sudo grep "Failed password for root" $LOGFILE | wc -l)
if [ $ROOT_FAIL -gt 0 ]; then
    echo "[WARNING] $ROOT_FAIL failed root login attempts detected!"
fi

# TODO: Check for brute force
BRUTE_FORCE=$(sudo grep "Failed password" $LOGFILE | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | awk '$1 > 10' | wc -l)
if [ $BRUTE_FORCE -gt 0 ]; then
    echo "[WARNING] $BRUTE_FORCE IPs show brute force patterns (>10 attempts)!"
fi

echo ""
echo "========================================"
echo "  END OF REPORT"
echo "========================================"
