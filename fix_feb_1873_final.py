#!/usr/bin/env python3
"""Fix February 2025 Chase 1873 by removing transactions that belong to account 2084."""

import csv
from pathlib import Path

# Correct transactions for Chase 1873 February 2025
# Removing online payments that belong to account 2084
chase_1873_transactions = [
    # Transfer FROM 1873 TO 8619 - this belongs to 1873
    ("02/06 Online Transfer To Chk ...8619 Transaction#: 23637622827", -4570.00, "2025-02-06", "Transfer"),
    
    # Check
    ("Check # 998", -280.00, "2025-01-22", "Check"),
    
    # All card purchases belong to 1873 (Card 0665)
    ("Card Purchase 01/09 Eyelab Factory Outlet San Ramon CA Card 0665", -35.00, "2025-01-10", "Debit"),
    ("Card Purchase 01/09 Chipotle 0221 San Ramon CA Card 0665", -18.98, "2025-01-10", "Debit"),
    ("Card Purchase With Pin 01/10 Treat Blvd 76 Concord CA Card 0665", -46.29, "2025-01-10", "Debit"),
    ("Card Purchase 01/11 Paypal *Pandarestau 626-372-8419 CA Card 0665", -61.84, "2025-01-13", "Debit"),
    ("Recurring Card Purchase 01/11 Ringcentral Inc. 888-898-4591 CA Card 0665", -47.90, "2025-01-13", "Debit"),
    ("Recurring Card Purchase 01/11 State Farm Insurance 800-956-6310 IL Card 0665", -623.03, "2025-01-13", "Debit"),
    ("Card Purchase With Pin 01/13 Safeway #1192 Concord CA Card 0665", -188.50, "2025-01-13", "Debit"),
    ("Card Purchase With Pin 01/14 Treat Blvd 76 Concord CA Card 0665", -30.86, "2025-01-14", "Debit"),
    ("Card Purchase With Pin 01/15 National Petroleum Con Concord CA Card 0665", -105.83, "2025-01-15", "Debit"),
    ("Card Purchase With Pin 01/16 Treat Blvd 76 Concord CA Card 0665", -50.00, "2025-01-16", "Debit"),
    ("Card Purchase 01/15 Buttercup Concord Concord CA Card 0665", -44.96, "2025-01-17", "Debit"),
    ("Card Purchase 01/16 4Te*Keller Williams R 925-934-2900 CA Card 0665", -125.00, "2025-01-17", "Debit"),
    ("Card Purchase 01/16 Tourfactory/Collabrat 888-458-3943 WA Card 0665", -29.95, "2025-01-17", "Debit"),
    ("Card Purchase 01/16 Mcdonald's F2033 Concord CA Card 0665", -16.10, "2025-01-17", "Debit"),
    ("Card Purchase With Pin 01/17 Treat Blvd 76 Concord CA Card 0665", -46.29, "2025-01-17", "Debit"),
    ("Card Purchase 01/17 Orange CO Superior C Acarlson@Occo CA Card 0665", -7.50, "2025-01-21", "Debit"),
    ("Recurring Card Purchase 01/19 Adobe *800-833-6687 Adobe.Ly/Enus CA Card 0665", -12.99, "2025-01-21", "Debit"),
    ("Card Purchase 01/19 Paypal *Pypl Payin4 402-935-7733 CA Card 0665", -18.97, "2025-01-21", "Debit"),
    ("Recurring Card Purchase 01/20 Dropbox*K96Hz98Smpxl Dropbox.Com CA Card 0665", -11.99, "2025-01-21", "Debit"),
    ("Card Purchase With Pin 01/21 Treat Blvd 76 Concord CA Card 0665", -30.86, "2025-01-21", "Debit"),
    ("Card Purchase With Pin 01/21 Wholefds Yvr#105 2941 Walnut Creek CA Card 0665", -41.20, "2025-01-21", "Debit"),
    ("Card Purchase 01/21 Kings Donuts Concord CA Card 0665", -8.50, "2025-01-22", "Debit"),
    ("Recurring Card Purchase 01/22 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", -55.62, "2025-01-23", "Debit"),
    ("Card Purchase With Pin 01/24 Kwik Stop Concord CA Card 0665", -179.93, "2025-01-24", "Debit"),
    ("Card Purchase With Pin 01/24 Kwik Stop Concord CA Card 0665", -30.00, "2025-01-24", "Debit"),
    ("Card Purchase With Pin 01/24 Kwik Stop Concord CA Card 0665", -160.50, "2025-01-24", "Debit"),
    ("Card Purchase 01/24 Par*Mr. Pickles Sandwic Concord CA Card 0665", -23.12, "2025-01-27", "Debit"),
    ("Recurring Card Purchase 01/25 Docusign Inc. 800-3799973 De Card 0665", -35.00, "2025-01-27", "Debit"),
    ("Recurring Card Purchase 01/26 Mailchimp *Misc Mailchimp.Com GA Card 0665", -198.00, "2025-01-27", "Debit"),
    ("Card Purchase 01/27 Baskin #360138 Concord CA Card 0665", -10.38, "2025-01-28", "Debit"),
    ("Card Purchase With Pin 01/28 M B Enterprises Pleasant Hill CA Card 0665", -50.00, "2025-01-28", "Debit"),
    ("Card Purchase 01/28 Kings Donuts Concord CA Card 0665", -12.00, "2025-01-29", "Debit"),
    ("Card Purchase With Pin 01/29 Vintage Wine Shoppe & Concord CA Card 0665", -36.38, "2025-01-29", "Debit"),
    ("Card Purchase 01/30 Vintage Wine Shoppe & L Concord CA Card 0665", -23.15, "2025-01-30", "Debit"),
    ("Card Purchase W/Cash 01/31 Petroleum & Amenities Walnut Creek CA Card 0665 Purchase $58.84 Cash Back $20.00", -78.84, "2025-01-31", "Debit"),
    ("Card Purchase 02/01 State Farm Insurance 800-956-6310 IL Card 0665", -106.51, "2025-02-03", "Debit"),
    ("Card Purchase 01/31 Orange CO Superior C Acarlson@Occo CA Card 0665", -15.00, "2025-02-03", "Debit"),
    ("Card Purchase 02/01 Cowell Hoa Walnutcountry CA Card 0665", -563.00, "2025-02-03", "Debit"),
    ("Card Purchase 02/01 Cowell Hoa Walnutcountry CA Card 0665", -563.00, "2025-02-03", "Debit"),
    ("Card Purchase 02/01 Uep*Tasty Szechuan Nood Concord CA Card 0665", -43.79, "2025-02-03", "Debit"),
    ("Recurring Card Purchase 02/02 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665", -19.99, "2025-02-03", "Debit"),
    ("Card Purchase With Pin 02/03 Lucky #705.Concord CA Concord CA Card 0665", -92.24, "2025-02-03", "Debit"),
    ("Recurring Card Purchase 02/03 Google *Nest 855-836-3987 CA Card 0665", -8.00, "2025-02-04", "Debit"),
    ("Card Purchase With Pin 02/04 Best Little Donut Hous Concord CA Card 0665", -14.50, "2025-02-04", "Debit"),
    ("Recurring Card Purchase 02/04 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", -42.18, "2025-02-05", "Debit"),
    ("Card Purchase 02/04 House of Sake Inc Walnut Creek CA Card 0665", -83.55, "2025-02-05", "Debit"),
    ("Card Purchase With Pin 02/06 Treat Blvd 76 Concord CA Card 0665", -30.86, "2025-02-06", "Debit"),
    ("Card Purchase 02/05 Jersey Mikes 20367 Walnut Creek CA Card 0665", -13.15, "2025-02-07", "Debit"),
    ("Card Purchase 02/06 Fast & Easy Liquors Concord CA Card 0665", -13.73, "2025-02-07", "Debit"),
    ("Card Purchase 02/06 Huckleberry's - Concord Concord CA Card 0665", -32.23, "2025-02-07", "Debit"),
    ("Card Purchase With Pin 02/07 Fashion Cleaners Walnut Creek CA Card 0665", -174.80, "2025-02-07", "Debit"),
    ("Card Purchase With Pin 02/07 Wholefds Yvr#105 2941 Walnut Creek CA Card 0665", -94.61, "2025-02-07", "Debit"),
    ("Card Purchase With Pin 02/07 Petroleum & Amenities Walnut Creek CA Card 0665", -90.20, "2025-02-07", "Debit"),
    
    # Electronic withdrawals specific to 1873
    ("State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", -33.66, "2025-01-14", "Withdrawal"),
    ("Venmo Payment 1039635550955 Web ID: 3264681992", -2500.00, "2025-01-16", "Withdrawal"),
    ("ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", -63.00, "2025-01-22", "Withdrawal"),
    ("Verizon Wireless Payments PPD ID: 4223344794", -126.64, "2025-01-28", "Withdrawal"),
    ("Venmo Payment 1039938525632 Web ID: 3264681992", -2500.00, "2025-01-30", "Withdrawal"),
    ("Venmo Payment 1039938515148 Web ID: 3264681992", -509.00, "2025-01-30", "Withdrawal"),
    ("Shwel8778111407 Webpayment Web ID: 3383693141", -480.08, "2025-01-30", "Withdrawal"),
    
    # Interest
    ("Interest Payment", 0.09, "2025-02-07", "Interest"),
]

