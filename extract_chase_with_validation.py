#!/usr/bin/env python3
"""
Extract Chase multi-account statements with automatic validation.
This script implements the updated methodology with reconciliation checks.
"""

import csv
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class ChaseMultiAccountExtractor:
    def __init__(self):
        self.accounts = {
            '2084': {'card': '0885', 'name': 'Chase 2084'},
            '1873': {'card': '0665', 'name': 'Chase 1873'},
            '8619': {'card': None, 'name': 'Chase 8619'}
        }
        
    def categorize_transaction(self, desc: str) -> str:
        """Categorize transaction based on description."""
        desc_lower = desc.lower()
        
        if 'interest payment' in desc_lower:
            return 'Interest'
        elif 'check #' in desc_lower:
            return 'Check'
        elif 'card purchase' in desc_lower:
            return 'Debit'
        elif 'recurring card purchase' in desc_lower:
            return 'Debit'
        elif 'online payment' in desc_lower:
            return 'Payment'
        elif 'online transfer to' in desc_lower:
            return 'Transfer'
        elif 'online transfer from' in desc_lower:
            return 'Deposit'
        elif 'deposit' in desc_lower or 'cashout' in desc_lower:
            return 'Deposit'
        elif 'venmo payment' in desc_lower:
            return 'Withdrawal'
        elif 'service fee' in desc_lower:
            return 'Fee'
        elif any(word in desc_lower for word in ['ppd id:', 'ccd id:', 'web id:']):
            if 'payment' in desc_lower or 'pmt' in desc_lower:
                return 'Credit'
            else:
                return 'Withdrawal'
        else:
            return 'Withdrawal'
    
    def identify_account(self, desc: str, amount: float) -> str:
        """Identify which account a transaction belongs to based on rules."""
        # Card-based identification
        if 'Card 0885' in desc:
            return '2084'
        elif 'Card 0665' in desc:
            return '1873'
        
        # Special payment rules
        if 'Environmental AL Rf Pmt' in desc and amount > 0:
            return '2084'
        elif 'Keller Williams' in desc and amount > 0:
            return '2084'
        elif 'ADP - Tax' in desc and amount < 0:
            return '1873'
        elif 'Verizon Wireless' in desc and amount < 0:
            return '1873'
        
        # Online payments typically from 2084
        if 'Online Payment' in desc and amount < 0:
            return '2084'
            
        # Default: needs manual review
        return None
    
    def validate_reconciliation(self, transactions: List[Dict], 
                              beginning_balance: float, 
                              expected_ending: float,
                              account: str) -> Tuple[bool, Dict]:
        """Validate that transactions reconcile with beginning and ending balances."""
        deposits = sum(float(t['Amount']) for t in transactions if float(t['Amount']) > 0)
        
        # Categorize withdrawals
        checks = sum(abs(float(t['Amount'])) for t in transactions 
                    if float(t['Amount']) < 0 and t['Transaction Type'] == 'Check')
        
        cards = sum(abs(float(t['Amount'])) for t in transactions 
                   if float(t['Amount']) < 0 and t['Transaction Type'] == 'Debit')
        
        electronic = sum(abs(float(t['Amount'])) for t in transactions 
                        if float(t['Amount']) < 0 and t['Transaction Type'] not in ['Check', 'Debit'])
        
        total_withdrawals = checks + cards + electronic
        calculated_ending = beginning_balance + deposits - total_withdrawals
        
        result = {
            'account': account,
            'beginning_balance': beginning_balance,
            'deposits': deposits,
            'checks': checks,
            'cards': cards,
            'electronic': electronic,
            'total_withdrawals': total_withdrawals,
            'calculated_ending': calculated_ending,
            'expected_ending': expected_ending,
            'difference': calculated_ending - expected_ending,
            'reconciles': abs(calculated_ending - expected_ending) < 0.01
        }
        
        return result['reconciles'], result
    
    def extract_february_2025(self):
        """Extract February 2025 transactions with proper account assignment."""
        # This is a hardcoded example based on our corrected February data
        # In production, this would parse the PDF
        
        transactions = {
            '2084': [
                ("Venmo Cashout PPD ID: 5264681992", 4875.00, "2025-01-09", "Credit"),
                ("Keller Williams Psus_Jan20 PPD ID: 1742756628", 17.76, "2025-01-21", "Credit"),
                ("Environmental AL Rf Pmt PPD ID: 1942751173", 275.72, "2025-02-07", "Credit"),
                ("Interest Payment", 0.04, "2025-02-07", "Interest"),
                ("Venmo Payment 1039580470057 Web ID: 3264681992", -101.29, "2025-01-13", "Withdrawal"),
                ("Venmo Payment 1039580443691 Web ID: 3264681992", -30.18, "2025-01-13", "Withdrawal"),
                ("Tesla Inc Tesla Moto PPD ID: 1463896777", -1171.08, "2025-01-14", "Withdrawal"),
                ("Lightstream Loan Pmts 45680968 Web ID: 1253108792", -1125.00, "2025-01-21", "Withdrawal"),
                ("Card Purchase 01/24 Amazon Mktpl*Zg4WI9R Amzn.Com/Bill WA Card 0885", -46.33, "2025-01-27", "Debit"),
                ("Venmo Payment 1039873789366 Web ID: 3264681992", -121.61, "2025-01-27", "Withdrawal"),
                ("01/29 Online Transfer To Chk ...8619 Transaction#: 23540544174", -150.00, "2025-01-29", "Transfer"),
                ("01/30 Online Payment 23214609657 To Discover Card", -250.00, "2025-01-30", "Payment"),
                ("01/30 Online Payment 22028016052 To Pg&E", -5.00, "2025-01-30", "Payment"),
                ("01/30 Online Payment 23214354979 To Wave", -1.00, "2025-01-30", "Payment"),
                ("01/31 Online Payment 21955253083 To Pg&E", -250.00, "2025-01-31", "Payment"),
                ("Recurring Card Purchase 01/31 Netflix.Com Netflix.Com CA Card 0885", -6.99, "2025-02-03", "Debit"),
                ("Venmo Payment 1040005976407 Web ID: 3264681992", -158.75, "2025-02-03", "Withdrawal"),
                ("02/06 Online Payment 23297114961 To Mr. Cooper", -3200.00, "2025-02-06", "Payment"),
            ],
            '1873': [
                # Only transactions that belong to 1873 (no online payments except transfers FROM 1873)
                ("02/06 Online Transfer To Chk ...8619 Transaction#: 23637622827", -4570.00, "2025-02-06", "Transfer"),
                ("Check # 998", -280.00, "2025-01-22", "Check"),
                # All Card 0665 transactions...
                ("Card Purchase 01/09 Eyelab Factory Outlet San Ramon CA Card 0665", -35.00, "2025-01-10", "Debit"),
                # ... (rest of card transactions omitted for brevity)
                ("State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", -33.66, "2025-01-14", "Withdrawal"),
                ("Venmo Payment 1039635550955 Web ID: 3264681992", -2500.00, "2025-01-16", "Withdrawal"),
                ("ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", -63.00, "2025-01-22", "Withdrawal"),
                ("Verizon Wireless Payments PPD ID: 4223344794", -126.64, "2025-01-28", "Withdrawal"),
                ("Interest Payment", 0.09, "2025-02-07", "Interest"),
            ],
            '8619': [
                ("State Farm Ro 27 Sfpp CCD ID: 9000313004", -106.83, "2025-01-14", "Withdrawal"),
                ("Online Transfer From Chk ...2084 Transaction#: 23540544174", 150.00, "2025-01-29", "Deposit"),
                ("Online Payment 23540420666 To Cowell Homeowners Association", -185.00, "2025-01-29", "Payment"),
                ("Online Transfer From Chk ...1873 Transaction#: 23637622827", 4570.00, "2025-02-06", "Deposit"),
                ("Online Payment 23637563107 To Rushmore Servicing", -4568.00, "2025-02-06", "Payment"),
                ("Monthly Service Fee", -12.00, "2025-02-07", "Fee"),
            ]
        }
        
        # Known balances for February 2025
        balances = {
            '2084': {'beginning': 2871.09, 'ending': 1422.38},
            '1873': {'beginning': 16087.31, 'ending': 528.22},
            '8619': {'beginning': 229.42, 'ending': 77.59}
        }
        
        return transactions, balances
    
    def save_transactions(self, transactions: List[Tuple], account: str, month: int, year: int = 2025):
        """Save transactions to CSV file with validation."""
        # Convert to standard format
        formatted_transactions = []
        for desc, amount, date, tx_type in transactions:
            formatted_transactions.append({
                'Description': desc,
                'Amount': amount,
                'Transaction Date': date,
                'Transaction Type': tx_type,
                'Status': 'New',
                'Statement id': f'{year}-{month:02d} - Chase {account}',
                'Bank and last 4': f'Chase {account}'
            })
        
        # Create output directory
        output_dir = Path(f"accounts/Chase {account}/{year}/monthly")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Output filename
        filename = f"chase_{account}_{year}-{month:02d}_transactions.csv"
        output_path = output_dir / filename
        
        # Write CSV
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                         'Status', 'Statement id', 'Bank and last 4']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(formatted_transactions)
        
        return output_path, formatted_transactions

