#!/usr/bin/env python3
"""Test the February extraction with complete transaction data."""

import csv
from pathlib import Path

# Complete February 2025 transactions based on our corrected extraction
transactions_2084 = [
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
]

# Load the actual corrected 1873 transactions
with open('accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    transactions_1873 = [(row['Description'], float(row['Amount']), row['Transaction Date'], row['Transaction Type']) 
                         for row in reader]

transactions_8619 = [
    ("State Farm Ro 27 Sfpp CCD ID: 9000313004", -106.83, "2025-01-14", "Withdrawal"),
    ("Online Transfer From Chk ...2084 Transaction#: 23540544174", 150.00, "2025-01-29", "Deposit"),
    ("Online Payment 23540420666 To Cowell Homeowners Association", -185.00, "2025-01-29", "Payment"),
    ("Online Transfer From Chk ...1873 Transaction#: 23637622827", 4570.00, "2025-02-06", "Deposit"),
    ("Online Payment 23637563107 To Rushmore Servicing", -4568.00, "2025-02-06", "Payment"),
    ("Monthly Service Fee", -12.00, "2025-02-07", "Fee"),
]

# Known balances
balances = {
    '2084': {'beginning': 2871.09, 'ending': 1422.38},
    '1873': {'beginning': 16087.31, 'ending': 528.22},
    '8619': {'beginning': 229.42, 'ending': 77.59}
}

def validate_account(transactions, account, beginning, ending):
    """Validate an account's transactions."""
    deposits = sum(amt for _, amt, _, _ in transactions if amt > 0)
    withdrawals = sum(amt for _, amt, _, _ in transactions if amt < 0)
    
    calculated = beginning + deposits + withdrawals
    difference = calculated - ending
    
    print(f"\nAccount {account}:")
    print(f"  Transactions: {len(transactions)}")
    print(f"  Beginning: ${beginning:,.2f}")
    print(f"  Deposits: ${deposits:,.2f}")
    print(f"  Withdrawals: ${withdrawals:,.2f}")
    print(f"  Calculated: ${calculated:,.2f}")
    print(f"  Expected: ${ending:,.2f}")
    print(f"  Difference: ${difference:,.2f}")
    print(f"  Status: {'✓ PASSED' if abs(difference) < 0.01 else '✗ FAILED'}")
    
    return abs(difference) < 0.01

# Validate all accounts
print("February 2025 Validation Test")
print("=" * 50)

all_passed = True
all_passed &= validate_account(transactions_2084, '2084', 
                              balances['2084']['beginning'], 
                              balances['2084']['ending'])

all_passed &= validate_account(transactions_1873, '1873',
                              balances['1873']['beginning'],
                              balances['1873']['ending'])

all_passed &= validate_account(transactions_8619, '8619',
                              balances['8619']['beginning'],
                              balances['8619']['ending'])

print("\n" + "=" * 50)
print(f"Overall Result: {'✓ ALL ACCOUNTS RECONCILE' if all_passed else '✗ RECONCILIATION FAILED'}")