#!/usr/bin/env python3
"""Move version/status to the beginning of filenames."""

import os
from pathlib import Path

def rename_files():
    """Rename all files to have version/status at the beginning."""
    
    accounts_dir = Path("accounts")
    renamed_count = 0
    
    for csv_file in accounts_dir.rglob("*.csv"):
        old_name = csv_file.name
        new_name = old_name
        
        # Skip consolidated and precompiled files (they have different format)
        if ' - ' in old_name:
            continue
            
        # Handle files with [VALIDATED] at the end
        if old_name.endswith('[VALIDATED].csv'):
            # chase_1873_2025-01[VALIDATED].csv -> [VALIDATED]chase_1873_2025-01.csv
            base_name = old_name.replace('[VALIDATED].csv', '.csv')
            new_name = f"[VALIDATED]{base_name}"
        
        # Handle files with [v#] at the end
        elif '[v' in old_name and old_name.endswith('].csv'):
            # chase_1873_2025-03[v1].csv -> [v1]chase_1873_2025-03.csv
            import re
            match = re.search(r'^(.+)\[v(\d+)\]\.csv$', old_name)
            if match:
                base_name = match.group(1)
                version = match.group(2)
                new_name = f"[v{version}]{base_name}.csv"
        
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