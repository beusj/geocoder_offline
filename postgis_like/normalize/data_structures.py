"""
Core data structures for address normalization.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NormAddress:
    """
    Normalized address structure matching PostGIS norm_addy type.
    
    Attributes:
        address: Street number (numeric)
        address_alphanumeric: Street number with letters (e.g., "123A")
        preDirAbbrev: Pre-directional abbreviation (N, S, E, W, etc.)
        streetName: Name of the street
        streetTypeAbbrev: Street type abbreviation (St, Ave, Rd, etc.)
        postDirAbbrev: Post-directional abbreviation
        internal: Internal address (Apt, Suite, etc.)
        location: City or location name
        stateAbbrev: State abbreviation
        zip: 5-digit zip code
        zip4: 4-digit zip extension
        parsed: Whether the address was successfully parsed
    """
    address: Optional[int] = None
    address_alphanumeric: Optional[str] = None
    preDirAbbrev: Optional[str] = None
    streetName: Optional[str] = None
    streetTypeAbbrev: Optional[str] = None
    postDirAbbrev: Optional[str] = None
    internal: Optional[str] = None
    location: Optional[str] = None
    stateAbbrev: Optional[str] = None
    zip: Optional[str] = None
    zip4: Optional[str] = None
    parsed: bool = False
