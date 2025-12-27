#!/usr/bin/env python3
"""
Example script demonstrating the degauss_like address parser.

This script shows various use cases and features of the address parser.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from degauss_like import Address


def print_address(label, addr):
    """Pretty print an address with all its components."""
    print(f"\n{label}")
    print("=" * 60)
    print(f"Original: {addr.text}")
    print(f"Number:   {addr.number}")
    print(f"Street:   {addr.street[0] if addr.street else 'N/A'}")
    if len(addr.street) > 1:
        print(f"          (also: {', '.join(addr.street[1:3])}{'...' if len(addr.street) > 3 else ''})")
    print(f"City:     {addr.city[0] if addr.city else 'N/A'}")
    print(f"State:    {addr.state}")
    print(f"ZIP:      {addr.zip}")
    if addr.prenum or addr.sufnum:
        print(f"Pre/Suf:  {addr.prenum}/{addr.sufnum}")
    if addr.po_box():
        print("Type:     PO Box")
    if addr.intersection():
        print("Type:     Intersection")


def main():
    """Run example address parsing scenarios."""
    
    print("=" * 60)
    print("DeGAUSS-like Address Parser - Examples")
    print("=" * 60)
    
    # Example 1: Famous address
    addr1 = Address("1600 Pennsylvania Avenue NW, Washington, DC 20500")
    print_address("Example 1: The White House", addr1)
    
    # Example 2: New York address
    addr2 = Address("350 Fifth Avenue, New York, NY 10118")
    print_address("Example 2: Empire State Building", addr2)
    
    # Example 3: Simple address
    addr3 = Address("742 Evergreen Terrace, Springfield, IL 62701")
    print_address("Example 3: Simple Address", addr3)
    
    # Example 4: Address with full state name
    addr4 = Address("1060 West Addison Street, Chicago, Illinois 60613")
    print_address("Example 4: Full State Name", addr4)
    
    # Example 5: PO Box
    addr5 = Address("PO Box 123, Springfield, IL 62701")
    print_address("Example 5: PO Box", addr5)
    
    # Example 6: Intersection
    addr6 = Address("Main Street at Elm Street, Springfield")
    print_address("Example 6: Intersection", addr6)
    
    # Example 7: Address with number words
    addr7 = Address("One Microsoft Way, Redmond, WA 98052")
    print_address("Example 7: Number Words", addr7)
    
    # Example 8: Address with ordinals
    addr8 = Address("221B Baker Street, London")
    print_address("Example 8: With Suffix Number", addr8)
    
    # Example 9: Using dictionary input
    print("\n" + "=" * 60)
    print("Example 9: Dictionary Input")
    print("=" * 60)
    addr9 = Address({
        'number': '123',
        'street': 'Main Street',
        'city': 'Springfield',
        'state': 'IL',
        'postal_code': '62701'
    })
    print(f"Created from dict: {addr9}")
    
    # Example 10: Demonstrating abbreviation expansion
    print("\n" + "=" * 60)
    print("Example 10: Abbreviation Expansion")
    print("=" * 60)
    addr10 = Address("123 Main St, Springfield, IL")
    print(f"Original: 123 Main St, Springfield, IL")
    print(f"Street variations generated: {len(addr10.street)}")
    for i, variation in enumerate(addr10.street[:5], 1):
        print(f"  {i}. {variation}")
    if len(addr10.street) > 5:
        print(f"  ... and {len(addr10.street) - 5} more")
    
    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
