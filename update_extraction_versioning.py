#!/usr/bin/env python3
"""Add versioning to extraction files."""

import os
import shutil
from pathlib import Path

def add_versioning_to_existing_files():
    """Add _v1 suffix to existing extraction files to start versioning."""
    
    accounts_dir = Path("accounts")
    
    # Find all CSV files without version suffix
    for csv_file in accounts_dir.rglob("*_transactions.csv"):
        # Skip if already has version suffix
        if "_v" in csv_file.stem:
            continue
            
        # Skip properly extracted files
        if "[Properly Extracted]" in csv_file.name:
            continue
            
        # Create new name with _v1
        new_name = csv_file.stem + "_v1" + csv_file.suffix
        new_path = csv_file.parent / new_name
        
        print(f"Renaming: {csv_file.name} -> {new_name}")
        shutil.move(str(csv_file), str(new_path))

def get_next_version(base_path: str) -> int:
    """Get the next version number for a file."""
    base = Path(base_path)
    parent = base.parent
    stem = base.stem.split('_transactions')[0] + '_transactions'
    
    # Find existing versions
    existing_versions = []
    for f in parent.glob(f"{stem}_v*.csv"):
        # Extract version number
        version_str = f.stem.split('_v')[-1]
        try:
            version = int(version_str)
            existing_versions.append(version)
        except ValueError:
            pass
    
    return max(existing_versions, default=0) + 1

if __name__ == "__main__":
    print("Adding versioning to existing extraction files...")
    add_versioning_to_existing_files()
    print("\nDone! All extraction files now have version numbers.")
    print("\nNext extractions should use format: chase_1873_2025-03_transactions_v2.csv")