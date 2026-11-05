import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 150 fictional loans
np.random.seed(42)
amounts = np.random.normal(45000, 15000, 150).astype(int)
amounts[5]=250000; amounts[22]=310000; amounts[88]=180000; amounts[101]=5000; amounts[133]=4500

df = pd.DataFrame({
    'loan_id': [f'LOAN_{i:03d}' for i in range(1,151)],
    'amount_kes': amounts,
    'days_to_first_repayment': (amounts/3000 + np.random.normal(20,5,150)).astype(int).clip(5,90),
    'county': np.random.choice(['Mombasa','Kwale','Kilifi'],150,p=[0.7,0.15,0.15])
})

# Statistical summary
print(df['amount_kes'].describe())

# IQR Outliers
Q1 = df['amount_kes'].quantile(0.25)
Q3 = df['amount_kes'].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
outliers = df[(df['amount_kes'] < lower) | (df['amount_kes'] > upper)]
print(f"Outliers found: {len(outliers)}")
print(outliers[['loan_id','amount_kes']])

# Correlation
corr = df['amount_kes'].corr(df['days_to_first_repayment'])
print(f"Correlation: {corr:.3f}")

# Histogram
plt.hist(df['amount_kes'], bins=20, edgecolor='black')
plt.title('Histogram of Loan Amounts')
plt.xlabel('Amount KES'); plt.ylabel('Frequency')
plt.savefig('loan_amounts_histogram.png')
plt.show()

df.to_csv('mombasa_loans.csv', index=False)
