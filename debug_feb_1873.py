#!/usr/bin/env python3
"""
Debug February 1873 extraction to find missing transactions.
"""

import PyPDF2
import re

def extract_page_transactions(page_text):
    """Extract transactions from a page, including debugging info."""
    transactions = []
    lines = page_text.split('\n')
    
    print(f"\nPage has {len(lines)} lines")
    
    for i, line in enumerate(lines):
        # Look for date patterns
        if re.match(r'^\d{2}/\d{2}', line.strip()):
            print(f"Line {i}: {line.strip()[:80]}...")
            
    # Also look for specific missing transactions
    if "Buttercup" in page_text:
        print("Found Buttercup transaction!")
    if "4,570" in page_text or "4570" in page_text:
        print("Found $4,570 transfer!")
    if "Interest Payment" in page_text:
        print("Found Interest Payment!")
        
    return transactions

def main():
    pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873/20250207-statements-1873-.pdf"
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        print("Analyzing Chase 1873 February 2025 PDF")
        print("=" * 60)
        
        # Focus on pages 3-5 (account 1873)
        for page_num in [2, 3, 4]:  # 0-indexed
            print(f"\n\nPage {page_num + 1}:")
            print("-" * 60)
            
            page_text = pdf_reader.pages[page_num].extract_text()
            
            # Check for account markers
            if "CHECKING SUMMARY" in page_text:
                print("*** CHECKING SUMMARY found ***")
                # Extract balance info
                if match := re.search(r'Beginning Balance\s*\$([0-9,]+\.\d{2})', page_text):
                    print(f"Beginning Balance: ${match.group(1)}")
                if match := re.search(r'Ending Balance\s*\$([0-9,]+\.\d{2})', page_text):
                    print(f"Ending Balance: ${match.group(1)}")
                    
            if "CHASE TOTAL CHECKING" in page_text:
                print("*** CHASE TOTAL CHECKING found - END OF 1873 ***")
                
            # Extract transactions
            extract_page_transactions(page_text)
            
            # Look for date ranges
            if "through" in page_text:
                date_matches = re.findall(r'(\w+\s+\d+,\s+\d{4})\s+through\s*(\w+\s+\d+,\s+\d{4})', page_text)
                for start, end in date_matches:
                    print(f"Date range: {start} through {end}")

if __name__ == "__main__":
    main()