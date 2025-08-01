import csv
import re
from datetime import datetime

# Transaction data extracted from the PDF for account 2084
transactions = [
    # December 2024 transactions
    ("2024-12-12", "Tesla Inc Tesla Moto PPD ID: 1463896777", 1171.08, "Purchase"),
    ("2024-12-13", "Zelle Payment To Jana Loureiro Jpm99Asvrd7K", 2500.00, "Purchase"),
    ("2024-12-16", "Remote Online Deposit", -1258.00, "Payment"),
    ("2024-12-16", "Online Transfer To Chk ...1873 Transaction#: 23052225013", 500.00, "Purchase"),
    ("2024-12-16", "Venmo Payment 1038982211722 Web ID: 3264681992", 97.72, "Purchase"),
    ("2024-12-18", "Online Transfer From Chk ...1873 Transaction#: 23092218255", -547.05, "Payment"),
    ("2024-12-18", "Lightstream Loan Pmts 45245501 Web ID: 1253108792", 1125.00, "Purchase"),
    ("2024-12-23", "Keller Williams Psus_Dec20 PPD ID: 1742756628", -355.61, "Payment"),
    ("2024-12-24", "Online Payment 19361398737 To Loan Care Servicing Center", 0.02, "Purchase"),
    ("2024-12-27", "Online Payment 22539713744 To Contra Costa Water District", 115.00, "Purchase"),
    ("2024-12-30", "Online Payment 22850227755 To Discover Card", 250.00, "Purchase"),
    ("2024-12-30", "Online Payment 22849872305 To Wave", 0.10, "Purchase"),
    ("2024-12-31", "Recurring Card Purchase Netflix.Com Netflix.Com CA Card 0885", 6.99, "Purchase"),
    
    # January 2025 transactions
    ("2025-01-03", "Venmo Payment 1039360000874 Web ID: 3264681992", 45.19, "Purchase"),
    ("2025-01-06", "Remote Online Deposit", -1258.00, "Payment"),
    ("2025-01-06", "Online Transfer From Chk ...0827 Transaction#: 23300565727", -34.28, "Payment"),
    ("2025-01-08", "Online Transfer From Chk ...1873 Transaction#: 23322879078", -5000.00, "Payment"),
    ("2025-01-08", "Online Payment 23322886751 To Republic Services", 125.00, "Purchase"),
    ("2025-01-08", "Online Payment 23322920228 To The Pool Shark", 280.00, "Purchase"),
    ("2025-01-08", "Online Payment 22944150138 To Mr. Cooper", 3200.00, "Purchase"),
    ("2025-01-08", "Interest Payment", -0.01, "Credit"),
]

# Create the directory structure if it doesn't exist
import os
directory = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase 2084/2025/monthly"
os.makedirs(directory, exist_ok=True)

# Write to CSV file
csv_file_path = os.path.join(directory, "chase_2084_2025-01_transactions.csv")

with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header
    writer.writerow(["Description", "Amount", "Transaction Date", "Transaction Type", "Status", "Statement id", "Bank and last 4"])
    
    # Write transactions
    for date, description, amount, trans_type in transactions:
        writer.writerow([
            description,
            f"{amount:.2f}",
            date,
            trans_type,
            "New",
            "2025-01 - Chase 2084",
            "Chase 2084"
        ])

print(f"CSV file created at: {csv_file_path}")
print(f"Total transactions: {len(transactions)}")

# Verify the balance calculations
deposits_credits = sum(amount for date, desc, amount, trans_type in transactions if amount < 0)
withdrawals_fees = sum(amount for date, desc, amount, trans_type in transactions if amount > 0)

print(f"\nBalance verification:")
print(f"Beginning Balance: $3,834.24")
print(f"Deposits and Additions: ${-deposits_credits:.2f}")
print(f"Withdrawals and Fees: ${withdrawals_fees:.2f}")
print(f"Net change: ${deposits_credits + withdrawals_fees:.2f}")
print(f"Calculated Ending Balance: ${3834.24 + deposits_credits + withdrawals_fees:.2f}")
print(f"Actual Ending Balance: $2,871.09")