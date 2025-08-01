#!/usr/bin/env python3
"""Extract May 2025 transactions from Chase multi-account PDF."""

import csv
import os
from pathlib import Path

# May 2025 transactions for all three Chase accounts
# Extracted from: 20250507-statements-1873-.pdf

# Chase Premier Plus Checking 2084 transactions
chase_2084_transactions = [
    ("2025-04-10", "Card Purchase 04/07 Amazon.Com*0E72Y3Ck3 Amzn.Com/Bill WA Card 0885", 5.00, "Debit"),
    ("2025-04-11", "Tesla Inc Tesla Moto PPD ID: 1463896777", 1171.08, "Withdrawal"),
    ("2025-04-14", "Venmo Payment 1041456651454 Web ID: 3264681992", 81.19, "Withdrawal"),
    ("2025-04-18", "Keller Williams Psus_Apr20 PPD ID: 1742756628", -2.76, "Credit"),
    ("2025-04-21", "Lightstream Loan Pmts 45680968 Web ID: 1253108792", 1125.00, "Withdrawal"),
    ("2025-04-24", "Venmo Payment 1041740949041 Web ID: 3264681992", 19.68, "Withdrawal"),
    ("2025-04-28", "Venmo Payment 1041878439834 Web ID: 3264681992", 223.38, "Withdrawal"),
    ("2025-04-28", "04/28 Online Payment 24514658208 To Discover Card", 250.00, "Payment"),
    ("2025-04-30", "Recurring Card Purchase 04/30 Netflix.Com Netflix.Com CA Card 0885", 6.99, "Debit"),
    ("2025-05-07", "Interest Payment", -0.01, "Interest"),
]

