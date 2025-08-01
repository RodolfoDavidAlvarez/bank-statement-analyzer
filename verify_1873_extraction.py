#!/usr/bin/env python3
"""Verify what's actually in the 1873 statement section of the PDF."""

# From the PDF page 3, account 1873 shows:
# Beginning Balance: $16,087.31
# Ending Balance: $528.22
# Deposits and Additions: $0.09
# Checks Paid: -$280.00
# ATM & Debit Card Withdrawals: -$4,496.80
# Electronic Withdrawals: -$10,782.38

print("Account 1873 - From PDF Statement Summary:")
print("=" * 60)
print(f"Beginning Balance: $16,087.31")
print(f"Deposits and Additions: $0.09")
print(f"Checks Paid: -$280.00")
print(f"ATM & Debit Card Withdrawals: -$4,496.80")
print(f"Electronic Withdrawals: -$10,782.38")
print(f"Total Withdrawals: ${280.00 + 4496.80 + 10782.38:,.2f}")
print(f"Expected Ending: $528.22")
print(f"Calculated: ${16087.31 + 0.09 - 280.00 - 4496.80 - 10782.38:,.2f}")

# Now let's check what the screenshot shows
print("\n\nFrom the screenshot, line items include:")
print("=" * 60)
print("Environmental AL Rf Pmt: $275.72 (line 3)")
print("Online Payment to Discover: -$250.00 (line 11)")
print("Online Payment to Pg&E: -$5.00 (line 12)")
print("Online Payment to Wave: -$1.00 (line 13)")
print("Online Payment to Pg&E: -$250.00 (line 14)")
print("Online Payment to Mr. Cooper: -$3,200.00 (line 15)")
print("Total of these items: ${275.72 - 250 - 5 - 1 - 250 - 3200:,.2f}")

print("\n\nThe issue:")
print("=" * 60)
print("If we include Environmental payment ($275.72), we'd have deposits of $275.81 not $0.09")
print("If we include online payments ($3,706), we'd have much higher electronic withdrawals")
print("\nThis confirms these transactions are NOT in account 1873's section of the PDF")