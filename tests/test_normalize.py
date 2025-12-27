"""
Tests for address normalization functionality.
"""

import unittest
from postgis_like import normalize_address, pprint_addy, NormAddress


class TestNormalizeAddress(unittest.TestCase):
    """Test cases for normalize_address function."""
    
    def test_simple_address(self):
        """Test parsing a simple address."""
        result = normalize_address("123 Main St")
        self.assertTrue(result.parsed)
        self.assertEqual(result.address, 123)
        self.assertEqual(result.streetName, "Main")
        self.assertEqual(result.streetTypeAbbrev, "ST")
    
    def test_address_with_city_state_zip(self):
        """Test parsing complete address with city, state, and zip."""
        result = normalize_address("456 Oak Ave, Springfield, IL 62701")
        self.assertTrue(result.parsed)
        self.assertEqual(result.address, 456)
        self.assertEqual(result.streetName, "Oak")
        self.assertEqual(result.streetTypeAbbrev, "AVE")
        self.assertEqual(result.location, "Springfield")
        self.assertEqual(result.stateAbbrev, "IL")
        self.assertEqual(result.zip, "62701")
    
    def test_address_with_directions(self):
        """Test parsing address with directional prefixes and suffixes."""
        result = normalize_address("789 N Elm St E")
        self.assertTrue(result.parsed)
        self.assertEqual(result.address, 789)
        self.assertEqual(result.preDirAbbrev, "N")
        self.assertEqual(result.streetName, "Elm")
        self.assertEqual(result.streetTypeAbbrev, "ST")
        self.assertEqual(result.postDirAbbrev, "E")
    
    def test_address_with_apartment(self):
        """Test parsing address with apartment number."""
        result = normalize_address("321 Park Blvd Apt 5B")
        self.assertTrue(result.parsed)
        self.assertEqual(result.address, 321)
        self.assertEqual(result.streetName, "Park")
        self.assertEqual(result.streetTypeAbbrev, "BLVD")
        self.assertIn("APT", result.internal.upper())
    
    def test_highway_address(self):
        """Test parsing highway-type address."""
        result = normalize_address("State Highway 101")
        self.assertTrue(result.parsed)
        self.assertEqual(result.streetName, "101")
        self.assertEqual(result.streetTypeAbbrev, "SR")
    
    def test_zip_plus_4(self):
        """Test parsing address with ZIP+4 code."""
        result = normalize_address("100 First Ave, New York, NY 10001-1234")
        self.assertTrue(result.parsed)
        self.assertEqual(result.zip, "10001")
        self.assertEqual(result.zip4, "1234")
    
    def test_alphanumeric_address(self):
        """Test parsing address with alphanumeric street number."""
        result = normalize_address("123A Main St")
        self.assertTrue(result.parsed)
        self.assertEqual(result.address_alphanumeric, "123A")
        self.assertEqual(result.address, 123)
    
    def test_empty_string(self):
        """Test handling of empty string."""
        result = normalize_address("")
        self.assertFalse(result.parsed)
    
    def test_only_zip(self):
        """Test handling of just a zip code."""
        result = normalize_address("12345")
        self.assertTrue(result.parsed)
        self.assertEqual(result.zip, "12345")
    
    def test_full_state_name(self):
        """Test state extraction with full state name."""
        result = normalize_address("100 Main St, Boston, Massachusetts 02101")
        self.assertTrue(result.parsed)
        self.assertEqual(result.stateAbbrev, "MA")
    
    def test_multi_word_state(self):
        """Test state extraction with multi-word state name."""
        result = normalize_address("200 Broadway, New York, NY 10001")
        self.assertTrue(result.parsed)
        self.assertEqual(result.stateAbbrev, "NY")
        self.assertEqual(result.location, "New York")


