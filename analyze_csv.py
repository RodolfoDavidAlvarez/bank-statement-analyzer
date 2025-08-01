import pandas as pd

# Read the CSV file
csv_path = '/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/bank-statement-analyzer/accounts/Chase 1873/2025/monthly/chase_1873_2025-02_transactions.csv'
df = pd.read_csv(csv_path)

# Display the DataFrame info
print('DataFrame shape:', df.shape)
print('\nColumn names:', df.columns.tolist())

# Calculate totals
total_debits = df['Amount'].sum()
total_credits = df[df['Amount'] > 0]['Amount'].sum()
total_withdrawals = abs(df[df['Amount'] < 0]['Amount'].sum())

print(f'\nTotal debits (negative amounts): ${total_withdrawals:,.2f}')
print(f'Total credits (positive amounts): ${total_credits:,.2f}')
print(f'Net change: ${total_debits:,.2f}')

# Count transactions by type
print('\nTransaction counts by type:')
print(df['Transaction Type'].value_counts())

# Calculate what the ending balance should be
beginning_balance = 16087.31
calculated_ending = beginning_balance + total_debits
expected_ending = 528.22
difference = expected_ending - calculated_ending

print(f'\nBeginning balance: ${beginning_balance:,.2f}')
print(f'Net change in CSV: ${total_debits:,.2f}')
print(f'Calculated ending balance: ${calculated_ending:,.2f}')
print(f'Expected ending balance: ${expected_ending:,.2f}')
print(f'Difference (missing from CSV): ${difference:,.2f}')

# Show transaction date range
print(f'\nTransaction date range:')
print(f'First: {df["Transaction Date"].min()}')
print(f'Last: {df["Transaction Date"].max()}')
