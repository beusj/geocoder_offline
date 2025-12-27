"""Number mapping module for address parsing.

This module provides classes for mapping ordinal and cardinal number words
to digits and vice versa, similar to the Ruby implementation in
degauss-org/geocoder.
"""

import re


class NumberMap(dict):
    """A bidirectional mapping between number words and digits.
    
    This class extends dict to provide a mapping that works both ways:
    words to numbers and numbers to words.
    """
    
    def __init__(self, items=None):
        """Initialize the NumberMap.
        
        Args:
            items: List of number words to map to sequential integers.
        """
        super().__init__()
        self.regexp = None
        self._count = 0
        
        if items:
            for item in items:
                self._add_item(item)
            self._build_match()
    
    def _clean(self, key):
        """Clean a key by converting to lowercase and removing non-alphanumeric chars.
        
        Args:
            key: The key to clean (string or int).
            
        Returns:
            Cleaned key (lowercase string with no special chars, or int).
        """
        if isinstance(key, str):
            return key.lower().replace('-', '').replace(' ', '')
        return key
    
    def _add_item(self, item):
        """Add an item to the mapping.
        
        Args:
            item: The word to add to the mapping.
        """
        clean_item = self._clean(item)
        self[clean_item] = self._count
        self[self._count] = item
        self._count += 1
    
    def _build_match(self):
        """Build a regular expression to match all keys in the mapping."""
        # Get all string keys (words)
        words = [k for k in self.keys() if isinstance(k, str)]
        if words:
            # Use original words (not cleaned) for the regex
            original_words = [self[i] for i in range(self._count)]
            pattern = r'\b(' + '|'.join(re.escape(w) for w in original_words) + r')\b'
            self.regexp = re.compile(pattern, re.IGNORECASE)
    
    def __getitem__(self, key):
        """Get an item from the mapping, cleaning the key first.
        
        Args:
            key: The key to look up.
            
        Returns:
            The value associated with the key.
        """
        clean_key = self._clean(key)
        return super().__getitem__(clean_key)
    
    def __contains__(self, key):
        """Check if a key exists in the mapping.
        
        Args:
            key: The key to check.
            
        Returns:
            True if the key exists, False otherwise.
        """
        clean_key = self._clean(key)
        return super().__contains__(clean_key)
    
    def get(self, key, default=None):
        """Get an item from the mapping with a default value.
        
        Args:
            key: The key to look up.
            default: Default value if key not found.
            
        Returns:
            The value associated with the key or default.
        """
        clean_key = self._clean(key)
        return super().get(clean_key, default)


# Cardinals constant maps digits to cardinal number words and back
_cardinal_words = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 
    'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 
    'sixteen', 'seventeen', 'eighteen', 'nineteen'
]

Cardinals = NumberMap(_cardinal_words)

# Add tens
_cardinal_tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

for tens in _cardinal_tens:
    Cardinals._add_item(tens)
    for n in range(1, 10):
        Cardinals._add_item(f"{tens}-{Cardinals[n]}")

Cardinals._build_match()


# Ordinals constant maps digits to ordinal number words and back
_ordinal_words = [
    'zeroth', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 
    'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 
    'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 
    'eighteenth', 'nineteenth'
]

Ordinals = NumberMap(_ordinal_words)

# Add tens
for tens in _cardinal_tens:
    ordinal_tens = tens.replace('y', 'ieth')
    Ordinals._add_item(ordinal_tens)
    for n in range(1, 10):
        Ordinals._add_item(f"{tens}-{Ordinals[n]}")

Ordinals._build_match()