class TestPprintAddy(unittest.TestCase):
    """Test cases for pprint_addy function."""
    
    def test_format_simple_address(self):
        """Test formatting a simple address."""
        addr = NormAddress(
            address=123,
            streetName="Main",
            streetTypeAbbrev="ST",
            parsed=True
        )
        result = pprint_addy(addr)
        self.assertEqual(result, "123 Main ST")
    
    def test_format_complete_address(self):
        """Test formatting a complete address."""
        addr = NormAddress(
            address=456,
            preDirAbbrev="N",
            streetName="Oak",
            streetTypeAbbrev="AVE",
            location="Springfield",
            stateAbbrev="IL",
            zip="62701",
            parsed=True
        )
        result = pprint_addy(addr)
        self.assertIn("456", result)
        self.assertIn("N Oak AVE", result)
        self.assertIn("Springfield", result)
        self.assertIn("IL", result)
        self.assertIn("62701", result)
    
    def test_format_with_apartment(self):
        """Test formatting address with apartment."""
        addr = NormAddress(
            address=789,
            streetName="Park",
            streetTypeAbbrev="BLVD",
            internal="APT 5B",
            parsed=True
        )
        result = pprint_addy(addr)
        self.assertIn("789 Park BLVD", result)
        self.assertIn("APT 5B", result)
    
    def test_format_highway(self):
        """Test formatting highway-type address."""
        addr = NormAddress(
            streetName="101",
            streetTypeAbbrev="SR",
            parsed=True
        )
        # For highways, type comes before name
        result = pprint_addy(addr)
        # This should format with type first for highways
        self.assertIn("101", result)
    
    def test_format_unparsed(self):
        """Test formatting unparsed address returns empty string."""
        addr = NormAddress(parsed=False)
        result = pprint_addy(addr)
        self.assertEqual(result, "")
    
    def test_format_with_zip4(self):
        """Test formatting address with ZIP+4."""
        addr = NormAddress(
            address=100,
            streetName="First",
            streetTypeAbbrev="AVE",
            stateAbbrev="NY",
            zip="10001",
            zip4="1234",
            parsed=True
        )
        result = pprint_addy(addr)
        self.assertIn("10001-1234", result)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_count_words(self):
        """Test word counting."""
        from postgis_like.normalize.utils import count_words
        
        self.assertEqual(count_words("one two three"), 3)
        self.assertEqual(count_words("single"), 1)
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words(None), -1)
        self.assertEqual(count_words("  multiple   spaces  "), 2)
    
    def test_soundex(self):
        """Test soundex encoding."""
        from postgis_like.normalize.utils import soundex
        
        # Classic soundex examples
        self.assertEqual(soundex("Robert"), "R163")
        self.assertEqual(soundex("Rupert"), "R163")
        self.assertEqual(soundex("Rubin"), "R150")
    
    def test_get_last_words(self):
        """Test extracting last N words."""
        from postgis_like.normalize.utils import get_last_words
        
        self.assertEqual(get_last_words("one two three four", 2), "three four")
        self.assertEqual(get_last_words("single", 1), "single")
        self.assertEqual(get_last_words("one two", 5), "one two")
        self.assertIsNone(get_last_words(None, 1))


class TestStateExtract(unittest.TestCase):
    """Test cases for state extraction."""
    
    def test_extract_state_abbrev(self):
        """Test extracting state abbreviation."""
        from postgis_like.normalize.state_extract import state_extract
        
        result = state_extract("123 Main St, Boston, MA 02101")
        self.assertIsNotNone(result)
        self.assertIn("MA", result)
    
    def test_extract_full_state_name(self):
        """Test extracting full state name."""
        from postgis_like.normalize.state_extract import state_extract
        
        result = state_extract("123 Main St, Boston, Massachusetts")
        self.assertIsNotNone(result)
        self.assertIn("MA", result)
    
    def test_extract_multi_word_state(self):
        """Test extracting multi-word state name."""
        from postgis_like.normalize.state_extract import state_extract
        
        result = state_extract("100 Broadway, New York")
        self.assertIsNotNone(result)
        self.assertIn("NY", result)
    
    def test_no_state_found(self):
        """Test when no state is found."""
        from postgis_like.normalize.state_extract import state_extract
        
        result = state_extract("123 Main Street")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
