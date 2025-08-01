#!/usr/bin/env python3
"""
Add the missing Interest Payment to Chase 1873 February 2025.
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

# Add the missing Interest Payment (from page 5 of PDF)
interest_payment = {
    'Description': 'Interest Payment',
    'Amount': '0.09',
    'Transaction Date': '2025-02-07',
    'Transaction Type': 'Interest',
    'Status': 'New',
    'Statement id': '2025-02 - Chase 1873',
    'Bank and last 4': 'Chase 1873'
}

# Add to list
transactions.append(interest_payment)

# Sort by date
transactions.sort(key=lambda x: x['Transaction Date'])

# Write back
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(transactions)

print(f"Added Interest Payment. Total transactions: {len(transactions)}")

# Calculate new totals
total_credits = sum(float(t['Amount']) for t in transactions if float(t['Amount']) > 0)
total_debits = sum(float(t['Amount']) for t in transactions if float(t['Amount']) < 0)
net_change = total_credits + total_debits

print(f"\nUpdated totals:")
print(f"Total credits: ${total_credits:,.2f}")
print(f"Total debits: ${total_debits:,.2f}")
print(f"Net change: ${net_change:,.2f}")
print(f"Expected ending balance: ${16087.31 + net_change:,.2f}")