# Lessons Learned & Best Practices

## Key Discoveries

### 1. Interest Charges Are Hidden
**Problem**: Initial extractions missed interest charges because they appear in a separate "Fees and Interest Charged" section, not in the main transaction list.

**Solution**: Always check the fees section and explicitly look for "TOTAL INTEREST FOR THIS PERIOD"

**Impact**: Missing ~$150 per month in interest charges significantly affects accounting accuracy

### 2. File Concatenation Issues
**Problem**: Using shell commands to concatenate CSV files resulted in missing line breaks between files, causing transactions to merge on single lines.

**Solution**: Use proper CSV handling (Python csv module) or ensure newlines are preserved

### 3. Amount Sign Convention
**Initial Understanding**: Payments positive, purchases negative
**Corrected Convention**: Purchases positive, payments negative
**Lesson**: Always verify the client's preferred convention early

### 4. Date Format Consistency
**Evolution**: 
- Started with MM/DD/YYYY
- Changed to YYYY-MM-DD for better sorting and consistency
**Best Practice**: Establish date format requirements upfront

### 5. Description Cleaning
**Issue**: Discover adds category text like "Services" or "Merchandise" to descriptions
**Solution**: Clean descriptions to show merchant name only
**Note**: This doesn't apply to all banks - Chase may have different formatting

## Best Practices Established

### 1. Multi-Agent Processing
- Deploy multiple agents for parallel processing
- Each agent handles one month
- Consolidate results after all complete
- Significant time savings for annual processing

### 2. Verification Protocol
- Count transactions in each file
- Verify consolidated file line count
- Spot-check for interest charges
- Confirm no merged lines

### 3. Documentation First
- Create clear extraction requirements (INSTRUCTIONS.md)
- Document each bank's specific format
- Maintain extraction logs

### 4. File Organization
```
extracted_data/
└── YYYY/
    └── bank_name/
        ├── monthly/
        └── consolidated/
```

### 5. Status Field Handling
- Discover may use "Posted" or "New"
- Standardize to "New" for consistency
- Document any bank-specific variations

## Technical Insights

### PDF Processing
- Direct PDF analysis works well for Discover
- Text extraction quality varies by bank
- Always verify numeric precision

### CSV Generation
- Use proper CSV libraries when possible
- Watch for special characters in merchant names
- Preserve decimal precision (.00)

### Error Prevention
1. Always read existing files before editing
2. Create backups before bulk operations
3. Test with single month before processing all
4. Verify output format matches requirements

## Future Improvements

1. **Automated Validation**: Build checksums based on statement totals
2. **Template System**: Create bank-specific extraction templates
3. **Error Detection**: Flag missing interest charges automatically
4. **Format Detection**: Auto-detect bank type from PDF structure

## Chase Preparation Notes

Based on Discover experience, for Chase we should:
1. Map transaction sections first
2. Identify where fees/interest appear
3. Document date and amount formats
4. Test with single statement
5. Note any multi-account complexities