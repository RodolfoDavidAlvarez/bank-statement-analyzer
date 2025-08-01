#!/usr/bin/env python3
"""Extract transactions from Chase multi-account PDF statements."""

import os
import sys
import subprocess
import re
import csv
from datetime import datetime
from pathlib import Path

def extract_pdf_text(pdf_path):
    """Extract text from PDF using macOS textutil command."""
    try:
        result = subprocess.run(
            ['textutil', '-convert', 'txt', '-stdout', pdf_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting PDF: {e}")
        return None

def parse_date(date_str):
    """Parse date from MM/DD format to YYYY-MM-DD."""
    month, day = date_str.split('/')
    year = 2025  # Hardcoded for now, could be extracted from statement
    return f"{year}-{int(month):02d}-{int(day):02d}"

def extract_transactions_for_account(text, account_number, statement_date):
    """Extract transactions for a specific account from the text."""
    transactions = []
    
    # Find the account section
    account_pattern = rf"Account number:.*{account_number}"
    account_match = re.search(account_pattern, text, re.IGNORECASE)
    
    if not account_match:
        print(f"Could not find account {account_number} in statement")
        return transactions
    
    # Extract text for this account (until next account or end)
    start_pos = account_match.start()
    next_account = re.search(r"Account number:", text[account_match.end():])
    
    if next_account:
        end_pos = account_match.end() + next_account.start()
        account_text = text[start_pos:end_pos]
    else:
        account_text = text[start_pos:]
    
    # Define bank name mapping
    bank_names = {
        '2084': 'Chase 2084',
        '1873': 'Chase 1873', 
        '8619': 'Chase 8619'
    }
    
    # Extract transactions based on account type
    if account_number in ['2084', '1873']:
        # Checking accounts - look for transaction patterns
        lines = account_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Match transaction patterns
            # Format: MM/DD Description Amount
            tx_pattern = r'^(\d{2}/\d{2})\s+(.+?)\s+([\d,]+\.\d{2})$'
            match = re.match(tx_pattern, line)
            
            if match:
                date_str, desc, amount_str = match.groups()
                amount = float(amount_str.replace(',', ''))
                
                # Determine transaction type and sign
                desc_lower = desc.lower()
                if any(word in desc_lower for word in ['deposit', 'credit', 'pmt', 'cashout']):
                    tx_type = 'Credit' if 'credit' in desc_lower else 'Deposit'
                elif any(word in desc_lower for word in ['payment', 'transfer to', 'venmo payment']):
                    tx_type = 'Payment' if 'payment' in desc_lower else 'Transfer'
                    amount = -amount
                elif 'card purchase' in desc_lower:
                    tx_type = 'Debit'
                    amount = -amount
                elif 'check' in desc_lower:
                    tx_type = 'Check'
                    amount = -amount
                elif any(word in desc_lower for word in ['withdrawal', 'ach']):
                    tx_type = 'Withdrawal'
                    amount = -amount
                elif 'recurring' in desc_lower:
                    tx_type = 'Debit'
                    amount = -amount
                elif 'interest payment' in desc_lower:
                    tx_type = 'Interest'
                else:
                    # Default to debit for unknown
                    tx_type = 'Debit'
                    amount = -amount
                
                transaction = {
                    'Description': desc,
                    'Amount': amount,
                    'Transaction Date': parse_date(date_str),
                    'Transaction Type': tx_type,
                    'Status': 'New',
                    'Statement id': statement_date,
                    'Bank and last 4': bank_names.get(account_number, f'Chase {account_number}')
                }
                transactions.append(transaction)
    
    elif account_number == '8619':
        # Total Checking - different format
        lines = account_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for transaction patterns specific to this account
            if 'State Farm' in line or 'Online Transfer' in line or 'Online Payment' in line:
                # Extract date and amount
                date_match = re.search(r'(\d{2}/\d{2})', line)
                amount_match = re.search(r'([\d,]+\.\d{2})$', line)
                
                if date_match and amount_match:
                    date_str = date_match.group(1)
                    amount = float(amount_match.group(1).replace(',', ''))
                    
                    # Extract description
                    desc = line[:amount_match.start()].strip()
                    desc = re.sub(r'\d{2}/\d{2}\s*', '', desc).strip()
                    
                    # Determine type and sign
                    if 'transfer from' in desc.lower() or 'deposit' in desc.lower():
                        tx_type = 'Deposit'
                    elif 'service fee' in desc.lower():
                        tx_type = 'Fee'
                        amount = -amount
                    else:
                        tx_type = 'Withdrawal'
                        amount = -amount
                    
                    transaction = {
                        'Description': desc,
                        'Amount': amount,
                        'Transaction Date': parse_date(date_str),
                        'Transaction Type': tx_type,
                        'Status': 'New',
                        'Statement id': statement_date,
                        'Bank and last 4': bank_names.get(account_number, f'Chase {account_number}')
                    }
                    transactions.append(transaction)
    
    # Look for interest if not found
    interest_match = re.search(r'Interest\s+payment\s+([\d,]+\.\d{2})', account_text, re.IGNORECASE)
    if interest_match and not any(t['Transaction Type'] == 'Interest' for t in transactions):
        amount = float(interest_match.group(1).replace(',', ''))
        # Find the date - usually at end of statement period
        transaction = {
            'Description': 'Interest Payment',
            'Amount': amount,
            'Transaction Date': f"2025-{statement_date.split('-')[1]}-07",  # Usually on 7th
            'Transaction Type': 'Interest',
            'Status': 'New',
            'Statement id': statement_date,
            'Bank and last 4': bank_names.get(account_number, f'Chase {account_number}')
        }
        transactions.append(transaction)
    
    return transactions

def save_transactions(transactions, account_number, month):
    """Save transactions to CSV file."""
    if not transactions:
        print(f"No transactions found for account {account_number}")
        return
    
    # Create output directory
    output_dir = Path(f"/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase {account_number}/2025/monthly")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output filename
    filename = f"chase_{account_number}_2025-{month:02d}_transactions.csv"
    output_path = output_dir / filename
    
    # Write CSV
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                     'Status', 'Statement id', 'Bank and last 4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)
    
    print(f"Saved {len(transactions)} transactions to {output_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_chase_multi_account.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Extract month from filename (assuming format: YYYYMMDD-statements-XXXX-.pdf)
    filename = os.path.basename(pdf_path)
    date_match = re.match(r'(\d{4})(\d{2})(\d{2})', filename)
    if date_match:
        year = date_match.group(1)
        month = int(date_match.group(2))
        statement_date = f"{year}-{month:02d} - Chase"
    else:
        print("Could not extract date from filename")
        sys.exit(1)
    
    # Extract PDF text
    print(f"Extracting text from {pdf_path}...")
    text = extract_pdf_text(pdf_path)
    if not text:
        print("Failed to extract text from PDF")
        sys.exit(1)
    
    # Extract transactions for each account
    accounts = ['2084', '1873', '8619']
    
    for account in accounts:
        print(f"\nExtracting transactions for account {account}...")
        transactions = extract_transactions_for_account(text, account, f"{statement_date} {account}")
        save_transactions(transactions, account, month)

if __name__ == "__main__":
    main()