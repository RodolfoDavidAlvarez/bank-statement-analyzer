#!/usr/bin/env python3
"""Rename files to remove 'transactions' and use square brackets for status."""

import os
from pathlib import Path

def rename_files():
    """Rename all transaction files to be more concise."""
    
    accounts_dir = Path("accounts")
    renamed_count = 0
    
    for csv_file in accounts_dir.rglob("*.csv"):
        old_name = csv_file.name
        new_name = old_name
        
        # Skip if already renamed or doesn't contain 'transactions'
        if 'transactions' not in old_name:
            continue
            
        # Handle validated files
        if '[VALIDATED]' in old_name:
            # [VALIDATED] discover_1342_2025-01_transactions.csv -> discover_1342_2025-01[VALIDATED].csv
            new_name = old_name.replace('_transactions', '').replace('[VALIDATED] ', '').replace('.csv', '[VALIDATED].csv')
        
        # Handle versioned files
        elif '_transactions_v' in old_name:
            # chase_1873_2025-03_transactions_v1.csv -> chase_1873_2025-03[v1].csv
            parts = old_name.split('_transactions_v')
            version = parts[1].replace('.csv', '')
            new_name = f"{parts[0]}[v{version}].csv"
        
        # Handle regular transaction files
        elif '_transactions' in old_name:
            # chase_1873_2025-03_transactions.csv -> chase_1873_2025-03.csv
            new_name = old_name.replace('_transactions', '')
        
        # Rename if changed
        if new_name != old_name:
            new_path = csv_file.parent / new_name
            print(f"Renaming: {old_name}")
            print(f"      to: {new_name}")
            csv_file.rename(new_path)
            renamed_count += 1
    
    print(f"\nRenamed {renamed_count} files")

if __name__ == "__main__":
    rename_files()