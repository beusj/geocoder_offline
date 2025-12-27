# Offline Geocoding

Inspired by other projects including postGIS and DeGAUSS, this is an attempt to collect methods and tools for offline geocoding, particularly in the clinical space, where HIPAA compliance is critical.

## Components

### degauss_like - US Address Parser

A Python implementation of the address parser from the [DeGAUSS project](https://github.com/degauss-org/geocoder/tree/master/lib/geocoder/us). This parser extracts structured components from US street addresses and place names.

#### Features

- Parses US street addresses into structured components (number, street, city, state, ZIP)
- Handles various address formats and abbreviations
- Expands street type abbreviations (St → Street, Ave → Avenue, etc.)
- Recognizes state names and abbreviations
- Extracts ZIP codes (including ZIP+4 format)
- Detects PO Boxes and intersections
- Handles number words (One, First, etc.)

#### Quick Start

```python
from degauss_like import Address

# Parse an address
addr = Address("1600 Pennsylvania Avenue NW, Washington, DC 20500")

print(f"Number: {addr.number}")      # 1600
print(f"Street: {addr.street}")      # ['pennsylvania avenue nw', ...]
print(f"City: {addr.city}")          # ['washington']
print(f"State: {addr.state}")        # DC
print(f"ZIP: {addr.zip}")            # 20500
```

#### Documentation

See [degauss_like/README.md](degauss_like/README.md) for detailed documentation and examples.

#### Running Examples

```bash
python examples.py
```

#### Running Tests

```bash
python test_address_parser.py
```

