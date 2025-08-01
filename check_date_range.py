#!/usr/bin/env python3
"""Check which transactions are outside the February statement date range."""

import csv
from datetime import datetime

# Read the February 1873 transactions
with open('accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

# Statement period: January 09, 2025 through February 07, 2025
start_date = datetime(2025, 1, 9)
end_date = datetime(2025, 2, 7)

before_period = []
in_period = []
after_period = []

for tx in transactions:
    date_str = tx['Transaction Date']
    tx_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    if tx_date < start_date:
        before_period.append(tx)
    elif tx_date > end_date:
        after_period.append(tx)
    else:
        in_period.append(tx)

print(f"Total transactions: {len(transactions)}")
print(f"Before period (< Jan 9): {len(before_period)}")
print(f"In period (Jan 9 - Feb 7): {len(in_period)}")
print(f"After period (> Feb 7): {len(after_period)}")

if before_period:
    print("\nTransactions BEFORE the statement period:")
    total_before = 0
    for tx in before_period:
        amount = float(tx['Amount'])
        print(f"  {tx['Transaction Date']}: {tx['Description'][:50]}... ${amount:.2f}")
        total_before += amount
    print(f"  Total impact: ${total_before:.2f}")

# Calculate what the reconciliation would be without the early transactions
print("\n" + "="*60)
print("RECONCILIATION CHECK:")
print("If we remove transactions before Jan 9:")

deposits_in_period = sum(float(tx['Amount']) for tx in in_period if float(tx['Amount']) > 0)
withdrawals_in_period = sum(float(tx['Amount']) for tx in in_period if float(tx['Amount']) < 0)

print(f"  Deposits in period: ${deposits_in_period:.2f}")
print(f"  Withdrawals in period: ${withdrawals_in_period:.2f}")
print(f"  Net change: ${deposits_in_period + withdrawals_in_period:.2f}")
print(f"\nWith beginning balance $16,087.31:")
print(f"  Calculated ending: ${16087.31 + deposits_in_period + withdrawals_in_period:.2f}")
print(f"  Expected ending: $528.22")
print(f"  Difference: ${16087.31 + deposits_in_period + withdrawals_in_period - 528.22:.2f}")