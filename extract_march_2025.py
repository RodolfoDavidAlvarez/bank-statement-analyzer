#!/usr/bin/env python3
"""Extract March 2025 transactions from Chase multi-account PDF."""

import csv
import os
from pathlib import Path

# March 2025 transactions for all three Chase accounts
# Extracted from: 20250307-statements-1873-.pdf

# Chase Premier Plus Checking 2084 transactions
chase_2084_transactions = [
    ("2025-02-10", "Venmo Payment 1040125103652 Web ID: 3264681992", 140.00, "Withdrawal"),
    ("2025-02-10", "Venmo Payment 1040125069889 Web ID: 3264681992", 70.14, "Withdrawal"),
    ("2025-02-10", "Venmo Payment 1040115653361 Web ID: 3264681992", 28.59, "Withdrawal"),
    ("2025-02-11", "Tesla Inc Tesla Moto PPD ID: 1463896777", 1171.08, "Withdrawal"),
    ("2025-02-17", "Card Purchase 02/12 Amazon.Com*Qx29L9Hs3 Amzn.Com/Bill WA Card 0885", 17.43, "Debit"),
    ("2025-02-20", "Keller Williams Psus_Feb20 PPD ID: 1742756628", -48.82, "Credit"),
    ("2025-02-20", "Lightstream Loan Pmts 45680968 Web ID: 1253108792", 1125.00, "Withdrawal"),
    ("2025-02-24", "Venmo Payment 1040434236470 Web ID: 3264681992", 80.00, "Withdrawal"),
    ("2025-02-27", "Card Purchase 02/23 Amazon Mktpl*1Y8FY39D3 Amzn.Com/Bill WA Card 0885", 8.62, "Debit"),
    ("2025-02-28", "Recurring Card Purchase 02/28 Netflix.Com Netflix.Com CA Card 0885", 6.99, "Debit"),
    ("2025-03-03", "Venmo Payment 1040591296551 Web ID: 3264681992", 45.74, "Withdrawal"),
    ("2025-03-07", "Interest Payment", -0.03, "Interest"),
]

