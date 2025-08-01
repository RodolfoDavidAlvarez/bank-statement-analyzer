#!/usr/bin/env python3
"""
Consolidate all 2025 Chase monthly files into annual consolidated files.
Uses standard library only.
"""

import csv
from pathlib import Path
from datetime import datetime

def consolidate_account(account: str, year: int = 2025):
    """Consolidate monthly files for a specific account."""
    
    # Paths
    monthly_dir = Path(f"accounts/Chase {account}/{year}/monthly")
    consolidated_dir = Path(f"accounts/Chase {account}/{year}/consolidated")
    consolidated_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all monthly files
    monthly_files = sorted(monthly_dir.glob(f"chase_{account}_{year}-*.csv"))
    
    if not monthly_files:
        print(f"No monthly files found for Chase {account}")
        return
        
    print(f"\nConsolidating Chase {account}:")
    print(f"Found {len(monthly_files)} monthly files")
    
    # Read all transactions
    all_transactions = []
    fieldnames = None
    
    for file in monthly_files:
        print(f"  Reading {file.name}")
        with open(file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if fieldnames is None:
                fieldnames = reader.fieldnames
            for row in reader:
                all_transactions.append(row)
    
    # Sort by transaction date
    all_transactions.sort(key=lambda x: x['Transaction Date'])
    
    # Output file
    output_file = consolidated_dir / f"{year} - Chase {account}.csv"
    
    # Write consolidated file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_transactions)
    
    print(f"  Consolidated {len(all_transactions)} transactions")
    print(f"  Saved to: {output_file}")
    
    # Summary statistics
    total_credits = sum(float(tx['Amount']) for tx in all_transactions if float(tx['Amount']) > 0)
    total_debits = sum(float(tx['Amount']) for tx in all_transactions if float(tx['Amount']) < 0)
    net_change = total_credits + total_debits
    
    print(f"  Total credits: ${total_credits:,.2f}")
    print(f"  Total debits: ${total_debits:,.2f}")
    print(f"  Net change: ${net_change:,.2f}")

def main():
    """Consolidate all Chase accounts."""
    
    print("Consolidating Chase 2025 statements")
    print("=" * 50)
    
    accounts = ['2084', '1873', '8619']
    
    for account in accounts:
        consolidate_account(account)
    
    print("\nConsolidation complete!")

if __name__ == "__main__":
    main()