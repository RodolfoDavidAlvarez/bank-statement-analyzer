# Discover Card Statement Extraction Guide

## Statement Structure

Discover statements have a consistent structure that makes extraction reliable:

1. **Header Section**: Account details, statement period
2. **Transaction List**: Main purchases and payments
3. **Fees and Interest Charged Section**: CRITICAL - Contains interest charges
4. **Summary Section**: Balances and totals

## Specific Extraction Steps

### 1. Locate Key Sections
- Main transaction list (usually starts after account summary)
- "Fees and Interest Charged" box (typically on page 2 or 3)
- Look for "TOTAL INTEREST FOR THIS PERIOD" line

### 2. Transaction Types

#### Purchases
- Regular merchant transactions
- Interest charges (from Fees section)
- Format: Positive amounts

#### Payments/Credits
- "PAYMENT - THANK YOU"
- "AUTOMATIC STATEMENT CREDIT"
- "CASHBACK BONUS REDEMPTION"
- Format: Negative amounts

### 3. Special Considerations

#### Interest Charges
**CRITICAL**: Interest charges appear in the "Fees and Interest Charged" section, NOT in the main transaction list.
- Look for: "INTEREST CHARGE ON PURCHASES"
- Transaction date: Usually the statement closing date
- Type: "Purchase" or "Interest Charge"

#### Statement Credits
- May appear at the beginning of the statement period
- Always negative amounts
- Type: "Credit"

## Example Transactions

```csv
Description,Amount,Transaction Date,Transaction Type,Status,Statement id,Bank and last 4
PY *SPACE SHOP STORAGE O NORTH OLMSTED,142.60,2025-01-02,Purchase,New,2025-01 - Discover 1342,Discover 1342
AUTOMATIC STATEMENT CREDIT,-4.55,2024-12-13,Credit,New,2025-01 - Discover 1342,Discover 1342
PAYMENT - THANK YOU,-250.00,2024-12-31,Payment,New,2025-01 - Discover 1342,Discover 1342
INTEREST CHARGE ON PURCHASES,161.83,2025-01-12,Purchase,New,2025-01 - Discover 1342,Discover 1342
```

## Validation Steps

1. **Transaction Count**: Verify against statement summary
2. **Interest Inclusion**: Confirm interest charges are captured
3. **Balance Check**: Starting balance - payments + purchases + interest = ending balance
4. **Date Range**: All transactions within statement period (except prior month carryovers)

## Common Patterns

- Amazon purchases: Often multiple variations (AMAZON.COM*, AMAZON PRIME*, etc.)
- Recurring charges: INTUIT, storage facilities, subscriptions
- Payment patterns: Usually 1-2 payments per month
- Interest: Appears when balance carried forward

## File Naming Convention

- Monthly: `discover_1342_2025-01_transactions.csv`
- Annual: `2025 - Discover 1342.csv`