"""
postgis_like: Python implementation of PostGIS address normalization functions.

This package provides address parsing and normalization functionality
similar to PostGIS tiger_geocoder's normalize functions.
"""

from .normalize.normalize_address import normalize_address, NormAddress
from .normalize.pprint_addy import pprint_addy

__all__ = ['normalize_address', 'NormAddress', 'pprint_addy']
