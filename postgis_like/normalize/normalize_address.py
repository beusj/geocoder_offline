"""
Main address normalization function.
"""

import re
from typing import Optional
from .data_structures import NormAddress
from .lookup_tables import (
    DIRECTION_LOOKUP,
    STREET_TYPE_LOOKUP,
    SECONDARY_UNIT_LOOKUP,
)
from .state_extract import state_extract
from .location_extract import location_extract
from .utils import cull_null


def normalize_address(raw_input: str) -> NormAddress:
    """
    Parse and normalize a US postal address string.
    
    This function takes an address string and parses it into components:
    - Street number (address)
    - Direction prefix (N, S, E, W, etc.)
    - Street name
    - Street type (St, Ave, Rd, etc.)
    - Direction suffix
    - Internal address (Apt, Suite, etc.)
    - Location (city/town)
    - State
    - Zip code
    
    The US postal address standard is used:
    <Street Number> <Direction Prefix> <Street Name> <Street Type>
    <Direction Suffix> <Internal Address> <Location> <State> <Zip Code>
    
    Args:
        raw_input: The raw address string to parse
        
    Returns:
        NormAddress object with parsed components
    """
    result = NormAddress()
    
    if not raw_input or not raw_input.strip():
        return result
    
    raw_input = raw_input.strip()
    ws = r'[ ,.\t\n\f\r]'
    
    # Extract address number (starts with digit)
    address_match = re.search(r'^([0-9]+[A-Za-z]?\d*)', raw_input)
    if address_match:
        result.address_alphanumeric = address_match.group(1)
        # Extract numeric part only
        numeric_match = re.search(r'^(\d+)', result.address_alphanumeric)
        if numeric_match:
            result.address = int(numeric_match.group(1))
    
    # Extract zip code (5 digits or 5+4 format)
    zip_match = re.search(r'\b(\d{5})(?:-(\d{4}))?\b(?:\s*$)', raw_input)
    if zip_match:
        result.zip = zip_match.group(1)
        result.zip4 = zip_match.group(2)
        # Remove zip from string
        raw_input = raw_input[:zip_match.start()].strip()
    
    # Extract state
    state_info = state_extract(raw_input)
    if state_info:
        parts = state_info.split(':')
        if len(parts) == 2:
            state_text, result.stateAbbrev = parts
            # Remove state from string (from the end)
            pattern = re.escape(state_text) + r'\s*$'
            raw_input = re.sub(pattern, '', raw_input, flags=re.IGNORECASE).strip()
    
    # Now work with what's left (street level address and possibly location)
    full_street = raw_input
    
    # Check for comma-separated location
    if ',' in full_street:
        parts = full_street.rsplit(',', 1)
        if len(parts) == 2:
            full_street = parts[0].strip()
            potential_location = parts[1].strip()
            # Check if this looks like a location (not an apartment number)
            if not re.match(r'^(APT|SUITE|UNIT|#)\s*\d+', potential_location, re.IGNORECASE):
                result.location = potential_location
    
    # Remove address number from full_street if present
    if result.address_alphanumeric:
        pattern = r'^' + re.escape(result.address_alphanumeric) + r'\s+'
        full_street = re.sub(pattern, '', full_street, flags=re.IGNORECASE).strip()
    
    # Extract secondary unit (apartment, suite, etc.)
    for unit in SECONDARY_UNIT_LOOKUP:
        pattern = r'\b(' + re.escape(unit["name"]) + r')(?:\s+#?\s*([0-9A-Za-z-]+))?\b'
        match = re.search(pattern, full_street, re.IGNORECASE)
        if match:
            result.internal = match.group(0).strip()
            # Remove from full_street
            full_street = full_street[:match.start()] + ' ' + full_street[match.end():]
            full_street = full_street.strip()
            break
    
    # Extract street type
    street_type_found = None
    street_type_abbrev = None
    is_highway = False
    
    # Sort by length (longest first) to match "STATE HIGHWAY" before "HIGHWAY"
    sorted_types = sorted(STREET_TYPE_LOOKUP, key=lambda x: len(x["name"]), reverse=True)
    
    for st_type in sorted_types:
        # Look for street type as whole word
        pattern = r'\b(' + re.escape(st_type["name"]) + r')\b'
        match = re.search(pattern, full_street, re.IGNORECASE)
        if match:
            street_type_found = match.group(1)
            street_type_abbrev = st_type["abbrev"]
            is_highway = st_type["is_hw"]
            result.streetTypeAbbrev = street_type_abbrev
            
            # For highways, the number often comes after the type
            if is_highway:
                # Look for number after highway type
                remaining = full_street[match.end():].strip()
                num_match = re.match(r'^(\d+[A-Za-z]?)', remaining)
                if num_match:
                    result.streetName = num_match.group(1)
                    # Remove everything up to and including the street name
                    full_street = remaining[num_match.end():].strip()
                else:
                    # No number found, remove street type from consideration
                    full_street = full_street[:match.start()] + ' ' + full_street[match.end():]
                    full_street = full_street.strip()
            else:
                # Regular street: name comes before type
                # Everything before the type is the street name (possibly with direction)
                before_type = full_street[:match.start()].strip()
                after_type = full_street[match.end():].strip()
                
                # Check for post direction after type
                for direction in sorted(DIRECTION_LOOKUP, key=lambda x: len(x["name"]), reverse=True):
                    dir_pattern = r'^(' + re.escape(direction["name"]) + r')\b'
                    dir_match = re.search(dir_pattern, after_type, re.IGNORECASE)
                    if dir_match:
                        result.postDirAbbrev = direction["abbrev"]
                        after_type = after_type[dir_match.end():].strip()
                        break
                
                # Check for pre direction before street name
                for direction in sorted(DIRECTION_LOOKUP, key=lambda x: len(x["name"]), reverse=True):
                    dir_pattern = r'^(' + re.escape(direction["name"]) + r')\b'
                    dir_match = re.search(dir_pattern, before_type, re.IGNORECASE)
                    if dir_match:
                        result.preDirAbbrev = direction["abbrev"]
                        before_type = before_type[dir_match.end():].strip()
                        break
                
                result.streetName = before_type
                full_street = after_type
            
            break
    
    # If no street type found, try to extract street name and directions
    if not street_type_found:
        # Check for directions at the beginning (pre-direction)
        for direction in sorted(DIRECTION_LOOKUP, key=lambda x: len(x["name"]), reverse=True):
            dir_pattern = r'^(' + re.escape(direction["name"]) + r')\b'
            dir_match = re.search(dir_pattern, full_street, re.IGNORECASE)
            if dir_match:
                result.preDirAbbrev = direction["abbrev"]
                full_street = full_street[dir_match.end():].strip()
                break
        
        # Check for directions at the end (post-direction)
        for direction in sorted(DIRECTION_LOOKUP, key=lambda x: len(x["name"]), reverse=True):
            dir_pattern = r'\b(' + re.escape(direction["name"]) + r')$'
            dir_match = re.search(dir_pattern, full_street, re.IGNORECASE)
            if dir_match:
                result.postDirAbbrev = direction["abbrev"]
                full_street = full_street[:dir_match.start()].strip()
                break
        
        # What remains is the street name
        if full_street:
            result.streetName = full_street.strip()
    
    # Try to extract location if not already found
    if not result.location and full_street:
        result.location = location_extract(full_street, result.stateAbbrev)
    
    # Clean up all fields
    if result.streetName:
        result.streetName = result.streetName.strip()
    if result.location:
        result.location = result.location.strip()
    if result.internal:
        result.internal = result.internal.strip()
    
    # Mark as successfully parsed if we found at least an address or street name
    result.parsed = bool(result.address or result.streetName or result.zip)
    
    return result
