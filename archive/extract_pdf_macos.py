#!/usr/bin/env python3
import subprocess
import os
import re
from datetime import datetime

pdf_path = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Bank Statement NB Personal Account/20250108-statements-2084-.pdf'

# Use macOS's Automator/AppleScript to extract text
applescript = f'''
on run
    set pdfFile to POSIX file "{pdf_path}"
    tell application "System Events"
        set pdfText to ""
        try
            -- This might work on some macOS versions
            set pdfText to do shell script "mdls -name kMDItemTextContent " & quoted form of POSIX path of pdfFile & " | cut -d'=' -f2"
        end try
        return pdfText
    end tell
end run
'''

try:
    # Try using osascript to run AppleScript
    result = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    if result.stdout.strip() and result.stdout.strip() != '(null)':
        print("Extracted text from metadata:")
        print(result.stdout)
    else:
        print("No text found in metadata, trying alternative approach...")
        
        # Try using textutil with rtf conversion
        rtf_path = '/tmp/temp_statement.rtf'
        txt_path = '/tmp/temp_statement.txt'
        
        try:
            # Convert PDF to RTF then to TXT
            subprocess.run(['textutil', '-convert', 'rtf', '-output', rtf_path, pdf_path], 
                         capture_output=True, check=True)
            subprocess.run(['textutil', '-convert', 'txt', '-output', txt_path, rtf_path], 
                         capture_output=True, check=True)
            
            with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print("Extracted content:")
                print(content)
                
        except Exception as e:
            print(f"Textutil conversion failed: {e}")
            
        finally:
            # Clean up temp files
            for path in [rtf_path, txt_path]:
                if os.path.exists(path):
                    os.remove(path)
                    
except Exception as e:
    print(f"Error: {e}")
    
# As a last resort, try to extract any visible text patterns
print("\n\nSearching for transaction patterns in raw data...")
try:
    result = subprocess.run(['strings', pdf_path], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.split('\n')
        
        # Look for date patterns
        date_pattern = re.compile(r'(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])')
        amount_pattern = re.compile(r'\$?[\d,]+\.\d{2}')
        
        potential_transactions = []
        for i, line in enumerate(lines):
            if date_pattern.search(line) or amount_pattern.search(line):
                # Get context around potential transaction
                start = max(0, i-2)
                end = min(len(lines), i+3)
                context = ' '.join(lines[start:end])
                if len(context) > 20 and len(context) < 200:
                    potential_transactions.append(context)
        
        if potential_transactions:
            print("\nPotential transaction data found:")
            for trans in potential_transactions[:20]:  # Show first 20
                print(trans)
                
except Exception as e:
    print(f"String search error: {e}")