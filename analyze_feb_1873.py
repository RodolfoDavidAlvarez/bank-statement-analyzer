#!/usr/bin/env python3
"""Analyze February 1873 reconciliation."""

import csv

# Read the CSV file
with open('accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

# Calculate totals
deposits = 0
withdrawals = 0
interest = 0

for tx in transactions:
    amount = float(tx['Amount'])
    if amount > 0:
        if tx['Transaction Type'] == 'Interest':
            interest += amount
        else:
            deposits += amount
    else:
        withdrawals += amount

print(f'Total deposits (excluding interest): ${deposits:.2f}')
print(f'Interest: ${interest:.2f}')
print(f'Total withdrawals: ${withdrawals:.2f}')
print(f'Net change: ${deposits + interest + withdrawals:.2f}')
print(f'')
print(f'Expected from statement:')
print(f'Beginning: $16,087.31')
print(f'Deposits: $0.09 (interest only)')
print(f'Withdrawals: -$15,559.18 (280 + 4,496.80 + 10,782.38)')
print(f'Expected ending: $528.22')
print(f'')
print(f'Our calculation:')
print(f'Beginning: $16,087.31')
print(f'Net change: ${deposits + interest + withdrawals:.2f}')
print(f'Calculated ending: ${16087.31 + deposits + interest + withdrawals:.2f}')