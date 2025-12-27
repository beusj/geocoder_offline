# Address Normalization

This module implements address normalization functionality similar to PostGIS tiger_geocoder's normalize functions.

## Features

- Parse US postal addresses into standardized components
- Extract and normalize:
  - Street numbers (including alphanumeric like "123A")
  - Directional prefixes and suffixes (N, S, E, W, etc.)
  - Street names
  - Street types (St, Ave, Rd, etc.)
  - Internal addresses (Apt, Suite, etc.)
  - City/location names
  - State abbreviations
  - ZIP codes (including ZIP+4 format)

## Usage

```python
from postgis_like import normalize_address, pprint_addy

# Parse an address
address = normalize_address("123 N Main St, Springfield, IL 62701")

# Access parsed components
print(f"Street Number: {address.address}")
print(f"Street Name: {address.streetName}")
print(f"Street Type: {address.streetTypeAbbrev}")
print(f"City: {address.location}")
print(f"State: {address.stateAbbrev}")
print(f"ZIP: {address.zip}")

# Format back to standardized string
formatted = pprint_addy(address)
print(f"Formatted: {formatted}")
```

## Examples

```python
# Simple address
normalize_address("456 Oak Ave")
# -> address=456, streetName="Oak", streetTypeAbbrev="AVE"

# With directions
normalize_address("789 N Elm St E")
# -> preDirAbbrev="N", streetName="Elm", postDirAbbrev="E"

# With apartment
normalize_address("321 Park Blvd Apt 5B, Boston, MA 02101")
# -> internal="Apt 5B", location="Boston", stateAbbrev="MA"

# Highway address
normalize_address("State Highway 101")
# -> streetName="101", streetTypeAbbrev="SR"

# Complete address
normalize_address("100 W First Ave Apt 2, New York, NY 10001-1234")
# -> Full parsing with all components
```

## Implementation Notes

This is a Python implementation inspired by PostGIS tiger_geocoder normalize functions:
https://github.com/postgis/postgis/tree/master/extras/tiger_geocoder/normalize

The implementation uses:
- Regular expressions for pattern matching
- Lookup tables for directions, street types, secondary units, and states
- Fuzzy matching for state name variations
- Standardized abbreviations following USPS guidelines

## Limitations

- Location (city/town) extraction is simplified and may not match all cases
- Does not include full place/county lookup tables (would require extensive geographic data)
- State extraction uses fuzzy matching but may not catch all variations
- Street name validation is not performed

## Testing

Run tests with:

```bash
python -m unittest tests.test_normalize
```
