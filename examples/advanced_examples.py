#!/usr/bin/env python
"""
Additional examples showing edge cases and advanced usage of address normalization.
"""

from postgis_like import normalize_address, pprint_addy


def test_edge_cases():
    """Test various edge cases and special address formats."""
    
    print("=" * 80)
    print("Edge Cases and Special Address Formats")
    print("=" * 80)
    print()
    
    # Test cases with various edge cases
    test_cases = [
        # Alphanumeric addresses
        ("123A Main Street", "Alphanumeric street number"),
        
        # Multiple word street names
        ("100 Martin Luther King Jr Blvd", "Multi-word street name"),
        
        # Highway variations
        ("US Route 66", "US Highway format"),
        ("Interstate 95", "Interstate format"),
        ("County Road 24", "County road format"),
        
        # Full state names vs abbreviations
        ("100 Main St, Boston, Massachusetts", "Full state name"),
        ("100 Main St, Boston, MA", "State abbreviation"),
        
        # Various apartment formats
        ("100 Main St # 5", "Apartment with # symbol"),
        ("100 Main St Unit 5B", "Unit format"),
        ("100 Main St Suite 200", "Suite format"),
        ("100 Main St Floor 3", "Floor format"),
        
        # Different direction combinations
        ("100 Northeast Main St", "Full direction prefix"),
        ("100 Main St Northwest", "Full direction suffix"),
        
        # Minimal addresses
        ("123 Main", "No street type"),
        ("12345", "Just a ZIP code"),
        
        # Complex addresses
        ("1600 Pennsylvania Avenue NW, Washington, DC 20500", "Famous address"),
        ("One Microsoft Way, Redmond, WA 98052", "Non-numeric start"),
    ]
    
    for address_str, description in test_cases:
        print(f"Test: {description}")
        print(f"Input:  {address_str}")
        
        addr = normalize_address(address_str)
        
        if addr.parsed:
            print("Components:")
            if addr.address or addr.address_alphanumeric:
                print(f"  - Number: {addr.address_alphanumeric or addr.address}")
            if addr.preDirAbbrev:
                print(f"  - Pre-Dir: {addr.preDirAbbrev}")
            if addr.streetName:
                print(f"  - Street: {addr.streetName}")
            if addr.streetTypeAbbrev:
                print(f"  - Type: {addr.streetTypeAbbrev}")
            if addr.postDirAbbrev:
                print(f"  - Post-Dir: {addr.postDirAbbrev}")
            if addr.internal:
                print(f"  - Unit: {addr.internal}")
            if addr.location:
                print(f"  - City: {addr.location}")
            if addr.stateAbbrev:
                print(f"  - State: {addr.stateAbbrev}")
            if addr.zip:
                print(f"  - ZIP: {addr.zip}{'-' + addr.zip4 if addr.zip4 else ''}")
            
            formatted = pprint_addy(addr)
            if formatted:
                print(f"Output: {formatted}")
        else:
            print("  [Not parsed or minimal parsing]")
        
        print()


def compare_formats():
    """Compare different variations of the same address."""
    
    print("=" * 80)
    print("Comparing Address Format Variations")
    print("=" * 80)
    print()
    
    # Same address in different formats
    variations = [
        "123 North Main Street, Springfield, Illinois 62701",
        "123 N Main St Springfield IL 62701",
        "123 N. Main St., Springfield, IL 62701",
        "123 n main street springfield il 62701",  # lowercase
    ]
    
    print("Testing variations of the same address:")
    print("-" * 80)
    
    for i, addr_str in enumerate(variations, 1):
        print(f"\nVariation {i}: {addr_str}")
        addr = normalize_address(addr_str)
        if addr.parsed:
            formatted = pprint_addy(addr)
            print(f"Normalized:  {formatted}")
            print(f"Components: Num={addr.address}, PreDir={addr.preDirAbbrev}, "
                  f"Street={addr.streetName}, Type={addr.streetTypeAbbrev}, "
                  f"City={addr.location}, State={addr.stateAbbrev}, ZIP={addr.zip}")
    
    print()


def batch_processing():
    """Demonstrate batch processing of multiple addresses."""
    
    print("=" * 80)
    print("Batch Address Processing")
    print("=" * 80)
    print()
    
    # Simulate a list of addresses to process
    addresses = [
        "100 W 1st St, Los Angeles, CA 90012",
        "2000 Broadway, New York, NY 10023",
        "500 Terry Francois Blvd, San Francisco, CA 94158",
        "1 Infinite Loop, Cupertino, CA 95014",
        "350 5th Ave, New York, NY 10118",
    ]
    
    print("Processing a batch of addresses:")
    print("-" * 80)
    
    results = []
    for addr_str in addresses:
        addr = normalize_address(addr_str)
        results.append({
            'original': addr_str,
            'parsed': addr,
            'normalized': pprint_addy(addr) if addr.parsed else None
        })
    
    # Display results
    for result in results:
        print(f"\nOriginal:   {result['original']}")
        if result['normalized']:
            print(f"Normalized: {result['normalized']}")
            addr = result['parsed']
            print(f"  → Street: {addr.address} "
                  f"{addr.preDirAbbrev or ''} "
                  f"{addr.streetName or ''} "
                  f"{addr.streetTypeAbbrev or ''}".strip())
            print(f"  → Location: {addr.location or 'N/A'}, "
                  f"{addr.stateAbbrev or 'N/A'} {addr.zip or ''}")
        else:
            print("  [Parse failed]")
    
    print()
    
    # Summary statistics
    success_count = sum(1 for r in results if r['normalized'])
    print(f"Summary: {success_count}/{len(results)} addresses successfully parsed")
    print()


def main():
    """Run all example demonstrations."""
    test_edge_cases()
    compare_formats()
    batch_processing()
    
    print("=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
