#!/usr/bin/env python3
"""
Fixed Chase extraction that properly captures all transactions including those
at page boundaries and spanning multiple lines.
"""

import PyPDF2
import re
import csv
from pathlib import Path
from typing import Dict, List, Tuple

class ChaseMultiAccountExtractor:
    """Extract transactions from Chase multi-account PDFs with improved parsing."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pages = []
        self.account_sections = {}
        self.month = None
        self.year = 2025
        
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
        """Identify which pages belong to which account based on CHECKING SUMMARY."""
        current_account = None
        
        for i, page in enumerate(self.pages):
            text = page['text']
            page_num = page['page_num']
            
            # Skip page 1 (cover page)
            if page_num == 1:
                continue
                
            # Look for CHECKING SUMMARY to identify account starts
            if 'CHECKING SUMMARY' in text and 'Beginning Balance' in text:
                # Extract balances
                beginning_match = re.search(r'Beginning Balance\s*\$([0-9,]+\.\d{2})', text)
                ending_match = re.search(r'Ending Balance\s*\$([0-9,]+\.\d{2})', text)
                
                # Determine which account based on context
                if 'CHASE TOTAL CHECKING' in text:
                    current_account = '8619'
                elif page_num == 2:  # First CHECKING SUMMARY is usually 2084
                    current_account = '2084'
                elif beginning_match and beginning_match.group(1) == '16,087.31':
                    # This is specifically the February 1873 starting balance
                    current_account = '1873'
                elif self.account_sections and '2084' in self.account_sections and '1873' not in self.account_sections:
                    # If we've seen 2084 but not 1873 yet, this should be 1873
                    current_account = '1873'
                else:
                    # Default sequence
                    if not self.account_sections:
                        current_account = '2084'
                    elif '2084' in self.account_sections and '1873' not in self.account_sections:
                        current_account = '1873'
                    else:
                        current_account = '8619'
                
                if current_account not in self.account_sections:
                    self.account_sections[current_account] = {
                        'pages': [page_num],
                        'start_page': page_num,
                        'transactions': [],
                        'beginning_balance': float(beginning_match.group(1).replace(',', '')) if beginning_match else 0,
                        'ending_balance': float(ending_match.group(1).replace(',', '')) if ending_match else 0
                    }
                    
            # Add continuation pages
            elif current_account:
                if current_account in self.account_sections:
                    if page_num not in self.account_sections[current_account]['pages']:
                        self.account_sections[current_account]['pages'].append(page_num)
                        
                # Check if this page has the start of the next account
                if 'CHASE TOTAL CHECKING' in text and 'CHECKING SUMMARY' in text and current_account == '1873':
                    # This page contains both end of 1873 and start of 8619
                    # We'll handle the split in transaction extraction
                    pass
                        
        print(f"\nIdentified account sections:")
        for account, info in self.account_sections.items():
            print(f"  Account {account}: pages {info['pages']} (Balance: ${info['beginning_balance']:,.2f} -> ${info['ending_balance']:,.2f})")
                
    def extract_transactions_from_page(self, text: str, account: str) -> List[Dict]:
        """Extract transactions from a page of text with improved parsing."""
        transactions = []
        
        # For account 1873, check if we need to stop at CHASE TOTAL CHECKING
        if account == '1873' and 'CHASE TOTAL CHECKING' in text:
            # Split the text at CHASE TOTAL CHECKING and only process the part before it
            split_index = text.find('CHASE TOTAL CHECKING')
            text = text[:split_index]
        
        # Split into lines but preserve the original structure better
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and headers
            if not line or 'TRANSACTION DETAIL' in line or 'CHECKING SUMMARY' in line or 'DATE DESCRIPTION' in line:
                i += 1
                continue
                
            # Look for transaction pattern: MM/DD at start of line
            date_match = re.match(r'^(\d{2}/\d{2})\s+(.+)', line)
            if date_match:
                date_str = date_match.group(1)
                rest_of_line = date_match.group(2).strip()
                
                # Special handling for "02/06 Online Transfer" format
                if re.match(r'^\d{2}/\d{2}\s+Online Transfer', rest_of_line):
                    # This is a transaction where the date appears twice
                    parts = rest_of_line.split(maxsplit=1)
                    if len(parts) > 1:
                        rest_of_line = parts[1]
                
                # Look for amount pattern at end of line
                # Pattern: amount balance (with optional negative sign and commas)
                amount_pattern = r'(-?\s*[0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})\s*$'
                amount_match = re.search(amount_pattern, rest_of_line)
                
                if amount_match:
                    # Found complete transaction on one line
                    amount_str = amount_match.group(1).replace(' ', '').replace(',', '')
                    balance_str = amount_match.group(2).replace(',', '')
                    description = rest_of_line[:amount_match.start()].strip()
                    
                    # Parse amount
                    amount = float(amount_str)
                    
                    # For Chase, amounts are shown as positive in PDF but need sign adjustment
                    if amount > 0 and not self.is_credit(description):
                        amount = -amount
                        
                    transactions.append({
                        'date': f"{self.year}-{date_str.replace('/', '-')}",
                        'description': description,
                        'amount': amount,
                        'type': self.categorize_transaction(description)
                    })
                else:
                    # Transaction might span multiple lines
                    # Collect the description across lines until we find the amount
                    description = rest_of_line
                    i += 1
                    
                    while i < len(lines):
                        next_line = lines[i].strip()
                        
                        # Stop if we hit another date
                        if re.match(r'^\d{2}/\d{2}', next_line):
                            i -= 1  # Back up to process this line in outer loop
                            break
                            
                        # Look for amount pattern in this line
                        amount_match = re.search(amount_pattern, next_line)
                        if amount_match:
                            amount_str = amount_match.group(1).replace(' ', '').replace(',', '')
                            
                            # Add any description part before amount
                            desc_part = next_line[:amount_match.start()].strip()
                            if desc_part and desc_part != '-':
                                description += ' ' + desc_part
                                
                            # Parse amount
                            amount = float(amount_str)
                            
                            # Adjust sign
                            if amount > 0 and not self.is_credit(description):
                                amount = -amount
                                
                            transactions.append({
                                'date': f"{self.year}-{date_str.replace('/', '-')}",
                                'description': description.strip(),
                                'amount': amount,
                                'type': self.categorize_transaction(description)
                            })
                            break
                        else:
                            # This line is part of the description
                            if next_line and next_line != '-':
                                description += ' ' + next_line
                        i += 1
                    
            i += 1
            
        return transactions
    
    def is_credit(self, description: str) -> bool:
        """Determine if transaction is a credit (positive amount)."""
        desc_lower = description.lower()
        credit_keywords = [
            'deposit', 'interest payment', 'online transfer from',
            'cashout', 'from chk', 'credit', 'environmental'
        ]
        return any(keyword in desc_lower for keyword in credit_keywords)
    
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
        elif 'environmental' in desc_lower:
            return 'Payment'
        else:
            return 'Withdrawal'
    
    def extract_all_accounts(self):
        """Extract transactions for all accounts."""
        self.load_pdf()
        self.identify_account_sections()
        
        # Extract month from filename
        if match := re.search(r'(\d{4})(\d{2})\d{2}-statements', self.pdf_path):
            self.month = int(match.group(2))
        
        # Extract transactions for each account
        for account, info in self.account_sections.items():
            print(f"\nExtracting account {account} from pages {info['pages']}")
            
            for page_num in info['pages']:
                page_text = self.pages[page_num - 1]['text']
                transactions = self.extract_transactions_from_page(page_text, account)
                info['transactions'].extend(transactions)
                
            print(f"Found {len(info['transactions'])} transactions for account {account}")
            
            # Calculate totals for verification
            total_credits = sum(t['amount'] for t in info['transactions'] if t['amount'] > 0)
            total_debits = sum(t['amount'] for t in info['transactions'] if t['amount'] < 0)
            net_change = total_credits + total_debits
            
            print(f"  Credits: ${total_credits:,.2f}")
            print(f"  Debits: ${total_debits:,.2f}")
            print(f"  Net change: ${net_change:,.2f}")
            
            expected_ending = info['beginning_balance'] + net_change
            print(f"  Expected ending: ${expected_ending:,.2f} (Actual: ${info['ending_balance']:,.2f})")
            
            # Check reconciliation
            diff = abs(expected_ending - info['ending_balance'])
            if diff < 0.01:
                print(f"  ✓ Reconciles perfectly!")
            else:
                print(f"  ✗ Reconciliation difference: ${diff:,.2f}")
            
    def save_transactions(self, account: str):
        """Save transactions for an account to CSV."""
        if account not in self.account_sections:
            print(f"No transactions found for account {account}")
            return
            
        transactions = self.account_sections[account]['transactions']
        
        # Create output directory
        output_dir = Path(f"accounts/Chase {account}/{self.year}/monthly")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Output filename
        filename = f"chase_{account}_{self.year}-{self.month:02d}_transactions.csv"
        output_path = output_dir / filename
        
        # Convert to standard format
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                         'Status', 'Statement id', 'Bank and last 4']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tx in transactions:
                writer.writerow({
                    'Description': tx['description'],
                    'Amount': tx['amount'],
                    'Transaction Date': tx['date'],
                    'Transaction Type': tx['type'],
                    'Status': 'New',
                    'Statement id': f'{self.year}-{self.month:02d} - Chase {account}',
                    'Bank and last 4': f'Chase {account}'
                })
                
        print(f"Saved {len(transactions)} transactions to {output_path}")
        return output_path

def main():
    """Extract February 2025 Chase statement with fixed parser."""
    
    pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873/20250207-statements-1873-.pdf"
    
    print("Extracting Chase February 2025 with fixed parser")
    print("=" * 70)
    
    extractor = ChaseMultiAccountExtractor(pdf_path)
    extractor.extract_all_accounts()
    
    # Save each account
    for account in ['2084', '1873', '8619']:
        extractor.save_transactions(account)

if __name__ == "__main__":
    main()