#!/usr/bin/env python3
"""
Final fix for Chase 1873 February 2025 - add missing Dropbox transaction.
"""

import csv
from pathlib import Path

# Read current transactions
csv_path = Path("accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv")

transactions = []
with open(csv_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    for row in reader:
        transactions.append(row)

# Check if we're missing the February Dropbox payment
has_feb_dropbox = any('02/02' in t['Description'] and 'Dropbox' in t['Description'] for t in transactions)

if not has_feb_dropbox:
    # Add the missing Dropbox transaction (from page 4, line 56)
    dropbox_payment = {
        'Description': 'Recurring Card Purchase 02/02 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665',
        'Amount': '-19.99',
        'Transaction Date': '2025-02-03',
        'Transaction Type': 'Debit',
        'Status': 'New',
        'Statement id': '2025-02 - Chase 1873',
        'Bank and last 4': 'Chase 1873'
    }
    transactions.append(dropbox_payment)
    print("Added missing Dropbox payment")

# Sort by date
transactions.sort(key=lambda x: x['Transaction Date'])

# Write back
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(transactions)

print(f"Total transactions: {len(transactions)}")

# Calculate final totals
total_credits = sum(float(t['Amount']) for t in transactions if float(t['Amount']) > 0)
total_debits = sum(float(t['Amount']) for t in transactions if float(t['Amount']) < 0)
net_change = total_credits + total_debits

print(f"\nFinal totals:")
print(f"Total credits: ${total_credits:,.2f}")
print(f"Total debits: ${total_debits:,.2f}")
print(f"Net change: ${net_change:,.2f}")
print(f"Beginning balance: $16,087.31")
print(f"Expected ending balance: ${16087.31 + net_change:,.2f}")
print(f"Actual ending balance: $528.22")
print(f"Difference: ${abs(528.22 - (16087.31 + net_change)):.2f}")

if abs(528.22 - (16087.31 + net_change)) < 0.01:
    print("\n✓ RECONCILES PERFECTLY!")