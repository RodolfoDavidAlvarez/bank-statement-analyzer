#!/usr/bin/env python3
import PyPDF2
import re
import csv
from datetime import datetime

def extract_discover_transactions(pdf_path):
    """Extract transactions from Discover credit card PDF statement"""
    
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        full_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text() + "\n"
    
    transactions = []
    
    # Split text into lines
    lines = full_text.split('\n')
    
    # Find where transactions start
    transaction_started = False
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for transaction section header
        if "DATE PURCHASES MERCHANT CATEGORY AMOUNT" in line:
            transaction_started = True
            i += 1
            continue
        
        # Look for payment section header
        if "DATE PAYMENTS AND CREDITS AMOUNT" in line:
            transaction_started = True
            i += 1
            continue
            
        # Also check for lines that look like transactions even without section headers
        # This handles cases where transactions appear mixed with other content
        if re.match(r'^\d{2}/\d{2}\s+', line) and not transaction_started:
            transaction_started = True
            
        if transaction_started:
            # Stop at section boundaries
            if any(phrase in line for phrase in ["PREVIOUS BALANCE", "TOTAL FEES", "CASHBACK  BONUS BALANCE", "Page", "Interest Charge Calculation"]):
                transaction_started = False
                continue
                
            # Pattern for dates at beginning of line
            date_pattern = r'^(\d{2}/\d{2})\s+'
            date_match = re.match(date_pattern, line)
            
            if date_match:
                date_str = date_match.group(1)
                
                # Get the rest of the line after the date
                rest_of_line = line[date_match.end():].strip()
                
                # Look for amount at the end of the line or on the next line
                amount_pattern = r'([-]?\$?[\d,]+\.\d{2})$'
                amount_match = re.search(amount_pattern, rest_of_line)
                
                if amount_match:
                    # Amount is on the same line
                    description = rest_of_line[:amount_match.start()].strip()
                    amount_str = amount_match.group(1)
                else:
                    # Amount might be on the next line
                    description = rest_of_line
                    
                    # Check next few lines for amount or additional description
                    j = i + 1
                    while j < len(lines) and j < i + 4:
                        next_line = lines[j].strip()
                        
                        # Check if this line has an amount
                        amount_match = re.search(amount_pattern, next_line)
                        if amount_match:
                            # Found amount
                            amount_str = amount_match.group(1)
                            # Add any text before the amount to description
                            extra_desc = next_line[:amount_match.start()].strip()
                            if extra_desc and not re.match(r'^[A-Z0-9\-]+$', extra_desc):
                                description += " " + extra_desc
                            i = j
                            break
                        elif next_line and not re.match(date_pattern, next_line):
                            # This looks like part of the description
                            if not re.match(r'^[A-Z0-9\-]+$', next_line):  # Skip reference numbers
                                description += " " + next_line
                        j += 1
                    else:
                        # No amount found, skip this entry
                        i += 1
                        continue
                
                # Clean up the description
                description = re.sub(r'\s+', ' ', description).strip()
                
                # Remove merchant category if present
                description = re.sub(r'\s+(Merchandise|Services|Restaurants|Groceries|Gas Stations|Travel)$', '', description)
                
                # Clean up amount
                amount_str = amount_str.replace('$', '').replace(',', '').strip()
                
                # Skip if no valid amount
                try:
                    amount = float(amount_str)
                except:
                    i += 1
                    continue
                
                # Determine transaction type
                if "PAYMENT" in description.upper() or "THANK YOU" in description.upper():
                    trans_type = "Payment"
                    amount = -abs(amount)  # Payments are negative
                elif "CREDIT" in description.upper() or "CASHBACK" in description.upper() or amount_str.startswith('-'):
                    trans_type = "Credit"
                    amount = -abs(amount)  # Credits are negative
                else:
                    trans_type = "Purchase"
                    amount = abs(amount)  # Purchases are positive
                
                # Format date with year
                full_date = f"{date_str}/2025"
                
                # Clean up description - remove extra spaces and transaction IDs
                description = re.sub(r'\s*[A-Z0-9]{10,}$', '', description).strip()
                
                transactions.append({
                    'Description': description,
                    'Amount': amount,
                    'Transaction Date': full_date,
                    'Transaction Type': trans_type,
                    'Status': 'New',
                    'Statement id': '2025-01 - Discover 1342',
                    'Bank and last 4': 'Discover 1342'
                })
                
                print(f"Extracted: {full_date} | {description} | ${amount:.2f} | {trans_type}")
        
        i += 1
    
    return transactions

# Main execution
pdf_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes documents for extraction/Taxes 2025 (Inprogress)/Credit Card Statements 2025/Discover CC /Discover-Statement-20250112-1342.pdf"
output_path = "/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-01_transactions.csv"

try:
    transactions = extract_discover_transactions(pdf_path)
    
    if not transactions:
        print("\nNo transactions found.")
    else:
        # Write to CSV
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 'Status', 'Statement id', 'Bank and last 4']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for trans in transactions:
                writer.writerow(trans)
        
        print(f"\nExtracted {len(transactions)} transactions and saved to {output_path}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()