#!/usr/bin/env python3
import csv

# Read the CSV file
input_file = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-01_transactions.csv'
output_file = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/discover_1342_2025-01_transactions.csv'

transactions = []
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Clean up the description
        desc = row['Description']
        # Remove location suffixes like "WAMerchandise", "CAMerchandise", "OHServices"
        desc = desc.replace('WAMerchandise', '').replace('CAMerchandise', '').replace('OHServices', '').strip()
        # Remove extra spaces
        desc = ' '.join(desc.split())
        row['Description'] = desc
        transactions.append(row)

# Write the cleaned data back
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 'Status', 'Statement id', 'Bank and last 4']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for trans in transactions:
        writer.writerow(trans)

print(f"Cleaned {len(transactions)} transactions")