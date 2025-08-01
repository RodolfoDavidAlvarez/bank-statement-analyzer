#!/usr/bin/env python3
"""Extract April 2025 transactions from Chase multi-account PDF."""

import csv
import os
from pathlib import Path

# April 2025 transactions for all three Chase accounts
# Extracted from: 20250407-statements-1873-.pdf

# Chase Premier Plus Checking 2084 transactions
chase_2084_transactions = [
    ("2025-03-10", "Venmo Payment 1040714328516 Web ID: 3264681992", 181.49, "Withdrawal"),
    ("2025-03-14", "Tesla Inc Tesla Moto PPD ID: 1463896777", 1171.08, "Withdrawal"),
    ("2025-03-18", "Lightstream Loan Pmts 45680968 Web ID: 1253108792", 1125.00, "Withdrawal"),
    ("2025-03-20", "Keller Williams Psus_Mar20 PPD ID: 1742756628", -0.02, "Credit"),
    ("2025-03-24", "Venmo Payment 1041015302695 Web ID: 3264681992", 28.44, "Withdrawal"),
    ("2025-03-26", "Online Transfer From Chk ...1873 Transaction#: 24125337455", -4850.00, "Deposit"),
    ("2025-03-31", "Recurring Card Purchase 03/31 Netflix.Com Netflix.Com CA Card 0885", 6.99, "Debit"),
    ("2025-04-07", "Venmo Payment 1041313018287 Web ID: 3264681992", 120.00, "Withdrawal"),
    ("2025-04-07", "Interest Payment", -0.12, "Interest"),
]

