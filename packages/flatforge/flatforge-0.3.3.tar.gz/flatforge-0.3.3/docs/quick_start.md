# FlatForge Quick Start Guide

## Introduction

FlatForge is a Python library for validating, transforming, and processing flat files (CSV, fixed-length, etc.). This quick start guide will help you get up and running with FlatForge v0.3.0, focusing on key features and examples.

## Installation

```bash
pip install flatforge
```

## Basic Usage

FlatForge uses YAML configuration files to define how your data should be validated and transformed. Here's a simple example:

```bash
# Validate a CSV file
flatforge validate --config config/employee.yaml --input data/employee.csv --output data/valid.csv --error data/errors.csv

# Transform a file from one format to another
flatforge transform --config config/transform.yaml --input data/input.csv --output data/output.txt --error data/errors.csv

# Process a file (validate and transform)
flatforge process --config config/process.yaml --input data/input.csv --output data/output.csv --error data/errors.csv
```

## Configuration File Structure

A basic FlatForge configuration file looks like this:

```yaml
file_format:
  type: csv
  delimiter: ","
  has_header: true

fields:
  - name: employee_id
    start_pos: 0
    length: 10
    rules:
      - type: required
      - type: string_length
        min: 5
        max: 10

  - name: first_name
    start_pos: 10
    length: 20
    rules:
      - type: required
    transformers:
      - type: trim
      - type: case
        case: upper

global_rules:
  - type: uniqueness
    fields: [employee_id]
```

## Key Features

### 1. Validation Rules

FlatForge supports various validation rules:

#### Required Field
```yaml
- type: required
```

#### String Length
```yaml
- type: string_length
  min: 5
  max: 10
```

#### Numeric Range
```yaml
- type: numeric_range
  min: 0
  max: 100
```

#### Date Format
```yaml
- type: date_format
  format: "%Y-%m-%d"
```

#### Regular Expression
```yaml
- type: regex
  pattern: "^[A-Z]{2}\\d{4}$"
```

#### Checksum Validation
```yaml
- type: checksum
  algorithm: sha256
  checksum_field: hash_value
  source_fields: [field1, field2, field3]
```

#### Luhn Algorithm (Credit Card Validation)
```yaml
- type: luhn
  message: "Invalid credit card number"
```

#### GUID Validation
```yaml
- type: guid
  message: "Invalid GUID format"
```

### 2. Transformation Rules

#### Trim
```yaml
transformers:
  - type: trim
```

#### Case Conversion
```yaml
transformers:
  - type: case
    case: upper  # Options: upper, lower, title
```

#### Padding
```yaml
transformers:
  - type: pad
    side: left  # Options: left, right
    char: "0"
    length: 10
```

#### Date Format Conversion
```yaml
transformers:
  - type: date_format
    input_format: "%m/%d/%Y"
    output_format: "%Y-%m-%d"
```

#### Substring
```yaml
transformers:
  - type: substring
    start: 0
    length: 5
```

#### Replace
```yaml
transformers:
  - type: replace
    pattern: "\\s+"
    replacement: "_"
```

#### Value Resolver
```yaml
transformers:
  - type: value_resolver
    mapping:
      "01": "Active"
      "02": "Inactive"
      "03": "Pending"
    default: "Unknown"
```

#### Field Masking
```yaml
transformers:
  - type: mask
    type: credit_card  # Predefined mask for credit cards
    # Or custom mask:
    # pattern: "XXXX-XXXX-XXXX-####"  # # shows original digits, X masks
```

#### GUID Generation
```yaml
transformers:
  - type: guid_generator
    version: 4  # UUID version to generate, defaults to 4
```

### 3. Global Rules

Global rules validate relationships between records:

#### Uniqueness Validation
```yaml
global_rules:
  - type: uniqueness
    fields: [employee_id]
    # Or composite key:
    # fields: [department_id, employee_id]
```

#### Record Count Validation
```yaml
global_rules:
  - type: count
    count_field: record_count  # Field in header that contains the expected count
    count_type: all  # Options: all, detail, specific_type
    # For specific_type:
    # record_type: "D"
    # record_type_field: record_indicator
```

#### Sum Validation
```yaml
global_rules:
  - type: sum
    sum_field: total_amount  # Field in header/trailer that contains the expected sum
    source_field: amount  # Field to sum across records
    # Optional filters:
    # record_type: "D"
    # record_type_field: record_indicator
```

### 4. File Settings

Control file-level options:

```yaml
file_settings:
  input_encoding: "ISO-8859-1"
  output_encoding: "UTF-8"
```

## Example: Credit Card Processing

This example validates credit card data using the Luhn algorithm and masks card numbers:

```yaml
file_format:
  type: csv
  delimiter: ","
  has_header: true

fields:
  - name: card_number
    rules:
      - type: required
      - type: luhn
        message: "Invalid credit card number"
    transformers:
      - type: mask
        type: credit_card

  - name: expiry_date
    rules:
      - type: required
      - type: date_format
        format: "%m/%Y"

  - name: card_type
    rules:
      - type: required
    transformers:
      - type: value_resolver
        mapping:
          "V": "Visa"
          "M": "Mastercard"
          "A": "American Express"
        default: "Unknown"
```

## Example: GUID Generation for User Records

This example validates user data and generates GUIDs for new records:

```yaml
file_format:
  type: csv
  delimiter: ","
  has_header: true

fields:
  - name: user_id
    rules:
      - type: required
      
  - name: email
    rules:
      - type: required
      - type: regex
        pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        message: "Invalid email format"
        
  - name: guid
    rules:
      - type: guid
        allow_empty: true  # Allow empty for new records
    transformers:
      - type: guid_generator
        # Only generate if field is empty
        condition: "field_value == ''"

global_rules:
  - type: uniqueness
    fields: [email]
```

## Example: Multi-Column Checksum Validation

This example validates orders using SHA256 checksum across multiple fields:

```yaml
file_format:
  type: csv
  delimiter: ","
  has_header: true

fields:
  - name: customer_id
    rules:
      - type: required
      
  - name: order_id
    rules:
      - type: required
      
  - name: amount
    rules:
      - type: required
      - type: numeric_range
        min: 0
        
  - name: checksum
    rules:
      - type: required
      - type: checksum
        algorithm: sha256
        source_fields: [customer_id, order_id, amount]
```

## Running the Sample Test Script

FlatForge includes a comprehensive test script that demonstrates all features:

```bash
# Test all features
python samples/test_new_features_v0.3.0_20250330.py

# Test specific features
python samples/test_new_features_v0.3.0_20250330.py --feature checksum
python samples/test_new_features_v0.3.0_20250330.py --feature credit_card
python samples/test_new_features_v0.3.0_20250330.py --feature guid
python samples/test_new_features_v0.3.0_20250330.py --feature encoding
```

## More Resources

- [User Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/README.md)
- [Rules Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/rules_guide.md)
- [CLI Examples](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/cli_examples.md)
- [Testing Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/testing/README.md) 