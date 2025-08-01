#!/usr/bin/env python3
"""Analyze discrepancy in February 1873 statement."""

# From the PDF statement:
# Beginning Balance: $16,087.31
# Ending Balance: $528.22
# Total change: -$15,559.09

# Statement shows:
# Deposits and Additions: $0.09 (interest only)
# Checks Paid: -$280.00
# ATM & Debit Card Withdrawals: -$4,496.80
# Electronic Withdrawals: -$10,782.38
# Total withdrawals: $280.00 + $4,496.80 + $10,782.38 = $15,559.18

# Let me categorize our current transactions
import csv

with open('accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

checks = []
card_withdrawals = []
electronic_withdrawals = []
deposits = []

for tx in transactions:
    amount = float(tx['Amount'])
    desc = tx['Description']
    tx_type = tx['Transaction Type']
    
    if amount > 0:
        deposits.append((desc, amount))
    elif tx_type == 'Check':
        checks.append((desc, amount))
    elif tx_type == 'Debit' or 'Card Purchase' in desc:
        card_withdrawals.append((desc, amount))
    else:
        electronic_withdrawals.append((desc, amount))

print("DEPOSITS:")
for desc, amt in deposits:
    print(f"  {desc}: ${amt:.2f}")
print(f"Total deposits: ${sum(amt for _, amt in deposits):.2f}")

print("\nCHECKS:")
for desc, amt in checks:
    print(f"  {desc}: ${amt:.2f}")
print(f"Total checks: ${abs(sum(amt for _, amt in checks)):.2f}")

print("\nCARD WITHDRAWALS:")
total_card = 0
for desc, amt in card_withdrawals:
    print(f"  {desc}: ${amt:.2f}")
    total_card += amt
print(f"Total card withdrawals: ${abs(total_card):.2f}")

print("\nELECTRONIC WITHDRAWALS:")
total_electronic = 0
for desc, amt in electronic_withdrawals:
    print(f"  {desc}: ${amt:.2f}")
    total_electronic += amt
print(f"Total electronic withdrawals: ${abs(total_electronic):.2f}")

print("\n" + "="*50)
print("SUMMARY:")
print(f"Expected from statement:")
print(f"  Checks: $280.00")
print(f"  Card Withdrawals: $4,496.80")
print(f"  Electronic Withdrawals: $10,782.38")
print(f"  Total: $15,559.18")
print(f"\nOur extraction:")
print(f"  Checks: ${abs(sum(amt for _, amt in checks)):.2f}")
print(f"  Card Withdrawals: ${abs(total_card):.2f}")
print(f"  Electronic Withdrawals: ${abs(total_electronic):.2f}")
print(f"  Total: ${abs(sum(amt for _, amt in checks)) + abs(total_card) + abs(total_electronic):.2f}")

# Check if some transactions should be in January
jan_transactions = []
for tx in transactions:
    date = tx['Transaction Date']
    if date < '2025-02-01':
        jan_transactions.append(tx)

print(f"\nTransactions before February: {len(jan_transactions)}")
print("These transactions might belong to January statement!")