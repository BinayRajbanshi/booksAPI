# validators.py
import re
from typing import Optional

def validate_username(username: Optional[str]) -> Optional[str]:
    """
    Validate username format.
    Args:
        username: Username string to validate
    Returns:
        Validated username
    Raises:
        ValueError: If username format is invalid
    """
    if username is None:
        return username
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValueError('Username must be alphanumeric, and may include underscores and hyphens')
    return username

def validate_password(password: str) -> str:
    """
    Validate password strength.
    Args:
        password: Password string to validate
    Returns:
        Validated password
    Raises:
        ValueError: If password doesn't meet strength requirements
    """
    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', password):
        raise ValueError('Password must contain at least one digit')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError('Password must contain at least one special character')
    return password

def validate_phone(phone: Optional[str]) -> Optional[str]:
    """
    Validate phone number format.
    Args:
        phone: Phone number string to validate
    Returns:
        Validated and formatted phone number
    Raises:
        ValueError: If phone number format is invalid
    """
    if phone is None:
        return phone
    # Remove any spaces, dashes, or parentheses
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if the number contains only digits
    if not cleaned_phone.isdigit():
        raise ValueError('Phone number must contain only digits, spaces, dashes, or parentheses')
    # Check length after removing formatting
    if not (10 <= len(cleaned_phone) <= 15):
        raise ValueError('Phone number must be between 10 and 15 digits')
    return cleaned_phone