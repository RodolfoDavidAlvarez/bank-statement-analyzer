#!/usr/bin/env python3
"""
Extract transactions from Chase multi-account PDFs following the updated methodology.
This script does NOT force reconciliation - it extracts exactly what's in each account section.
"""

import PyPDF2
import re
import csv
from pathlib import Path
from typing import Dict, List, Tuple

class ChaseMultiAccountExtractor:
    """Extract transactions from Chase multi-account PDFs."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pages = []
        self.account_sections = {}
        
    def load_pdf(self):
        """Load PDF and extract text from all pages."""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                self.pages.append({
                    'page_num': page_num + 1,
                    'text': page_text
                })
                
    def identify_account_sections(self):
        """Identify which pages belong to which account."""
        current_account = None
        
        for page in self.pages:
            text = page['text']
            page_num = page['page_num']
            
            # Check if this page starts a new account section
            if 'CHECKING SUMMARY' in text and 'Beginning Balance' in text:
                # This is the start of a new account
                # Try to identify which account
                if 'Ending Balance $2,871.09' in text or 'Ending Balance $1,422.38' in text:
                    current_account = '2084'  # These are typical 2084 ending balances
                elif '16,087.31' in text or '4,584.13' in text:
                    current_account = '1873'  # These appear in 1873 sections
                elif 'CHASE TOTAL CHECKING' in text:
                    current_account = '8619'
                else:
                    # Try to determine from context
                    if page_num == 2:
                        current_account = '2084'  # Usually first
                    elif current_account == '2084':
                        current_account = '1873'  # Usually second
                    else:
                        current_account = '8619'  # Usually third
                
                if current_account not in self.account_sections:
                    self.account_sections[current_account] = {
                        'pages': [],
                        'start_page': page_num,
                        'transactions': []
                    }
                    
            # Check if this is a continuation page
            elif '(continued)' in text and current_account:
                # This page continues the current account
                pass
            
            # Check for explicit account changes
            elif 'CHASE TOTAL CHECKING' in text and 'CHECKING SUMMARY' in text:
                current_account = '8619'
                if '8619' not in self.account_sections:
                    self.account_sections['8619'] = {
                        'pages': [],
                        'start_page': page_num,
                        'transactions': []
                    }
            
            # Add page to current account if identified
            if current_account and current_account in self.account_sections:
                self.account_sections[current_account]['pages'].append(page_num)
                
    def extract_transactions_from_text(self, text: str) -> List[Dict]:
        """Extract transactions from text."""
        transactions = []
        lines = text.split('\n')
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
                
            # Look for transaction patterns
            # Format: MM/DD Description Amount Balance
            date_match = re.match(r'^(\d{2}/\d{2})\s+(.+?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})$', line)
            if date_match:
                date_str = date_match.group(1)
                desc = date_match.group(2).strip()
                amount_str = date_match.group(3)
                
                # Parse amount and determine sign
                amount = float(amount_str.replace(',', ''))
                
                # Determine transaction type from description
                tx_type = self.categorize_transaction(desc)
                
                # Determine sign based on description
                if any(word in desc.lower() for word in ['deposit', 'from chk', 'cashout', 'interest payment']):
                    # These are credits
                    pass
                else:
                    # Most transactions are debits
                    amount = -amount
                    
                transactions.append({
                    'date': date_str,
                    'description': desc,
                    'amount': amount,
                    'type': tx_type
                })
                
        return transactions
    
    def categorize_transaction(self, desc: str) -> str:
        """Categorize transaction based on description."""
        desc_lower = desc.lower()
        
        if 'interest payment' in desc_lower:
            return 'Interest'
        elif 'check' in desc_lower and '#' in desc:
            return 'Check'
        elif 'card purchase' in desc_lower:
            return 'Debit'
        elif 'online payment' in desc_lower:
            return 'Payment'
        elif 'online transfer to' in desc_lower:
            return 'Transfer'
        elif 'online transfer from' in desc_lower:
            return 'Deposit'
        elif 'deposit' in desc_lower:
            return 'Deposit'
        elif 'fee' in desc_lower:
            return 'Fee'
        elif 'venmo' in desc_lower:
            return 'Withdrawal'
        else:
            return 'Withdrawal'
    
    def extract_all_accounts(self):
        """Extract transactions for all accounts."""
        self.load_pdf()
        self.identify_account_sections()
        
        # Extract transactions for each account
        for account, info in self.account_sections.items():
            print(f"\nExtracting account {account} from pages {info['pages']}")
            
            for page_num in info['pages']:
                page_text = self.pages[page_num - 1]['text']
                transactions = self.extract_transactions_from_text(page_text)
                info['transactions'].extend(transactions)
                
            print(f"Found {len(info['transactions'])} transactions for account {account}")
            
    def save_transactions(self, account: str, month: int, year: int = 2025):
        """Save transactions for an account to CSV."""
        if account not in self.account_sections:
            print(f"No transactions found for account {account}")
            return
            
        transactions = self.account_sections[account]['transactions']
        
        # Create output directory
        output_dir = Path(f"accounts/Chase {account}/{year}/monthly")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Output filename
        filename = f"chase_{account}_{year}-{month:02d}_transactions.csv"
        output_path = output_dir / filename
        
        # Convert to standard format
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                         'Status', 'Statement id', 'Bank and last 4']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tx in transactions:
                # Convert date from MM/DD to YYYY-MM-DD
                month_str, day_str = tx['date'].split('/')
                date_formatted = f"{year}-{month_str.zfill(2)}-{day_str.zfill(2)}"
                
                writer.writerow({
                    'Description': tx['description'],
                    'Amount': tx['amount'],
                    'Transaction Date': date_formatted,
                    'Transaction Type': tx['type'],
                    'Status': 'New',
                    'Statement id': f'{year}-{month:02d} - Chase {account}',
                    'Bank and last 4': f'Chase {account}'
                })
                
        print(f"Saved {len(transactions)} transactions to {output_path}")

def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_chase_multipage.py <pdf_path> [month]")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    month = int(sys.argv[2]) if len(sys.argv) > 2 else 2  # Default to February
    
    print(f"Extracting from: {pdf_path}")
    print("Note: This extraction does NOT force reconciliation")
    print("It extracts exactly what appears in each account section")
    
    extractor = ChaseMultiAccountExtractor(pdf_path)
    extractor.extract_all_accounts()
    
    # Save each account
    for account in ['2084', '1873', '8619']:
        extractor.save_transactions(account, month)

if __name__ == "__main__":
    main()