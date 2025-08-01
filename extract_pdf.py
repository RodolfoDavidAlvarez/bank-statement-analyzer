#!/usr/bin/env python3
import subprocess
import sys
import os

pdf_path = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Bank Statement NB Personal Account/20250108-statements-2084-.pdf'

# Try using macOS's built-in sips command to convert PDF to text
try:
    # First convert PDF to TIFF
    tiff_path = '/tmp/temp_statement.tiff'
    subprocess.run(['sips', '-s', 'format', 'tiff', pdf_path, '--out', tiff_path], check=True, capture_output=True)
    
    # Then use tesseract if available, or try other methods
    try:
        result = subprocess.run(['tesseract', tiff_path, '-', '--psm', '6'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Tesseract error: {result.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print("Tesseract not found, trying alternative method", file=sys.stderr)
        
    # Clean up
    if os.path.exists(tiff_path):
        os.remove(tiff_path)
        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    
    # Try using strings command as last resort
    try:
        result = subprocess.run(['strings', pdf_path], capture_output=True, text=True)
        if result.returncode == 0:
            # Filter for readable text patterns
            lines = result.stdout.split('\n')
            for line in lines:
                # Look for transaction-like patterns
                if any(char.isdigit() for char in line) and len(line) > 10:
                    print(line)
    except Exception as e2:
        print(f"Strings error: {e2}", file=sys.stderr)