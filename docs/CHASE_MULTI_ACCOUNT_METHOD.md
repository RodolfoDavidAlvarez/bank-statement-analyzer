# Chase Multi-Account Statement Extraction Method

## Applicable Accounts

**This method applies specifically to:**
- Chase Premier Plus Checking (2084)
- Chase Premier Plus Checking (1873)  
- Chase Total Checking (8619)

**Note:** Other Chase accounts (e.g., Chase 5036) may use a different statement format and require a separate extraction method.

## Overview

These specific Chase checking accounts are provided in a consolidated statement format where multiple accounts appear in a single PDF. Each account must be extracted separately while maintaining our standard CSV format.

## CRITICAL: Understanding the PDF Structure

### 1. Multi-Account Format
- Single PDF contains all 3 checking accounts
- Each account has its own section
- **WARNING**: The header on EVERY page shows "Primary Account: 2084" but this is misleading
- **IMPORTANT**: Look for "Account Number:" within each section to identify which account the transactions belong to

### 2. Account Identification Rules
To determine which account a transaction belongs to:

1. **Card Numbers**:
   - Card 0885 = Account 2084
   - Card 0665 = Account 1873
   - No card mentioned = Check other indicators

2. **Online Payments**: 
   - "Online Payment" transactions typically originate from account 2084
   - Exception: If the page clearly shows "Account Number: 1873" or "Account Number: 8619"

3. **Transfers**:
   - "Online Transfer To Chk ...XXXX" = Debit from the current account
   - "Online Transfer From Chk ...XXXX" = Credit to the current account
   - Pay attention to which account is sending vs receiving

4. **Special Payments**:
   - Environmental AL Rf Pmt = Usually to account 2084
   - Keller Williams payments = Usually to account 2084
   - State Farm Ro 27 = Check account number on the page
   - ADP Tax = Usually from account 1873
   - Verizon Wireless = Usually from account 1873

## Extraction Method

### Step 1: Pre-Analysis
1. Scan the entire PDF to understand the account structure
2. Note which pages contain which account's transactions
3. Create a mental map of transaction ownership

### Step 2: Extract Per Account

For each account, extract ONLY transactions that belong to that account:

#### Transaction Information
- **Date**: Convert MM/DD to YYYY-MM-DD (add year based on statement period)
- **Description**: Full transaction description
- **Amount**: 
  - Deposits/Credits/Interest: Positive
  - Withdrawals/Debits/Fees/Payments: Negative
- **Transaction Type**: Map based on description

#### Common Pitfalls to Avoid
1. **DO NOT** assign online payments to multiple accounts
2. **DO NOT** rely on the "Primary Account" shown in headers
3. **DO** verify card numbers match the account
4. **DO** check the "Account Number:" field on each page
5. **DO** ensure transfers balance (one account's debit is another's credit)

### Step 3: Validation Before Saving

**CRITICAL**: Before saving any file, verify:
1. Calculate: Beginning Balance + Total Credits - Total Debits = Ending Balance
2. If reconciliation fails, review transaction assignments
3. Check for duplicate transactions across accounts
4. Verify total withdrawals match statement categories:
   - Checks Paid
   - ATM & Debit Card Withdrawals  
   - Electronic Withdrawals

### Step 4: Create Separate Files

Create individual files for each account:
- `chase_2084_2025-MM_transactions.csv`
- `chase_1873_2025-MM_transactions.csv`
- `chase_8619_2025-MM_transactions.csv`

## Transaction Type Mapping

| Chase Transaction | Our Type | Notes |
|------------------|----------|-------|
| Deposit | Deposit | Credits to account |
| Electronic Deposit | Credit | Credits to account |
| ATM Withdrawal | Withdrawal | Debits from account |
| Debit Card Purchase | Debit | Card purchases |
| Check Paid | Check | Physical checks |
| Electronic Withdrawal | Withdrawal | ACH/Wire |
| Service Fee | Fee | Monthly fees |
| Interest Payment | Interest | Interest earned |
| Online Transfer From | Deposit | Money coming in |
| Online Transfer To | Transfer | Money going out |
| Online Payment | Payment | Bill payments |
| Venmo Payment | Withdrawal | P2P payments |
| Recurring Card Purchase | Debit | Subscriptions |

## Reconciliation Formula

For each account:
```
Beginning Balance
+ Deposits and Additions (sum of positive amounts)
- Checks Paid (sum of checks)
- ATM & Debit Card Withdrawals (sum of card transactions)
- Electronic Withdrawals (sum of other withdrawals)
= Ending Balance
```

## Example Reconciliation Check

Account 1873 February 2025:
- Beginning: $16,087.31
- Deposits: $0.09 (interest only)
- Checks: -$280.00
- Card Withdrawals: -$4,496.80
- Electronic: -$10,782.38
- Ending: $528.22 ✓

## Red Flags That Indicate Extraction Errors

1. Reconciliation difference of exactly common amounts ($150, $250, $3200, etc.)
2. Same transaction appearing in multiple accounts
3. Online payments from account 1873 (usually from 2084)
4. Card 0885 transactions in account 1873
5. Card 0665 transactions in account 2084

## Output Structure

```
accounts/
├── Chase 2084/
│   └── 2025/
│       └── monthly/
│           └── chase_2084_2025-MM_transactions.csv
├── Chase 1873/
│   └── 2025/
│       └── monthly/
│           └── chase_1873_2025-MM_transactions.csv
└── Chase 8619/
    └── 2025/
        └── monthly/
            └── chase_8619_2025-MM_transactions.csv
```