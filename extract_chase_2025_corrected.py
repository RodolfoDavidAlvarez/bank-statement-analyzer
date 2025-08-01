#!/usr/bin/env python3
"""
Extract Chase 2025 statements using corrected methodology.
These are multi-account PDFs stored in individual account directories.
"""

import PyPDF2
import re
import csv
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class ChaseMultiAccountExtractor:
    """Extract transactions from Chase multi-account PDFs following corrected methodology."""
    
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
        account_start_page = None
        
        for i, page in enumerate(self.pages):
            text = page['text']
            page_num = page['page_num']
            
            # Skip page 1 (cover page)
            if page_num == 1:
                continue
                
            # Look for CHECKING SUMMARY to identify account starts
            if 'CHECKING SUMMARY' in text and 'Beginning Balance' in text:
                # Save previous account's end page if needed
                if current_account and current_account in self.account_sections:
                    self.account_sections[current_account]['end_page'] = page_num - 1
                
                # Extract balances
                beginning_match = re.search(r'Beginning Balance\s*\$([0-9,]+\.\d{2})', text)
                ending_match = re.search(r'Ending Balance\s*\$([0-9,]+\.\d{2})', text)
                
                # Determine which account based on context and position
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
                    # Try to identify from account number if visible
                    if '000000526021873' in text or 'Account ...1873' in text:
                        current_account = '1873'
                    elif '000000837532084' in text or 'Account ...2084' in text:
                        current_account = '2084'
                    elif '000001248068619' in text or 'Account ...8619' in text:
                        current_account = '8619'
                
                account_start_page = page_num
                
                if current_account:
                    self.account_sections[current_account] = {
                        'start_page': page_num,
                        'end_page': None,  # Will be set when next account starts or at end
                        'pages': [page_num],
                        'transactions': [],
                        'beginning_balance': float(beginning_match.group(1).replace(',', '')) if beginning_match else 0,
                        'ending_balance': float(ending_match.group(1).replace(',', '')) if ending_match else 0
                    }
                    
            # Add continuation pages
            elif current_account and ('(continued)' in text or 'TRANSACTION DETAIL' in text):
                if current_account in self.account_sections:
                    if page_num not in self.account_sections[current_account]['pages']:
                        self.account_sections[current_account]['pages'].append(page_num)
                        
        # Set end page for last account
        if current_account and current_account in self.account_sections:
            self.account_sections[current_account]['end_page'] = len(self.pages)
                        
        print(f"\nIdentified account sections:")
        for account, info in self.account_sections.items():
            print(f"  Account {account}: pages {info['pages']} (Balance: ${info['beginning_balance']:,.2f} -> ${info['ending_balance']:,.2f})")
                
    def extract_transactions_from_page(self, text: str, account: str) -> List[Dict]:
        """Extract transactions from a page of text."""
        transactions = []
        lines = text.split('\n')
        
        # For account 8619, also check if we've reached the next account's section
        if account == '1873' and 'CHASE TOTAL CHECKING' in text:
            # Split the text at CHASE TOTAL CHECKING and only process the part before it
            split_index = text.find('CHASE TOTAL CHECKING')
            text = text[:split_index]
            lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and headers
            if not line or 'TRANSACTION DETAIL' in line or 'CHECKING SUMMARY' in line:
                i += 1
                continue
                
            # Look for date pattern at start of line (MM/DD)
            date_match = re.match(r'^(\d{2}/\d{2})\s+(.+)', line)
            if date_match:
                date_str = date_match.group(1)
                rest_of_line = date_match.group(2)
                
                # Try to extract amount and balance from end of line
                # Pattern: amount balance (both with optional commas and decimals)
                amount_match = re.search(r'([0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})\s*$', rest_of_line)
                if amount_match:
                    # Found complete transaction on one line
                    amount_str = amount_match.group(1)
                    balance_str = amount_match.group(2)
                    description = rest_of_line[:amount_match.start()].strip()
                    
                    amount = float(amount_str.replace(',', ''))
                    
                    # Determine sign based on description
                    if self.is_credit(description):
                        pass  # Keep positive
                    else:
                        amount = -amount
                        
                    transactions.append({
                        'date': f"{self.year}-{date_str.replace('/', '-')}",
                        'description': description,
                        'amount': amount,
                        'type': self.categorize_transaction(description)
                    })
                else:
                    # Transaction might span multiple lines
                    description = rest_of_line
                    i += 1
                    
                    # Look for amount on next line(s)
                    while i < len(lines):
                        next_line = lines[i].strip()
                        
                        # Stop if we hit another date or certain keywords
                        if re.match(r'^\d{2}/\d{2}', next_line) or 'CHECKING SUMMARY' in next_line:
                            i -= 1  # Back up to process this line in the outer loop
                            break
                            
                        if next_line:
                            # Check if this line has the amount
                            amount_match = re.search(r'([0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})\s*$', next_line)
                            if amount_match:
                                amount_str = amount_match.group(1)
                                amount = float(amount_str.replace(',', ''))
                                
                                # Add any description part before amount
                                desc_part = next_line[:amount_match.start()].strip()
                                if desc_part:
                                    description += ' ' + desc_part
                                    
                                # Determine sign
                                if self.is_credit(description):
                                    pass  # Keep positive
                                else:
                                    amount = -amount
                                    
                                transactions.append({
                                    'date': f"{self.year}-{date_str.replace('/', '-')}",
                                    'description': description,
                                    'amount': amount,
                                    'type': self.categorize_transaction(description)
                                })
                                break
                            else:
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
            print(f"  Expected ending: ${info['beginning_balance'] + net_change:,.2f} (Actual: ${info['ending_balance']:,.2f})")
            
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
    """Extract all Chase statements from February to June 2025."""
    
    # Base directories - the PDFs are duplicated in multiple locations
    base_dirs = {
        '2084': Path("/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statement NB Personal Account"),
        '1873': Path("/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873")
    }
    
    # Statement files to process
    months = {
        2: "20250207-statements-",
        3: "20250307-statements-", 
        4: "20250407-statements-",
        5: "20250507-statements-",
        6: "20250606-statements-"
    }
    
    print("Extracting Chase multi-account statements using corrected methodology")
    print("=" * 70)
    print("Key points:")
    print("- These ARE multi-account PDFs (containing 2084, 1873, and 8619)")
    print("- Ignoring misleading 'Primary Account' headers")
    print("- Using CHECKING SUMMARY to identify account sections")
    print("- Following (continued) markers correctly")
    print("- NOT forcing reconciliation\n")
    
    # Process each month
    for month, file_prefix in months.items():
        print(f"\n{'='*70}")
        print(f"Processing Month {month}/2025")
        print(f"{'='*70}")
        
        # Try to find the PDF in either directory
        pdf_path = None
        for account, base_dir in base_dirs.items():
            potential_path = base_dir / f"{file_prefix}{account}-.pdf"
            if potential_path.exists():
                pdf_path = potential_path
                print(f"Found PDF at: {pdf_path}")
                break
                
        if not pdf_path:
            print(f"Warning: No PDF found for month {month}")
            continue
            
        extractor = ChaseMultiAccountExtractor(str(pdf_path))
        extractor.extract_all_accounts()
        
        # Save each account
        for account in ['2084', '1873', '8619']:
            extractor.save_transactions(account)
            
    print("\n\nExtraction complete!")
    print("All transactions extracted based on their actual position in the PDF.")
    print("No transactions were moved between accounts to force reconciliation.")

if __name__ == "__main__":
    main()