# Save corrected file
output_path = Path("/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv")

with open(output_path, 'w', newline='') as csvfile:
    fieldnames = ['Description', 'Amount', 'Transaction Date', 'Transaction Type', 
                 'Status', 'Statement id', 'Bank and last 4']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for desc, amount, date, tx_type in chase_1873_transactions:
        writer.writerow({
            'Description': desc,
            'Amount': amount,
            'Transaction Date': date,
            'Transaction Type': tx_type,
            'Status': 'New',
            'Statement id': '2025-02 - Chase 1873',
            'Bank and last 4': 'Chase 1873'
        })

print(f"Fixed Chase 1873 February 2025 transactions")
print(f"Removed online payments that belong to account 2084:")
print(f"  - Online Transfer To Chk ...8619 ($150.00)")
print(f"  - Online Payment to Discover Card ($250.00)")  
print(f"  - Online Payment to Pg&E ($5.00)")
print(f"  - Online Payment to Wave ($1.00)")
print(f"  - Online Payment to Pg&E ($250.00)")
print(f"  - Online Payment to Mr. Cooper ($3,200.00)")
print(f"Total removed: $3,856.00")
print(f"\nTotal transactions: {len(chase_1873_transactions)}")

# Verify reconciliation
deposits = sum(amt for _, amt, _, _ in chase_1873_transactions if amt > 0)
withdrawals = sum(amt for _, amt, _, _ in chase_1873_transactions if amt < 0)
print(f"\nReconciliation:")
print(f"Beginning Balance: $16,087.31")
print(f"Deposits: ${deposits:.2f}")
print(f"Withdrawals: ${withdrawals:.2f}")
print(f"Net Change: ${deposits + withdrawals:.2f}")
print(f"Calculated Ending: ${16087.31 + deposits + withdrawals:.2f}")
print(f"Expected Ending: $528.22")

# Check totals match statement
checks = sum(amt for desc, amt, _, _ in chase_1873_transactions if 'Check' in desc)
cards = sum(amt for desc, amt, _, tx_type in chase_1873_transactions if tx_type == 'Debit')
electronic = sum(amt for desc, amt, _, tx_type in chase_1873_transactions if tx_type in ['Withdrawal', 'Transfer', 'Payment'])

print(f"\nBy category:")
print(f"Checks: ${abs(checks):.2f} (expected: $280.00)")
print(f"Card withdrawals: ${abs(cards):.2f} (expected: $4,496.80)")
print(f"Electronic withdrawals: ${abs(electronic):.2f} (expected: $10,782.38)")