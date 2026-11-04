import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate 18 months daily data with seasonal variation
np.random.seed(42)
dates = pd.date_range(start='2023-05-01', end='2024-10-31', freq='D')

# Seasonal: Dec high, Feb low
month = dates.month
seasonal = np.where(month==12, 1.35, np.where(month==11, 1.15, 
           np.where(month==2, 0.75, np.where(month==1, 0.85, 1.0))))

trend = np.linspace(0, 80, len(dates)) # genuine growth
noise = np.random.normal(0, 25, len(dates))
daily_tx = (300 + trend) * seasonal + noise

df = pd.DataFrame({'transactions': daily_tx.astype(int)}, index=dates)

# Step 2: Monthly totals + 30-day rolling
df_monthly = df.resample('ME').sum()
df['rolling_30d'] = df['transactions'].rolling(30).mean()

# Step 3: Plot bars + rolling line
fig, ax = plt.subplots(figsize=(12,6))
ax.bar(df_monthly.index, df_monthly['transactions'], width=20, alpha=0.7, label='Monthly Total', color='#2E75B6')

ax2 = ax.twinx()
ax2.plot(df.index, df['rolling_30d'], color='#C00000', linewidth=2, label='30-Day Rolling Avg')

ax.set_title('Nairobi Supermarket: Foot Traffic Trend (May 2023 - Oct 2024)')
ax.set_ylabel('Monthly Total Transactions')
ax2.set_ylabel('Daily Avg (30-day rolling)')
ax.legend(loc='upper left'); ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('nairobi_foot_traffic.png', dpi=200)