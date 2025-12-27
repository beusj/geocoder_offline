# Implementation Comparison: Ruby → Python

This document shows the mapping between the Ruby implementation from DeGAUSS and the Python implementation in `degauss_like`.

## File Structure

| Ruby (degauss-org/geocoder) | Python (degauss_like) | Status |
|------------------------------|----------------------|--------|
| `lib/geocoder/us/numbers.rb` | `numbers.py` | ✓ Complete |
| `lib/geocoder/us/constants.rb` | `constants.py` | ✓ Complete |
| `lib/geocoder/us/address.rb` | `address.py` | ✓ Complete |
| N/A | `__init__.py` | ✓ Added (Python package) |

## Class/Module Mapping

### Numbers Module

| Ruby | Python | Notes |
|------|--------|-------|
| `NumberMap` class | `NumberMap` class | Inherits from `Hash` (Ruby) / `dict` (Python) |
| `Cardinals` constant | `Cardinals` constant | Maps cardinal numbers to words |
| `Ordinals` constant | `Ordinals` constant | Maps ordinal numbers to words |

### Constants Module

| Ruby | Python | Notes |
|------|--------|-------|
| `Map` class | `Map` class | Bidirectional mapping with regex support |
| `Directional` | `Directional` | Compass directions |
| `Prefix_Qualifier` | `Prefix_Qualifier` | Feature prefix qualifiers |
| `Suffix_Qualifier` | `Suffix_Qualifier` | Feature suffix qualifiers |
| `Prefix_Type` | `Prefix_Type` | Street type prefixes |
| `Suffix_Type` | `Suffix_Type` | Street type suffixes |
| `Unit_Type` | `Unit_Type` | Unit type abbreviations |
| `Std_Abbr` | `Std_Abbr` | Standard abbreviations |
| `Name_Abbr` | `Name_Abbr` | Toponym abbreviations |
| `State` | `State` | US state/territory mappings |

### Address Class

| Ruby Method/Attribute | Python Method/Attribute | Status |
|-----------------------|-------------------------|--------|
| `initialize(text)` | `__init__(text)` | ✓ |
| `clean(value)` | `_clean(value)` | ✓ |
| `assign_text_to_address(text)` | `_assign_text_to_address(text)` | ✓ |
| `expand_numbers(string)` | `_expand_numbers(string)` | ✓ |
| `parse_zip(regex_match, text)` | `_parse_zip(regex_match, text)` | ✓ |
| `parse_state(regex_match, text)` | `_parse_state(regex_match, text)` | ✓ |
| `parse_number(regex_match, text)` | `_parse_number(regex_match, text)` | ✓ |
| `parse` | `_parse()` | ✓ |
| `expand_streets(street)` | `_expand_streets(streets)` | ✓ |
| `street_parts` | `_street_parts()` | ✓ |
| `remove_noise_words(strings)` | `_remove_noise_words(strings)` | ✓ |
| `city_parts` | `city_parts()` | ✓ |
| `city=(strings)` | `set_city(city_strings)` | ✓ (renamed) |
| `po_box?` | `po_box()` | ✓ |
| `intersection?` | `intersection()` | ✓ |
| N/A | `__repr__()` | ✓ Added (Python convention) |

### Attributes

| Ruby | Python | Notes |
|------|--------|-------|
| `@text` | `self.text` | Original address text |
| `@prenum` | `self.prenum` | Pre-number component |
| `@number` | `self.number` | Street number |
| `@sufnum` | `self.sufnum` | Suffix number component |
| `@street` | `self.street` | Street name variations (list) |
| `@city` | `self.city` | City name variations (list) |
| `@state` | `self.state` | State abbreviation |
| `@zip` | `self.zip` | ZIP code |
| `@plus4` | `self.plus4` | ZIP+4 extension |
| `@full_state` | `self._full_state` | Full state name (private) |

## Regular Expression Patterns

| Ruby | Python | Status |
|------|--------|--------|
| `Match[:number]` | `Match['number']` | ✓ |
| `Match[:street]` | `Match['street']` | ✓ |
| `Match[:city]` | `Match['city']` | ✓ |
| `Match[:state]` | `Match['state']` | ✓ |
| `Match[:zip]` | `Match['zip']` | ✓ |
| `Match[:at]` | `Match['at']` | ✓ |
| `Match[:po_box]` | `Match['po_box']` | ✓ |

## Key Differences

1. **Method Naming**: Python uses `snake_case` consistently, private methods prefixed with `_`
2. **Boolean Methods**: Ruby's `?` suffix becomes regular method names in Python (e.g., `po_box?` → `po_box()`)
3. **Setter Methods**: Ruby's `city=` becomes `set_city()` in Python
4. **String Representation**: Added `__repr__()` for Pythonic object representation
5. **Dictionary Access**: Ruby uses symbols (`:key`), Python uses strings (`'key'`)
6. **Regular Expressions**: Ruby's `/pattern/io` becomes `re.compile(r'pattern', re.IGNORECASE)`

## Test Coverage

All major functionality from the Ruby implementation is tested:
- ✓ Basic address parsing
- ✓ State name/abbreviation handling
- ✓ ZIP code extraction
- ✓ Street abbreviation expansion
- ✓ Number word expansion (cardinals and ordinals)
- ✓ PO Box detection
- ✓ Intersection detection
- ✓ Dictionary input parsing
- ✓ Error handling

## Not Implemented

The following files from the Ruby implementation are NOT ported (as they were not in the core address parsing module):
- `database.rb` - Database geocoding functionality
- `metaphone.rb` - Metaphone phonetic algorithm
- `rest.rb` - REST API interface

These components are specific to the geocoding service and not part of the address parsing functionality requested.
