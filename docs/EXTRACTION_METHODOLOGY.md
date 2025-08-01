# Bank Statement Extraction Methodology

## Overview

This document describes the complete methodology for extracting transaction data from bank statement PDFs into standardized CSV format.

## Core Principles

1. **Direct PDF Analysis**: We analyze PDFs directly without relying on pre-existing tools
2. **Accuracy First**: Every transaction must be captured, including interest charges
3. **Standardized Output**: Consistent CSV format across all statement types
4. **Verification**: Always verify line counts and totals

## Extraction Process

### Step 1: Statement Analysis
1. Identify statement period and account details
2. Locate transaction sections
3. Find "Fees and Interest Charged" section (CRITICAL)
4. Note any special transaction types

### Step 2: Data Extraction
1. Extract all regular transactions from main section
2. **IMPORTANT**: Extract interest charges from "Fees and Interest Charged" section
3. Capture all payment transactions
4. Include any credits or adjustments

### Step 3: Data Formatting

#### Amount Formatting Rules
- **Positive amounts**: Purchases, interest charges, fees
- **Negative amounts**: Payments, credits, cashback redemptions
- Always use 2 decimal places (e.g., 81.00 not 81.0)

#### Date Formatting
- Use YYYY-MM-DD format consistently
- Convert from MM/DD/YYYY if needed

#### Description Cleaning
- Remove category text (e.g., "Services", "Merchandise")
- Keep merchant name only
- Preserve original merchant formatting

#### Statement ID Format
- Format: "YYYY-MM - Bank 0000"
- Example: "2025-01 - Discover 1342"

### Step 4: CSV Generation

Standard columns (in order):
1. Description
2. Amount
3. Transaction Date
4. Transaction Type
5. Status
6. Statement id
7. Bank and last 4

### Step 5: Consolidation

1. Create individual monthly CSV files
2. Combine into annual consolidated file
3. Verify total transaction count
4. Check for proper line breaks between files

## Common Pitfalls to Avoid

1. **Missing Interest Charges**: Always check "Fees and Interest Charged" section
2. **Incorrect Line Breaks**: When concatenating files, ensure proper newlines
3. **Decimal Formatting**: Always use .00 format
4. **Category Text**: Remove "Services", "Merchandise" etc. from descriptions
5. **Status Field**: Some extractions may use "Posted" instead of "New"

## Verification Checklist

- [ ] All transactions from main section extracted
- [ ] Interest charges from fees section included
- [ ] Dates in YYYY-MM-DD format
- [ ] Amounts have correct signs (+/-)
- [ ] Descriptions are clean (no categories)
- [ ] Line count matches expected total
- [ ] No merged lines in consolidated file

## Multi-Agent Processing

For efficiency, use multiple agents to process statements in parallel:
- Agent 1: January statement
- Agent 2: February statement
- etc.

Then consolidate results into single annual file.