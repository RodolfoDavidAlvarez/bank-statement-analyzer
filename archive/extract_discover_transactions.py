#!/usr/bin/env python3
import pdfplumber
import pandas as pd
import re
from datetime import datetime

def extract_discover_transactions(pdf_path, output_csv):
    """Extract transactions from Discover credit card statement PDF"""
    
    transactions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # Process each page
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            
            # Look for transaction sections
            in_purchase_section = False
            in_payment_section = False
            in_fees_section = False
            
            for i, line in enumerate(lines):
                # Check for purchase section
                if "NEW CHARGES" in line or "Trans Date Description" in line:
                    in_purchase_section = True
                    in_payment_section = False
                    in_fees_section = False
                    continue
                
                # Check for payment section
                if "PAYMENTS & CREDITS" in line or "PAYMENT" in line.upper() and "CREDIT" in line.upper():
                    in_payment_section = True
                    in_purchase_section = False
                    in_fees_section = False
                    continue
                
                # Check for fees and interest section
                if "FEES AND INTEREST CHARGED" in line or "INTEREST CHARGE" in line:
                    in_fees_section = True
                    in_purchase_section = False
                    in_payment_section = False
                    continue
                
                # End sections at certain markers
                if "TOTAL" in line and "$" in line:
                    in_purchase_section = False
                    in_payment_section = False
                    in_fees_section = False
                
                # Extract transactions
                if in_purchase_section or in_payment_section or in_fees_section:
                    # Look for transaction pattern: date followed by description and amount
                    # Discover format: MM/DD description amount
                    date_pattern = r'(\d{2}/\d{2})'
                    amount_pattern = r'(\d+\.\d{2})'
                    
                    if re.match(date_pattern, line):
                        # Extract date
                        date_match = re.match(date_pattern, line)
                        if date_match:
                            trans_date = date_match.group(1)
                            # Add current year (2025)
                            trans_date_full = f"{trans_date}/2025"
                            
                            # Extract amount (look for dollar amounts)
                            amount_matches = re.findall(amount_pattern, line)
                            if amount_matches:
                                amount = float(amount_matches[-1])  # Take the last amount found
                                
                                # Extract description (between date and amount)
                                desc_start = len(date_match.group(0))
                                desc_text = line[desc_start:].strip()
                                # Remove the amount from description
                                desc_text = re.sub(r'\s*\d+\.\d{2}\s*$', '', desc_text).strip()
                                
                                # Determine transaction type and sign
                                if in_payment_section:
                                    trans_type = "Payment/Credit"
                                    amount = -amount  # Negative for payments/credits
                                elif in_fees_section or "INTEREST CHARGE" in desc_text.upper():
                                    trans_type = "Interest/Fee"
                                    # Keep positive for interest charges
                                else:
                                    trans_type = "Purchase"
                                    # Keep positive for purchases
                                
                                transaction = {
                                    'Description': desc_text,
                                    'Amount': amount,
                                    'Transaction Date': trans_date_full,
                                    'Transaction Type': trans_type,
                                    'Status': 'New',
                                    'Statement id': '2025-05 - Discover 1342',
                                    'Bank and last 4': 'Discover 1342'
                                }
                                transactions.append(transaction)
                    
                    # Also check for interest charges that might be on a separate line
                    elif in_fees_section and "INTEREST CHARGE ON PURCHASES" in line:
                        # Look for amount on same or next line
                        amount_matches = re.findall(amount_pattern, line)
                        if amount_matches:
                            amount = float(amount_matches[-1])
                            transaction = {
                                'Description': 'INTEREST CHARGE ON PURCHASES',
                                'Amount': amount,
                                'Transaction Date': '05/12/2025',  # Use statement date
                                'Transaction Type': 'Interest/Fee',
                                'Status': 'New',
                                'Statement id': '2025-05 - Discover 1342',
                                'Bank and last 4': 'Discover 1342'
                            }
                            transactions.append(transaction)
    
    # Create DataFrame and save to CSV
    if transactions:
        df = pd.DataFrame(transactions)
        df.to_csv(output_csv, index=False)
        print(f"Extracted {len(transactions)} transactions to {output_csv}")
        print("\nTransaction summary:")
        print(f"- Purchases: {len([t for t in transactions if t['Transaction Type'] == 'Purchase'])}")
        print(f"- Payments/Credits: {len([t for t in transactions if t['Transaction Type'] == 'Payment/Credit'])}")
        print(f"- Interest/Fees: {len([t for t in transactions if t['Transaction Type'] == 'Interest/Fee'])}")
        print(f"- Total amount: ${df['Amount'].sum():.2f}")
    else:
        print("No transactions found in the PDF")

if __name__ == "__main__":
    pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250512-1342.pdf"
    output_csv = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-05_transactions.csv"
    
    extract_discover_transactions(pdf_path, output_csv)