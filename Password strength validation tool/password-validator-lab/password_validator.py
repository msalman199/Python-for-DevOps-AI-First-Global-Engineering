#!/usr/bin/env python3
import re
import sys

# Common weak passwords list
COMMON_PASSWORDS = [
    'password', '123456', '12345678', 'qwerty', 'abc123',
    'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
    'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
    'bailey', 'passw0rd', 'shadow', '123123', '654321'
]
def check_length(password):
    """
    Check if password meets minimum length requirement.
    
    Args:
        password (str): The password to validate
    
    Returns:
        tuple: (bool, str) - (is_valid, feedback_message)
    """
    min_length = 8
    max_length = 128
    
    # TODO: Check if password length is between min_length and max_length
    # TODO: Return (True, "Length is adequate") if valid
    # TODO: Return (False, "Password must be 8-128 characters") if invalid
    
    pass
def check_complexity(password):
    """
    Check if password contains required character types.
    
    Args:
        password (str): The password to validate
    
    Returns:
        tuple: (int, list) - (score, list_of_missing_requirements)
    """
    score = 0
    missing = []
    
    # TODO: Check for lowercase letters using re.search(r'[a-z]', password)
    # TODO: Check for uppercase letters using re.search(r'[A-Z]', password)
    # TODO: Check for digits using re.search(r'\d', password)
    # TODO: Check for special characters using re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    # TODO: Add 1 to score for each type found
    # TODO: Add missing types to the missing list
    
    pass
def check_common_patterns(password):
    """
    Check for common weak patterns in password.
    
    Args:
        password (str): The password to validate
    
    Returns:
        tuple: (bool, list) - (has_weak_patterns, list_of_issues)
    """
    issues = []
    
    # TODO: Check if password is in COMMON_PASSWORDS list (case-insensitive)
    # TODO: Check for sequential numbers like "123" or "abc" using regex
    # TODO: Check for repeated characters (3+ times) like "aaa" or "111"
    # TODO: Add found issues to the issues list
    
    pass
def calculate_strength(password):
    """
    Calculate overall password strength score.
    
    Args:
        password (str): The password to validate
    
    Returns:
        dict: Dictionary containing score, strength level, and feedback
    """
    total_score = 0
    feedback = []
    
    # Check length
    length_valid, length_msg = check_length(password)
    if not length_valid:
        feedback.append(length_msg)
        return {
            'score': 0,
            'strength': 'Invalid',
            'feedback': feedback
        }
    else:
        total_score += 20
    
    # TODO: Call check_complexity() and add complexity_score * 15 to total_score
    # TODO: Add missing requirements to feedback list
    
    # TODO: Call check_common_patterns() and subtract 30 from total_score if weak patterns found
    # TODO: Add pattern issues to feedback list
    
    # TODO: Add bonus points for length > 12 characters (10 points)
    # TODO: Add bonus points for length > 16 characters (additional 10 points)
    
    # TODO: Determine strength level based on total_score:
    # 0-30: Weak, 31-60: Fair, 61-80: Good, 81-100: Strong
    
    pass
def main():
    """
    Main function to run the password validator.
    """
    print("=" * 50)
    print("Password Strength Validator")
    print("=" * 50)
    
    # TODO: Get password input from user (use getpass for hidden input in production)
    # For this lab, use: password = input("Enter password to validate: ")
    
    # TODO: Call calculate_strength(password)
    
    # TODO: Print the results in a formatted way:
    # - Strength level
    # - Score
    # - Feedback messages
    
    pass

def check_length(password):
    """Check if password meets minimum length requirement."""
    min_length = 8
    max_length = 128
    
    if min_length <= len(password) <= max_length:
        return (True, "Length is adequate")
    else:
        return (False, f"Password must be {min_length}-{max_length} characters")

def load_common_passwords(filename='common_passwords.txt'):
    """
    Load common passwords from file.
    
    Args:
        filename (str): Path to password dictionary file
    
    Returns:
        set: Set of common passwords
    """
    # TODO: Try to open and read the file
    # TODO: Return a set of lowercase passwords (one per line)
    # TODO: Handle FileNotFoundError and return empty set if file doesn't exist
    
    pass
def batch_test(filename):
    """
    Test multiple passwords from a file.
    
    Args:
        filename (str): Path to file containing passwords (one per line)
    """
    # TODO: Read passwords from file
    # TODO: Test each password and print results
    # TODO: Print summary statistics (total tested, strong, weak, etc.)
    
    pass

# Add this test function temporarily
def run_tests():
    test_cases = [
        ("abc123", "Should detect sequential pattern"),
        ("Password123", "Should detect common word"),
        ("aaa111", "Should detect repetition"),
        ("Tr0ng!P@ss#2024", "Should score high")
    ]
    
    for password, description in test_cases:
        result = calculate_strength(password)
        print(f"\n{description}")
        print(f"Password: {password}")
        print(f"Result: {result}")

run_tests()


if __name__ == "__main__":
    main()



