#!/usr/bin/env python3
"""
Extract all Chase multi-account statements (Feb-June 2025) using corrected methodology.
This script properly identifies account sections using CHECKING SUMMARY markers
and follows (continued) pages correctly.
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
        
        for i, page in enumerate(self.pages):
            text = page['text']
            page_num = page['page_num']
            
            # Skip page 1 (cover page)
            if page_num == 1:
                continue
                
            # Look for CHECKING SUMMARY to identify account starts
            if 'CHECKING SUMMARY' in text:
                # Extract balances to help identify account
                beginning_match = re.search(r'Beginning Balance.*?\$([0-9,]+\.\d{2})', text)
                ending_match = re.search(r'Ending Balance.*?\$([0-9,]+\.\d{2})', text)
                
                # Determine which account based on patterns
                if 'CHASE TOTAL CHECKING' in text:
                    current_account = '8619'
                elif page_num == 2:  # First CHECKING SUMMARY is usually 2084
                    current_account = '2084'
                elif current_account == '2084':  # Second is usually 1873
                    current_account = '1873'
                else:
                    # Try to identify from balance patterns or card numbers
                    if 'Card 0665' in text:
                        current_account = '1873'
                    elif 'Card 0885' in text:
                        current_account = '2084'
                    else:
                        # Default sequence
                        current_account = '1873' if current_account == '2084' else '8619'
                
                if current_account not in self.account_sections:
                    self.account_sections[current_account] = {
                        'pages': [page_num],
                        'start_page': page_num,
                        'transactions': [],
                        'beginning_balance': float(beginning_match.group(1).replace(',', '')) if beginning_match else 0,
                        'ending_balance': float(ending_match.group(1).replace(',', '')) if ending_match else 0
                    }
                else:
                    # New CHECKING SUMMARY for same account shouldn't happen
                    print(f"Warning: Multiple CHECKING SUMMARY for account {current_account}")
                    
            # Add continuation pages
            elif current_account and ('(continued)' in text or 'TRANSACTION DETAIL' in text):
                if current_account in self.account_sections:
                    if page_num not in self.account_sections[current_account]['pages']:
                        self.account_sections[current_account]['pages'].append(page_num)
                        
        print(f"\nIdentified account sections:")
        for account, info in self.account_sections.items():
            print(f"  Account {account}: pages {info['pages']} (Balance: ${info['beginning_balance']:,.2f} -> ${info['ending_balance']:,.2f})")
                
    def extract_transactions_from_page(self, text: str) -> List[Dict]:
        """Extract transactions from a page of text."""
        transactions = []
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
                    while i < len(lines) and not re.match(r'^\d{2}/\d{2}', lines[i]):
                        next_line = lines[i].strip()
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
                    continue
                    
            i += 1
            
        return transactions
    
    def is_credit(self, description: str) -> bool:
        """Determine if transaction is a credit (positive amount)."""
        desc_lower = description.lower()
        credit_keywords = [
            'deposit', 'interest payment', 'online transfer from',
            'cashout', 'from chk', 'credit'
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
        
        # Extract month from PDF text
        for page in self.pages[:2]:  # Check first two pages
            if match := re.search(r'(January|February|March|April|May|June)\s+\d+,?\s*\d{4}', page['text']):
                month_name = match.group(1)
                self.month = {
                    'January': 1, 'February': 2, 'March': 3,
                    'April': 4, 'May': 5, 'June': 6
                }.get(month_name, 2)
                break
        
        # Extract transactions for each account
        for account, info in self.account_sections.items():
            print(f"\nExtracting account {account} from pages {info['pages']}")
            
            for page_num in info['pages']:
                page_text = self.pages[page_num - 1]['text']
                transactions = self.extract_transactions_from_page(page_text)
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
    
    # Base directory for statements
    base_dir = Path("/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025")
    
    # Find all Chase statement PDFs
    statement_files = {
        2: "Nancy - Bennet - Chase Statements (Personal) - Februray 2025.pdf",
        3: "Nancy - Bennet - Chase Statements (Personal) - March 2025.pdf",
        4: "Nancy - Bennet - Chase Statements (Personal) - April 2025.pdf",
        5: "Nancy - Bennet - Chase Statements (Personal) - May 2025.pdf",
        6: "Nancy - Bennet - Chase Statements (Personal) - June 2025.pdf"
    }
    
    print("Extracting Chase multi-account statements using corrected methodology")
    print("=" * 70)
    print("Key points:")
    print("- Ignoring misleading 'Primary Account' headers")
    print("- Using CHECKING SUMMARY to identify account sections")
    print("- Following (continued) markers correctly")
    print("- NOT forcing reconciliation\n")
    
    for month, filename in statement_files.items():
        pdf_path = base_dir / filename
        
        if not pdf_path.exists():
            print(f"\nWarning: {filename} not found, skipping...")
            continue
            
        print(f"\n{'='*70}")
        print(f"Processing {filename} (Month {month})")
        print(f"{'='*70}")
        
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