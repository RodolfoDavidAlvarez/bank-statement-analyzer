# Chase Multi-Account Statement Extraction Method

## Applicable Accounts

**This method applies specifically to:**
- Chase Premier Plus Checking (2084)
- Chase Premier Plus Checking (1873)  
- Chase Total Checking (8619)

**Note:** Other Chase accounts (e.g., Chase 5036) may use a different statement format and require a separate extraction method.

## CRITICAL: Understanding Multi-Account PDF Structure

### Key Discovery
**IGNORE the "Primary Account" shown in page headers** - it always shows account 2084 regardless of which account's transactions are on that page.

### How to Identify Account Sections

1. **Look for CHECKING SUMMARY sections** - Each account starts with its own CHECKING SUMMARY that shows:
   - Beginning Balance
   - Ending Balance
   - Account Number (may be embedded in text)

2. **Look for (continued) markers** - Pages marked "TRANSACTION DETAIL (continued)" belong to the previous account

3. **Account order is typically**:
   - Account 2084 (Personal Premier Plus Checking)
   - Account 1873 (Business Premier Plus Checking)
   - Account 8619 (Total Checking)

### Page Structure Pattern

**Example from actual statements:**

January 2025 Statement:
- Page 2: Account 2084 (complete with CHECKING SUMMARY)
- Page 3: Account 1873 starts (CHECKING SUMMARY shows Beginning: $4,584.13)
- Page 4: Account 1873 (continued)
- Page 5: Account 1873 (continued) ends with balance $16,087.31
- Page 6: Account 8619 starts

February 2025 Statement:
- Page 2: Account 2084 (complete with CHECKING SUMMARY)
- Page 3: Account 1873 starts (CHECKING SUMMARY shows Beginning: $16,087.31)
- Page 4: Account 1873 (continued)
- Page 5: Account 1873 (continued) ends with balance $528.22, then Account 8619 starts

## Extraction Rules

### Rule 1: Start of Account Section
When you see a CHECKING SUMMARY with:
- Beginning Balance
- Ending Balance
- Deposits and Additions
- Various withdrawal categories

This marks the START of a new account section.

### Rule 2: Continuation Pages
Pages with "TRANSACTION DETAIL (continued)" at the top belong to the account that started on the previous page(s).

### Rule 3: End of Account Section
An account section ends when:
- You see a new CHECKING SUMMARY (start of next account)
- You reach the ending balance shown in that account's CHECKING SUMMARY
- The next account type appears (e.g., "CHASE TOTAL CHECKING")

### Rule 4: Transaction Ownership
To determine which account a transaction belongs to:

1. **Position in PDF**: Which account section is the transaction in?
2. **Card Numbers** (confirmation):
   - Card 0885 = Account 2084
   - Card 0665 = Account 1873
   - No card = Could be any account, use position
3. **DO NOT use transaction type** to determine account ownership

## Common Extraction Errors to Avoid

### Error 1: Using Page Headers
**WRONG**: "This page header says Primary Account 2084, so these transactions belong to 2084"
**RIGHT**: Ignore headers, use CHECKING SUMMARY sections to identify accounts

### Error 2: Assuming Transaction Types Determine Account
**WRONG**: "Online Payments always come from account 2084"
**RIGHT**: Transactions belong to whichever account section they appear in

### Error 3: Not Following (continued) Pages
**WRONG**: "New page, might be new account"
**RIGHT**: If page says "(continued)", it's still the same account

## Validation Process

### DO NOT Force Reconciliation
**IMPORTANT**: Extract exactly what's in each account section. Do not move transactions between accounts to make balances reconcile.

### Verification Steps
1. Count pages for each account section
2. Verify the section includes all (continued) pages
3. Extract ALL transactions in that section
4. Record the total but DO NOT adjust if it doesn't reconcile

### If Balances Don't Reconcile
- Double-check you included all (continued) pages
- Verify you started and ended at the right places
- Document the discrepancy but DO NOT move transactions

## Example Extraction Process

For February 2025 statement:
1. Page 2: Found CHECKING SUMMARY → This is account 2084
2. Page 3: Found CHECKING SUMMARY with Beginning Balance $16,087.31 → This is account 1873
3. Page 4: Says "(continued)" → Still account 1873
4. Page 5: Says "(continued)" → Still account 1873 until we see "CHASE TOTAL CHECKING"
5. Page 5 (bottom): Found "CHASE TOTAL CHECKING" → Account 8619 starts here

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