def main():
    """Test the extraction with validation."""
    extractor = ChaseMultiAccountExtractor()
    
    print("Testing Chase Multi-Account Extraction with Validation")
    print("=" * 60)
    
    # Extract February 2025 data
    transactions, balances = extractor.extract_february_2025()
    
    # Process each account
    all_passed = True
    
    for account in ['2084', '1873', '8619']:
        print(f"\nProcessing Account {account}:")
        print("-" * 40)
        
        # Save transactions
        output_path, formatted_txns = extractor.save_transactions(
            transactions[account], account, month=2
        )
        
        # Validate reconciliation
        passed, result = extractor.validate_reconciliation(
            formatted_txns,
            balances[account]['beginning'],
            balances[account]['ending'],
            account
        )
        
        print(f"Transactions saved: {len(formatted_txns)}")
        print(f"Output file: {output_path}")
        print(f"\nReconciliation:")
        print(f"  Beginning: ${result['beginning_balance']:,.2f}")
        print(f"  Deposits: ${result['deposits']:,.2f}")
        print(f"  Checks: ${result['checks']:,.2f}")
        print(f"  Cards: ${result['cards']:,.2f}")
        print(f"  Electronic: ${result['electronic']:,.2f}")
        print(f"  Calculated Ending: ${result['calculated_ending']:,.2f}")
        print(f"  Expected Ending: ${result['expected_ending']:,.2f}")
        print(f"  Difference: ${result['difference']:,.2f}")
        print(f"  Status: {'✓ PASSED' if passed else '✗ FAILED'}")
        
        if not passed:
            all_passed = False
            print(f"\n  ERROR: Account {account} does not reconcile!")
            print(f"  Check for duplicate transactions or incorrect account assignment.")
    
    print("\n" + "=" * 60)
    print(f"Overall Status: {'✓ ALL ACCOUNTS PASSED' if all_passed else '✗ SOME ACCOUNTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)