# Chase Premier Plus Checking 1873 transactions  
chase_1873_transactions = [
    ("2025-02-07", "Card Purchase 02/07 Treat Blvd 76 Concord CA Card 0665", 46.29, "Debit"),
    ("2025-02-10", "State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", 33.66, "Withdrawal"),
    ("2025-02-10", "Venmo Payment 1040115664498 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-02-10", "Card Purchase 02/08 Kings Donuts Concord CA Card 0665", 16.50, "Debit"),
    ("2025-02-10", "Card Purchase 02/07 Kinder's Meats Deli Bb Concord CA Card 0665", 38.35, "Debit"),
    ("2025-02-10", "Recurring Card Purchase 02/10 State Farm Insurance 800-956-6310 IL Card 0665", 623.03, "Debit"),
    ("2025-02-10", "Recurring Card Purchase 02/10 Ringcentral Inc. 888-898-4591 CA Card 0665", 47.90, "Debit"),
    ("2025-02-10", "Card Purchase 02/10 Chipotle 0221 San Ramon CA Card 0665", 17.42, "Debit"),
    ("2025-02-11", "Card Purchase 02/10 Tesco Dublin CA Card 0665", 15.06, "Debit"),
    ("2025-02-12", "Card Purchase 02/10 Treats Mini Mart Concord CA Card 0665", 9.40, "Debit"),
    ("2025-02-12", "Card Purchase 02/10 Buttercup Concord Concord CA Card 0665", 46.85, "Debit"),
    ("2025-02-13", "02/13 Online Transfer To Chk ...8619 Transaction#: 23748537511", 150.00, "Transfer"),
    ("2025-02-13", "Card Purchase With Pin 02/13 M B Enterprises Pleasant Hill CA Card 0665", 50.00, "Debit"),
    ("2025-02-14", "Card Purchase 02/13 Kings Donuts Concord CA Card 0665", 15.50, "Debit"),
    ("2025-02-14", "Card Purchase 02/13 Tesco Dublin CA Card 0665", 46.35, "Debit"),
    ("2025-02-14", "Card Purchase 02/13 Baskin #360138 Concord CA Card 0665", 10.58, "Debit"),
    ("2025-02-15", "Card Purchase 02/14 Starbucks Store 11063 Concord CA Card 0665", 6.00, "Debit"),
    ("2025-02-18", "Card Purchase With Pin 02/18 Arco#12252 Concord CA Card 0665", 46.73, "Debit"),
    ("2025-02-18", "Card Purchase 02/15 Amazon.Com*8B1Rx5Yj0 Amzn.Com/Bill WA Card 0665", 40.18, "Debit"),
    ("2025-02-18", "Card Purchase 02/16 Buttercup Concord Concord CA Card 0665", 42.80, "Debit"),
    ("2025-02-18", "Card Purchase 02/16 Tesco Dublin CA Card 0665", 11.10, "Debit"),
    ("2025-02-18", "Card Purchase 02/16 Tourfactory/Collabrat 888-458-3943 WA Card 0665", 29.95, "Debit"),
    ("2025-02-18", "Card Purchase 02/17 Mi Rancho #16 Concord CA Card 0665", 38.64, "Debit"),
    ("2025-02-19", "Card Purchase 02/18 Taqueria Los Gallos Concord CA Card 0665", 18.46, "Debit"),
    ("2025-02-19", "Recurring Card Purchase 02/18 Adobe *800-833-6687 Adobe.Ly/Enus CA Card 0665", 12.99, "Debit"),
    ("2025-02-19", "Card Purchase 02/18 Orange CO Superior C Acarlson@Occo CA Card 0665", 15.00, "Debit"),
    ("2025-02-19", "ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", 63.00, "Withdrawal"),
    ("2025-02-20", "Card Purchase 02/19 Huckleberry's - Concord Concord CA Card 0665", 42.28, "Debit"),
    ("2025-02-20", "Card Purchase 02/19 Panda Express #1996 Concord CA Card 0665", 34.09, "Debit"),
    ("2025-02-20", "Recurring Card Purchase 02/19 Dropbox*K96Hz98Smpxl Dropbox.Com CA Card 0665", 11.99, "Debit"),
    ("2025-02-21", "Card Purchase 02/20 Swensen's Ice Cream-Conc Concord CA Card 0665", 15.07, "Debit"),
    ("2025-02-21", "Card Purchase With Pin 02/21 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-02-24", "Card Purchase 02/22 Kings Donuts Concord CA Card 0665", 15.50, "Debit"),
    ("2025-02-24", "Recurring Card Purchase 02/22 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 55.62, "Debit"),
    ("2025-02-24", "Card Purchase With Pin 02/24 Lucky #705.Concord CA Concord CA Card 0665", 102.12, "Debit"),
    ("2025-02-25", "Card Purchase 02/24 Paypal *Pandarestau 626-372-8419 CA Card 0665", 44.84, "Debit"),
    ("2025-02-25", "Recurring Card Purchase 02/24 Docusign Inc. 800-3799973 De Card 0665", 35.00, "Debit"),
    ("2025-02-25", "Venmo Payment 1040444642785 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-02-25", "Venmo Payment 1040444641616 Web ID: 3264681992", 509.00, "Withdrawal"),
    ("2025-02-26", "Recurring Card Purchase 02/25 Mailchimp *Misc Mailchimp.Com GA Card 0665", 198.00, "Debit"),
    ("2025-02-26", "Card Purchase With Pin 02/26 M B Enterprises Pleasant Hill CA Card 0665", 30.00, "Debit"),
    ("2025-02-26", "Card Purchase 02/25 Taqueria Los Gallos Concord CA Card 0665", 25.60, "Debit"),
    ("2025-02-26", "Verizon Wireless Payments PPD ID: 4223344794", 126.64, "Withdrawal"),
    ("2025-02-27", "Card Purchase 02/26 The Kebab Shop Concord CA Card 0665", 42.85, "Debit"),
    ("2025-02-28", "Card Purchase With Pin 02/28 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-03-01", "Shwel8778111407 Webpayment Web ID: 3383693141", 480.08, "Withdrawal"),
    ("2025-03-01", "Recurring Card Purchase 03/01 State Farm Insurance 800-956-6310 IL Card 0665", 106.51, "Debit"),
    ("2025-03-01", "Card Purchase With Pin 03/01 Safeway #1192 Concord CA Card 0665", 149.49, "Debit"),
    ("2025-03-03", "Card Purchase 03/01 Paypal *Pandarestau 626-372-8419 CA Card 0665", 45.44, "Debit"),
    ("2025-03-03", "Recurring Card Purchase 03/02 Google *Nest 855-836-3987 CA Card 0665", 8.00, "Debit"),
    ("2025-03-03", "Card Purchase 03/01 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-03-03", "Card Purchase 03/01 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-03-03", "Recurring Card Purchase 03/02 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665", 19.99, "Debit"),
    ("2025-03-04", "Card Purchase 03/03 Amazon.Com*Zk0Ow30F2 Amzn.Com/Bill WA Card 0665", 13.37, "Debit"),
    ("2025-03-04", "Card Purchase 03/03 Kings Donuts Concord CA Card 0665", 13.50, "Debit"),
    ("2025-03-05", "Card Purchase 03/04 Rite Aid Store #05839 Concord CA Card 0665", 22.39, "Debit"),
    ("2025-03-05", "Card Purchase 03/04 Paypal *Mochomacaro 408-842-6800 CA Card 0665", 107.23, "Debit"),
    ("2025-03-05", "Recurring Card Purchase 03/04 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 42.18, "Debit"),
    ("2025-03-06", "02/27 Online Transfer To Chk ...8619 Transaction#: 23891339871", 300.00, "Transfer"),
    ("2025-03-06", "03/06 Online Payment 23966146507 To Mr. Cooper", 3200.00, "Payment"),
    ("2025-03-06", "Card Purchase 03/05 Buttercup Concord Concord CA Card 0665", 48.35, "Debit"),
    ("2025-03-07", "Card Purchase With Pin 03/07 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-03-07", "Check # 999", 280.00, "Check"),
    ("2025-03-07", "Interest Payment", -0.04, "Interest"),
]

# Chase Total Checking 8619 transactions
chase_8619_transactions = [
    ("2025-02-10", "State Farm Ro 27 Sfpp CCD ID: 9000313004", 106.83, "Withdrawal"),
    ("2025-02-13", "Online Transfer From Chk ...1873 Transaction#: 23748537511", -150.00, "Deposit"),
    ("2025-02-13", "Online Payment 23748466117 To Cowell Homeowners Association", 185.00, "Withdrawal"),
    ("2025-02-27", "Online Transfer From Chk ...1873 Transaction#: 23891339871", -300.00, "Deposit"),
    ("2025-02-27", "Online Payment 23891209166 To Rushmore Servicing", 300.00, "Withdrawal"),
    ("2025-03-07", "Monthly Service Fee", 12.00, "Fee"),
]

def save_transactions(transactions, account_number, month=3):
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
    print("Extracting March 2025 Chase transactions...")
    
    # Save transactions for each account
    total = 0
    total += save_transactions(chase_2084_transactions, '2084', month=3)
    total += save_transactions(chase_1873_transactions, '1873', month=3)
    total += save_transactions(chase_8619_transactions, '8619', month=3)
    
    print(f"\nTotal transactions extracted: {total}")

if __name__ == "__main__":
    main()