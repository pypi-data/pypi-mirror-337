# Transformers

Transformers are used to modify field values during the parsing process. They can be used to:
- Format dates
- Convert case
- Calculate and append check digits
- And more...

## Available Transformers

### Luhn Transformer

The Luhn transformer calculates and appends a check digit to a numeric value using the Luhn algorithm. This is commonly used for credit card numbers and other identification numbers.

**Parameters:**
- `name`: The name of the transformer
- `input_field`: The field to transform
- `output_field`: The field to store the transformed value

**Example:**
```yaml
transformers:
  - name: "card_number_luhn"
    type: "luhn"
    input_field: "card_number"
    output_field: "card_number_with_check"
    description: "Appends Luhn check digit to card number"
```

**Input/Output:**
- Input: "453201511283036"
- Output: "4532015112830366" (6 is the check digit)

**Notes:**
- The input value must contain at least one digit
- Non-digit characters (spaces, dashes) are preserved in the output
- The resulting number will be a valid Luhn number

### Case Transformer

The case transformer converts text to uppercase or lowercase.

**Parameters:**
- `name`: The name of the transformer
- `input_field`: The field to transform
- `output_field`: The field to store the transformed value
- `case`: Either "upper" or "lower"

**Example:**
```yaml
transformers:
  - name: "uppercase"
    type: "case"
    input_field: "name"
    output_field: "name_upper"
    case: "upper"
    description: "Converts name to uppercase"
```

### Date Transformer

The date transformer reformats dates between different formats.

**Parameters:**
- `name`: The name of the transformer
- `input_field`: The field to transform
- `output_field`: The field to store the transformed value
- `input_format`: The format of the input date
- `output_format`: The desired output format

**Example:**
```yaml
transformers:
  - name: "date_format"
    type: "date"
    input_field: "transaction_date"
    output_field: "formatted_date"
    input_format: "%Y%m%d"
    output_format: "%Y-%m-%d"
    description: "Reformats date from YYYYMMDD to YYYY-MM-DD"
```

## Using Transformers

Transformers are defined in the configuration file and are applied during the parsing process. They can be used to:

1. Validate data by ensuring it meets certain format requirements
2. Normalize data by converting it to a standard format
3. Calculate derived values like check digits
4. Format data for display or storage

To use a transformer:

1. Add it to the `transformers` section of your configuration file
2. Specify the input and output fields
3. Configure any additional parameters required by the transformer

The transformed values will be available in the output field after parsing is complete. 