# Chase Premier Plus Checking 1873 transactions
chase_1873_transactions = [
    ("2025-03-07", "Card Purchase 03/06 Eggroll Kung Fu Tea Concord CA Card 0665", 31.69, "Debit"),
    ("2025-03-10", "State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", 33.66, "Withdrawal"),
    ("2025-03-10", "Venmo Payment 1040704977816 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-03-10", "Card Purchase 03/08 In-N-Out Burger 0259 Concord CA Card 0665", 16.71, "Debit"),
    ("2025-03-10", "Card Purchase 03/07 Tesco Dublin CA Card 0665", 12.42, "Debit"),
    ("2025-03-10", "Card Purchase 03/08 Baskin #360138 Concord CA Card 0665", 19.96, "Debit"),
    ("2025-03-10", "Recurring Card Purchase 03/09 Ringcentral Inc. 888-898-4591 CA Card 0665", 47.90, "Debit"),
    ("2025-03-10", "Recurring Card Purchase 03/09 State Farm Insurance 800-956-6310 IL Card 0665", 623.03, "Debit"),
    ("2025-03-11", "Card Purchase With Pin 03/11 Lucky #705.Concord CA Concord CA Card 0665", 55.60, "Debit"),
    ("2025-03-11", "Card Purchase 03/10 Paypal *Mochomacaro 408-842-6800 CA Card 0665", 49.00, "Debit"),
    ("2025-03-12", "Card Purchase 03/11 Chipotle 0221 San Ramon CA Card 0665", 18.25, "Debit"),
    ("2025-03-12", "Card Purchase 03/11 Kings Donuts Concord CA Card 0665", 13.50, "Debit"),
    ("2025-03-13", "Card Purchase 03/12 Chick-Fil-A #04663 Concord CA Card 0665", 29.63, "Debit"),
    ("2025-03-13", "Card Purchase 03/12 Huckleberry's - Concord Concord CA Card 0665", 37.45, "Debit"),
    ("2025-03-14", "Card Purchase With Pin 03/14 M B Enterprises Pleasant Hill CA Card 0665", 37.00, "Debit"),
    ("2025-03-17", "Card Purchase 03/15 Tesco Dublin CA Card 0665", 53.23, "Debit"),
    ("2025-03-17", "Card Purchase 03/15 Tesco Dublin CA Card 0665", 10.61, "Debit"),
    ("2025-03-17", "Card Purchase 03/15 Tourfactory/Collabrat 888-458-3943 WA Card 0665", 29.95, "Debit"),
    ("2025-03-18", "Card Purchase 03/17 Tj Maxx #0598 Concord CA Card 0665", 53.78, "Debit"),
    ("2025-03-18", "Card Purchase 03/17 Jersey Mikes 20367 Walnut Creek CA Card 0665", 15.46, "Debit"),
    ("2025-03-19", "Recurring Card Purchase 03/18 Adobe *800-833-6687 Adobe.Ly/Enus CA Card 0665", 12.99, "Debit"),
    ("2025-03-19", "Recurring Card Purchase 03/18 Orange CO Superior C Acarlson@Occo CA Card 0665", 22.50, "Debit"),
    ("2025-03-19", "Card Purchase 03/18 Orange CO Superior C Acarlson@Occo CA Card 0665", 15.00, "Debit"),
    ("2025-03-19", "ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", 63.00, "Withdrawal"),
    ("2025-03-20", "Card Purchase 03/19 Dairy Queen #14283 Walnut Creek CA Card 0665", 33.87, "Debit"),
    ("2025-03-20", "Recurring Card Purchase 03/19 Dropbox*K96Hz98Smpxl Dropbox.Com CA Card 0665", 11.99, "Debit"),
    ("2025-03-21", "Card Purchase With Pin 03/21 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-03-21", "Card Purchase 03/20 Goodwill Retail Sto Concord CA Card 0665", 10.73, "Debit"),
    ("2025-03-21", "Card Purchase 03/20 Goodwill Retail Sto Concord CA Card 0665", 5.49, "Debit"),
    ("2025-03-21", "Card Purchase 03/20 Mcdonald's F2033 Concord CA Card 0665", 10.01, "Debit"),
    ("2025-03-24", "Recurring Card Purchase 03/22 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 55.62, "Debit"),
    ("2025-03-24", "Card Purchase 03/22 Mcdonald's F2033 Concord CA Card 0665", 11.27, "Debit"),
    ("2025-03-24", "Card Purchase 03/23 Kings Donuts Concord CA Card 0665", 19.35, "Debit"),
    ("2025-03-25", "Recurring Card Purchase 03/24 Docusign Inc. 800-3799973 De Card 0665", 35.00, "Debit"),
    ("2025-03-25", "Card Purchase 03/24 Chick-Fil-A #04663 Concord CA Card 0665", 21.57, "Debit"),
    ("2025-03-25", "Venmo Payment 1041043468821 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-03-25", "Venmo Payment 1041043466910 Web ID: 3264681992", 509.00, "Withdrawal"),
    ("2025-03-26", "03/26 Online Transfer To Chk ...2084 Transaction#: 24125337455", 4850.00, "Transfer"),
    ("2025-03-26", "Recurring Card Purchase 03/25 Mailchimp *Misc Mailchimp.Com GA Card 0665", 198.00, "Debit"),
    ("2025-03-26", "Card Purchase 03/25 Baskin #360138 Concord CA Card 0665", 13.58, "Debit"),
    ("2025-03-26", "Verizon Wireless Payments PPD ID: 4223344794", 126.64, "Withdrawal"),
    ("2025-03-27", "Card Purchase With Pin 03/27 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-03-28", "Card Purchase 03/27 Baskin #360138 Concord CA Card 0665", 19.29, "Debit"),
    ("2025-03-28", "Environmental AL Rf Pmt PPD ID: 1942751173", -275.72, "Credit"),
    ("2025-03-29", "Card Purchase 03/28 Jersey Mikes 20367 Walnut Creek CA Card 0665", 14.48, "Debit"),
    ("2025-03-31", "Shwel8778111407 Webpayment Web ID: 3383693141", 480.08, "Withdrawal"),
    ("2025-03-31", "03/27 Online Transfer To Chk ...8619 Transaction#: 24169576326", 150.00, "Transfer"),
    ("2025-04-01", "Recurring Card Purchase 04/01 State Farm Insurance 800-956-6310 IL Card 0665", 106.51, "Debit"),
    ("2025-04-01", "Card Purchase 03/30 Paypal *Pandarestau 626-372-8419 CA Card 0665", 42.24, "Debit"),
    ("2025-04-01", "Card Purchase 03/30 Uep*Tasty Szechuan Nood Concord CA Card 0665", 55.51, "Debit"),
    ("2025-04-01", "Card Purchase 03/31 Card Purchase 03/31 Treats Mini Mart Concord CA Card 0665", 6.95, "Debit"),
    ("2025-04-01", "Card Purchase 03/31 Card Purchase 03/31 Treats Mini Mart Concord CA Card 0665", 3.50, "Debit"),
    ("2025-04-01", "Card Purchase 03/31 Orange CO Superior C Acarlson@Occo CA Card 0665", 7.50, "Debit"),
    ("2025-04-01", "Card Purchase 03/31 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-04-01", "Card Purchase 03/31 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-04-02", "Recurring Card Purchase 04/01 Google *Nest 855-836-3987 CA Card 0665", 8.00, "Debit"),
    ("2025-04-02", "Recurring Card Purchase 04/01 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665", 19.99, "Debit"),
    ("2025-04-02", "Card Purchase 04/01 Paypal *Oilchangers 925-969-6700 CA Card 0665", 107.04, "Debit"),
    ("2025-04-03", "04/03 Online Payment 24216606329 To Mr. Cooper", 3200.00, "Payment"),
    ("2025-04-03", "Card Purchase With Pin 04/03 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-04-04", "04/04 Online Payment 24232965468 To Pg&E", 250.00, "Payment"),
    ("2025-04-04", "Card Purchase 04/03 Kings Donuts Concord CA Card 0665", 21.00, "Debit"),
    ("2025-04-04", "Recurring Card Purchase 04/03 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 42.18, "Debit"),
    ("2025-04-07", "Card Purchase 04/04 Buttercup Concord Concord CA Card 0665", 54.73, "Debit"),
    ("2025-04-07", "Card Purchase 04/04 Paypal *Pandarestau 626-372-8419 CA Card 0665", 37.39, "Debit"),
    ("2025-04-07", "Card Purchase 04/05 Chipotle 0221 San Ramon CA Card 0665", 29.84, "Debit"),
    ("2025-04-07", "Card Purchase 04/05 Kings Donuts Concord CA Card 0665", 11.50, "Debit"),
    ("2025-04-07", "Interest Payment", -0.13, "Interest"),
]

# Chase Total Checking 8619 transactions
chase_8619_transactions = [
    ("2025-03-14", "State Farm Ro 27 Sfpp CCD ID: 9000313004", 106.83, "Withdrawal"),
    ("2025-03-27", "Online Transfer From Chk ...1873 Transaction#: 24169576326", -150.00, "Deposit"),
    ("2025-03-27", "Online Payment 24169419066 To Cowell Homeowners Association", 185.00, "Withdrawal"),
    ("2025-04-07", "Monthly Service Fee", 12.00, "Fee"),
]

def save_transactions(transactions, account_number, month=4):
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
    print("Extracting April 2025 Chase transactions...")
    
    # Save transactions for each account
    total = 0
    total += save_transactions(chase_2084_transactions, '2084', month=4)
    total += save_transactions(chase_1873_transactions, '1873', month=4)
    total += save_transactions(chase_8619_transactions, '8619', month=4)
    
    print(f"\nTotal transactions extracted: {total}")

if __name__ == "__main__":
    main()