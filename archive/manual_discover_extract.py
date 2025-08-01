#!/usr/bin/env python3
"""
Manual extraction of Discover credit card transactions
Since we cannot install PyPDF2, we'll need to manually enter the transactions
"""

import csv
from datetime import datetime

# Based on typical Discover credit card statement format, let's manually enter the transactions
# Format: Date, Description, Amount (positive for purchases, negative for payments)

transactions_data = [
    # Please update this list with actual transactions from the PDF
    # Example format:
    # ("03/01/2025", "AMAZON.COM", 45.99, "Purchase"),
    # ("03/05/2025", "PAYMENT - THANK YOU", -500.00, "Payment"),
    # Add all transactions here
]

# Convert to the required format
transactions = []
for date_str, description, amount, trans_type in transactions_data:
    transactions.append({
        'Description': description,
        'Amount': amount,
        'Transaction Date': date_str,
        'Transaction Type': trans_type,
        'Status': 'New',
        'Statement id': '2025-04 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })

# Write to CSV
output_path = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-04_transactions.csv'

if transactions:
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 'Status', 'Statement id', 'Bank and last 4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)
    
    print(f"Saved {len(transactions)} transactions to: {output_path}")
else:
    print("No transactions to save. Please update the transactions_data list with actual data from the PDF.")

# Instructions for manual entry:
print("\nTo complete this task:")
print("1. Open the PDF: /Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250412-1342.pdf")
print("2. Look for the transactions section (usually after account summary)")
print("3. For each transaction, note:")
print("   - Transaction date (MM/DD/YYYY)")
print("   - Merchant/Description")
print("   - Amount (positive for purchases, negative for payments/credits)")
print("   - Type (Purchase, Payment, or Credit)")
print("4. Update the transactions_data list in this script")
print("5. Run this script again")