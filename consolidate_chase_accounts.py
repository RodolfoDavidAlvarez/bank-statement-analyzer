#!/usr/bin/env python3
"""Consolidate monthly Chase CSV files into annual files for each account."""

import csv
import os
from pathlib import Path

def consolidate_account(account_number, year=2025):
    """Consolidate monthly CSV files for a Chase account into an annual file."""
    
    # Define paths
    monthly_dir = Path(f"/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase {account_number}/{year}/monthly")
    consolidated_dir = Path(f"/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase {account_number}/{year}/consolidated")
    precompiled_dir = Path(f"/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase {account_number}/extracted_precompiled")
    
    # Create directories if they don't exist
    consolidated_dir.mkdir(parents=True, exist_ok=True)
    precompiled_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all transactions
    all_transactions = []
    months_found = []
    
    # Read all monthly files
    for month in range(1, 13):  # 1-12
        monthly_file = monthly_dir / f"chase_{account_number}_{year}-{month:02d}_transactions.csv"
        
        if monthly_file.exists():
            months_found.append(month)
            with open(monthly_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_transactions.append(row)
    
    if not all_transactions:
        print(f"No transactions found for Chase {account_number}")
        return 0
    
    # Sort by date
    all_transactions.sort(key=lambda x: x['Transaction Date'])
    
    # Define output filenames
    consolidated_filename = f"{year} - Chase {account_number}.csv"
    consolidated_path = consolidated_dir / consolidated_filename
    precompiled_path = precompiled_dir / consolidated_filename
    
    # Write consolidated file
    fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                 'Status', 'Statement id', 'Bank and last 4']
    
    with open(consolidated_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_transactions)
    
    # Copy to precompiled directory
    with open(precompiled_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_transactions)
    
    print(f"Chase {account_number}:")
    print(f"  - Months found: {months_found}")
    print(f"  - Total transactions: {len(all_transactions)}")
    print(f"  - Consolidated file: {consolidated_path}")
    print(f"  - Precompiled copy: {precompiled_path}")
    
    return len(all_transactions)

def main():
    print("Consolidating Chase account files...\n")
    
    total_transactions = 0
    
    # Consolidate each account
    for account in ['2084', '1873', '8619']:
        count = consolidate_account(account)
        total_transactions += count
        print()
    
    print(f"Total transactions across all accounts: {total_transactions}")

if __name__ == "__main__":
    main()