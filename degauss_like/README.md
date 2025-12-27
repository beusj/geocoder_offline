# degauss_like - US Address Parser

A Python implementation of the address parser from the [DeGAUSS project](https://github.com/degauss-org/geocoder/tree/master/lib/geocoder/us). This parser extracts structured components from US street addresses and place names.

## Features

- Parses US street addresses into structured components
- Handles various address formats and abbreviations
- Expands street type abbreviations (St → Street, Ave → Avenue, etc.)
- Recognizes state names and abbreviations
- Extracts ZIP codes (including ZIP+4 format)
- Detects PO Boxes and intersections
- Handles number words (One, First, etc.)

## Installation

The module is self-contained with no external dependencies. Simply import it:

```python
from degauss_like import Address
```

## Usage

### Basic Example

```python
from degauss_like import Address

# Parse a simple address
addr = Address("1600 Pennsylvania Avenue NW, Washington, DC 20500")

print(f"Number: {addr.number}")      # 1600
print(f"Street: {addr.street}")      # ['pennsylvania avenue nw', 'pennsylvania ave nw', ...]
print(f"City: {addr.city}")          # ['washington']
print(f"State: {addr.state}")        # DC
print(f"ZIP: {addr.zip}")            # 20500
```

### More Examples

```python
# Parse address with full state name
addr = Address("350 Fifth Avenue, New York, New York 10118")
print(addr)  # Address(number=350, street=['fifth avenue', '5th avenue', ...], city=['new york'], state=NY, zip=10118)

# Simple street address
addr = Address("123 Main St")
print(f"Number: {addr.number}")  # 123
print(f"Street: {addr.street}")  # ['main st', 'main street']

# Check for PO Box
addr = Address("PO Box 123, Springfield, IL 62701")
print(addr.po_box())  # True

# Check for intersection
addr = Address("Main St at Elm St")
print(addr.intersection())  # True

# Parse from dictionary
addr = Address({
    'number': '123',
    'street': 'Main Street',
    'city': 'Springfield',
    'state': 'IL',
    'postal_code': '62701'
})
print(f"State: {addr.state}")  # IL
```

## Address Components

The `Address` class provides the following attributes:

- `text`: Original address text
- `number`: Street number
- `prenum`: Pre-number component (e.g., "A" in "A123")
- `sufnum`: Suffix number component (e.g., "B" in "123B")
- `street`: List of street name variations (with abbreviations expanded)
- `city`: List of city name variations
- `state`: Two-letter state abbreviation
- `zip`: 5-digit ZIP code
- `plus4`: ZIP+4 extension (if provided)

## Methods

- `po_box()`: Returns `True` if the address is a PO Box
- `intersection()`: Returns `True` if the address is an intersection
- `city_parts()`: Returns all possible city name substrings
- `set_city(city_strings)`: Removes city name from street strings

## How It Works

The parser uses regular expressions and lookup tables to:

1. Extract ZIP codes from the end of the address
2. Extract state names/abbreviations from the end
3. Extract street numbers from the beginning
4. Parse remaining text for street and city names
5. Expand abbreviations into their full forms
6. Generate variations of each component

The parser is based on USPS standards and TIGER/Line technical documentation, supporting:
- Standard street type abbreviations
- Directional prefixes and suffixes (N, South, NW, etc.)
- State and territory names
- Cardinal and ordinal number words

## Based On

This implementation is a Python port of the Ruby address parser from:
https://github.com/degauss-org/geocoder/tree/master/lib/geocoder/us

The Ruby version is part of the DeGAUSS (Decentralized Geomarker Assessment for Multi-Site Studies) project, which provides HIPAA-compliant geocoding tools for clinical research.

## License

This implementation follows the structure and logic of the original Ruby implementation from the DeGAUSS project.
