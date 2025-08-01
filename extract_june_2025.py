#!/usr/bin/env python3
"""Extract June 2025 transactions from Chase multi-account PDF."""

import csv
import os
from pathlib import Path

# June 2025 transactions for all three Chase accounts
# Extracted from: 20250606-statements-1873-.pdf

# Chase Premier Plus Checking 2084 transactions
chase_2084_transactions = [
    ("2025-05-09", "Tesla Inc Tesla Moto PPD ID: 1463896777", 1171.08, "Withdrawal"),
    ("2025-05-15", "Card Purchase 05/10 Amazon.Com*Jg68O2Fm1 Amzn.Com/Bill WA Card 0885", 21.65, "Debit"),
    ("2025-05-19", "Lightstream Loan Pmts 45680968 Web ID: 1253108792", 1125.00, "Withdrawal"),
    ("2025-05-20", "Keller Williams Psus_May20 PPD ID: 1742756628", -64.81, "Credit"),
    ("2025-05-21", "Venmo Payment 1042053866027 Web ID: 3264681992", 30.00, "Withdrawal"),
    ("2025-05-30", "Recurring Card Purchase 05/30 Netflix.Com Netflix.Com CA Card 0885", 6.99, "Debit"),
    ("2025-06-06", "Interest Payment", -0.02, "Interest"),
]

