#!/usr/bin/env python3
"""
Vulnerable application demonstrating unsafe input handling
WARNING: This is for educational purposes only
"""

import os

def unsafe_command_execution(user_input):
    """
    VULNERABLE: Executes user input directly
    """
    command = f"echo {user_input}"
    os.system(command)

def unsafe_file_access(filename):
    """
    VULNERABLE: Opens files without validation
    """
    try:
        with open(filename, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Vulnerable Application Demo ===")
    
    # Test 1: Command injection vulnerability
    print("\n[Test 1] Command Injection:")
    user_input = "Hello; ls -la"  # Malicious input
    print(f"Input: {user_input}")
    unsafe_command_execution(user_input)
    
    # Test 2: Path traversal vulnerability
    print("\n[Test 2] Path Traversal:")
    filename = "../../etc/passwd"  # Malicious path
    print(f"Filename: {filename}")
    unsafe_file_access(filename)
