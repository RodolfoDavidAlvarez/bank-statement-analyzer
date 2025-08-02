# Bank Statement Analyzer

A comprehensive system for extracting and organizing transaction data from bank statements for multiple accounts across different banks.

## Project Overview

This project automates the extraction of transaction data from PDF bank statements into standardized CSV format, organizing data by account and year for easy access and analysis.

### Key Features
- Multi-account support (Discover, Chase, etc.)
- Year-based organization
- Automated PDF transaction extraction
- Standardized CSV output format
- Consolidated annual reports
- Pre-compiled data for quick access

## Directory Structure

```
bank-statement-analyzer/
├── README.md                          # This file
├── INSTRUCTIONS.md                    # Core extraction requirements
├── PROJECT_MEMORY.md                  # Claude AI project context
├── docs/                             # Documentation
│   ├── EXTRACTION_METHODOLOGY.md     # Detailed extraction process
│   ├── DISCOVER_GUIDE.md            # Discover-specific instructions
│   ├── CHASE_GUIDE.md               # Chase-specific instructions
│   └── LESSONS_LEARNED.md           # Best practices and pitfalls
├── accounts/                         # All account data organized here
│   ├── Discover 1342/               # Discover account ending in 1342
│   │   ├── 2025/                    # Year folder
│   │   │   ├── monthly/             # Individual monthly CSV files
│   │   │   └── consolidated/        # Annual consolidated file
│   │   └── extracted_precompiled/   # Ready-to-use consolidated files
│   └── Chase 5036/                  # Chase account ending in 5036
│       ├── 2025/
│       │   ├── monthly/
│       │   └── consolidated/
│       └── extracted_precompiled/
└── archive/                         # Original working files
```

## Account Structure

Each account follows this organization:
- **Account Folder**: Named as "Bank Name + Last 4" (e.g., "Discover 1342")
- **Year Folders**: Contains all data for that year
- **Monthly**: Individual statement extractions
- **Consolidated**: Combined annual file
- **Extracted Precompiled**: Ready-to-use files for quick access

## Output Format

All CSV files follow this standard format:
- **Description**: Merchant name (clean, no categories)
- **Amount**: 
  - Discover/Credit Cards: Positive for purchases/fees, negative for payments/credits
  - Chase Checking: Positive for deposits/credits, negative for withdrawals/payments
- **Transaction Date**: YYYY-MM-DD format
- **Transaction Type**: Purchase, Payment, Credit, Interest, Deposit, Withdrawal, etc.
- **Status**: "New" for all transactions
- **Statement id**: "YYYY-MM - Bank 0000" format
- **Bank and last 4**: e.g., "Discover 1342"

## Extraction Methods

### Available Extractors
- **`extract_chase_robust.py`**: Handles Chase multi-account PDFs (2084, 1873, 8619)
  - Usage: `python3 extract_chase_robust.py statement.pdf [account]`
- **`extract_discover_enhanced.py`**: Handles Discover credit card statements
  - Usage: `python3 extract_discover_enhanced.py statement.pdf`

### File Naming Convention
Simplified naming without redundant "transactions" word:
- Initial extraction: `chase_1873_2025-03.csv`
- Re-extractions: `[v1]chase_1873_2025-03.csv`, `[v2]chase_1873_2025-03.csv`
- Validated files: `[VALIDATED]chase_1873_2025-03.csv`

Version/status indicators appear as prefixes for easy visibility.

## Quick Start

1. Navigate to the desired account folder (e.g., `accounts/Discover 1342/`)
2. For current data, check `extracted_precompiled/`
3. For specific months, see `YYYY/monthly/`
4. For annual summaries, see `YYYY/consolidated/`

## Adding New Accounts

To add a new account:
1. Create folder: `accounts/[Bank Name] [Last 4]/`
2. Add year folder: `accounts/[Bank Name] [Last 4]/YYYY/`
3. Create subfolders: `monthly/` and `consolidated/`
4. Create `extracted_precompiled/` for ready-to-use files

## Currently Supported Accounts

### Active
- **Discover 1342**: Credit card, 2025 data extracted and organized
- **Chase 2084**: Premier Plus Checking, 2025 data validated
- **Chase 1873**: Premier Plus Checking (Business), 2025 data validated  
- **Chase 8619**: Total Checking, 2025 data validated

### Prepared (Awaiting Different Method)
- **Chase 5036**: Credit card, requires separate extraction method

## Contact

For questions or issues, please refer to the documentation in the `docs/` folder.