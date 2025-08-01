#!/usr/bin/env python3
import re
import csv
from datetime import datetime

def extract_all_pdf_transactions(pdf_text):
    """Extract all transactions from PDF text with improved parsing"""
    transactions = []
    lines = pdf_text.split('\n')
    
    # Manual extraction of all transactions from the PDF
    pdf_transactions_raw = [
        # Page 3-4 transactions
        ("01/10", "Card Purchase 01/09 Eyelab Factory Outlet San Ramon CA Card 0665", -35.00),
        ("01/10", "Card Purchase 01/09 Chipotle 0221 San Ramon CA Card 0665", -18.98),
        ("01/10", "Card Purchase With Pin 01/10 Treat Blvd 76 Concord CA Card 0665", -46.29),
        ("01/13", "Card Purchase 01/11 Paypal *Pandarestau 626-372-8419 CA Card 0665", -61.84),
        ("01/13", "Recurring Card Purchase 01/11 Ringcentral Inc. 888-898-4591 CA Card 0665", -47.90),
        ("01/13", "Recurring Card Purchase 01/11 State Farm Insurance 800-956-6310 IL Card 0665", -623.03),
        ("01/13", "Card Purchase With Pin 01/13 Safeway #1192 Concord CA Card 0665", -188.50),
        ("01/14", "State Farm Ro 27 Cpc-Client 02 S 1067268602 CCD ID: 9000313004", -33.66),
        ("01/14", "Card Purchase With Pin 01/14 Treat Blvd 76 Concord CA Card 0665", -30.86),
        ("01/15", "Card Purchase With Pin 01/15 National Petroleum Con Concord CA Card 0665", -105.83),
        ("01/16", "Venmo Payment 1039635550955 Web ID: 3264681992", -2500.00),
        ("01/16", "Card Purchase With Pin 01/16 Treat Blvd 76 Concord CA Card 0665", -50.00),
        ("01/17", "Card Purchase 01/15 Buttercup Concord Concord CA Card 0665", -44.96),  # MISSING IN CSV
        ("01/17", "Card Purchase 01/16 4Te*Keller Williams R 925-934-2900 CA Card 0665", -125.00),
        ("01/17", "Card Purchase 01/16 Tourfactory/Collabrat 888-458-3943 WA Card 0665", -29.95),
        ("01/17", "Card Purchase 01/16 Mcdonald's F2033 Concord CA Card 0665", -16.10),
        ("01/17", "Card Purchase With Pin 01/17 Treat Blvd 76 Concord CA Card 0665", -46.29),
        ("01/21", "Card Purchase 01/17 Orange CO Superior C Acarlson@Occo CA Card 0665", -7.50),
        ("01/21", "Recurring Card Purchase 01/19 Adobe *800-833-6687 Adobe.Ly/Enus CA Card 0665", -12.99),
        ("01/21", "Card Purchase 01/19 Paypal *Pypl Payin4 402-935-7733 CA Card 0665", -18.97),
        ("01/21", "Recurring Card Purchase 01/20 Dropbox*K96Hz98Smpxl Dropbox.Com CA Card 0665", -11.99),
        ("01/21", "Card Purchase With Pin 01/21 Treat Blvd 76 Concord CA Card 0665", -30.86),
        ("01/21", "Card Purchase With Pin 01/21 Wholefds Yvr#105 2941 Walnut Creek CA Card 0665", -41.20),
        ("01/22", "Card Purchase 01/21 Kings Donuts Concord CA Card 0665", -8.50),
        ("01/22", "ADP - Tax ADP - Tax 731061468955A00 CCD ID: 9333006057", -63.00),
        ("01/22", "Check # 998", -280.00),
        ("01/23", "Recurring Card Purchase 01/22 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", -55.62),
        ("01/24", "Card Purchase With Pin 01/24 Kwik Stop Concord CA Card 0665", -179.93),
        ("01/24", "Card Purchase With Pin 01/24 Kwik Stop Concord CA Card 0665", -30.00),
        ("01/24", "Card Purchase With Pin 01/24 Kwik Stop Concord CA Card 0665", -160.50),
        ("01/27", "Card Purchase 01/24 Par*Mr. Pickles Sandwic Concord CA Card 0665", -23.12),
        ("01/27", "Recurring Card Purchase 01/25 Docusign Inc. 800-3799973 De Card 0665", -35.00),
        ("01/27", "Recurring Card Purchase 01/26 Mailchimp *Misc Mailchimp.Com GA Card 0665", -198.00),
        ("01/28", "Card Purchase 01/27 Baskin #360138 Concord CA Card 0665", -10.38),
        ("01/28", "Verizon Wireless Payments PPD ID: 4223344794", -126.64),
        ("01/28", "Card Purchase With Pin 01/28 M B Enterprises Pleasant Hill CA Card 0665", -50.00),
        ("01/29", "Card Purchase 01/28 Kings Donuts Concord CA Card 0665", -12.00),
        ("01/29", "Card Purchase With Pin 01/29 Vintage Wine Shoppe & Concord CA Card 0665", -36.38),
        ("01/30", "Card Purchase 01/30 Vintage Wine Shoppe & L Concord CA Card 0665", -23.15),
        ("01/30", "Venmo Payment 1039938525632 Web ID: 3264681992", -2500.00),
        ("01/30", "Venmo Payment 1039938515148 Web ID: 3264681992", -509.00),
        ("01/30", "Shwel8778111407 Webpayment Web ID: 3383693141", -480.08),
        ("01/31", "Card Purchase W/Cash 01/31 Petroleum & Amenities Walnut Creek CA Card 0665", -78.84),
        ("02/03", "Card Purchase 02/01 State Farm Insurance 800-956-6310 IL Card 0665", -106.51),
        ("02/03", "Card Purchase 01/31 Orange CO Superior C Acarlson@Occo CA Card 0665", -15.00),
        ("02/03", "Card Purchase 02/01 Cowell Hoa Walnutcountry CA Card 0665", -563.00),
        ("02/03", "Card Purchase 02/01 Cowell Hoa Walnutcountry CA Card 0665", -563.00),
        ("02/03", "Card Purchase 02/01 Uep*Tasty Szechuan Nood Concord CA Card 0665", -43.79),
        # Page 5 transactions (February)
        ("02/03", "Recurring Card Purchase 02/02 Dropbox*Gq4Yk3Hbdkkt Dropbox.Com CA Card 0665", -19.99),  # MISSING IN CSV
        ("02/03", "Card Purchase With Pin 02/03 Lucky #705.Concord CA Concord CA Card 0665", -92.24),  # MISSING IN CSV
        ("02/04", "Recurring Card Purchase 02/03 Google *Nest 855-836-3987 CA Card 0665", -8.00),  # MISSING IN CSV
        ("02/04", "Card Purchase With Pin 02/04 Best Little Donut Hous Concord CA Card 0665", -14.50),  # MISSING IN CSV
        ("02/05", "Recurring Card Purchase 02/04 Paypal *Pypl Paymthly 402-935-7733 CA Card 0665", -42.18),  # MISSING IN CSV
        ("02/05", "Card Purchase 02/04 House of Sake Inc Walnut Creek CA Card 0665", -83.55),  # MISSING IN CSV
        ("02/06", "Card Purchase With Pin 02/06 Treat Blvd 76 Concord CA Card 0665", -30.86),  # MISSING IN CSV
        ("02/06", "02/06 Online Transfer To Chk ...8619 Transaction#: 23637622827", -4570.00),  # MISSING IN CSV
        ("02/07", "Card Purchase 02/05 Jersey Mikes 20367 Walnut Creek CA Card 0665", -13.15),  # MISSING IN CSV
        ("02/07", "Card Purchase 02/06 Fast & Easy Liquors Concord CA Card 0665", -13.73),  # MISSING IN CSV
        ("02/07", "Card Purchase 02/06 Huckleberry's - Concord Concord CA Card 0665", -32.23),  # MISSING IN CSV
        ("02/07", "Card Purchase With Pin 02/07 Fashion Cleaners Walnut Creek CA Card 0665", -174.80),  # MISSING IN CSV
        ("02/07", "Card Purchase With Pin 02/07 Wholefds Yvr#105 2941 Walnut Creek CA Card 0665", -94.61),  # MISSING IN CSV
        ("02/07", "Card Purchase With Pin 02/07 Petroleum & Amenities Walnut Creek CA Card 0665", -90.20),  # MISSING IN CSV
        ("02/07", "Interest Payment", 0.09),  # MISSING IN CSV
    ]
    
    return pdf_transactions_raw

