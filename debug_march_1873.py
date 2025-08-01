#!/usr/bin/env python3
"""
Debug March 1873 PDF to understand why account 1873 isn't being detected.
"""

import PyPDF2

def main():
    pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873/20250307-statements-1873-.pdf"
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        print("Analyzing March 2025 Chase PDF")
        print("=" * 60)
        print(f"Total pages: {len(pdf_reader.pages)}")
        
        # Check each page for account markers
        for i in range(min(8, len(pdf_reader.pages))):
            page_text = pdf_reader.pages[i].extract_text()
            
            print(f"\n\nPage {i+1}:")
            print("-" * 60)
            
            # Look for account numbers
            if '000000837532084' in page_text or '2084' in page_text:
                print("✓ Found reference to account 2084")
            if '000000526021873' in page_text or '1873' in page_text:
                print("✓ Found reference to account 1873")
            if '000001248068619' in page_text or '8619' in page_text:
                print("✓ Found reference to account 8619")
                
            # Look for CHECKING SUMMARY
            if 'CHECKING SUMMARY' in page_text:
                print("✓ Found CHECKING SUMMARY")
                
                # Try to extract balance info
                import re
                if match := re.search(r'Beginning Balance\s*\$([0-9,]+\.\d{2})', page_text):
                    print(f"  Beginning Balance: ${match.group(1)}")
                if match := re.search(r'Ending Balance\s*\$([0-9,]+\.\d{2})', page_text):
                    print(f"  Ending Balance: ${match.group(1)}")
                    
            # Look for specific markers
            if 'CHASE TOTAL CHECKING' in page_text:
                print("✓ Found CHASE TOTAL CHECKING")
                
            # Check for transaction markers
            if 'TRANSACTION DETAIL' in page_text:
                print("✓ Found TRANSACTION DETAIL")
                
            # Look for Card 0665 (1873's card)
            if 'Card 0665' in page_text:
                print("✓ Found Card 0665 (1873's card)")
                
            # Print first few lines to understand structure
            lines = page_text.split('\n')[:5]
            print("\nFirst 5 lines:")
            for line in lines:
                if line.strip():
                    print(f"  {line.strip()}")

if __name__ == "__main__":
    main()