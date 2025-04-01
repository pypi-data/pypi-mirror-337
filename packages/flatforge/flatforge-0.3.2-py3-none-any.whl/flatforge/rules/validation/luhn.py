"""
Luhn validation rule for FlatForge.

This module contains the LuhnRule class that validates numbers using the Luhn algorithm.
"""
from typing import Dict, List, Optional, Any, Tuple

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class LuhnRule(ValidationRule):
    """Rule that validates numbers using the Luhn algorithm."""
    
    def __init__(self, config: dict):
        """
        Initialize a LuhnRule.
        
        Args:
            config: Configuration dictionary containing:
                - column: The name of the column to validate
                - strip_spaces: Whether to strip spaces from the value
                - strip_hyphens: Whether to strip hyphens from the value
                - error_message: Custom error message to use
        """
        super().__init__(config.get('column', ''), config)
        self.column = config.get('column', '')
        self.strip_spaces = config.get('strip_spaces', True)
        self.strip_hyphens = config.get('strip_hyphens', True)
        self.error_message = config.get('error_message', "Invalid credit card number")
    
    def _is_valid_luhn(self, number: str) -> bool:
        """
        Check if a number is valid according to the Luhn algorithm.
        
        Args:
            number: The number to check
            
        Returns:
            bool: True if the number is valid, False otherwise
        """
        digits = [int(d) for d in str(number)]
        checksum = 0
        is_even = len(digits) % 2 == 0
        
        for i, digit in enumerate(digits):
            if is_even:
                if i % 2 == 0:
                    doubled = digit * 2
                    checksum += doubled if doubled < 10 else doubled - 9
                else:
                    checksum += digit
            else:
                if i % 2 == 1:
                    doubled = digit * 2
                    checksum += doubled if doubled < 10 else doubled - 9
                else:
                    checksum += digit
                    
        return checksum % 10 == 0
    
    def validate(self, record: dict) -> Tuple[bool, str]:
        """
        Validate a number using the Luhn algorithm.
        
        Args:
            record: The record containing the field to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if self.column not in record:
            return False, f"Column '{self.column}' not found"
            
        value = str(record[self.column])
        if self.strip_spaces:
            value = value.replace(" ", "")
        if self.strip_hyphens:
            value = value.replace("-", "")
            
        if not value.isdigit():
            return False, "Credit card number contains non-digit characters"
            
        if len(value) < 13 or len(value) > 19:
            return False, "Invalid credit card number length"
            
        if not self._is_valid_luhn(value):
            return False, self.error_message
            
        return True, "" 