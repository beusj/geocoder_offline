"""
State extraction functionality for address normalization.
"""

import re
from typing import Optional, Tuple
from .lookup_tables import STATE_LOOKUP
from .utils import levenshtein_distance


def state_extract(address_string: str) -> Optional[str]:
    """
    Extract state information from an address string.
    Returns a string in format "state_name:state_abbrev" or None if not found.
    
    This function looks for state names or abbreviations in the address string
    and returns both the matched text and the standard abbreviation.
    
    Args:
        address_string: The address string to extract from
        
    Returns:
        String in format "matched_text:abbreviation" or None
    """
    if not address_string:
        return None
    
    address_upper = address_string.upper().strip()
    ws = r'[ ,.\t\n\f\r]'
    
    # First, try exact matches with state abbreviations (2 letters)
    # Look for 2-letter state codes at word boundaries
    for state in STATE_LOOKUP:
        if len(state["name"]) == 2:  # Only abbreviations
            # Look for the abbreviation as a whole word
            pattern = rf'(?:^|{ws})({re.escape(state["name"])})(?:{ws}|$)'
            match = re.search(pattern, address_upper)
            if match:
                matched_text = match.group(1)
                return f"{matched_text}:{state['abbrev']}"
    
    # Try exact matches with full state names
    # Sort by length (longest first) to match "NEW YORK" before "YORK"
    sorted_states = sorted(
        [s for s in STATE_LOOKUP if len(s["name"]) > 2],
        key=lambda x: len(x["name"]),
        reverse=True
    )
    
    for state in sorted_states:
        pattern = rf'(?:^|{ws})({re.escape(state["name"])})(?:{ws}|$)'
        match = re.search(pattern, address_upper)
        if match:
            matched_text = match.group(1)
            return f"{matched_text}:{state['abbrev']}"
    
    # Try fuzzy matching for full state names (not abbreviations)
    # Only consider states with names longer than 2 characters
    words = address_upper.split()
    
    # Try matching last few words (states can be multi-word like "NEW YORK")
    for num_words in range(min(3, len(words)), 0, -1):
        if len(words) >= num_words:
            last_words = ' '.join(words[-num_words:])
            
            # Find closest match
            best_match = None
            best_distance = float('inf')
            
            for state in STATE_LOOKUP:
                if len(state["name"]) <= 2:  # Skip abbreviations for fuzzy match
                    continue
                
                distance = levenshtein_distance(last_words, state["name"])
                # Allow fuzzy match if distance is small relative to length
                max_distance = max(2, len(state["name"]) // 3)
                
                if distance < best_distance and distance <= max_distance:
                    best_distance = distance
                    best_match = state
            
            if best_match:
                return f"{last_words}:{best_match['abbrev']}"
    
    return None
