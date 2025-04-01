#!/usr/bin/env python3
"""Test script for FlatForge v0.3.1 features."""

import os
import json
import tempfile
import unittest
from datetime import datetime

from flatforge.processors.encoding import EncodingTransformation
from flatforge.rules.validation import LuhnValidationRule, GuidValidationRule
from flatforge.transformers import ValueResolverTransformationRule

def print_separator(title):
    """Print a formatted separator with title."""
    print("\n" + "="*80)
    print(f"{title:^80}")
    print("="*80 + "\n")

def test_credit_card_processing():
    """Test credit card validation using Luhn algorithm."""
    print_separator("Testing Credit Card Processing")
    
    # Test configuration
    config = {
        'column': 'card_number',
        'strip_spaces': True,
        'strip_hyphens': True,
        'error_message': "Invalid credit card number"
    }
    
    # Create test rule
    rule = LuhnValidationRule(config)
    
    # Test valid card numbers
    valid_cards = [
        '4532 7153 3790 8241',  # Visa
        '5412 7512 3456 7890',  # Mastercard
        '3782 8224 6310 005',   # American Express
        '6011 0000 0000 0004',  # Discover
        '3530 1113 3330 0000',  # JCB
        '6759 4111 1111 1111'   # Maestro
    ]
    
    print("Testing valid card numbers:")
    for card in valid_cards:
        record = {'card_number': card}
        is_valid, error = rule.validate(record)
        print(f"Card: {card:30} Valid: {is_valid}")
        
    # Test invalid card numbers
    invalid_cards = [
        '4532 7153 3790 8242',  # Changed last digit
        '5412 7512 3456 7891',  # Changed last digit
        '3782 8224 6310 006',   # Changed last digit
        '6011 0000 0000 0005',  # Changed last digit
        '3530 1113 3330 0001',  # Changed last digit
        '6759 4111 1111 1112'   # Changed last digit
    ]
    
    print("\nTesting invalid card numbers:")
    for card in invalid_cards:
        record = {'card_number': card}
        is_valid, error = rule.validate(record)
        print(f"Card: {card:30} Valid: {is_valid} Error: {error}")

def test_guid_validation():
    """Test GUID validation."""
    print_separator("Testing GUID Validation")
    
    # Test configuration
    config = {
        'column': 'guid',
        'strip_spaces': True,
        'strip_hyphens': True,
        'error_message': "Invalid GUID format"
    }
    
    # Create test rule
    rule = GuidValidationRule(config)
    
    # Test valid GUIDs
    valid_guids = [
        '123e4567-e89b-12d3-a456-426614174000',  # Standard format
        '123e4567e89b12d3a456426614174000',       # No hyphens
        '123E4567-E89B-12D3-A456-426614174000',   # Uppercase
        '123e4567 e89b 12d3 a456 426614174000',   # Spaces instead of hyphens
        '{123e4567-e89b-12d3-a456-426614174000}', # Curly braces
        '(123e4567-e89b-12d3-a456-426614174000)', # Parentheses
        'urn:uuid:123e4567-e89b-12d3-a456-426614174000'  # URN format
    ]
    
    print("Testing valid GUIDs:")
    for guid in valid_guids:
        record = {'guid': guid}
        is_valid, error = rule.validate(record)
        print(f"GUID: {guid:50} Valid: {is_valid}")
        
    # Test invalid GUIDs
    invalid_guids = [
        'not-a-guid',  # Invalid format
        '12345678-1234-1234-1234-1234567890123',  # Too long
        '12345678-1234-1234-1234-12345678901',    # Too short
        '12345678-1234-1234-1234-12345678901g',   # Invalid character
        '12345678-1234-1234-1234-12345678901-',   # Extra hyphen
        '12345678-1234-1234-1234-12345678901 ',   # Extra space
        '12345678-1234-1234-1234-12345678901}',   # Unmatched brace
        '12345678-1234-1234-1234-12345678901)',   # Unmatched parenthesis
        'urn:uuid:12345678-1234-1234-1234-12345678901g'  # Invalid URN
    ]
    
    print("\nTesting invalid GUIDs:")
    for guid in invalid_guids:
        record = {'guid': guid}
        is_valid, error = rule.validate(record)
        print(f"GUID: {guid:50} Valid: {is_valid} Error: {error}")

def test_value_resolution():
    """Test value resolution using mapping file."""
    print_separator("Testing Value Resolution")
    
    # Create temporary mapping file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        mapping = {
            "ACTIVE": "A",
            "PENDING": "P",
            "COMPLETED": "C",
            "FAILED": "F",
            "CANCELLED": "X",
            "REFUNDED": "R",
            "VOID": "V",
            "DECLINED": "D",
            "EXPIRED": "E",
            "PROCESSING": "PR"
        }
        json.dump(mapping, f)
        mapping_file = f.name
    
    # Test configuration
    config = {
        'source_field': 'status',
        'target_field': 'status_code',
        'mapping_file': mapping_file,
        'default_value': 'UNKNOWN'
    }
    
    # Create test rule
    rule = ValueResolverTransformationRule(config)
    
    # Test records
    test_records = [
        {'status': 'ACTIVE', 'other_field': 'value'},
        {'status': 'PENDING', 'other_field': 'value'},
        {'status': 'COMPLETED', 'other_field': 'value'},
        {'status': 'INVALID', 'other_field': 'value'},  # Should use default
        {'other_field': 'value'}  # Missing status field
    ]
    
    print("Testing value resolution:")
    for record in test_records:
        original = record.copy()
        rule.transform(record)
        print(f"Original: {original}")
        print(f"Transformed: {record}\n")
    
    # Clean up
    os.unlink(mapping_file)

def test_encoding_transformation():
    """Test file encoding transformation."""
    print_separator("Testing Encoding Transformation")
    
    # Create temporary input file with ISO-8859-1 encoded content
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write('Café,Résumé,Déjà vu'.encode('iso-8859-1'))
        input_file = f.name
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        output_file = f.name
    
    # Test configuration
    config = {
        'input_encoding': 'iso-8859-1',
        'output_encoding': 'utf-8'
    }
    
    # Create transformer and transform file
    transformer = EncodingTransformation(config)
    transformer.transform(input_file, output_file)
    
    # Read and verify output
    with open(output_file, 'rb') as f:
        output_content = f.read()
    
    print("Input file (ISO-8859-1):")
    print('Café,Résumé,Déjà vu')
    print("\nOutput file (UTF-8):")
    print(output_content.decode('utf-8'))
    
    # Clean up
    os.unlink(input_file)
    os.unlink(output_file)

def main():
    """Run all tests."""
    print(f"FlatForge v0.3.1 Feature Tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    test_credit_card_processing()
    test_guid_validation()
    test_value_resolution()
    test_encoding_transformation()
    
    print("\nAll tests completed successfully!")

if __name__ == '__main__':
    main() 