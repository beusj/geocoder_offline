"""Address parsing module for US addresses.

This module provides the Address class which parses US street addresses
and place names into structured components. Based on the Ruby implementation
in degauss-org/geocoder.
"""

import re
from .constants import (
    State, Name_Abbr, Std_Abbr, Prefix_Type, Suffix_Type, Directional
)
from .numbers import Cardinals, Ordinals


# Regular expression patterns for matching address components
Match = {
    'number': re.compile(r'^(\d+\W|[a-z]+)?(\d+)([a-z]?)\b', re.IGNORECASE),
    'street': re.compile(r'(?:\b(?:\d+\w*|[a-z\'-]+)\s*)+', re.IGNORECASE),
    'city': re.compile(r'(?:\b[a-z\'-]+\s*)+', re.IGNORECASE),
    'state': re.compile(State.regexp.pattern + r'\s*$', re.IGNORECASE) if State.regexp else None,
    'zip': re.compile(r'(\d{5})(?:-\d{4})?\s*$'),
    'at': re.compile(r'\s(at|@|and|&)\s', re.IGNORECASE),
    'po_box': re.compile(r'\b[P|p]*(OST|ost)*\.*\s*[O|o|0]*(ffice|FFICE)*\.*\s*[B|b][O|o|0][X|x]\b')
}


