#!/usr/bin/env python3
import PyPDF2
import re
from datetime import datetime
import csv

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def parse_date(date_str):
    """Convert date from MM/DD format to YYYY-MM-DD"""
    try:
        # Assuming year 2025 based on the statement date
        month, day = date_str.strip().split('/')
        return f"2025-{month.zfill(2)}-{day.zfill(2)}"
    except:
        return date_str

def extract_transactions(text):
    """Extract all transactions from the text"""
    transactions = []
    
    # Print full text to understand structure
    print("\n--- FULL TEXT FOR DEBUGGING ---")
    print(text)
    print("\n--- END FULL TEXT ---\n")
    
    # Split text into lines
    lines = text.split('\n')
    
    # Look for transactions by finding date patterns throughout the document
    for i, line in enumerate(lines):
        # Look for date pattern at start of line (MM/DD or M/D)
        date_match = re.match(r'^(\d{1,2}/\d{1,2})\s+(.+)', line.strip())
        if date_match:
            date_str = date_match.group(1)
            rest_of_line = date_match.group(2)
            
            # Look for amount - could be negative or positive
            # Try to find amount at the end of the line or in the next line
            amount_match = re.search(r'(-?\$?[\d,]+\.\d{2})$', rest_of_line)
            
            if not amount_match and i + 1 < len(lines):
                # Check next line for amount
                next_line = lines[i + 1].strip()
                amount_match = re.search(r'^(-?\$?[\d,]+\.\d{2})$', next_line)
                if amount_match:
                    description = rest_of_line.strip()
                else:
                    continue
            elif amount_match:
                description = rest_of_line[:amount_match.start()].strip()
            else:
                continue
            
            if amount_match:
                amount_str = amount_match.group(1)
                # Clean up amount
                amount = float(amount_str.replace('$', '').replace(',', '').replace('-', ''))
                
                # Determine transaction type and sign
                if "-" in amount_str or "PAYMENT" in description.upper() or "THANK YOU" in description.upper():
                    trans_type = "Payment"
                    amount = -abs(amount)  # Payments are negative
                elif "CREDIT" in description.upper():
                    trans_type = "Credit"
                    amount = -abs(amount)  # Credits are negative
                else:
                    trans_type = "Purchase"
                    amount = abs(amount)  # Purchases are positive
                
                transactions.append({
                    'date': parse_date(date_str),
                    'description': description,
                    'amount': amount,
                    'type': trans_type
                })
                
                print(f"Found transaction: {date_str} | {description} | ${amount:.2f}")
    
    # Look for interest charges in the Fees section
    for i, line in enumerate(lines):
        if "INTEREST CHARGE ON PURCHASES" in line:
            # Look for the amount in the same or next line
            amount_match = re.search(r'\$?([\d,]+\.\d{2})', line)
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
                transactions.append({
                    'date': '2025-05-12',  # Use statement date
                    'description': 'INTEREST CHARGE ON PURCHASES',
                    'amount': amount,
                    'type': 'Interest Charge'
                })
    
    return transactions

def main():
    pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250512-1342.pdf"
    output_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-05_transactions.csv"
    
    # Extract text from PDF
    print("Extracting text from PDF...")
    text = extract_pdf_text(pdf_path)
    
    # Print extracted text for debugging
    print("\n--- EXTRACTED TEXT ---")
    print(text[:2000])  # Print first 2000 characters
    print("\n--- END OF SAMPLE ---\n")
    
    # Extract transactions
    print("Parsing transactions...")
    transactions = extract_transactions(text)
    
    # Write to CSV
    print(f"\nWriting {len(transactions)} transactions to CSV...")
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 'Status', 'Statement id', 'Bank and last 4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for trans in transactions:
            writer.writerow({
                'Description': trans['description'],
                'Amount': trans['amount'],
                'Transaction Date': trans['date'],
                'Transaction Type': trans['type'],
                'Status': 'New',
                'Statement id': '2025-05 - Discover 1342',
                'Bank and last 4': 'Discover 1342'
            })
    
    print(f"\nTransactions saved to: {output_path}")
    
    # Print summary
    print("\nTransaction Summary:")
    for trans in transactions:
        print(f"{trans['date']} | {trans['description'][:40]:40} | ${trans['amount']:>10.2f} | {trans['type']}")

if __name__ == "__main__":
    main()