# Chase Premier Plus Checking 1873 transactions
chase_1873_transactions = [
    ("2025-05-07", "Card Purchase 05/06 Treats Mini Mart Concord CA Card 0665", 8.59, "Debit"),
    ("2025-05-07", "Card Purchase 05/06 Buttercup Concord Concord CA Card 0665", 31.14, "Debit"),
    ("2025-05-08", "Venmo Payment 1041916113607 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-05-08", "Card Purchase 05/07 Kings Donuts Concord CA Card 0665", 14.00, "Debit"),
    ("2025-05-09", "Recurring Card Purchase 05/08 Ringcentral Inc. 888-898-4591 CA Card 0665", 47.90, "Debit"),
    ("2025-05-09", "Recurring Card Purchase 05/08 State Farm Insurance 800-956-6310 IL Card 0665", 623.03, "Debit"),
    ("2025-05-09", "Card Purchase 05/08 Chick-Fil-A #04663 Concord CA Card 0665", 27.31, "Debit"),
    ("2025-05-12", "State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", 33.66, "Withdrawal"),
    ("2025-05-12", "Card Purchase With Pin 05/12 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-05-13", "Card Purchase 05/10 Kings Donuts Concord CA Card 0665", 9.50, "Debit"),
    ("2025-05-13", "Card Purchase 05/10 Paypal *Mochomacaro 408-842-6800 CA Card 0665", 45.22, "Debit"),
    ("2025-05-13", "Card Purchase 05/11 Mcdonald's F2033 Concord CA Card 0665", 3.00, "Debit"),
    ("2025-05-13", "Card Purchase 05/11 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-05-14", "Card Purchase With Pin 05/14 M B Enterprises Pleasant Hill CA Card 0665", 50.00, "Debit"),
    ("2025-05-14", "Card Purchase 05/13 Kings Donuts Concord CA Card 0665", 9.50, "Debit"),
    ("2025-05-15", "Card Purchase 05/14 Best Little Donut Hous Concord CA Card 0665", 17.00, "Debit"),
    ("2025-05-16", "Card Purchase 05/15 Tourfactory/Collabrat 888-458-3943 WA Card 0665", 29.95, "Debit"),
    ("2025-05-16", "Environmental AL Rf Pmt PPD ID: 1942751173", -275.72, "Credit"),
    ("2025-05-19", "Card Purchase 05/17 Mi Rancho #16 Concord CA Card 0665", 50.66, "Debit"),
    ("2025-05-19", "Card Purchase 05/16 Kings Donuts Concord CA Card 0665", 11.50, "Debit"),
    ("2025-05-19", "Recurring Card Purchase 05/18 Adobe *800-833-6687 Adobe.Ly/Enus CA Card 0665", 12.99, "Debit"),
    ("2025-05-19", "Card Purchase 05/17 In-N-Out Burger 0259 Concord CA Card 0665", 26.18, "Debit"),
    ("2025-05-19", "Card Purchase With Pin 05/19 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-05-20", "Recurring Card Purchase 05/19 Orange CO Superior C Acarlson@Occo CA Card 0665", 22.50, "Debit"),
    ("2025-05-20", "Card Purchase 05/19 Orange CO Superior C Acarlson@Occo CA Card 0665", 15.00, "Debit"),
    ("2025-05-20", "Recurring Card Purchase 05/19 Dropbox*K96Hz98Smpxl Dropbox.Com CA Card 0665", 11.99, "Debit"),
    ("2025-05-20", "ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", 63.00, "Withdrawal"),
    ("2025-05-21", "Card Purchase 05/20 Chipotle 0221 San Ramon CA Card 0665", 34.49, "Debit"),
    ("2025-05-21", "Card Purchase 05/20 Taqueria Los Gallos Concord CA Card 0665", 9.65, "Debit"),
    ("2025-05-22", "Recurring Card Purchase 05/21 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 55.62, "Debit"),
    ("2025-05-22", "Card Purchase 05/21 Baskin #360138 Concord CA Card 0665", 5.43, "Debit"),
    ("2025-05-23", "Recurring Card Purchase 05/22 Docusign Inc. 800-3799973 De Card 0665", 35.00, "Debit"),
    ("2025-05-23", "Card Purchase 05/22 Buttercup Concord Concord CA Card 0665", 33.70, "Debit"),
    ("2025-05-26", "05/23 Online Transfer To Chk ...8619 Transaction#: 24802648522", 300.00, "Transfer"),
    ("2025-05-26", "Venmo Payment 1042148866598 Web ID: 3264681992", 2500.00, "Withdrawal"),
    ("2025-05-26", "Venmo Payment 1042148864669 Web ID: 3264681992", 509.00, "Withdrawal"),
    ("2025-05-26", "Card Purchase 05/23 Papa Murphy's #1013 Concord CA Card 0665", 33.18, "Debit"),
    ("2025-05-27", "Card Purchase With Pin 05/27 Safeway #1192 Concord CA Card 0665", 108.34, "Debit"),
    ("2025-05-27", "Recurring Card Purchase 05/25 Mailchimp *Misc Mailchimp.Com GA Card 0665", 198.00, "Debit"),
    ("2025-05-27", "Verizon Wireless Payments PPD ID: 4223344794", 126.64, "Withdrawal"),
    ("2025-05-27", "Card Purchase With Pin 05/27 Treat Blvd 76 Concord CA Card 0665", 15.43, "Debit"),
    ("2025-05-28", "Card Purchase 05/27 Paypal *Pandarestau 626-372-8419 CA Card 0665", 26.01, "Debit"),
    ("2025-05-29", "05/29 Online Payment 24813625530 To Contra Costa Water District", 115.00, "Payment"),
    ("2025-05-30", "Shwel8778111407 Webpayment Web ID: 3383693141", 480.08, "Withdrawal"),
    ("2025-05-30", "Card Purchase 05/29 Kings Donuts Concord CA Card 0665", 22.00, "Debit"),
    ("2025-05-30", "Card Purchase 05/29 Chipotle 0221 San Ramon CA Card 0665", 21.50, "Debit"),
    ("2025-05-30", "Card Purchase 05/29 Jamba Juice #50163 Concord CA Card 0665", 9.20, "Debit"),
    ("2025-05-30", "Card Purchase 05/29 Orange CO Superior C Acarlson@Occo CA Card 0665", 7.50, "Debit"),
    ("2025-05-30", "Card Purchase 05/29 Cowell Hoa Walnutcountry CA Card 0665", 563.00, "Debit"),
    ("2025-06-01", "Card Purchase 05/31 Paypal *Pandarestau 626-372-8419 CA Card 0665", 45.50, "Debit"),
    ("2025-06-02", "Card Purchase 05/31 Tj Maxx #0598 Concord CA Card 0665", 58.29, "Debit"),
    ("2025-06-02", "Card Purchase 05/31 Treats Mini Mart Concord CA Card 0665", 10.42, "Debit"),
    ("2025-06-02", "Recurring Card Purchase 06/01 State Farm Insurance 800-956-6310 IL Card 0665", 106.51, "Debit"),
    ("2025-06-03", "Recurring Card Purchase 06/02 Google *Nest 855-836-3987 CA Card 0665", 8.00, "Debit"),
    ("2025-06-03", "Card Purchase 06/01 Huckleberry's - Concord Concord CA Card 0665", 41.67, "Debit"),
    ("2025-06-03", "Card Purchase 06/01 Dairy Queen #14283 Walnut Creek CA Card 0665", 36.13, "Debit"),
    ("2025-06-03", "Recurring Card Purchase 06/02 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665", 19.99, "Debit"),
    ("2025-06-04", "Card Purchase With Pin 06/04 Treat Blvd 76 Concord CA Card 0665", 30.86, "Debit"),
    ("2025-06-04", "Recurring Card Purchase 06/03 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", 42.18, "Debit"),
    ("2025-06-05", "06/05 Online Payment 24906183161 To Mr. Cooper", 3200.00, "Payment"),
    ("2025-06-05", "Card Purchase 06/04 In-N-Out Burger 0259 Concord CA Card 0665", 20.72, "Debit"),
    ("2025-06-05", "Card Purchase 06/04 Kings Donuts Concord CA Card 0665", 9.50, "Debit"),
    ("2025-06-06", "Interest Payment", -0.10, "Interest"),
]

# Chase Total Checking 8619 transactions
chase_8619_transactions = [
    ("2025-05-14", "State Farm Ro 27 Sfpp CCD ID: 9000313004", 106.83, "Withdrawal"),
    ("2025-05-23", "Online Transfer From Chk ...1873 Transaction#: 24802648522", -300.00, "Deposit"),
    ("2025-05-23", "Online Payment 24802530388 To Cowell Homeowners Association", 185.00, "Withdrawal"),
    ("2025-05-23", "Online Payment 24802507547 To Rushmore Servicing", 300.00, "Withdrawal"),
    ("2025-06-06", "Monthly Service Fee", 12.00, "Fee"),
]

def save_transactions(transactions, account_number, month=6):
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
    print("Extracting June 2025 Chase transactions...")
    
    # Save transactions for each account
    total = 0
    total += save_transactions(chase_2084_transactions, '2084', month=6)
    total += save_transactions(chase_1873_transactions, '1873', month=6)
    total += save_transactions(chase_8619_transactions, '8619', month=6)
    
    print(f"\nTotal transactions extracted: {total}")

if __name__ == "__main__":
    main()