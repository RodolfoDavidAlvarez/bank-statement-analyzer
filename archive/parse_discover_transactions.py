#!/usr/bin/env python3
import re
import csv
from datetime import datetime

def parse_discover_statement(text):
    """Parse Discover statement text and extract transactions."""
    transactions = []
    
    # Find transactions section - payments and credits
    payments_pattern = r'(\d{2}/\d{2})\s+(AUTOMATIC STATEMENT CREDIT|PAYMENT - THANK YOU)\s+-\$([0-9,]+\.\d{2})'
    for match in re.finditer(payments_pattern, text):
        date = match.group(1) + "/2025"  # Add year
        description = match.group(2)
        amount = "-" + match.group(3).replace(",", "")  # Negative for credits/payments
        
        transactions.append({
            'Description': description,
            'Amount': amount,
            'Transaction Date': date,
            'Transaction Type': 'Payment' if 'PAYMENT' in description else 'Credit',
            'Status': 'New',
            'Statement id': '2025-05 - Discover 1342',
            'Bank and last 4': 'Discover 1342'
        })
    
    # Find purchases section
    purchases_section = text.split('PURCHASES MERCHANT CATEGORY AMOUNT')[1].split('INTEREST CHARGED FOR THIS PERIOD')[0]
    
    # Parse individual purchases
    purchase_pattern = r'(\d{2}/\d{2})\s+([^\$]+?)\s+\$([0-9,]+\.\d{2})'
    
    lines = purchases_section.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        # Check if line starts with date
        date_match = re.match(r'^(\d{2}/\d{2})\s+(.+)', line)
        if date_match:
            date = date_match.group(1) + "/2025"
            rest_of_line = date_match.group(2)
            
            # Look for amount at the end
            amount_match = re.search(r'\$([0-9,]+\.\d{2})$', rest_of_line)
            if amount_match:
                amount = amount_match.group(1).replace(",", "")
                description = rest_of_line[:amount_match.start()].strip()
                
                # Clean up description - remove category words at the end
                description = re.sub(r'\s+(Services|Merchandise|OH|CA|WA|IL|MI).*$', '', description)
                
                transactions.append({
                    'Description': description.strip(),
                    'Amount': amount,  # Positive for purchases
                    'Transaction Date': date,
                    'Transaction Type': 'Purchase',
                    'Status': 'New',
                    'Statement id': '2025-05 - Discover 1342',
                    'Bank and last 4': 'Discover 1342'
                })
            else:
                # Multi-line transaction - combine with next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    combined = rest_of_line + " " + next_line
                    amount_match = re.search(r'\$([0-9,]+\.\d{2})$', combined)
                    if amount_match:
                        amount = amount_match.group(1).replace(",", "")
                        description = combined[:amount_match.start()].strip()
                        description = re.sub(r'\s+(Services|Merchandise|OH|CA|WA|IL|MI).*$', '', description)
                        
                        transactions.append({
                            'Description': description.strip(),
                            'Amount': amount,
                            'Transaction Date': date,
                            'Transaction Type': 'Purchase',
                            'Status': 'New',
                            'Statement id': '2025-05 - Discover 1342',
                            'Bank and last 4': 'Discover 1342'
                        })
                        i += 1  # Skip next line since we used it
        i += 1
    
    return transactions

def save_to_csv(transactions, filename):
    """Save transactions to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 'Status', 'Statement id', 'Bank and last 4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)

# Read the extracted text from file
with open('discover_extracted.txt', 'r') as f:
    text = f.read()

# Parse transactions
transactions = parse_discover_statement(text)

# Save to CSV
output_file = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-05_transactions.csv'
save_to_csv(transactions, output_file)

print(f"Extracted {len(transactions)} transactions and saved to {output_file}")
for t in transactions:
    print(f"{t['Transaction Date']} - {t['Description'][:50]:<50} ${t['Amount']:>10} ({t['Transaction Type']})")