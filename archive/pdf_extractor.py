#!/usr/bin/env python3
"""
Try to extract text from Discover PDF using various methods
"""

import subprocess
import os

pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250612-1342.pdf"

# Method 1: Try using macOS built-in textutil (won't work well for PDFs but worth trying)
print("Method 1: Using textutil...")
try:
    result = subprocess.run(['textutil', '-convert', 'txt', '-stdout', pdf_path], 
                          capture_output=True, text=True)
    if result.stdout:
        with open('discover_textutil_output.txt', 'w') as f:
            f.write(result.stdout)
        print(f"Output saved to discover_textutil_output.txt ({len(result.stdout)} characters)")
    else:
        print("No output from textutil")
except Exception as e:
    print(f"Error with textutil: {e}")

# Method 2: Try using strings command to extract any readable text
print("\nMethod 2: Using strings command...")
try:
    result = subprocess.run(['strings', pdf_path], 
                          capture_output=True, text=True)
    if result.stdout:
        lines = result.stdout.split('\n')
        # Filter for potentially useful lines
        useful_lines = [line for line in lines if len(line) > 10 and not line.startswith('%')]
        with open('discover_strings_output.txt', 'w') as f:
            f.write('\n'.join(useful_lines))
        print(f"Output saved to discover_strings_output.txt ({len(useful_lines)} lines)")
except Exception as e:
    print(f"Error with strings: {e}")

# Method 3: Try using mdls to get metadata
print("\nMethod 3: Getting PDF metadata...")
try:
    result = subprocess.run(['mdls', pdf_path], 
                          capture_output=True, text=True)
    if result.stdout:
        print("PDF Metadata:")
        print(result.stdout)
except Exception as e:
    print(f"Error with mdls: {e}")

print("\nPDF extraction attempts complete.")
print("Please check the output files for any useful information.")