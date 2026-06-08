#!/bin/bash
# Simple DNS query logger

DOMAINS=("google.com" "github.com" "stackoverflow.com" "example.com")
LOGFILE="dns_queries.log"

echo "=== DNS Query Log - $(date) ===" >> $LOGFILE

for domain in "${DOMAINS[@]}"; do
    echo "Querying: $domain" >> $LOGFILE
    dig +short $domain >> $LOGFILE
    echo "---" >> $LOGFILE
done
Make it executable and run:

chmod +x query_domains.sh
./query_domains.sh
cat dns_queries.log
Task 2: Build DNS Anomaly Simulator
Step 1: Create Python DNS Resolver
Create a Python script that performs DNS lookups:

nano dns_resolver.py
Add this starter code:

#!/usr/bin/env python3
"""
DNS Resolution and Anomaly Detection Tool
"""

import dns.resolver
import time
from datetime import datetime

def resolve_domain(domain, record_type='A'):
    """
    Resolve a domain name to its DNS records.
    
    Args:
        domain (str): Domain name to resolve
        record_type (str): Type of DNS record (A, AAAA, MX, etc.)
    
    Returns:
        list: List of resolved addresses or None if failed
    """
    try:
        # TODO: Create a DNS resolver object
        resolver = dns.resolver.Resolver()
        
        # TODO: Query the domain for specified record type
        answers = resolver.resolve(domain, record_type)
        
        # TODO: Extract and return the results
        results = [str(rdata) for rdata in answers]
        return results
        
    except dns.resolver.NXDOMAIN:
        print(f"[ERROR] Domain {domain} does not exist")
        return None
    except dns.resolver.Timeout:
        print(f"[ERROR] Query timeout for {domain}")
        return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

def check_domain_list(domains):
    """
    Check multiple domains and display results.
    
    Args:
        domains (list): List of domain names to check
    """
    print(f"\n{'='*60}")
    print(f"DNS Resolution Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    for domain in domains:
        print(f"Checking: {domain}")
        results = resolve_domain(domain)
        
        if results:
            for ip in results:
                print(f"  -> {ip}")
        else:
            print(f"  -> Resolution failed")
        print()

# Test the resolver
if __name__ == "__main__":
    test_domains = [
        "google.com",
        "github.com",
        "localhost"
    ]
    
    check_domain_list(test_domains)
