"""
Utility functions for address normalization.
"""

import re
from typing import Optional


def count_words(text: Optional[str]) -> int:
    """
    Count the number of words in a string.
    Words are separated by spaces. Multiple spaces between words are allowed.
    
    Args:
        text: The string to count words in
        
    Returns:
        Number of words, -1 if text is None, 0 if text is empty
    """
    if text is None:
        return -1
    
    text = text.strip()
    if len(text) == 0:
        return 0
    
    # Split by whitespace and count non-empty parts
    words = text.split()
    return len(words)


def get_last_words(text: Optional[str], num_words: int) -> Optional[str]:
    """
    Get the last N words from a string.
    
    Args:
        text: The string to extract from
        num_words: Number of words to extract
        
    Returns:
        The last N words, or None if text is None
    """
    if text is None:
        return None
    
    words = text.split()
    if len(words) <= num_words:
        return text
    
    return ' '.join(words[-num_words:])


def cull_null(value: Optional[str]) -> str:
    """
    Convert None to empty string, otherwise return the value.
    
    Args:
        value: The value to check
        
    Returns:
        Empty string if value is None, otherwise the value
    """
    return '' if value is None else value


def end_soundex(text: Optional[str]) -> Optional[str]:
    """
    Get soundex of the last word in the string.
    This is a simplified implementation without the fuzzystrmatch dependency.
    
    Args:
        text: The string to process
        
    Returns:
        Soundex of last word, or None if text is None
    """
    if text is None:
        return None
    
    # Extract last word
    match = re.search(r'[ ,.\n\t\f]([a-zA-Z0-9]*)$', text)
    if match:
        last_word = match.group(1)
    else:
        last_word = text
    
    # Simple soundex implementation
    return soundex(last_word) if last_word else None


def soundex(text: str) -> str:
    """
    Calculate the Soundex code for a string.
    
    Args:
        text: The string to encode
        
    Returns:
        4-character Soundex code
    """
    if not text:
        return "0000"
    
    text = text.upper()
    
    # Keep first letter
    soundex_code = text[0]
    
    # Mapping of letters to codes
    codes = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    
    prev_code = codes.get(text[0], '0')
    
    for char in text[1:]:
        code = codes.get(char, '0')
        if code != '0' and code != prev_code:
            soundex_code += code
            if len(soundex_code) == 4:
                break
        if code != '0':
            prev_code = code
    
    # Pad with zeros
    soundex_code = soundex_code.ljust(4, '0')
    
    return soundex_code[:4]


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    Used for fuzzy matching.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        The Levenshtein distance
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
