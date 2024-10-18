import os
import pytest
import pyperclip
import random
import sys
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../SRC')))
from Utilities import generate_password, password_strength

def test_generate_password_length():
    password = generate_password()
    assert 10 <= len(password) <= 12  # Password length should be between 10 and 12

def test_generate_password_content():
    password = generate_password()
    assert any(char.islower() for char in password)  # At least one lowercase letter
    assert any(char.isupper() for char in password)  # At least one uppercase letter
    assert any(char.isdigit() for char in password)  # At least one digit
    assert any(char in '!@#$%^&*()' for char in password)  # At least one symbol

def test_generate_password_pyperclip_copy():
    with patch("pyperclip.copy") as mock_copy:
        password = generate_password()
        mock_copy.assert_called_once_with(password)

@pytest.mark.parametrize("password, expected", [
    ("abc", "WEAK"),           # Length < 6
    ("abcdef", "MEDIUM"),      # No uppercase or digit
    ("Abcdef", "MEDIUM"),      # No digit
    ("Abc123", "STRONG"),      # Has uppercase and digit
])
def test_password_strength(password, expected):
    assert password_strength(password) == expected