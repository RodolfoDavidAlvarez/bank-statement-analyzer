# Chase Card Statement Extraction Guide (Preparation)

## Status: In Development

This guide is being prepared based on lessons learned from Discover statement extraction. Chase statements have different formatting that will require adaptation of our methodology.

## Expected Differences from Discover

### 1. Statement Structure
- Chase may have different section layouts
- Interest and fees location may vary
- Multiple account types (Business, Personal) may appear differently

### 2. Transaction Format
- Date formats may differ
- Description formatting likely different
- Transaction categorization approach unknown

## Pre-Extraction Checklist

Before processing Chase statements, we need to:

### 1. Analyze Sample Statement
- [ ] Identify main transaction section
- [ ] Locate fees and interest section
- [ ] Note date format used
- [ ] Document amount formatting (positive/negative conventions)
- [ ] Find statement period location
- [ ] Identify account number format

### 2. Map Transaction Types
- [ ] Regular purchases
- [ ] Payments
- [ ] Credits/Returns
- [ ] Interest charges
- [ ] Fees
- [ ] Cash advances (if applicable)

### 3. Special Considerations
- [ ] Multi-page handling
- [ ] Business vs Personal account differences
- [ ] Rewards/Points sections (ignore or include?)
- [ ] Foreign transaction handling

## Proposed Extraction Approach

### Step 1: Format Analysis
1. Open sample Chase PDF
2. Document section structure
3. Note any unique identifiers
4. Compare to Discover format

### Step 2: Test Extraction
1. Extract single month manually
2. Verify all transaction types captured
3. Confirm interest/fees included
4. Validate totals

### Step 3: Standardization
1. Map Chase format to our standard CSV
2. Handle any Chase-specific fields
3. Ensure consistent output

## Required Information

To complete this guide, we need:
1. Sample Chase statement PDFs
2. Expected transaction volume
3. Account types to support
4. Any Chase-specific requirements

## Standard Output Format (Same as Discover)

```csv
Description,Amount,Transaction Date,Transaction Type,Status,Statement id,Bank and last 4
[Merchant Name],[+/-Amount],YYYY-MM-DD,[Type],New,YYYY-MM - Chase XXXX,Chase XXXX
```

## Next Steps

1. Obtain Chase statement samples
2. Complete format analysis
3. Update this guide with specific instructions
4. Test extraction process
5. Document any new lessons learned

## Notes from Discover Experience

Key things to check in Chase statements:
- Where interest charges appear (separate section?)
- How payments are labeled
- Credit/refund formatting
- Statement credit handling
- Date format consistency
- Multi-account considerations