# Chase Premier Plus Checking 1873 transactions
chase_1873_transactions = [
    ("2025-04-07", "Card Purchase With Pin 04/07 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-04-07", "Card Purchase 04/06 Mi Rancho #16 Concord CA Card 0665", 51.78, "Debit"),
    ("2025-04-07", "Card Purchase 04/06 Kings Donuts Concord CA Card 0665", 10.00, "Debit"),
    ("2025-04-08", "Card Purchase 04/07 Buttercup Concord Concord CA Card 0665", 45.12, "Debit"),
    ("2025-04-09", "Venmo Payment 1041385161651 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-04-09", "Recurring Card Purchase 04/08 State Farm Insurance 800-956-6310 IL Card 0665", 623.03, "Debit"),
    ("2025-04-09", "Recurring Card Purchase 04/08 Ringcentral Inc. 888-898-4591 CA Card 0665", 47.90, "Debit"),
    ("2025-04-10", "State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", 33.66, "Withdrawal"),
    ("2025-04-10", "Card Purchase With Pin 04/10 Lucky #705.Concord CA Concord CA Card 0665", 93.31, "Debit"),
    ("2025-04-10", "Card Purchase 04/09 Kings Donuts Concord CA Card 0665", 8.50, "Debit"),
    ("2025-04-11", "Card Purchase With Pin 04/11 M B Enterprises Pleasant Hill CA Card 0665", 25.00, "Debit"),
    ("2025-04-11", "Card Purchase 04/10 Buttercup Concord Concord CA Card 0665", 50.21, "Debit"),
    ("2025-04-11", "Card Purchase 04/10 Tesco Dublin CA Card 0665", 13.52, "Debit"),
    ("2025-04-14", "Card Purchase With Pin 04/14 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-04-14", "Card Purchase 04/12 Tj Maxx #0598 Concord CA Card 0665", 35.18, "Debit"),
    ("2025-04-14", "Card Purchase 04/12 Kings Donuts Concord CA Card 0665", 13.00, "Debit"),
    ("2025-04-14", "Card Purchase 04/12 Paypal *Pypl Payin4 402-935-7733 CA Card 0665", 18.97, "Debit"),
    ("2025-04-14", "Card Purchase 04/13 Papa Murphy's #1013 Concord CA Card 0665", 38.44, "Debit"),
    ("2025-04-15", "Card Purchase 04/14 Kings Donuts Concord CA Card 0665", 8.50, "Debit"),
    ("2025-04-16", "Card Purchase 04/15 Tourfactory/Collabrat 888-458-3943 WA Card 0665", 29.95, "Debit"),
    ("2025-04-17", "Card Purchase 04/16 Dairy Queen #14283 Walnut Creek CA Card 0665", 28.74, "Debit"),
    ("2025-04-18", "Card Purchase 04/17 Treats Mini Mart Concord CA Card 0665", 10.42, "Debit"),
    ("2025-04-18", "Recurring Card Purchase 04/17 Orange CO Superior C Acarlson@Occo CA Card 0665", 22.50, "Debit"),
    ("2025-04-18", "Card Purchase 04/17 Orange CO Superior C Acarlson@Occo CA Card 0665", 7.50, "Debit"),
    ("2025-04-18", "ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", 63.00, "Withdrawal"),
    ("2025-04-21", "Card Purchase 04/19 Subway 17502 Concord CA Card 0665", 14.89, "Debit"),
    ("2025-04-21", "Recurring Card Purchase 04/19 Adobe *800-833-6687 Adobe.Ly/Enus CA Card 0665", 12.99, "Debit"),
    ("2025-04-21", "Recurring Card Purchase 04/20 Dropbox*K96Hz98Smpxl Dropbox.Com CA Card 0665", 11.99, "Debit"),
    ("2025-04-21", "Card Purchase With Pin 04/21 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-04-22", "Recurring Card Purchase 04/21 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 55.62, "Debit"),
    ("2025-04-23", "Card Purchase 04/22 Baskin #360138 Concord CA Card 0665", 10.72, "Debit"),
    ("2025-04-23", "Card Purchase 04/22 Chipotle 0221 San Ramon CA Card 0665", 19.01, "Debit"),
    ("2025-04-24", "Recurring Card Purchase 04/23 Docusign Inc. 800-3799973 De Card 0665", 35.00, "Debit"),
    ("2025-04-24", "Card Purchase 04/23 Kings Donuts Concord CA Card 0665", 13.50, "Debit"),
    ("2025-04-25", "Venmo Payment 1041746763846 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-04-25", "Venmo Payment 1041746761980 Web ID: 3264681992", 509.00, "Withdrawal"),
    ("2025-04-25", "Card Purchase With Pin 04/25 Fashion Cleaners Walnut Creek CA Card 0665", 139.40, "Debit"),
    ("2025-04-28", "Verizon Wireless Payments PPD ID: 4223344794", 126.64, "Withdrawal"),
    ("2025-04-28", "Recurring Card Purchase 04/26 Mailchimp *Misc Mailchimp.Com GA Card 0665", 198.00, "Debit"),
    ("2025-04-28", "Card Purchase With Pin 04/28 Safeway #1192 Concord CA Card 0665", 128.73, "Debit"),
    ("2025-04-28", "Card Purchase With Pin 04/28 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-04-29", "04/25 Online Transfer To Chk ...8619 Transaction#: 24471468883", 150.00, "Transfer"),
    ("2025-04-29", "Card Purchase 04/27 Uep*Tasty Szechuan Nood Concord CA Card 0665", 42.24, "Debit"),
    ("2025-04-30", "Shwel8778111407 Webpayment Web ID: 3383693141", 480.08, "Withdrawal"),
    ("2025-04-30", "Card Purchase 04/29 Kings Donuts Concord CA Card 0665", 9.00, "Debit"),
    ("2025-05-01", "Card Purchase 04/30 Buttercup Concord Concord CA Card 0665", 52.11, "Debit"),
    ("2025-05-01", "Card Purchase 04/30 Orange CO Superior C Acarlson@Occo CA Card 0665", 15.00, "Debit"),
    ("2025-05-01", "Recurring Card Purchase 05/01 State Farm Insurance 800-956-6310 IL Card 0665", 106.51, "Debit"),
    ("2025-05-01", "Card Purchase 04/30 Treats Mini Mart Concord CA Card 0665", 6.95, "Debit"),
    ("2025-05-01", "Card Purchase 04/30 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-05-01", "Card Purchase 04/30 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-05-02", "Card Purchase 05/01 Paypal *Pandarestau 626-372-8419 CA Card 0665", 32.78, "Debit"),
    ("2025-05-02", "Recurring Card Purchase 05/01 Google *Nest 855-836-3987 CA Card 0665", 8.00, "Debit"),
    ("2025-05-02", "Recurring Card Purchase 05/01 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665", 19.99, "Debit"),
    ("2025-05-03", "05/03 Online Payment 24546613498 To Pg&E", 250.00, "Payment"),
    ("2025-05-03", "Card Purchase 05/02 Kings Donuts Concord CA Card 0665", 13.50, "Debit"),
    ("2025-05-03", "Recurring Card Purchase 05/02 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 42.18, "Debit"),
    ("2025-05-05", "Card Purchase With Pin 05/05 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-05-05", "Card Purchase With Pin 05/05 Wholefds Yvr#105 2941 Walnut Creek CA Card 0665", 129.69, "Debit"),
    ("2025-05-06", "05/06 Online Payment 24582175329 To Mr. Cooper", 3200.00, "Payment"),
    ("2025-05-06", "Card Purchase 05/04 Chipotle 0221 San Ramon CA Card 0665", 24.01, "Debit"),
    ("2025-05-06", "Card Purchase 05/05 Buttercup Concord Concord CA Card 0665", 42.66, "Debit"),
    ("2025-05-06", "Card Purchase 05/05 Kings Donuts Concord CA Card 0665", 8.50, "Debit"),
    ("2025-05-07", "Check # 1000", 280.00, "Check"),
    ("2025-05-07", "Interest Payment", -0.12, "Interest"),
]

# Chase Total Checking 8619 transactions
chase_8619_transactions = [
    ("2025-04-14", "State Farm Ro 27 Sfpp CCD ID: 9000313004", 106.83, "Withdrawal"),
    ("2025-04-25", "Online Transfer From Chk ...1873 Transaction#: 24471468883", -150.00, "Deposit"),
    ("2025-04-25", "Online Payment 24471317681 To Cowell Homeowners Association", 185.00, "Withdrawal"),
    ("2025-05-07", "Monthly Service Fee", 12.00, "Fee"),
]

def save_transactions(transactions, account_number, month=5):
    """Save transactions to CSV file."""
    # Create output directory
    output_dir = Path(f"/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase {account_number}/2025/monthly")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output filename
    filename = f"chase_{account_number}_2025-{month:02d}_transactions.csv"
    output_path = output_dir / filename
    
    # Convert to standard format
    formatted_transactions = []
    for date, desc, amount, tx_type in transactions:
        # Apply correct sign convention for Chase
        # Deposits and Interest are positive (credits to account)
        # Withdrawals, payments, fees, debits are negative (debits from account)
        if tx_type in ["Credit", "Interest", "Deposit"]:
            final_amount = abs(amount)
        else:
            final_amount = -abs(amount)
            
        formatted_transactions.append({
            'Description': desc,
            'Amount': final_amount,
            'Transaction Date': date,
            'Transaction Type': tx_type,
            'Status': 'New',
            'Statement id': f'2025-{month:02d} - Chase {account_number}',
            'Bank and last 4': f'Chase {account_number}'
        })
    
    # Write CSV
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                     'Status', 'Statement id', 'Bank and last 4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for transaction in formatted_transactions:
            writer.writerow(transaction)
    
    print(f"Saved {len(transactions)} transactions to {output_path}")
    return len(transactions)

def main():
    print("Extracting May 2025 Chase transactions...")
    
    # Save transactions for each account
    total = 0
    total += save_transactions(chase_2084_transactions, '2084', month=5)
    total += save_transactions(chase_1873_transactions, '1873', month=5)
    total += save_transactions(chase_8619_transactions, '8619', month=5)
    
    print(f"\nTotal transactions extracted: {total}")

if __name__ == "__main__":
    main()