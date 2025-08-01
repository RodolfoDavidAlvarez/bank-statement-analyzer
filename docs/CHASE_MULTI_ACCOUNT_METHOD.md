# Chase Multi-Account Statement Extraction Method

## Applicable Accounts

**This method applies specifically to:**
- Chase Premier Plus Checking (2084)
- Chase Premier Plus Checking (1873)  
- Chase Total Checking (8619)

**Note:** Other Chase accounts (e.g., Chase 5036) may use a different statement format and require a separate extraction method.

## Overview

These specific Chase checking accounts are provided in a consolidated statement format where multiple accounts appear in a single PDF. Each account must be extracted separately while maintaining our standard CSV format.

## Statement Structure

### 1. Multi-Account Format
- Single PDF contains all 3 checking accounts
- Each account has its own section
- Accounts are clearly separated by pages
- Consolidated balance summary on page 1

### 2. Account Types in This Format
- Chase Premier Plus Checking (2084) - Personal checking
- Chase Premier Plus Checking (1873) - Business checking
- Chase Total Checking (8619) - Secondary checking

## Extraction Method

### Step 1: Identify Account Sections
1. Parse consolidated summary on page 1
2. Locate each account's section start
3. Note account numbers and types

### Step 2: Extract Per Account

For each account, extract:

#### Transaction Information
- **Date**: Convert MM/DD to YYYY-MM-DD (add year 2024 or 2025 based on context)
- **Description**: Full transaction description
- **Amount**: 
  - Deposits/Interest: Positive (credits to account)
  - Withdrawals/Fees/Payments: Negative (debits from account)
- **Transaction Type**: Map Chase types to our standard:
  - Deposits → "Payment"
  - Withdrawals → "Purchase"
  - Interest → "Credit"
  - Fees → "Purchase"
  - Checks → "Purchase"

#### Special Handling

1. **Checks**: Include check number in description
2. **Electronic Transfers**: Keep full description with confirmation numbers
3. **Card Transactions**: Include last 4 of card if shown
4. **Service Fees**: Treat as purchases
5. **Interest Earned**: Treat as credits (negative amount)

### Step 3: Create Separate Files

Create individual files for each account:
- `chase_2084_2025-01_transactions.csv`
- `chase_1873_2025-01_transactions.csv`
- `chase_8619_2025-01_transactions.csv`

### Step 4: Statement ID Format
- Format: "2025-01 - Chase 2084"
- One statement ID per account, not per PDF

## CSV Mapping

| Chase Field | Our CSV Field | Notes |
|------------|---------------|-------|
| Date (MM/DD) | Transaction Date | Convert to YYYY-MM-DD |
| Description | Description | Full text, clean formatting |
| Deposit Amount | Amount (positive) | Deposits are credits to account |
| Withdrawal Amount | Amount (negative) | Withdrawals are debits from account |
| N/A | Transaction Type | Derive from transaction |
| N/A | Status | Always "New" |
| N/A | Statement id | "YYYY-MM - Chase XXXX" |
| Account ending | Bank and last 4 | "Chase 2084" |

## Transaction Type Mapping

| Chase Transaction | Our Type |
|------------------|----------|
| Deposit | Payment |
| Electronic Deposit | Payment |
| ATM Withdrawal | Purchase |
| Debit Card Purchase | Purchase |
| Check Paid | Purchase |
| Electronic Withdrawal | Purchase |
| Service Fee | Purchase |
| Interest Payment | Credit |
| Online Transfer From | Payment |
| Online Transfer To | Purchase |

## Validation Points

1. Beginning balance + deposits - withdrawals = ending balance
2. All transactions within statement period
3. No missing fees or interest
4. Check numbers sequential (if applicable)

## Output Structure

```
accounts/
├── Chase 2084/
│   └── 2025/
│       └── monthly/
│           └── chase_2084_2025-01_transactions.csv
├── Chase 1873/
│   └── 2025/
│       └── monthly/
│           └── chase_1873_2025-01_transactions.csv
└── Chase 8619/
    └── 2025/
        └── monthly/
            └── chase_8619_2025-01_transactions.csv
```