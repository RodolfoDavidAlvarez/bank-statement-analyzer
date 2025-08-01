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
    processed_transactions = set()  # To avoid duplicates
    
    # Split text into lines
    lines = full_text.split('\n')
    
    # Find where transactions typically start
    transaction_sections = []
    for i, line in enumerate(lines):
        if "DATE PURCHASES MERCHANT CATEGORY AMOUNT" in line or "DATE PAYMENTS AND CREDITS AMOUNT" in line:
            transaction_sections.append(i)
    
    # Process all lines
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check if we're in or near a transaction section
        in_transaction_section = any(abs(i - section_start) < 50 for section_start in transaction_sections)
        
        # Look for lines starting with dates
        if re.match(r'^\d{2}/\d{2}\s+', line) or (in_transaction_section and re.search(r'\d{2}/\d{2}\s+', line)):
            # Handle lines that might have multiple transactions concatenated
            # Split by date patterns but keep the dates
            parts = re.split(r'(?=\d{2}/\d{2}\s+)', line)
            
            for part in parts:
                if not part.strip():
                    continue
                    
                # Try to parse this part as a transaction
                # Pattern: date, description, amount (amount might be on next line)
                match = re.match(r'(\d{2}/\d{2})\s+(.+?)(?:\s+([-]?\$?[\d,]+\.\d{2}))?$', part.strip())
                
                if match:
                    date_str = match.group(1)
                    description = match.group(2).strip()
                    amount_str = match.group(3)
                    
                    # If no amount found, check the next line
                    if not amount_str and i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        # Look for amount pattern
                        amount_match = re.search(r'^([-]?\$?[\d,]+\.\d{2})(?:\s|$)', next_line)
                        if amount_match:
                            amount_str = amount_match.group(1)
                            # Also check if there's more description before the amount
                            extra_desc = next_line[:amount_match.start()].strip()
                            if extra_desc and not re.match(r'^[A-Z0-9\-]+$', extra_desc):
                                description += " " + extra_desc
                    
                    # Continue collecting description from following lines if needed
                    j = i + 1
                    while j < len(lines) and j < i + 4 and not amount_str:
                        check_line = lines[j].strip()
                        if not check_line:
                            j += 1
                            continue
                            
                        # Check if this line has a date (new transaction)
                        if re.match(r'^\d{2}/\d{2}\s+', check_line):
                            break
                            
                        # Check for amount
                        amount_match = re.search(r'([-]?\$?[\d,]+\.\d{2})$', check_line)
                        if amount_match:
                            amount_str = amount_match.group(1)
                            # Add any text before amount to description
                            extra_desc = check_line[:amount_match.start()].strip()
                            if extra_desc and not re.match(r'^[A-Z0-9\-]+$', extra_desc):
                                description += " " + extra_desc
                            break
                        else:
                            # This might be part of the description
                            if not re.match(r'^[A-Z0-9\-]+$', check_line) and len(check_line) > 2:
                                description += " " + check_line
                        j += 1
                    
                    if amount_str:
                        # Clean up amount
                        amount_str = amount_str.replace('$', '').replace(',', '').strip()
                        
                        try:
                            amount = float(amount_str)
                            
                            # Clean up description
                            description = re.sub(r'\s+(Merchandise|Services|Restaurants|Groceries|Gas Stations|Travel)\s*$', '', description)
                            description = re.sub(r'\s+', ' ', description).strip()
                            
                            # Create unique key to avoid duplicates
                            trans_key = f"{date_str}_{description}_{amount}"
                            if trans_key in processed_transactions:
                                continue
                            processed_transactions.add(trans_key)
                            
                            # Determine transaction type
                            if "PAYMENT" in description.upper() or "THANK YOU" in description.upper():
                                trans_type = "Payment"
                                amount = -abs(amount)
                            elif "CREDIT" in description.upper() or "CASHBACK" in description.upper() or amount_str.startswith('-'):
                                trans_type = "Credit"
                                amount = -abs(amount)
                            else:
                                trans_type = "Purchase"
                                amount = abs(amount)
                            
                            # Format date with year
                            full_date = f"{date_str}/2025"
                            
                            # Final cleanup of description - remove transaction IDs at the end
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
                        except Exception as e:
                            print(f"Error processing amount '{amount_str}': {e}")
        
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
        # Sort transactions by date
        transactions.sort(key=lambda x: datetime.strptime(x['Transaction Date'], '%m/%d/%Y'))
        
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