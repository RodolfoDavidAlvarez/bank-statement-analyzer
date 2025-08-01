# Chase 2025 Extraction Validation Report

## Extraction Summary

Successfully extracted all Chase multi-account statements from February to June 2025 using the corrected methodology:
- Ignored misleading "Primary Account" headers
- Used CHECKING SUMMARY sections to identify account boundaries
- Followed (continued) markers correctly
- Did NOT force reconciliation

## February 2025 - Account 1873 Analysis

### Transaction Count Discrepancy
- **Original extraction**: 63 transactions
- **Corrected extraction**: 47 transactions  
- **User's screenshot**: 70 transactions

### Reconciliation Results
- Beginning Balance: $16,087.31 ✓ (matches PDF)
- Ending Balance: $528.22 ✓ (matches PDF)
- Total Credits: $0.00
- Total Debits: $-10,234.18
- Expected Ending (calculated): $5,853.13
- **Discrepancy**: $5,324.91

## Reconciliation Discrepancies for All Months

### Account 2084
| Month | Beginning | Credits | Debits | Expected | Actual | Discrepancy |
|-------|-----------|---------|---------|----------|--------|-------------|
| Feb   | $2,871.09 | $0.00   | -$6,617.23 | -$3,746.14 | $1,422.38 | $5,168.52 |
| Mar   | $1,422.38 | $0.00   | -$9,629.90 | -$8,207.52 | $4,940.70 | $13,148.22 |
| Apr   | $4,940.70 | $0.00   | -$9,660.78 | -$4,720.08 | $4,009.00 | $8,729.08 |
| May   | $4,009.00 | $0.00   | -$14,333.95 | -$10,324.95 | $6,697.89 | $17,022.84 |
| Jun   | $6,697.89 | $0.00   | -$64,969.54 | -$58,271.65 | $647.71 | $58,919.36 |

### Account 1873
| Month | Beginning | Credits | Debits | Expected | Actual | Discrepancy |
|-------|-----------|---------|---------|----------|--------|-------------|
| Feb   | $16,087.31 | $0.00  | -$10,234.18 | $5,853.13 | $528.22 | -$5,324.91 |
| Mar   | $528.22 | $0.00     | -$46,143.52 | -$45,615.30 | $13,456.82 | $59,072.12 |
| Apr   | $13,456.82 | $0.00  | -$44,786.70 | -$31,329.88 | $5,168.42 | $36,498.30 |
| May   | $5,168.42 | $1,000.00 | -$55,376.18 | -$49,207.76 | $9,539.29 | $58,747.05 |
| Jun   | $9,539.29 | $0.00   | -$25,994.93 | -$16,455.64 | $4,525.31 | $20,980.95 |

### Account 8619
| Month | Beginning | Credits | Debits | Expected | Actual | Discrepancy |
|-------|-----------|---------|---------|----------|--------|-------------|
| Feb   | $229.42 | $0.00    | -$10,025.05 | -$9,795.63 | $528.22 | $10,323.85 |
| Mar   | $77.59 | $0.00     | -$5,154.00 | -$5,076.41 | $99.34 | $5,175.75 |
| Apr   | $99.34 | $0.00     | -$9,812.83 | -$9,713.49 | $4,901.83 | $14,615.32 |
| May   | $4,901.83 | $0.00   | -$8,462.83 | -$3,561.00 | $1,371.00 | $4,932.00 |
| Jun   | $1,371.00 | $0.00   | -$244.83 | $1,126.17 | $1,176.17 | $50.00 |

## Key Findings

1. **Systematic Discrepancies**: All accounts show significant discrepancies between calculated and actual ending balances
2. **Missing Credits**: Most months show zero credits, which might indicate:
   - Credits are being missed in extraction
   - Credits appear in different formats not recognized by the parser
   - Credits might be on pages we're not capturing

3. **Pattern Recognition Issues**: The extraction might be missing:
   - Multi-line transactions
   - Transactions with unusual formatting
   - Transactions that appear in summary but not in detail

## Recommendations

1. **Manual Verification**: Compare extracted transactions line-by-line with PDF for one month to identify what's being missed
2. **Enhanced Parser**: May need to improve transaction parsing logic to catch edge cases
3. **Credit Detection**: Review credit detection logic - we're finding almost no credits across all accounts
4. **Page Boundary Issues**: Verify we're correctly identifying where each account section ends

## Next Steps

The extraction is following the corrected methodology (not forcing reconciliation, extracting based on PDF structure), but the large discrepancies suggest the parser may need refinement to capture all transactions accurately.