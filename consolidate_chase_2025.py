#!/usr/bin/env python3
"""
Consolidate all 2025 Chase monthly files into annual consolidated files.
"""

import pandas as pd
from pathlib import Path

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
    
    # Read and combine all files
    all_transactions = []
    
    for file in monthly_files:
        print(f"  Reading {file.name}")
        df = pd.read_csv(file)
        all_transactions.append(df)
    
    # Combine all dataframes
    consolidated_df = pd.concat(all_transactions, ignore_index=True)
    
    # Sort by transaction date
    consolidated_df['Transaction Date'] = pd.to_datetime(consolidated_df['Transaction Date'])
    consolidated_df = consolidated_df.sort_values('Transaction Date')
    
    # Output file
    output_file = consolidated_dir / f"{year} - Chase {account}.csv"
    consolidated_df.to_csv(output_file, index=False)
    
    print(f"  Consolidated {len(consolidated_df)} transactions")
    print(f"  Saved to: {output_file}")
    
    # Summary statistics
    total_credits = consolidated_df[consolidated_df['Amount'] > 0]['Amount'].sum()
    total_debits = consolidated_df[consolidated_df['Amount'] < 0]['Amount'].sum()
    net_change = total_credits + total_debits
    
    print(f"  Total credits: ${total_credits:,.2f}")
    print(f"  Total debits: ${total_debits:,.2f}")
    print(f"  Net change: ${net_change:,.2f}")
    
    return consolidated_df

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