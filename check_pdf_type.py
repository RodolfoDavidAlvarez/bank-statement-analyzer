#!/usr/bin/env python3
"""
Quick check to see if these are multi-account or single-account PDFs.
"""

import PyPDF2

# Check February 1873 statement
pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873/20250207-statements-1873-.pdf"

with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    print(f"Number of pages in 1873 February PDF: {num_pages}")
    
    # Check first few pages for account references
    for i in range(min(3, num_pages)):
        page_text = pdf_reader.pages[i].extract_text()
        print(f"\n--- Page {i+1} ---")
        
        # Look for account references
        if "2084" in page_text:
            print("Found reference to account 2084")
        if "1873" in page_text:
            print("Found reference to account 1873")
        if "8619" in page_text:
            print("Found reference to account 8619")
            
        # Look for key markers
        if "CHECKING SUMMARY" in page_text:
            print("Found CHECKING SUMMARY")
        if "Primary Account" in page_text:
            print("Found Primary Account header")
            
        # Extract first few lines
        lines = page_text.split('\n')[:10]
        print("First 10 lines:")
        for line in lines:
            if line.strip():
                print(f"  {line.strip()}")