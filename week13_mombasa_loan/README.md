# Mombasa Microfinance - Loan Repayment Analysis

**Objective:** Help board understand typical loan size, unusual loans, and link between loan size and repayment time.

**Dataset:** 150 fictional loans - columns: loan_id, amount_kes, days_to_first_repayment, county (Mombasa, Kwale, Kilifi)

**Key Findings:**
- Typical loan: Median 44,470 KES, Mean 47,326 KES, Std 33,048 KES
- Outliers (IQR method, 7 loans): LOAN_006 (250k), LOAN_023 (310k), LOAN_089 (180k) are unusually large; LOAN_102 (5k) and LOAN_134 (4.5k) unusually small. Flagged for board review.
- Correlation: 0.848 between loan amount and days to first repayment.

**In plain language for board:** The bigger the loan, the longer customers take to start repaying. Customers with large loans need more follow-up time.

**Files:** mombasa_loans.csv, histogram plot
