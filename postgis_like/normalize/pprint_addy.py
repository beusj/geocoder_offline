"""
Pretty print address function.
"""

from .data_structures import NormAddress
from .lookup_tables import STREET_TYPE_LOOKUP
from .utils import cull_null


def is_pretype(street_type_abbrev: str) -> bool:
    """
    Determine if a street type should be placed before the street name.
    This applies to highway-type roads (e.g., "Highway 101" not "101 Highway").
    
    Args:
        street_type_abbrev: The street type abbreviation
        
    Returns:
        True if the type should come before the name
    """
    if not street_type_abbrev:
        return False
    
    for st_type in STREET_TYPE_LOOKUP:
        if st_type["abbrev"].upper() == street_type_abbrev.upper():
            return st_type.get("is_hw", False)
    
    return False


def pprint_addy(address: NormAddress) -> str:
    """
    Format a normalized address as a standardized string.
    
    This creates a human-readable address string from a NormAddress object,
    following USPS formatting standards.
    
    Args:
        address: The normalized address to format
        
    Returns:
        Formatted address string, or empty string if not parsed
    """
    if not address.parsed:
        return ""
    
    result_parts = []
    
    # Address number
    if address.address_alphanumeric:
        result_parts.append(address.address_alphanumeric)
    elif address.address:
        result_parts.append(str(address.address))
    
    # Pre-direction
    if address.preDirAbbrev:
        result_parts.append(address.preDirAbbrev)
    
    # Street type before name (for highways)
    if address.streetTypeAbbrev and is_pretype(address.streetTypeAbbrev):
        result_parts.append(address.streetTypeAbbrev)
    
    # Street name
    if address.streetName:
        result_parts.append(address.streetName)
    
    # Street type after name (for regular streets)
    if address.streetTypeAbbrev and not is_pretype(address.streetTypeAbbrev):
        result_parts.append(address.streetTypeAbbrev)
    
    # Post-direction
    if address.postDirAbbrev:
        result_parts.append(address.postDirAbbrev)
    
    # Join street-level parts
    street_level = ' '.join(result_parts)
    
    # Start building final result
    final_parts = []
    if street_level:
        final_parts.append(street_level)
    
    # Internal address (apartment, suite, etc.)
    if address.internal:
        final_parts.append(address.internal)
    
    # Location (city)
    if address.location:
        final_parts.append(address.location)
    
    # State and zip
    state_zip_parts = []
    if address.stateAbbrev:
        state_zip_parts.append(address.stateAbbrev)
    
    if address.zip:
        zip_str = address.zip
        if address.zip4:
            zip_str += f"-{address.zip4}"
        state_zip_parts.append(zip_str)
    
    if state_zip_parts:
        final_parts.append(' '.join(state_zip_parts))
    
    # Join with commas appropriately
    if len(final_parts) == 0:
        return ""
    elif len(final_parts) == 1:
        return final_parts[0]
    else:
        # First part (street level) doesn't need comma
        result = final_parts[0]
        for part in final_parts[1:]:
            result += ", " + part
        return result
