# Bank Statement Extraction Methods

This document describes the specific extraction methods for different bank statement types. Each bank has unique formatting that requires tailored extraction logic.

## 1. Discover Credit Card Method

**File**: `extract_discover_enhanced.py`

**Characteristics**:
- Single account per PDF
- Clear transaction table format
- Interest charges in separate "Fees and Interest Charged" section

**Key Features**:
- Extracts main transactions from table
- Separately extracts interest charges from fees section
- Handles multi-line merchant descriptions
- Cleans category text from descriptions

**Amount Signs**:
- Purchases/Fees: Positive (+)
- Payments/Credits: Negative (-)

**Usage**:
```bash
python3 extract_discover_enhanced.py statement.pdf
```

## 2. Chase Multi-Account Checking Method

**File**: `extract_chase_robust.py`

**Characteristics**:
- Multiple accounts (2084, 1873, 8619) in single PDF
- Statement periods span month boundaries (e.g., Feb 8 - Mar 7)
- Account numbers appear in headers (must be ignored)
- Complex page layouts with shared pages

**Key Features**:
- Identifies account sections using CHECKING SUMMARY only
- Handles transactions split across pages
- Captures deposits without balance on same line
- Extracts Monthly Service Fee from end of statement
- Special handling for Interest Payment (typically $0.05)
- Fixes reversal transaction amounts

**Amount Signs**:
- Deposits/Credits: Positive (+)
- Withdrawals/Payments: Negative (-)

**Critical Issues Solved**:
1. **Header Account Numbers**: Only looks in CHECKING SUMMARY section
2. **Date Handling**: Uses actual transaction date, not statement month
3. **Interest Payment**: Often shows balance instead of amount
4. **Reversals**: May have corrupted amounts in PDF

**Usage**:
```bash
python3 extract_chase_robust.py statement.pdf [account_number]
# Example: python3 extract_chase_robust.py march.pdf 1873
```

## 3. Chase Credit Card Method (Chase 5036)

**Status**: Not yet implemented
**Notes**: Different format from checking accounts, requires separate method

## 4. Wells Fargo Method

**Status**: To be developed as needed

## Common Extraction Challenges

### 1. Multi-Line Transactions
Some transactions span multiple lines in the PDF. The extraction must:
- Detect incomplete transactions
- Combine description parts
- Extract amount from the correct line

### 2. Page Boundaries
Transactions can be split across pages:
- Description on one page, amount on next
- Account sections spanning multiple pages
- Shared pages between accounts

### 3. Special Transactions
- **Interest Payments**: Often very small amounts (<$1.00)
- **Service Fees**: May appear inline with balance
- **Reversals**: Credit for previously charged amount
- **Transfers**: Between accounts in same statement

### 4. Date Handling
- Chase statements span month boundaries
- Must use actual transaction date, not statement date
- Handle year transitions for December/January

## Testing Extraction Methods

Always verify:
1. Transaction count matches expected
2. Credits and debits sum correctly
3. Net change matches statement summary
4. All special transactions captured
5. Dates are in correct YYYY-MM-DD format

## Adding New Extraction Methods

When creating a new extraction method:
1. Analyze PDF structure thoroughly
2. Identify unique patterns for the bank
3. Handle all edge cases found
4. Test on multiple months
5. Document specific quirks and solutions