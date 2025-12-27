#!/usr/bin/env python
"""
Example usage of the postgis_like address normalization functions.
"""

from postgis_like import normalize_address, pprint_addy


def main():
    """Demonstrate address normalization functionality."""
    
    # Sample addresses to parse
    test_addresses = [
        "123 N Main St, Springfield, IL 62701",
        "456 Oak Ave Apt 2B, Boston, MA 02101-1234",
        "789 W Elm Street, New York, NY 10001",
        "State Highway 101, Sacramento, CA 95814",
        "100 SE First Avenue, Portland, OR 97201",
        "555 Park Blvd Suite 200, San Diego, California 92101",
    ]
    
    print("=" * 80)
    print("Address Normalization Examples")
    print("=" * 80)
    print()
    
    for raw_address in test_addresses:
        print(f"Input:  {raw_address}")
        
        # Parse the address
        addr = normalize_address(raw_address)
        
        if addr.parsed:
            # Display parsed components
            print(f"  Address Number:  {addr.address_alphanumeric or addr.address}")
            if addr.preDirAbbrev:
                print(f"  Pre-Direction:   {addr.preDirAbbrev}")
            if addr.streetName:
                print(f"  Street Name:     {addr.streetName}")
            if addr.streetTypeAbbrev:
                print(f"  Street Type:     {addr.streetTypeAbbrev}")
            if addr.postDirAbbrev:
                print(f"  Post-Direction:  {addr.postDirAbbrev}")
            if addr.internal:
                print(f"  Internal:        {addr.internal}")
            if addr.location:
                print(f"  City:            {addr.location}")
            if addr.stateAbbrev:
                print(f"  State:           {addr.stateAbbrev}")
            if addr.zip:
                zip_display = addr.zip
                if addr.zip4:
                    zip_display += f"-{addr.zip4}"
                print(f"  ZIP:             {zip_display}")
            
            # Format back to standardized string
            formatted = pprint_addy(addr)
            print(f"Output: {formatted}")
        else:
            print("  [Failed to parse]")
        
        print()
    
    print("=" * 80)
    print("\nDemonstrating individual component access:")
    print("-" * 80)
    
    # Example with component access
    address = normalize_address("100 W 5th Street Apt 301, Los Angeles, CA 90013")
    print(f"\nOriginal: 100 W 5th Street Apt 301, Los Angeles, CA 90013")
    print(f"\nParsed components:")
    print(f"  Street Address: {address.address}")
    print(f"  Full Street: {address.preDirAbbrev or ''} {address.streetName or ''} {address.streetTypeAbbrev or ''}".strip())
    print(f"  Apartment: {address.internal or 'N/A'}")
    print(f"  City: {address.location or 'N/A'}")
    print(f"  State: {address.stateAbbrev or 'N/A'}")
    print(f"  ZIP: {address.zip or 'N/A'}")
    print(f"\nStandardized: {pprint_addy(address)}")
    print()


if __name__ == "__main__":
    main()
