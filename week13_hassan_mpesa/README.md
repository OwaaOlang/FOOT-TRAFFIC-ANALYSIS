# Hassan - Mpesa Revenue Analysis

## Question
How has Hassan's Mpesa revenue changed from Jan to Aug 2024?

## Files
- `week13_hassan_mpesa.py` - Main analysis script
- `revenue_trend.png` - Revenue trend chart
- `loan_amounts_histogram.png` - Distribution of loan amounts

## What I Did
1. Loaded Mpesa revenue data with pandas
2. Calculated month-over-month growth % with `pct_change()`
3. Calculated 3-month rolling average with `rolling(3).mean()` to smooth seasonal spikes
4. Plotted revenue trend and loan amounts histogram

## Key Findings
- **Total 8-month revenue:** KES 1,502,000
- **Best month:** August 2024 - KES 234,000
- **Worst month:** January 2024 - KES 145,000
- **Overall growth (Jan-Aug):** 61.4%

Revenue grew strongly from January to August, with August as the clear peak.

## Tools
Python, pandas, matplotlib
