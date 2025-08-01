#!/usr/bin/env python3
import re
from decimal import Decimal
import csv

def parse_pdf_transactions(pdf_text):
    """Parse transactions from PDF text"""
    transactions = []
    
    # Pattern to match transaction lines in the PDF
    # Date (MM/DD) followed by description and amount
    lines = pdf_text.split('\n')
    
    for i, line in enumerate(lines):
        # Look for lines that start with a date pattern
        if re.match(r'^\d{2}/\d{2}\s', line):
            # Extract date
            date_match = re.match(r'^(\d{2}/\d{2})\s+(.+)', line)
            if date_match:
                date = date_match.group(1)
                rest = date_match.group(2).strip()
                
                # Look for amount at the end of line or on next line
                # Check if amount is on the same line
                amount_match = re.search(r'[\s-]+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})$', rest)
                if amount_match:
                    amount = amount_match.group(1).replace(',', '')
                    balance = amount_match.group(2).replace(',', '')
                    description = rest[:amount_match.start()].strip()
                else:
                    # Check next line for amount
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        amount_match = re.match(r'^[\s\d-]*([\d,]+\.\d{2})\s+([\d,]+\.\d{2})', next_line)
                        if amount_match:
                            amount = amount_match.group(1).replace(',', '')
                            balance = amount_match.group(2).replace(',', '')
                            description = rest.strip()
                        else:
                            continue
                    else:
                        continue
                
                # Add a negative sign for debits (all transactions in this statement appear to be debits)
                amount = '-' + amount if not amount.startswith('-') else amount
                
                transactions.append({
                    'date': date,
                    'description': description,
                    'amount': float(amount),
                    'balance': float(balance)
                })
    
    # Also look for special transactions like interest payment
    if "Interest Payment" in pdf_text:
        match = re.search(r'(\d{2}/\d{2})\s+Interest Payment\s+([\d,]+\.\d{2})', pdf_text)
        if match:
            transactions.append({
                'date': match.group(1),
                'description': 'Interest Payment',
                'amount': float(match.group(2).replace(',', '')),
                'balance': float(match.group(2).replace(',', ''))
            })
    
    return transactions

def parse_csv_transactions(csv_path):
    """Parse transactions from CSV file"""
    transactions = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Amount']:
                transactions.append({
                    'date': row['Transaction Date'][5:10],  # Extract MM-DD
                    'description': row['Description'],
                    'amount': float(row['Amount']),
                    'type': row['Transaction Type']
                })
    
    return transactions

# Read the PDF text
with open('pdf_extract.txt', 'r') as f:
    pdf_text = f.read()

# Parse transactions from both sources
pdf_transactions = parse_pdf_transactions(pdf_text)
csv_transactions = parse_csv_transactions('/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv')

print("PDF TRANSACTION ANALYSIS")
print("=" * 80)

# Extract summary from PDF
beginning_balance = 16087.31
ending_balance = 528.22

# Extract totals from PDF summary section
deposits_match = re.search(r'Deposits and Additions\s+([\d,]+\.\d{2})', pdf_text)
checks_match = re.search(r'Checks Paid\s+-([\d,]+\.\d{2})', pdf_text)
debit_match = re.search(r'ATM & Debit Card Withdrawals\s+-([\d,]+\.\d{2})', pdf_text)
electronic_match = re.search(r'Electronic Withdrawals\s+-([\d,]+\.\d{2})', pdf_text)

deposits = float(deposits_match.group(1).replace(',', '')) if deposits_match else 0
checks = float(checks_match.group(1).replace(',', '')) if checks_match else 0
debit_withdrawals = float(debit_match.group(1).replace(',', '')) if debit_match else 0
electronic_withdrawals = float(electronic_match.group(1).replace(',', '')) if electronic_match else 0

