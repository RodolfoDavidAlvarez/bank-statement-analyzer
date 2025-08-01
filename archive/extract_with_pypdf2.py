#!/usr/bin/env python3
"""
Extract text from Discover PDF using PyPDF2
"""

import PyPDF2
import re

pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250612-1342.pdf"

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        print(f"Number of pages: {len(pdf_reader.pages)}")
        
        # Extract text from all pages
        all_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            all_text += f"\n\n--- PAGE {page_num + 1} ---\n\n"
            all_text += text
        
        # Save the extracted text
        with open('discover_extracted_text.txt', 'w', encoding='utf-8') as output:
            output.write(all_text)
        
        print(f"Text extracted and saved to discover_extracted_text.txt")
        print(f"Total characters extracted: {len(all_text)}")
        
        # Try to find transaction patterns
        print("\nSearching for transaction patterns...")
        
        # Common patterns in credit card statements
        date_pattern = r'\d{2}/\d{2}'
        amount_pattern = r'\$?\d+\.\d{2}'
        
        # Find potential transactions
        lines = all_text.split('\n')
        for i, line in enumerate(lines[:100]):  # Check first 100 lines
            if re.search(date_pattern, line) or re.search(amount_pattern, line):
                print(f"Line {i}: {line[:100]}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()