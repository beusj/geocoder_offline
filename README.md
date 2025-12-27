# Offline Geocoding

Inspired by other projects including PostGIS and DeGAUSS, this is an attempt to collect methods and tools for offline geocoding, particularly in the clinical space, where HIPAA compliance is critical.

## Features

### Address Normalization (postgis_like)

Python implementation of PostGIS tiger_geocoder normalize functions for parsing and standardizing US postal addresses.

**Key capabilities:**
- Parse addresses into standardized components (street number, name, type, city, state, ZIP)
- Handle directional prefixes/suffixes (N, S, E, W, etc.)
- Extract internal addresses (Apt, Suite, etc.)
- Normalize street types and state abbreviations
- Support ZIP+4 format
- Format addresses to USPS standards

**Quick Example:**
```python
from postgis_like import normalize_address, pprint_addy

# Parse an address
address = normalize_address("123 N Main St Apt 5, Springfield, IL 62701")

# Access components
print(address.streetName)  # "Main"
print(address.stateAbbrev)  # "IL"

# Format to standard string
print(pprint_addy(address))  # "123 N Main ST, APT 5, Springfield, IL 62701"
```

See [postgis_like/normalize/README.md](postgis_like/normalize/README.md) for detailed documentation.

## Installation

```bash
pip install -e .
```

## Testing

```bash
python -m unittest discover tests
```

## Project Structure

```
geocoder_offline/
├── postgis_like/          # PostGIS-like functionality
│   └── normalize/         # Address normalization
│       ├── normalize_address.py  # Main parsing function
│       ├── pprint_addy.py       # Address formatting
│       ├── lookup_tables.py      # Standard abbreviations
│       └── utils.py              # Helper functions
└── tests/                 # Unit tests
```

## References

- PostGIS Tiger Geocoder: https://github.com/postgis/postgis/tree/master/extras/tiger_geocoder
- USPS Address Standards: https://pe.usps.com/text/pub28/welcome.htm
