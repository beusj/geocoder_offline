"""degauss_like - US Address Parser

A Python implementation of the address parser from the DeGAUSS project.
This parser extracts structured components from US street addresses.

Based on the Ruby implementation at:
https://github.com/degauss-org/geocoder/tree/master/lib/geocoder/us

Example:
    >>> from degauss_like import Address
    >>> addr = Address("1600 Pennsylvania Avenue NW, Washington, DC 20500")
    >>> print(f"Number: {addr.number}")
    >>> print(f"Street: {addr.street}")
    >>> print(f"City: {addr.city}")
    >>> print(f"State: {addr.state}")
    >>> print(f"ZIP: {addr.zip}")
"""

from .address import Address
from .constants import (
    State, Directional, Prefix_Type, Suffix_Type, 
    Name_Abbr, Std_Abbr, Map
)
from .numbers import Cardinals, Ordinals, NumberMap

__version__ = "0.1.0"

__all__ = [
    'Address',
    'State',
    'Directional',
    'Prefix_Type',
    'Suffix_Type',
    'Name_Abbr',
    'Std_Abbr',
    'Map',
    'Cardinals',
    'Ordinals',
    'NumberMap',
]