print(f"Beginning Balance: ${beginning_balance:,.2f}")
print(f"Ending Balance: ${ending_balance:,.2f}")
print(f"\nPDF Summary:")
print(f"  Deposits and Additions: ${deposits:,.2f}")
print(f"  Checks Paid: -${checks:,.2f}")
print(f"  ATM & Debit Card Withdrawals: -${debit_withdrawals:,.2f}")
print(f"  Electronic Withdrawals: -${electronic_withdrawals:,.2f}")
print(f"  Total Change: ${deposits - checks - debit_withdrawals - electronic_withdrawals:,.2f}")

# Calculate CSV totals
csv_total = sum(t['amount'] for t in csv_transactions)
csv_credits = sum(t['amount'] for t in csv_transactions if t['amount'] > 0)
csv_debits = sum(t['amount'] for t in csv_transactions if t['amount'] < 0)

print(f"\nCSV Summary:")
print(f"  Total Credits: ${csv_credits:,.2f}")
print(f"  Total Debits: ${csv_debits:,.2f}")
print(f"  Net Change: ${csv_total:,.2f}")

# Calculate differences
expected_change = ending_balance - beginning_balance
csv_change = csv_total
difference = expected_change - csv_change

print(f"\nReconciliation:")
print(f"  Expected change (from PDF): ${expected_change:,.2f}")
print(f"  CSV change: ${csv_change:,.2f}")
print(f"  Difference: ${difference:,.2f}")

# Find missing transactions
print(f"\nMISSING TRANSACTIONS FROM CSV:")
print("=" * 80)

# Look for specific missing transactions mentioned in PDF
missing_transactions = []

# 1. Interest Payment on 02/07
if "Interest Payment" in pdf_text:
    interest_found = any('Interest Payment' in t['description'] for t in csv_transactions)
    if not interest_found:
        missing_transactions.append("02/07 Interest Payment: $0.09")

# 2. Buttercup Concord transaction
buttercup_found = any('Buttercup' in t['description'] for t in csv_transactions)
if not buttercup_found:
    missing_transactions.append("01/15 Buttercup Concord: -$44.96")

# 3. Online Transfer on 02/06
transfer_found = any('Online Transfer' in t['description'] for t in csv_transactions)
if not transfer_found:
    missing_transactions.append("02/06 Online Transfer To Chk ...8619: -$4,570.00")

# 4. Additional February transactions from PDF
feb_transactions_in_pdf = [
    ("02/02 Dropbox*Gq4Yk3Hbdkkt", -19.99),
    ("02/03 Lucky #705.Concord", -92.24),
    ("02/03 Google *Nest", -8.00),
    ("02/04 Best Little Donut Hous", -14.50),
    ("02/04 Paypal *Pypl Paymthly", -42.18),
    ("02/04 House of Sake Inc", -83.55),
    ("02/06 Treat Blvd 76", -30.86),
    ("02/05 Jersey Mikes 20367", -13.15),
    ("02/06 Fast & Easy Liquors", -13.73),
    ("02/06 Huckleberry's - Concord", -32.23),
    ("02/07 Fashion Cleaners", -174.80),
    ("02/07 Wholefds Yvr#105 2941", -94.61),
    ("02/07 Petroleum & Amenities", -90.20)
]

for desc, amount in feb_transactions_in_pdf:
    # Check if transaction exists in CSV
    found = False
    for csv_t in csv_transactions:
        if any(key in csv_t['description'] for key in desc.split()[1:]):
            found = True
            break
    if not found:
        missing_transactions.append(f"{desc}: ${amount:,.2f}")

print(f"\nFound {len(missing_transactions)} missing transactions:")
for trans in missing_transactions:
    print(f"  - {trans}")

# Calculate total of missing transactions
missing_total = -44.96 + 0.09 - 4570.00 - 19.99 - 92.24 - 8.00 - 14.50 - 42.18 - 83.55 - 30.86 - 13.15 - 13.73 - 32.23 - 174.80 - 94.61 - 90.20

print(f"\nTotal of identified missing transactions: ${missing_total:,.2f}")
print(f"This accounts for ${missing_total:,.2f} of the ${difference:,.2f} difference")
print(f"Remaining unexplained difference: ${difference - missing_total:,.2f}")