# Claude Project Memory - Bank Statement Analyzer

## IMPORTANT: Before Starting Any Task

**ALWAYS** take a few minutes to review recent git commits to understand:
1. What has been done previously
2. The direction the project is moving
3. Any patterns or conventions established
4. Recent changes that might affect your work

Use: `git log --oneline -10` to see recent commits
Use: `git show HEAD` to see the last commit details

## Project Context

This is a bank statement extraction system that processes PDF statements from multiple bank accounts and converts them into standardized CSV format for accounting purposes.

## Key Understanding Points

### 1. Project Structure
```
accounts/
├── [Bank Name] [Last 4]/        # e.g., "Discover 1342"
│   ├── YYYY/                    # Year folders
│   │   ├── monthly/             # Individual month CSVs
│   │   └── consolidated/        # Annual summary
│   └── extracted_precompiled/   # Ready-to-use files
```

### 2. Account Naming Convention
- Always use format: "Bank Name + Space + Last 4 digits"
- Examples: "Discover 1342", "Chase 5036"
- This naming is used for folders AND in CSV data

### 3. CSV Format Requirements
```csv
Description,Amount,Transaction Date,Transaction Type,Status,Statement id,Bank and last 4
```
- **Amounts**: 
  - **Discover/Credit Cards**: Positive = purchases/fees, Negative = payments/credits
  - **Chase Checking**: Positive = deposits/credits, Negative = withdrawals/payments
- **Dates**: YYYY-MM-DD format (e.g., 2025-01-15)
- **Statement ID**: "YYYY-MM - Bank 0000" (e.g., "2025-01 - Discover 1342")
- **Status**: Always "New"

### 4. Critical Extraction Rules

#### ALWAYS Check Interest Charges
- Interest charges appear in "Fees and Interest Charged" section
- NOT in main transaction list
- Look for "INTEREST CHARGE ON PURCHASES"
- Add as positive amount with transaction type "Purchase"

#### Description Cleaning
- Remove category text (Services, Merchandise, etc.)
- Keep merchant name only
- No extra formatting

#### Multi-Statement Processing
- Use parallel agents for efficiency
- One agent per month
- Consolidate after all complete

### 5. File Organization

#### When Processing New Statements
1. Extract to: `accounts/[Bank] [Last4]/YYYY/monthly/`
2. Name format: `[bank]_[last4]_YYYY-MM_transactions.csv`
3. Create consolidated: `YYYY - [Bank] [Last4].csv`
4. Copy consolidated to `extracted_precompiled/`

### 6. Known Accounts
- **Discover 1342**: Credit card, active, 2025 data available
- **Chase 2084, 1873, 8619**: Checking accounts, multi-account PDF format, validated
- **Chase 5036**: Credit card, different format, awaiting method development

### 7. Common Mistakes to Avoid
1. Missing interest charges from fees section
2. Wrong amount signs (purchases should be positive)
3. Incorrect date format (must be YYYY-MM-DD)
4. Forgetting to clean merchant descriptions
5. Line break issues when consolidating files

### 8. When Adding New Accounts
1. Create account folder: `accounts/[Bank Name] [Last 4]/`
2. Add year structure
3. Follow same CSV format
4. Update documentation

### 9. Verification Steps
- Count transactions per file
- Verify interest charges included
- Check consolidated file line breaks
- Confirm date formatting
- Validate amount signs

## Remember
This project prioritizes accuracy and organization. Every transaction matters, especially interest charges. The folder structure by account and year makes it easy to find and manage data.