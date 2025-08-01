import csv
import os

def read_csv_file(filepath):
    """Read CSV file and return list of dictionaries"""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def correct_chase_files():
    accounts = ['Chase 2084', 'Chase 1873', 'Chase 8619']
    
    for account in accounts:
        account_num = account.split()[1]
        
        # Read validation file
        validation_file = f'accounts/{account}/validation/validation_2025-01.csv'
        if not os.path.exists(validation_file):
            print(f"No validation file for {account}")
            continue
            
        validation_data = read_csv_file(validation_file)
        
        # Create corrected file with validation data format
        output_file = f'accounts/{account}/2025/monthly/{account.lower().replace(" ", "_")}_2025-01_transactions.csv'
        
        with open(output_file, 'w', newline='') as f:
            fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 'Status', 'Statement id', 'Bank and last 4']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in validation_data:
                # Write with our standard column names
                writer.writerow({
                    'Description': row['Description'],
                    'Amount': row['Amount'],
                    'Transaction Date': row['Transaction Date'],
                    'Transaction Type': row['Transaction Type'],
                    'Status': 'New',  # Use 'New' instead of 'Verified'
                    'Statement id': row['Statement id'],
                    'Bank and last 4': row['Bank']
                })
        
        print(f"Corrected {account}: {len(validation_data)} transactions")

if __name__ == "__main__":
    correct_chase_files()