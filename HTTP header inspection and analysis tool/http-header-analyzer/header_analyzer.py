#!/usr/bin/env python3
"""
HTTP Header Security Analyzer
Extracts and analyzes HTTP headers for security issues
"""

import requests
import sys
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def fetch_headers(url):
    """
    Fetch HTTP headers from a given URL
    
    Args:
        url (str): Target URL to analyze
    
    Returns:
        dict: Response headers or None if error
    """
    try:
        # TODO: Add timeout parameter (10 seconds)
        # TODO: Use requests.get() to fetch the URL
        # TODO: Return response.headers
        pass
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error fetching URL: {e}")
        return None

def display_headers(headers):
    """
    Display all HTTP headers in a formatted way
    
    Args:
        headers (dict): HTTP response headers
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}HTTP HEADERS FOUND")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    # TODO: Loop through headers dictionary
    # TODO: Print each header name and value
    pass

# Security headers that should be present
SECURITY_HEADERS = {
    'Strict-Transport-Security': 'Enforces HTTPS connections',
    'X-Frame-Options': 'Prevents clickjacking attacks',
    'X-Content-Type-Options': 'Prevents MIME-type sniffing',
    'Content-Security-Policy': 'Controls resource loading',
    'X-XSS-Protection': 'Enables XSS filtering',
    'Referrer-Policy': 'Controls referrer information',
    'Permissions-Policy': 'Controls browser features'
}

# Insecure header values to flag
INSECURE_VALUES = {
    'X-Frame-Options': ['ALLOW'],
    'X-XSS-Protection': ['0'],
    'Strict-Transport-Security': []  # Check for low max-age
}
def analyze_security_headers(headers):
    """
    Analyze headers for security issues
    
    Args:
        headers (dict): HTTP response headers
    
    Returns:
        tuple: (missing_headers, insecure_headers)
    """
    missing = []
    insecure = []
    
    # TODO: Check for missing security headers
    # Loop through SECURITY_HEADERS
    # If header not in response headers, add to missing list
    
    # TODO: Check for insecure configurations
    # Check X-XSS-Protection value
    # Check X-Frame-Options value
    # Check Strict-Transport-Security max-age
    
    return missing, insecure

def display_security_report(missing, insecure):
    """
    Display security analysis report
    
    Args:
        missing (list): List of missing security headers
        insecure (list): List of insecure header configurations
    """
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{Fore.YELLOW}SECURITY ANALYSIS REPORT")
    print(f"{Fore.YELLOW}{'='*60}\n")
    
    # Display missing headers
    if missing:
        print(f"{Fore.RED}Missing Security Headers ({len(missing)}):")
        # TODO: Loop through missing headers and print each one
        # Include the description from SECURITY_HEADERS
    else:
        print(f"{Fore.GREEN}All critical security headers present!")
    
    # Display insecure configurations
    if insecure:
        print(f"\n{Fore.RED}Insecure Configurations Found ({len(insecure)}):")
        # TODO: Loop through insecure headers and print details
    else:
        print(f"\n{Fore.GREEN}No insecure configurations detected!")

def main():
    """
    Main function to run the header analyzer
    """
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Usage: python3 header_analyzer.py <URL>")
        print(f"{Fore.YELLOW}Example: python3 header_analyzer.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Add https:// if not present
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"{Fore.CYAN}Analyzing: {url}\n")
    
    # TODO: Call fetch_headers()
    # TODO: Check if headers were retrieved successfully
    # TODO: Call display_headers()
    # TODO: Call analyze_security_headers()
    # TODO: Call display_security_report()

if __name__ == "__main__":
    main()



