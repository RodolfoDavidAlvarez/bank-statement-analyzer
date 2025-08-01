#!/usr/bin/env python3
"""
Extract transactions from Discover credit card PDF statement using basic tools
"""

import subprocess
import re
import csv
import os

def extract_text_with_strings(pdf_path):
    """Extract text from PDF using strings command"""
    try:
        # Use strings command to extract readable text
        result = subprocess.run(['strings', pdf_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error running strings command: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_discover_transactions(text):
    """Parse Discover credit card transactions from extracted text"""
    transactions = []
    
    # Split text into lines
    lines = text.split('\n')
    
    # Common Discover transaction patterns
    # Look for lines with dates (MM/DD) followed by description and amount
    
    # First, let's identify the statement period to determine the year
    year = "2025"  # Default based on filename
    
    # Track sections
    in_purchases = False
    in_payments = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check for section headers
        if "PURCHASES AND ADJUSTMENTS" in line.upper() or "PURCHASES" in line.upper():
            in_purchases = True
            in_payments = False
            continue
        elif "PAYMENTS AND CREDITS" in line.upper() or "PAYMENTS" in line.upper():
            in_purchases = False
            in_payments = True
            continue
        elif "INTEREST CHARGED" in line.upper() or "FEES" in line.upper():
            # End of transactions
            break
            
        # Look for transaction patterns
        # Try to match date at the beginning of the line
        date_match = re.match(r'^(\d{2}/\d{2})\s+(.+?)(\d+\.\d{2})$', line)
        if not date_match:
            # Try another pattern with more spacing
            date_match = re.match(r'^(\d{2}/\d{2})\s+(.+?)\s+(\d+\.\d{2})$', line)
        
        if date_match:
            trans_date = date_match.group(1)
            description = date_match.group(2).strip()
            amount = date_match.group(3)
            
            # Determine transaction type
            if in_payments:
                trans_type = "Payment"
                amount = f"-{amount}"
            else:
                trans_type = "Purchase"
                amount = f"+{amount}"
            
            # Check if description contains payment/credit keywords
            if "PAYMENT" in description.upper():
                trans_type = "Payment"
                amount = f"-{amount.replace('+', '').replace('-', '')}"
            elif "CREDIT" in description.upper() or "REFUND" in description.upper():
                trans_type = "Credit"
                amount = f"-{amount.replace('+', '').replace('-', '')}"
            
            transaction = {
                'Description': description,
                'Amount': amount,
                'Transaction Date': f"{trans_date}/{year}",
                'Transaction Type': trans_type,
                'Status': "New",
                'Statement id': "2025-06 - Discover 1342",
                'Bank and last 4': "Discover 1342"
            }
            
            transactions.append(transaction)
        else:
            # Try to match transactions that might be on multiple lines
            # Look for dates without amounts on the same line
            simple_date_match = re.match(r'^(\d{2}/\d{2})\s+(.+)$', line)
            if simple_date_match and i + 1 < len(lines):
                # Check if next line has just an amount
                next_line = lines[i + 1].strip()
                amount_match = re.match(r'^(\d+\.\d{2})$', next_line)
                if amount_match:
                    trans_date = simple_date_match.group(1)
                    description = simple_date_match.group(2).strip()
                    amount = amount_match.group(1)
                    
                    # Determine transaction type
                    if in_payments:
                        trans_type = "Payment"
                        amount = f"-{amount}"
                    else:
                        trans_type = "Purchase"
                        amount = f"+{amount}"
                    
                    transaction = {
                        'Description': description,
                        'Amount': amount,
                        'Transaction Date': f"{trans_date}/{year}",
                        'Transaction Type': trans_type,
                        'Status': "New",
                        'Statement id': "2025-06 - Discover 1342",
                        'Bank and last 4': "Discover 1342"
                    }
                    
                    transactions.append(transaction)
    
    return transactions

def save_to_csv(transactions, output_path):
    """Save transactions to CSV file"""
    if not transactions:
        print("No transactions found to save")
        return
        
    fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                  'Status', 'Statement id', 'Bank and last 4']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)
    
    print(f"Saved {len(transactions)} transactions to {output_path}")

def main():
    pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250612-1342.pdf"
    output_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-06_transactions.csv"
    
    # Extract text from PDF
    print(f"Extracting text from: {pdf_path}")
    text = extract_text_with_strings(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    # Save raw text for debugging
    debug_path = output_path.replace('.csv', '_raw.txt')
    with open(debug_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved raw text to: {debug_path}")
    
    # Parse transactions
    print("Parsing transactions...")
    transactions = parse_discover_transactions(text)
    
    if not transactions:
        print("\nNo transactions found with basic parsing.")
        print("Showing sample of extracted text for manual inspection:")
        print("-" * 50)
        lines = text.split('\n')
        for i, line in enumerate(lines[:100]):  # Show first 100 lines
            if line.strip():
                print(f"{i}: {line.strip()}")
    else:
        # Save to CSV
        save_to_csv(transactions, output_path)

if __name__ == "__main__":
    main()