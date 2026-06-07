#!/usr/bin/env python3
"""
Secure Input Sanitizer Module
Provides functions to sanitize and validate user input
"""

import re
import html

class InputSanitizer:
    """
    A class to sanitize and validate user inputs
    """
    
    # Define dangerous characters and patterns
    DANGEROUS_CHARS = ['<', '>', '&', '"', "'", ';', '|', '`', '$', '(', ')', '{', '}']
    SQL_KEYWORDS = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--', '/*']
    
    @staticmethod
    def remove_dangerous_chars(user_input):
        """
        Remove potentially dangerous characters from input
        
        Args:
            user_input (str): Raw user input
            
        Returns:
            str: Sanitized input with dangerous characters removed
        """
        # TODO: Implement character removal
        # Hint: Loop through DANGEROUS_CHARS and replace each with empty string
        sanitized = user_input
        for char in InputSanitizer.DANGEROUS_CHARS:
            sanitized = sanitized.replace(char, '')
        return sanitized
    
    @staticmethod
    def validate_alphanumeric(user_input, allow_spaces=True):
        """
        Validate that input contains only alphanumeric characters
        
        Args:
            user_input (str): Input to validate
            allow_spaces (bool): Whether to allow spaces
            
        Returns:
            bool: True if valid, False otherwise
        """
        # TODO: Use regex to validate alphanumeric pattern
        # Pattern with spaces: ^[a-zA-Z0-9 ]+$
        # Pattern without spaces: ^[a-zA-Z0-9]+$
        if allow_spaces:
            pattern = r'^[a-zA-Z0-9 ]+$'
        else:
            pattern = r'^[a-zA-Z0-9]+$'
        
        return bool(re.match(pattern, user_input))
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid email format, False otherwise
        """
        # TODO: Implement email validation using regex
        # Basic email pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize filename to prevent path traversal
        
        Args:
            filename (str): Filename to sanitize
            
        Returns:
            str: Sanitized filename
        """
        # TODO: Remove path traversal patterns (../, ..\, /)
        # TODO: Keep only the base filename
        import os
        # Remove any path components
        sanitized = os.path.basename(filename)
        # Remove dangerous characters
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', sanitized)
        return sanitized
    
    @staticmethod
    def escape_html(user_input):
        """
        Escape HTML special characters to prevent XSS
        
        Args:
            user_input (str): Input containing potential HTML
            
        Returns:
            str: HTML-escaped string
        """
        # TODO: Use html.escape() to escape HTML characters
        return html.escape(user_input)
    
    @staticmethod
    def check_sql_injection(user_input):
        """
        Check for common SQL injection patterns
        
        Args:
            user_input (str): Input to check
            
        Returns:
            bool: True if suspicious patterns found, False otherwise
        """
        # TODO: Check if input contains SQL keywords
        # Convert to uppercase for comparison
        upper_input = user_input.upper()
        for keyword in InputSanitizer.SQL_KEYWORDS:
            if keyword in upper_input:
                return True
        return False
