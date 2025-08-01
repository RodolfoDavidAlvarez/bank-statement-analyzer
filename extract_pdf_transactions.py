#!/usr/bin/env python3
import PyPDF2
import re
from decimal import Decimal

def extract_transactions_from_pdf(pdf_path):
    """Extract transactions from Chase bank statement PDF"""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Focus on pages 3-5 (0-indexed: 2-4)
        text_content = ""
        for page_num in range(2, min(5, len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text() + "\n"
        
        print("Extracted text from pages 3-5:")
        print("="*80)
        print(text_content)
        print("="*80)
        
        # Look for beginning and ending balance
        beginning_match = re.search(r'Beginning balance.*?\$?([\d,]+\.\d{2})', text_content, re.IGNORECASE)
        ending_match = re.search(r'Ending balance.*?\$?([\d,]+\.\d{2})', text_content, re.IGNORECASE)
        
        if beginning_match:
            print(f"\nFound Beginning Balance: ${beginning_match.group(1)}")
        if ending_match:
            print(f"Found Ending Balance: ${ending_match.group(1)}")
        
        # Extract transaction lines - looking for date patterns
        transaction_pattern = r'(\d{2}/\d{2})\s+(.*?)\s+([\d,]+\.\d{2})'
        transactions = re.findall(transaction_pattern, text_content)
        
        print(f"\nFound {len(transactions)} potential transactions")
        
        return text_content, transactions

# Run the extraction
pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873/20250207-statements-1873-.pdf"
text, transactions = extract_transactions_from_pdf(pdf_path)

# Save the extracted text for manual review
with open('pdf_extract.txt', 'w') as f:
    f.write(text)
    
print("\nFull extracted text saved to pdf_extract.txt")