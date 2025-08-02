# Validation Status

This document tracks which bank statement extractions have been validated and reconciled.

## Naming Convention
- **[VALIDATED]** prefix: Extraction has been verified and reconciles correctly
- **_v[N]** suffix: Version number for extraction attempts

## Validation Status by Account

### ✅ Discover 1342 (Credit Card)
- **2025-01**: [VALIDATED] ✓
- **2025-02**: [VALIDATED] ✓
- **2025-03**: [VALIDATED] ✓
- **2025-04**: [VALIDATED] ✓
- **2025-05**: [VALIDATED] ✓
- **2025-06**: [VALIDATED] ✓

### ✅ Chase 1873 (Business Checking)
- **2025-01**: [VALIDATED] ✓
- **2025-02**: [VALIDATED] ✓
- **2025-03**: Extracted (v1) - Pending validation
- **2025-04**: Extracted - Needs re-extraction with robust method
- **2025-05**: Extracted - Needs re-extraction with robust method
- **2025-06**: Extracted - Needs re-extraction with robust method

### ⏳ Chase 2084 (Premier Plus Checking)
- **2025-01**: Extracted - Needs re-extraction with robust method
- **2025-02**: Extracted - Needs re-extraction with robust method
- **2025-03**: Extracted - Needs re-extraction with robust method
- **2025-04**: Extracted - Needs re-extraction with robust method
- **2025-05**: Extracted - Needs re-extraction with robust method
- **2025-06**: Extracted - Needs re-extraction with robust method

### ⏳ Chase 8619 (Total Checking)
- **2025-01**: Extracted - Needs re-extraction with robust method
- **2025-02**: Extracted - Needs re-extraction with robust method
- **2025-03**: Extracted - Needs re-extraction with robust method
- **2025-04**: Extracted - Needs re-extraction with robust method
- **2025-05**: Extracted - Needs re-extraction with robust method
- **2025-06**: Extracted - Needs re-extraction with robust method

### ❌ Chase 5036 (Credit Card)
- Requires different extraction method (not multi-account format)

## Summary
- **Fully Validated**: Discover 1342 (all 2025), Chase 1873 (Jan-Feb 2025)
- **Needs Work**: Chase 2084, Chase 8619 (all need robust method)
- **Not Started**: Chase 5036 (different format)

## Validation Criteria
An extraction is considered validated when:
1. All transactions are captured (verified against statement)
2. Amounts reconcile with beginning/ending balances
3. Dates are in correct format (YYYY-MM-DD)
4. Transaction types are properly categorized
5. No duplicate or missing transactions