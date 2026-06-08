#!/usr/bin/env python3
"""
DNS Anomaly Detector - Detects suspicious DNS patterns
"""

import dns.resolver
import re
from collections import Counter

class DNSAnomalyDetector:
    """Detects anomalies in DNS queries and responses"""
    
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
    
    def calculate_entropy(self, domain):
        """
        Calculate Shannon entropy of domain name.
        High entropy suggests random/generated domains.
        
        Args:
            domain (str): Domain name
        
        Returns:
            float: Entropy value
        """
        # TODO: Remove TLD for analysis
        domain_part = domain.split('.')[0]
        
        # TODO: Calculate character frequency
        if not domain_part:
            return 0
        
        # Count character occurrences
        counter = Counter(domain_part)
        length = len(domain_part)
        
        # Calculate entropy
        entropy = 0
        for count in counter.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * (probability.bit_length() - 1)
        
        return entropy
    
    def check_domain_length(self, domain):
        """
        Check if domain length is suspicious.
        
        Args:
            domain (str): Domain name
        
        Returns:
            dict: Analysis result
        """
        domain_part = domain.split('.')[0]
        length = len(domain_part)
        
        result = {
            'check': 'domain_length',
            'length': length,
            'suspicious': False,
            'reason': ''
        }
        
        # TODO: Flag unusually long domains (potential DGA)
        if length > 20:
            result['suspicious'] = True
            result['reason'] = 'Unusually long domain (possible DGA)'
        elif length < 3:
            result['suspicious'] = True
            result['reason'] = 'Unusually short domain'
        
        return result
    
    def check_entropy(self, domain):
        """
        Check domain entropy for randomness.
        
        Args:
            domain (str): Domain name
        
        Returns:
            dict: Analysis result
        """
        entropy = self.calculate_entropy(domain)
        
        result = {
            'check': 'entropy',
            'entropy': round(entropy, 2),
            'suspicious': False,
            'reason': ''
        }
        
        # TODO: High entropy suggests random generation
        if entropy > 3.5:
            result['suspicious'] = True
            result['reason'] = 'High entropy suggests DGA or random generation'
        
        return result
    
    def check_numeric_ratio(self, domain):
        """
        Check ratio of numbers in domain.
        
        Args:
            domain (str): Domain name
        
        Returns:
            dict: Analysis result
        """
        domain_part = domain.split('.')[0]
        if not domain_part:
            return {'check': 'numeric_ratio', 'suspicious': False}
        
        numeric_count = sum(c.isdigit() for c in domain_part)
        ratio = numeric_count / len(domain_part)
        
        result = {
            'check': 'numeric_ratio',
            'ratio': round(ratio, 2),
            'suspicious': False,
            'reason': ''
        }
        
        # TODO: High number ratio is suspicious
        if ratio > 0.3:
            result['suspicious'] = True
            result['reason'] = 'High numeric ratio (unusual for legitimate domains)'
        
        return result
    
    def analyze_domain(self, domain):
        """
        Perform complete analysis on a domain.
        
        Args:
            domain (str): Domain to analyze
        
        Returns:
            dict: Complete analysis results
        """
        print(f"\nAnalyzing: {domain}")
        print("-" * 60)
        
        checks = [
            self.check_domain_length(domain),
            self.check_entropy(domain),
            self.check_numeric_ratio(domain)
        ]
        
        suspicious_count = sum(1 for check in checks if check['suspicious'])
        
        # Display results
        for check in checks:
            status = "[SUSPICIOUS]" if check['suspicious'] else "[OK]"
            print(f"{status} {check['check']}: ", end="")
            
            if 'length' in check:
                print(f"Length = {check['length']}")
            elif 'entropy' in check:
                print(f"Entropy = {check['entropy']}")
            elif 'ratio' in check:
                print(f"Ratio = {check['ratio']}")
            
            if check.get('reason'):
                print(f"  Reason: {check['reason']}")
        
        # Overall assessment
        print(f"\nOverall: ", end="")
        if suspicious_count >= 2:
            print("HIGH RISK - Multiple anomalies detected")
        elif suspicious_count == 1:
            print("MEDIUM RISK - One anomaly detected")
        else:
            print("LOW RISK - No significant anomalies")
        
        return checks

def main():
    """Main detection routine"""
    
    detector = DNSAnomalyDetector()
    
    print("\n" + "="*70)
    print("DNS ANOMALY DETECTOR")
    print("="*70)
    
    # Test domains
    test_domains = [
        "google.com",  # Legitimate
        "github.com",  # Legitimate
        "aksjdhfkjashdfkjhaskjdfh.com",  # High entropy (DGA-like)
        "test12345678901234567890.com",  # Long with numbers
        "abc123xyz789.com"  # High numeric ratio
    ]
    
    for domain in test_domains:
        detector.analyze_domain(domain)
    
    print("\n" + "="*70)
    print("Detection Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
