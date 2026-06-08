#!/usr/bin/env python3
"""
Secure Configuration Loader and Validator
This script loads configuration files and validates them for security issues.
"""

import yaml
import json
import os
import re
from typing import Dict, List, Tuple

class ConfigValidator:
    """
    A class to load and validate configuration files for security issues.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the validator with a configuration file path.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config_data = None
        self.errors = []
        self.warnings = []
    
    def load_config(self) -> bool:
        """
        Load the configuration file safely.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            # TODO: Check if file exists
            if not os.path.exists(self.config_path):
                self.errors.append(f"Configuration file not found: {self.config_path}")
                return False
            
            # TODO: Check file permissions (should not be world-readable)
            file_stat = os.stat(self.config_path)
            file_permissions = oct(file_stat.st_mode)[-3:]
            
            if file_permissions[2] != '0':
                self.warnings.append("Configuration file is world-readable")
            
            # TODO: Load YAML file
            with open(self.config_path, 'r') as file:
                self.config_data = yaml.safe_load(file)
            
            return True
            
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading config: {str(e)}")
            return False
    
    def validate_required_fields(self, required_schema: Dict) -> bool:
        """
        Validate that all required fields are present.
        
        Args:
            required_schema: Dictionary defining required fields
            
        Returns:
            True if all required fields present, False otherwise
        """
        # TODO: Implement validation logic
        # Check each section and required field
        is_valid = True
        
        for section, fields in required_schema.items():
            if section not in self.config_data:
                self.errors.append(f"Missing required section: {section}")
                is_valid = False
                continue
            
            for field in fields:
                if field not in self.config_data[section]:
                    self.errors.append(f"Missing required field: {section}.{field}")
                    is_valid = False
        
        return is_valid
    
    def check_weak_passwords(self) -> List[str]:
        """
        Check for weak or common passwords in configuration.
        
        Returns:
            List of fields with weak passwords
        """
        weak_passwords = []
        weak_patterns = ['123456', 'password', 'admin', 'root', '12345']
        
        # TODO: Recursively search for password fields
        def search_passwords(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    if 'password' in key.lower() or 'passwd' in key.lower():
                        # Check password strength
                        if isinstance(value, str):
                            # Check length
                            if len(value) < 8:
                                weak_passwords.append(f"{current_path}: Too short (< 8 chars)")
                            # Check for common weak passwords
                            if value.lower() in weak_patterns:
                                weak_passwords.append(f"{current_path}: Common weak password")
                    else:
                        search_passwords(value, current_path)
        
        search_passwords(self.config_data)
        return weak_passwords
    
    def check_insecure_protocols(self) -> List[str]:
        """
        Check for insecure protocol usage (HTTP instead of HTTPS, SSL disabled).
        
        Returns:
            List of insecure protocol issues
        """
        issues = []
        
        # TODO: Check for HTTP URLs
        def search_urls(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    if isinstance(value, str) and value.startswith('http://'):
                        issues.append(f"{current_path}: Using insecure HTTP protocol")
                    elif key.lower() in ['ssl_enabled', 'tls_enabled'] and value is False:
                        issues.append(f"{current_path}: SSL/TLS is disabled")
                    else:
                        search_urls(value, current_path)
        
        search_urls(self.config_data)
        return issues
    
    def check_dangerous_settings(self) -> List[str]:
        """
        Check for dangerous configuration settings.
        
        Returns:
            List of dangerous settings found
        """
        dangerous = []
        
        # TODO: Check for debug mode in production
        if self.config_data.get('logging', {}).get('level') == 'DEBUG':
            self.warnings.append("Debug logging enabled - may expose sensitive information")
        
        # TODO: Check for root/admin usernames
        db_user = self.config_data.get('database', {}).get('username', '')
        if db_user.lower() in ['root', 'admin', 'administrator']:
            dangerous.append(f"Using privileged username: {db_user}")
        
        return dangerous
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive validation report.
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("CONFIGURATION SECURITY VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"\nConfiguration File: {self.config_path}\n")
        
        # Errors
        if self.errors:
            report.append("\n[ERRORS] - Critical Issues:")
            for error in self.errors:
                report.append(f"  - {error}")
        
        # Warnings
        if self.warnings:
            report.append("\n[WARNINGS] - Security Concerns:")
            for warning in self.warnings:
                report.append(f"  - {warning}")
        
        # Summary
        if not self.errors and not self.warnings:
            report.append("\n[SUCCESS] Configuration passed all security checks!")
        else:
            report.append(f"\nTotal Errors: {len(self.errors)}")
            report.append(f"Total Warnings: {len(self.warnings)}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)


def main():
    """
    Main function to run the configuration validator.
    """
    # Define required schema
    required_schema = {
        'database': ['host', 'port', 'username', 'password'],
        'api': ['endpoint', 'timeout'],
        'logging': ['level']
    }
    
    # Test configurations
    config_files = [
        'config_secure.yaml',
        'config_insecure.yaml',
        'config_incomplete.yaml'
    ]
    
    for config_file in config_files:
        print(f"\n\nValidating: {config_file}")
        print("-" * 60)
        
        validator = ConfigValidator(config_file)
        
        # Load configuration
        if not validator.load_config():
            print(validator.generate_report())
            continue
        
        # Validate required fields
        validator.validate_required_fields(required_schema)
        
        # Check for weak passwords
        weak_passwords = validator.check_weak_passwords()
        for issue in weak_passwords:
            validator.warnings.append(f"Weak password: {issue}")
        
        # Check for insecure protocols
        insecure_protocols = validator.check_insecure_protocols()
        for issue in insecure_protocols:
            validator.warnings.append(f"Insecure protocol: {issue}")
        
        # Check for dangerous settings
        dangerous_settings = validator.check_dangerous_settings()
        for issue in dangerous_settings:
            validator.warnings.append(f"Dangerous setting: {issue}")
        
        # Generate and print report
        print(validator.generate_report())


if __name__ == "__main__":
    main()