class Address:
    """Parse and structure US street addresses.
    
    The Address class takes a US street address or place name and constructs
    a structured parse of the address string, extracting components like
    street number, street name, city, state, and ZIP code.
    
    Attributes:
        text: The original address text
        prenum: Pre-number component (e.g., "A" in "A123 Main St")
        number: Street number
        sufnum: Suffix number component (e.g., "B" in "123B Main St")
        street: List of possible street name variations
        city: List of possible city name variations
        state: State abbreviation
        zip: ZIP code (5 digits)
        plus4: ZIP+4 extension
    """
    
    def __init__(self, text):
        """Initialize and parse an address.
        
        Args:
            text: Address string or dictionary of address components.
            
        Raises:
            ValueError: If no text is provided or text is empty.
        """
        if not text:
            raise ValueError("no text provided")
        
        self.text = ""
        self.prenum = ""
        self.number = ""
        self.sufnum = ""
        self.street = []
        self.city = []
        self.state = ""
        self.zip = ""
        self.plus4 = ""
        self._full_state = ""
        
        if isinstance(text, dict):
            self._assign_text_to_address(text)
        else:
            self.text = self._clean(text)
            self._parse()
    
    def _clean(self, value):
        """Remove non-address characters from a string.
        
        Args:
            value: String to clean.
            
        Returns:
            Cleaned string with only address-relevant characters.
        """
        value = value.strip()
        value = re.sub(r"[^a-z0-9 ,'&@\/-]+", "", value, flags=re.IGNORECASE)
        value = re.sub(r'\s+', ' ', value)
        return value
    
    def _assign_text_to_address(self, text_dict):
        """Assign address components from a dictionary.
        
        Args:
            text_dict: Dictionary containing address components.
        """
        if 'address' in text_dict:
            self.text = self._clean(text_dict['address'])
            self._parse()
        else:
            self.street = []
            self.prenum = text_dict.get('prenum', '')
            self.sufnum = text_dict.get('sufnum', '')
            
            if text_dict.get('street'):
                self.street = Match['street'].findall(text_dict['street'])
            
            self.number = ""
            if self.street:
                if text_dict.get('number') is None:
                    # Extract number from street
                    new_streets = []
                    for single_street in self.street:
                        single_street = single_street.lower()
                        number_match = Match['number'].findall(single_street)
                        if number_match:
                            self.number = ''.join(number_match[0])
                            single_street = Match['number'].sub('', single_street, count=1)
                            single_street = re.sub(r'^\s*,?\s*', '', single_street)
                        new_streets.append(single_street)
                    self.street = new_streets
                else:
                    self.number = str(text_dict['number'])
                
                self.street = self._expand_streets(self.street)
                self._street_parts()
            
            self.city = []
            if text_dict.get('city'):
                self.city.append(text_dict['city'])
            else:
                self.city.append("")
            
            if text_dict.get('region'):
                self.state = text_dict['region']
                if len(self.state) > 2:
                    self.state = State.get(self.state, self.state)
            elif text_dict.get('country'):
                self.state = text_dict['country']
            elif text_dict.get('state'):
                self.state = text_dict['state']
            else:
                self.state = ""
            
            self.zip = text_dict.get('postal_code', '')
            self.plus4 = text_dict.get('plus4', '')
            if not self.zip:
                self.zip = self.plus4 = ""
    
    def _expand_numbers(self, string):
        """Expand number words and ordinals in a string.
        
        Args:
            string: String potentially containing number words.
            
        Returns:
            List of string variations with different number formats.
        """
        num = None
        match = None
        
        # Check for numeric ordinals (1st, 2nd, etc.)
        numeric_ordinal = re.search(r'\b\d+(?:st|nd|rd|th)?\b', string, re.IGNORECASE)
        if numeric_ordinal:
            match = numeric_ordinal.group()
            num = int(re.sub(r'[^\d]', '', match))
        elif Ordinals.regexp and Ordinals.regexp.search(string):
            match = Ordinals.regexp.search(string).group()
            num = Ordinals.get(match)
        elif Cardinals.regexp and Cardinals.regexp.search(string):
            match = Cardinals.regexp.search(string).group()
            num = Cardinals.get(match)
        
        strings = []
        if num is not None and num < 100:
            replacements = [str(num)]
            if num in Ordinals:
                replacements.append(Ordinals[num])
            if num in Cardinals:
                replacements.append(Cardinals[num])
            
            for replace in replacements:
                strings.append(string.replace(match, replace, 1))
        else:
            strings.append(string)
        
        return strings
    
    def _parse_zip(self, regex_match, text):
        """Extract ZIP code from text.
        
        Args:
            regex_match: The regex match object.
            text: The text to parse.
            
        Returns:
            Text with ZIP code removed.
        """
        match_str = regex_match.group()
        idx = text.rfind(match_str)
        text = text[:idx] + text[idx+len(match_str):]
        text = re.sub(r'\s*,?\s*$', '', text)
        
        # self.zip already contains the matched zip code string
        # No need to process it further - it's already in the correct format
        
        return text
    
    def _parse_state(self, regex_match, text):
        """Extract state from text.
        
        Args:
            regex_match: The regex match object.
            text: The text to parse.
            
        Returns:
            Text with state removed.
        """
        match_str = regex_match.group()
        idx = text.rfind(match_str)
        text = text[:idx] + text[idx+len(match_str):]
        text = re.sub(r'\s*,?\s*$', '', text)
        
        self._full_state = self.state.strip()
        self.state = State.get(self._full_state, self._full_state)
        
        return text
    
    def _parse_number(self, regex_match, text):
        """Extract street number from text.
        
        Args:
            regex_match: The regex match object.
            text: The text to parse.
            
        Returns:
            Text with number removed.
        """
        match_str = regex_match.group()
        idx = text.find(match_str)
        text = text[:idx] + text[idx+len(match_str):]
        text = re.sub(r'^\s*,?\s*', '', text)
        
        number_parts = [s.strip() if s else "" for s in self.number]
        self.prenum = number_parts[0] if len(number_parts) > 0 else ""
        self.number = number_parts[1] if len(number_parts) > 1 else ""
        self.sufnum = number_parts[2] if len(number_parts) > 2 else ""
        
        return text
    
    def _parse(self):
        """Parse the address text into components."""
        text = self.text.lower()
        
        # Extract ZIP code
        zip_matches = Match['zip'].findall(text)
        if zip_matches:
            self.zip = zip_matches[-1]
            zip_match = None
            for match in Match['zip'].finditer(text):
                zip_match = match
            if zip_match:
                text = self._parse_zip(zip_match, text)
        else:
            self.zip = self.plus4 = ""
        
        # Extract state
        if Match['state']:
            state_matches = Match['state'].findall(text)
            if state_matches:
                self.state = state_matches[-1] if isinstance(state_matches[-1], str) else state_matches[-1][0] if state_matches[-1] else ""
                # Find the last match
                state_match = None
                for match in Match['state'].finditer(text):
                    state_match = match
                if state_match:
                    text = self._parse_state(state_match, text)
            else:
                self._full_state = ""
                self.state = ""
        else:
            self._full_state = ""
            self.state = ""
        
        # Extract street number
        number_matches = Match['number'].findall(text)
        if number_matches:
            self.number = number_matches[0]
            number_match = Match['number'].search(text)
            if number_match:
                text = self._parse_number(number_match, text)
        else:
            self.prenum = self.number = self.sufnum = ""
        
        # Extract street
        self.street = Match['street'].findall(text)
        self.street = self._expand_streets(self.street)
        
        # Special case: state name used as street
        if not self.street and self.state and self._full_state:
            if self.state.lower() != self._full_state.lower():
                self.street.append(self._full_state)
        
        # Extract city
        self.city = Match['city'].findall(text)
        if self.city:
            self.city = [self.city[-1].strip()]
            # Expand abbreviations in city names
            expanded_cities = []
            for city_name in self.city:
                if Name_Abbr.regexp:
                    expanded = Name_Abbr.regexp.sub(
                        lambda m: Name_Abbr.get(m.group(), m.group()),
                        city_name
                    )
                    if expanded != city_name:
                        expanded_cities.append(expanded)
            self.city.extend(expanded_cities)
            self.city = [c.lower() for c in self.city]
            self.city = list(set(self.city))  # Remove duplicates
        else:
            self.city = []
        
        # Special case: state name as city
        if self.state and self._full_state:
            if self.state.lower() != self._full_state.lower():
                self.city.append(self._full_state.lower())
    
    def _expand_streets(self, streets):
        """Expand street name abbreviations.
        
        Args:
            streets: List of street names.
            
        Returns:
            List of street name variations with abbreviations expanded.
        """
        if not streets or not streets[0]:
            return []
        
        streets = [s.strip() for s in streets if s]
        
        # Expand name abbreviations
        expanded = []
        for street in streets:
            if Name_Abbr.regexp:
                exp = Name_Abbr.regexp.sub(
                    lambda m: Name_Abbr.get(m.group(), m.group()),
                    street
                )
                if exp != street:
                    expanded.append(exp)
        streets.extend(expanded)
        
        # Expand standard abbreviations
        expanded = []
        for street in streets:
            if Std_Abbr.regexp:
                exp = Std_Abbr.regexp.sub(
                    lambda m: Std_Abbr.get(m.group(), m.group()),
                    street
                )
                if exp != street:
                    expanded.append(exp)
        streets.extend(expanded)
        
        # Expand numbers
        expanded = []
        for street in streets:
            num_expanded = self._expand_numbers(street)
            expanded.extend(num_expanded)
        streets = expanded
        
        # Lowercase and remove duplicates
        streets = [s.lower() for s in streets]
        streets = list(dict.fromkeys(streets))  # Remove duplicates while preserving order
        
        return streets
    
    def _street_parts(self):
        """Generate all possible street name substrings.
        
        Returns:
            List of street name variations.
        """
        strings = []
        
        # Get all substrings delimited by whitespace
        for string in self.street:
            tokens = string.split()
            for i in range(len(tokens)):
                for j in range(i, len(tokens)):
                    strings.append(' '.join(tokens[i:j+1]))
        
        strings = self._remove_noise_words(strings)
        
        # Try adding the number if everything is an abbreviation
        if all(s in Std_Abbr or s in Name_Abbr for s in strings):
            strings.append(self.number)
        
        return list(set(strings))
    
    def _remove_noise_words(self, strings):
        """Remove directionals and type words from street name parts.
        
        Args:
            strings: List of street name strings.
            
        Returns:
            Filtered list with noise words removed.
        """
        prefix = re.compile(r'^' + Prefix_Type.regexp.pattern + r'\s*', re.IGNORECASE) if Prefix_Type.regexp else None
        suffix = re.compile(r'\s*' + Suffix_Type.regexp.pattern + r'$', re.IGNORECASE) if Suffix_Type.regexp else None
        predxn = re.compile(r'^' + Directional.regexp.pattern + r'\s*', re.IGNORECASE) if Directional.regexp else None
        sufdxn = re.compile(r'\s*' + Directional.regexp.pattern + r'$', re.IGNORECASE) if Directional.regexp else None
        
        good_strings = []
        for s in strings:
            s = s[:]  # Copy string
            if predxn:
                s = predxn.sub('', s)
            if sufdxn:
                s = sufdxn.sub('', s)
            if prefix:
                s = prefix.sub('', s)
            if suffix:
                s = suffix.sub('', s)
            if s:
                good_strings.append(s)
        
        if good_strings:
            # Only use filtered strings if we have some that aren't just abbreviations
            non_abbr = [s for s in good_strings if s not in Std_Abbr and s not in Name_Abbr]
            if non_abbr:
                return good_strings
        
        return strings
    
    def city_parts(self):
        """Generate all possible city name substrings.
        
        Returns:
            List of city name variations.
        """
        strings = []
        
        for city_str in self.city:
            tokens = city_str.split()
            for i in range(len(tokens)-1, -1, -1):
                for j in range(i, len(tokens)):
                    strings.append(' '.join(tokens[i:j+1]))
        
        # Don't return strings that are just abbreviations
        good_strings = [s for s in strings if s not in Std_Abbr]
        if good_strings:
            strings = good_strings
        
        return list(set(strings))
    
    def set_city(self, city_strings):
        """Remove city name from street strings.
        
        Args:
            city_strings: List of city name strings to remove from streets.
        """
        city_strings = self._expand_streets(city_strings)
        
        if city_strings:
            match = re.compile(
                r'\s*\b(?:' + '|'.join(re.escape(c) for c in city_strings) + r')\b\s*$',
                re.IGNORECASE
            )
            
            # Only remove city from street strings if address was parsed
            if self.text:
                self.street = [
                    match.sub('', s) for s in self.street
                ]
                self.street = [s for s in self.street if s]
    
    def po_box(self):
        """Check if address is a PO Box.
        
        Returns:
            True if address contains a PO Box pattern.
        """
        return bool(Match['po_box'].search(self.text))
    
    def intersection(self):
        """Check if address is an intersection.
        
        Returns:
            True if address contains an intersection pattern.
        """
        return bool(Match['at'].search(self.text))
    
    def __repr__(self):
        """Return string representation of the Address."""
        parts = []
        if self.number:
            parts.append(f"number={self.number}")
        if self.street:
            parts.append(f"street={self.street[0] if len(self.street) == 1 else self.street}")
        if self.city:
            parts.append(f"city={self.city[0] if len(self.city) == 1 else self.city}")
        if self.state:
            parts.append(f"state={self.state}")
        if self.zip:
            parts.append(f"zip={self.zip}")
        return f"Address({', '.join(parts)})"
