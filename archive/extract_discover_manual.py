#!/usr/bin/env python3
"""
Manual extraction of Discover credit card transactions based on the PDF text output
"""

def extract_discover_transactions():
    """Extract transactions from Discover statement text"""
    
    transactions = []
    
    # Based on the extracted text, here are all the transactions:
    
    # Payments and Credits
    transactions.append({
        'Description': 'AUTOMATIC STATEMENT CREDIT',
        'Amount': 5.24,
        'Transaction Date': '01/13/2025',
        'Transaction Type': 'Credit',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'PAYMENT - THANK YOU',
        'Amount': 250.00,
        'Transaction Date': '01/31/2025',
        'Transaction Type': 'Payment',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    # Purchases
    transactions.append({
        'Description': 'AMAZON PRIME*ZG6F616H2 AMZN.COM/BILLWA',
        'Amount': -7.64,
        'Transaction Date': '01/17/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'FASTPOST 2099144140 CA',
        'Amount': -81.00,
        'Transaction Date': '01/22/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'INTUIT *QBOOKS ONLINE CL.INTUIT.COMCA',
        'Amount': -35.00,
        'Transaction Date': '01/26/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'PY *SPACE SHOP STORAGE O NORTH OLMSTEDOH',
        'Amount': -142.60,
        'Transaction Date': '02/01/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'AMZN DIGITAL*Z77UZ0AS0 888-802-3080 WA',
        'Amount': -19.99,
        'Transaction Date': '02/03/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'PRIME VIDEO CHANNELS AMZN.COM/BILLWA',
        'Amount': -12.99,
        'Transaction Date': '02/07/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'AMAZON.COM*RP3RH10S3 AMZN.COM/BILLWA',
        'Amount': -34.89,
        'Transaction Date': '02/09/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'AMAZON.COM*CS5YS5A23 AMZN.COM/BILLWA',
        'Amount': -34.89,
        'Transaction Date': '02/09/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    transactions.append({
        'Description': 'AMAZON.COM*GY8GI2XH3 AMZN.COM/BILLWA',
        'Amount': -8.28,
        'Transaction Date': '02/10/2025',
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    # Interest charges (treating as a fee/purchase)
    transactions.append({
        'Description': 'INTEREST CHARGE ON PURCHASES',
        'Amount': -168.05,
        'Transaction Date': '02/12/2025',  # Using statement end date
        'Transaction Type': 'Purchase',
        'Status': 'New',
        'Statement id': '2025-02 - Discover 1342',
        'Bank and last 4': 'Discover 1342'
    })
    
    return transactions

# Run the extraction
transactions = extract_discover_transactions()

# Print summary
print(f"\nTotal transactions extracted: {len(transactions)}")
print(f"Total purchases: {sum(1 for t in transactions if t['Transaction Type'] == 'Purchase')}")
print(f"Total payments: {sum(1 for t in transactions if t['Transaction Type'] == 'Payment')}")
print(f"Total credits: {sum(1 for t in transactions if t['Transaction Type'] == 'Credit')}")

# Calculate totals
total_charges = sum(t['Amount'] for t in transactions if t['Amount'] < 0)
total_payments_credits = sum(t['Amount'] for t in transactions if t['Amount'] > 0)
print(f"\nTotal charges: ${abs(total_charges):.2f}")
print(f"Total payments/credits: ${total_payments_credits:.2f}")
print(f"Net activity: ${total_charges + total_payments_credits:.2f}")

# Print in CSV format
print("\n=== CSV FORMAT ===")
print("Description,Amount,Transaction Date,Transaction Type,Status,Statement id,Bank and last 4")
for t in transactions:
    print(f"\"{t['Description']}\",{t['Amount']},{t['Transaction Date']},{t['Transaction Type']},{t['Status']},{t['Statement id']},{t['Bank and last 4']}")