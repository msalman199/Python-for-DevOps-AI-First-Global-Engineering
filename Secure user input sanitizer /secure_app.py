#!/usr/bin/env python3
"""
Secure Application using Input Sanitizer
"""

from input_sanitizer import InputSanitizer

def process_username(username):
    """
    Securely process username input
    """
    print(f"\n[Processing Username: {username}]")
    
    # TODO: Validate username is alphanumeric (no spaces)
    if not InputSanitizer.validate_alphanumeric(username, allow_spaces=False):
        print("❌ Invalid username: Only alphanumeric characters allowed")
        return False
    
    # TODO: Remove dangerous characters
    sanitized = InputSanitizer.remove_dangerous_chars(username)
    print(f"✓ Sanitized username: {sanitized}")
    return True

def process_email(email):
    """
    Securely process email input
    """
    print(f"\n[Processing Email: {email}]")
    
    # TODO: Validate email format
    if not InputSanitizer.validate_email(email):
        print("❌ Invalid email format")
        return False
    
    print(f"✓ Valid email: {email}")
    return True

def process_comment(comment):
    """
    Securely process comment input
    """
    print(f"\n[Processing Comment: {comment}]")
    
    # TODO: Check for SQL injection attempts
    if InputSanitizer.check_sql_injection(comment):
        print("❌ Suspicious SQL patterns detected")
        return False
    
    # TODO: Escape HTML to prevent XSS
    escaped = InputSanitizer.escape_html(comment)
    print(f"✓ HTML-escaped comment: {escaped}")
    return True

def process_filename(filename):
    """
    Securely process filename input
    """
    print(f"\n[Processing Filename: {filename}]")
    
    # TODO: Sanitize filename to prevent path traversal
    sanitized = InputSanitizer.sanitize_filename(filename)
    print(f"✓ Sanitized filename: {sanitized}")
    
    if sanitized != filename:
        print("⚠ Warning: Filename was modified for security")
    
    return sanitized

if __name__ == "__main__":
    print("=== Secure Input Processing Demo ===")
    
    # Test cases
    test_cases = {
        "usernames": ["john_doe", "admin'; DROP TABLE users--", "user<script>"],
        "emails": ["user@example.com", "invalid.email", "test@domain.co.uk"],
        "comments": ["Great product!", "SELECT * FROM users", "<script>alert('XSS')</script>"],
        "filenames": ["document.pdf", "../../etc/passwd", "file;rm -rf.txt"]
    }
    
    # Test usernames
    print("\n" + "="*50)
    print("Testing Usernames:")
    print("="*50)
    for username in test_cases["usernames"]:
        process_username(username)
    
    # Test emails
    print("\n" + "="*50)
    print("Testing Emails:")
    print("="*50)
    for email in test_cases["emails"]:
        process_email(email)
    
    # Test comments
    print("\n" + "="*50)
    print("Testing Comments:")
    print("="*50)
    for comment in test_cases["comments"]:
        process_comment(comment)
    
    # Test filenames
    print("\n" + "="*50)
    print("Testing Filenames:")
    print("="*50)
    for filename in test_cases["filenames"]:
        process_filename(filename)
