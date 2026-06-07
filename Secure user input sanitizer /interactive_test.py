#!/usr/bin/env python3
"""
Interactive Input Sanitizer Testing
"""

from input_sanitizer import InputSanitizer

def main():
    """
    Interactive menu for testing sanitization functions
    """
    while True:
        print("\n" + "="*50)
        print("Secure Input Sanitizer - Interactive Testing")
        print("="*50)
        print("1. Test Username Validation")
        print("2. Test Email Validation")
        print("3. Test HTML Escaping")
        print("4. Test Filename Sanitization")
        print("5. Test SQL Injection Detection")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            username = input("Enter username to test: ")
            is_valid = InputSanitizer.validate_alphanumeric(username, allow_spaces=False)
            print(f"Valid: {is_valid}")
            if is_valid:
                sanitized = InputSanitizer.remove_dangerous_chars(username)
                print(f"Sanitized: {sanitized}")
        
        elif choice == '2':
            email = input("Enter email to test: ")
            is_valid = InputSanitizer.validate_email(email)
            print(f"Valid email format: {is_valid}")
        
        elif choice == '3':
            text = input("Enter text with HTML: ")
            escaped = InputSanitizer.escape_html(text)
            print(f"Original: {text}")
            print(f"Escaped: {escaped}")
        
        elif choice == '4':
            filename = input("Enter filename to sanitize: ")
            sanitized = InputSanitizer.sanitize_filename(filename)
            print(f"Original: {filename}")
            print(f"Sanitized: {sanitized}")
        
        elif choice == '5':
            query = input("Enter text to check for SQL injection: ")
            is_suspicious = InputSanitizer.check_sql_injection(query)
            print(f"SQL injection detected: {is_suspicious}")
        
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
