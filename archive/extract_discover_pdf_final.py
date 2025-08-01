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
    
    # Process all lines looking for transaction patterns
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Special handling for lines that contain multiple entries
        # Check if line contains date pattern anywhere
        date_patterns = list(re.finditer(r'(\d{2}/\d{2})\s+', line))
        
        if date_patterns:
            for match in date_patterns:
                # Extract from this date match to the end of line or next date
                start_pos = match.start()
                
                # Find next date or end of line
                next_date_pos = len(line)
                for next_match in date_patterns:
                    if next_match.start() > start_pos:
                        next_date_pos = next_match.start()
                        break
                
                # Extract this transaction segment
                transaction_text = line[start_pos:next_date_pos].strip()
                
                # Parse the transaction
                trans_match = re.match(r'(\d{2}/\d{2})\s+(.+?)(?:\s+([-]?\$?[\d,]+\.\d{2}))?$', transaction_text)
                
                if trans_match:
                    date_str = trans_match.group(1)
                    description = trans_match.group(2).strip()
                    amount_str = trans_match.group(3)
                    
                    if not amount_str:
                        # Check next line for amount
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            amount_match = re.search(r'^([-]?\$?[\d,]+\.\d{2})(?:\s|$)', next_line)
                            if amount_match:
                                amount_str = amount_match.group(1)
                    
                    if amount_str:
                        # Clean up amount
                        amount_str = amount_str.replace('$', '').replace(',', '').strip()
                        
                        try:
                            amount = float(amount_str)
                            
                            # Clean up description
                            description = re.sub(r'\s+(Merchandise|Services|Restaurants|Groceries|Gas Stations|Travel)$', '', description)
                            description = re.sub(r'\s+', ' ', description).strip()
                            
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
                            
                            # Clean up description - remove transaction IDs
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
                        except:
                            pass
        
        # Also check if line looks like it continues a description from previous line
        if i > 0 and not date_patterns and line and len(transactions) > 0:
            # Check if this might be additional info for the last transaction
            if re.match(r'^[A-Z0-9\-]{10,}$', line):
                # This looks like a transaction reference number, skip it
                pass
            elif re.search(r'^\$?[\d,]+\.\d{2}$', line):
                # This might be an amount on its own line
                pass
        
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