def load_csv_transactions(csv_path):
    """Load and normalize CSV transactions"""
    transactions = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Amount']:
                # Convert date from YYYY-MM-DD to MM/DD
                date = datetime.strptime(row['Transaction Date'], '%Y-%m-%d')
                transactions.append({
                    'date': date.strftime('%m/%d'),
                    'description': row['Description'].strip(),
                    'amount': float(row['Amount'])
                })
    return transactions

# Load data
csv_path = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv'
csv_transactions = load_csv_transactions(csv_path)
pdf_transactions = extract_all_pdf_transactions("")

print("DETAILED RECONCILIATION ANALYSIS")
print("=" * 80)

# Compare transactions
missing_transactions = []
total_missing = 0

for pdf_date, pdf_desc, pdf_amount in pdf_transactions:
    # Try to find matching transaction in CSV
    found = False
    
    for csv_trans in csv_transactions:
        # Check if dates match and amounts are close
        if csv_trans['date'] == pdf_date and abs(csv_trans['amount'] - pdf_amount) < 0.01:
            # Check if description has some common words
            pdf_words = set(pdf_desc.lower().split())
            csv_words = set(csv_trans['description'].lower().split())
            
            # If there's significant overlap in description, consider it a match
            if len(pdf_words & csv_words) >= 2:
                found = True
                break
    
    if not found:
        missing_transactions.append((pdf_date, pdf_desc, pdf_amount))
        total_missing += pdf_amount

