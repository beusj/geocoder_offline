"""Test suite for the degauss_like address parser.

This module contains tests to validate the address parsing functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from degauss_like import Address


def test_basic_address():
    """Test parsing a basic address."""
    addr = Address("1600 Pennsylvania Avenue NW, Washington, DC 20500")
    
    assert addr.number == "1600", f"Expected number '1600', got '{addr.number}'"
    assert any("pennsylvania" in s for s in addr.street), f"Expected 'pennsylvania' in street, got {addr.street}"
    assert addr.state == "DC", f"Expected state 'DC', got '{addr.state}'"
    assert addr.zip == "20500", f"Expected ZIP '20500', got '{addr.zip}'"
    print("✓ Basic address test passed")


def test_simple_address():
    """Test parsing a simple address without city."""
    addr = Address("123 Main St")
    
    assert addr.number == "123", f"Expected number '123', got '{addr.number}'"
    assert any("main" in s for s in addr.street), f"Expected 'main' in street, got {addr.street}"
    print("✓ Simple address test passed")


def test_address_with_suite():
    """Test parsing an address with apartment/suite."""
    addr = Address("742 Evergreen Terrace, Springfield, IL 62701")
    
    assert addr.number == "742", f"Expected number '742', got '{addr.number}'"
    assert any("evergreen" in s for s in addr.street), f"Expected 'evergreen' in street, got {addr.street}"
    assert addr.state == "IL", f"Expected state 'IL', got '{addr.state}'"
    assert addr.zip == "62701", f"Expected ZIP '62701', got '{addr.zip}'"
    print("✓ Address with suite test passed")


def test_state_full_name():
    """Test parsing an address with full state name."""
    addr = Address("350 Fifth Avenue, New York, New York 10118")
    
    assert addr.number == "350", f"Expected number '350', got '{addr.number}'"
    assert any("fifth" in s or "5th" in s for s in addr.street), f"Expected 'fifth' or '5th' in street, got {addr.street}"
    assert addr.state == "NY", f"Expected state 'NY', got '{addr.state}'"
    assert addr.zip == "10118", f"Expected ZIP '10118', got '{addr.zip}'"
    print("✓ State full name test passed")


def test_po_box():
    """Test PO Box detection."""
    addr = Address("PO Box 123, Springfield, IL 62701")
    
    assert addr.po_box(), "Expected address to be identified as PO Box"
    print("✓ PO Box test passed")


def test_intersection():
    """Test intersection detection."""
    addr = Address("Main St at Elm St")
    
    assert addr.intersection(), "Expected address to be identified as intersection"
    print("✓ Intersection test passed")


def test_no_text_error():
    """Test that empty text raises an error."""
    try:
        addr = Address("")
        assert False, "Expected ValueError for empty text"
    except ValueError as e:
        assert "no text provided" in str(e)
        print("✓ No text error test passed")


def test_abbreviation_expansion():
    """Test that abbreviations are expanded."""
    addr = Address("123 Main St, Springfield, IL")
    
    # Should have both abbreviated and expanded forms
    assert len(addr.street) > 1, "Expected multiple street variations"
    print("✓ Abbreviation expansion test passed")


def test_number_words():
    """Test parsing addresses with number words."""
    addr = Address("One Main Street, Boston, MA 02101")
    
    # Should recognize 'One' as a number
    assert addr.street, "Expected street to be parsed"
    print("✓ Number words test passed")


def test_dict_input():
    """Test parsing from dictionary input."""
    addr = Address({
        'number': '123',
        'street': 'Main Street',
        'city': 'Springfield',
        'state': 'IL',
        'postal_code': '62701'
    })
    
    assert addr.number == "123", f"Expected number '123', got '{addr.number}'"
    assert addr.state == "IL", f"Expected state 'IL', got '{addr.state}'"
    assert addr.zip == "62701", f"Expected ZIP '62701', got '{addr.zip}'"
    print("✓ Dict input test passed")


def run_all_tests():
    """Run all test functions."""
    print("Running address parser tests...\n")
    
    tests = [
        test_basic_address,
        test_simple_address,
        test_address_with_suite,
        test_state_full_name,
        test_po_box,
        test_intersection,
        test_no_text_error,
        test_abbreviation_expansion,
        test_number_words,
        test_dict_input,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
