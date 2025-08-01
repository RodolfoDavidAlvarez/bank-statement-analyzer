#!/usr/bin/env python3
"""
Extract all remaining Chase 1873 statements (March-June 2025) using the robust extractor.
"""

from extract_chase_robust import ChaseRobustExtractor
from pathlib import Path

def main():
    """Extract March through June 2025 statements for Chase 1873."""
    
    # Base directory where PDFs are located
    base_dir = Path("/Users/rodolfoalvarez/Documents/Better Systems AI/Nancy Bennet  - Bank Staments Automation/Client Items/Taxes/Taxes 2025 (Inprogress)/Bank Statment NB Business Acct 1873")
    
    # Statement files to process (March through June)
    statement_files = {
        3: "20250307-statements-1873-.pdf",
        4: "20250407-statements-1873-.pdf", 
        5: "20250507-statements-1873-.pdf",
        6: "20250606-statements-1873-.pdf"
    }
    
    print("Extracting remaining Chase 1873 statements (March-June 2025)")
    print("Using robust extraction method that handles all edge cases")
    print("=" * 70)
    
    results = {}
    
    for month, filename in statement_files.items():
        pdf_path = base_dir / filename
        
        if not pdf_path.exists():
            print(f"\nWarning: {filename} not found")
            continue
            
        print(f"\n{'='*70}")
        print(f"Processing {filename} (Month {month}/2025)")
        print(f"{'='*70}")
        
        try:
            extractor = ChaseRobustExtractor(str(pdf_path))
            extractor.extract_all_accounts()
            
            # Save only account 1873
            output_path = extractor.save_transactions('1873')
            
            # Store results
            if '1873' in extractor.account_sections:
                info = extractor.account_sections['1873']
                total_credits = sum(t['amount'] for t in info['transactions'] if t['amount'] > 0)
                total_debits = sum(t['amount'] for t in info['transactions'] if t['amount'] < 0)
                net_change = total_credits + total_debits
                expected_ending = info['beginning_balance'] + net_change
                
                results[month] = {
                    'filename': filename,
                    'transactions': len(info['transactions']),
                    'beginning': info['beginning_balance'],
                    'ending': info['ending_balance'],
                    'credits': total_credits,
                    'debits': total_debits,
                    'net_change': net_change,
                    'expected_ending': expected_ending,
                    'reconciles': abs(expected_ending - info['ending_balance']) < 0.01
                }
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    # Summary report
    print(f"\n\n{'='*70}")
    print("EXTRACTION SUMMARY - Chase 1873")
    print(f"{'='*70}")
    
    all_reconcile = True
    
    for month in sorted(results.keys()):
        r = results[month]
        status = "✓" if r['reconciles'] else "✗"
        print(f"\nMonth {month}/2025: {status}")
        print(f"  Transactions: {r['transactions']}")
        print(f"  Beginning: ${r['beginning']:,.2f}")
        print(f"  Credits: ${r['credits']:,.2f}")
        print(f"  Debits: ${r['debits']:,.2f}")
        print(f"  Net Change: ${r['net_change']:,.2f}")
        print(f"  Expected Ending: ${r['expected_ending']:,.2f}")
        print(f"  Actual Ending: ${r['ending']:,.2f}")
        if not r['reconciles']:
            diff = abs(r['expected_ending'] - r['ending'])
            print(f"  Difference: ${diff:,.2f}")
            all_reconcile = False
            
    print(f"\n{'='*70}")
    if all_reconcile:
        print("✓ ALL MONTHS RECONCILE PERFECTLY!")
    else:
        print("✗ Some months need review")
        
    # Also check balance continuity
    print(f"\n{'='*70}")
    print("BALANCE CONTINUITY CHECK")
    print(f"{'='*70}")
    
    # February ending should equal March beginning
    feb_ending = 528.22  # From our successful February extraction
    if 3 in results:
        mar_beginning = results[3]['beginning']
        if abs(feb_ending - mar_beginning) < 0.01:
            print(f"✓ Feb ending (${feb_ending:,.2f}) = Mar beginning (${mar_beginning:,.2f})")
        else:
            print(f"✗ Feb ending (${feb_ending:,.2f}) ≠ Mar beginning (${mar_beginning:,.2f})")
            
    # Check month-to-month continuity
    months = sorted(results.keys())
    for i in range(len(months) - 1):
        curr_month = months[i]
        next_month = months[i + 1]
        
        curr_ending = results[curr_month]['ending']
        next_beginning = results[next_month]['beginning']
        
        if abs(curr_ending - next_beginning) < 0.01:
            print(f"✓ Month {curr_month} ending (${curr_ending:,.2f}) = Month {next_month} beginning (${next_beginning:,.2f})")
        else:
            print(f"✗ Month {curr_month} ending (${curr_ending:,.2f}) ≠ Month {next_month} beginning (${next_beginning:,.2f})")

if __name__ == "__main__":
    main()