print(f"Total PDF transactions: {len(pdf_transactions)}")
print(f"Total CSV transactions: {len(csv_transactions)}")
print(f"Missing transactions: {len(missing_transactions)}")
print(f"\nMISSING TRANSACTIONS:")
print("-" * 80)

for date, desc, amount in missing_transactions:
    print(f"{date} | {desc[:60]:<60} | ${amount:>10,.2f}")

print("-" * 80)
print(f"Total missing amount: ${total_missing:,.2f}")

# Verify reconciliation
beginning_balance = 16087.31
ending_balance = 528.22
expected_change = ending_balance - beginning_balance

csv_total = sum(t['amount'] for t in csv_transactions)

print(f"\nRECONCILIATION SUMMARY:")
print(f"Beginning Balance: ${beginning_balance:,.2f}")
print(f"Expected Ending Balance: ${ending_balance:,.2f}")
print(f"Expected Change: ${expected_change:,.2f}")
print(f"\nCSV Total: ${csv_total:,.2f}")
print(f"Missing Transactions Total: ${total_missing:,.2f}")
print(f"CSV + Missing: ${csv_total + total_missing:,.2f}")
print(f"\nDifference from expected: ${(csv_total + total_missing) - expected_change:,.2f}")

# Group missing by type
print(f"\nMISSING TRANSACTIONS BY TYPE:")
feb_missing = [(d, desc, amt) for d, desc, amt in missing_transactions if d.startswith('02/')]
jan_missing = [(d, desc, amt) for d, desc, amt in missing_transactions if d.startswith('01/')]

print(f"\nJanuary missing ({len(jan_missing)} transactions): ${sum(amt for _, _, amt in jan_missing):,.2f}")
for date, desc, amt in jan_missing:
    print(f"  {date} {desc[:50]:<50} ${amt:>10,.2f}")

print(f"\nFebruary missing ({len(feb_missing)} transactions): ${sum(amt for _, _, amt in feb_missing):,.2f}")
for date, desc, amt in feb_missing:
    print(f"  {date} {desc[:50]:<50} ${amt:>10,.2f}")