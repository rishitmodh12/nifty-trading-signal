"""
NIFTY Trading Signal - Data Preparation Script
Merges all CSV parts and prepares data for ML model
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("📊 NIFTY TRADING SIGNAL - DATA PREPARATION")
print("=" * 70)

# Step 1: Load and merge all CSV files
print("\n[1/6] Loading CSV files...")
dfs = []
for i in range(1, 7):
    print(f"   Loading NIFTY_part_{i}.csv...")
    df = pd.read_csv(f'NIFTY_part_{i}.csv')
    dfs.append(df)
    print(f"   ✓ Part {i}: {len(df):,} rows")

print(f"\n[2/6] Merging all parts...")
df_full = pd.concat(dfs, ignore_index=True)
print(f"   ✓ Total rows: {len(df_full):,}")

# Step 2: Clean and prepare data
print(f"\n[3/6] Cleaning data...")

# Fix date format (remove ="..." formatting)
df_full['date'] = df_full['date'].str.replace('="', '').str.replace('"', '')

# Convert to datetime
df_full['datetime'] = pd.to_datetime(df_full['date'] + ' ' + df_full['time'], 
                                      format='%d-%m-%y %H:%M:%S')

# Sort by datetime
df_full = df_full.sort_values('datetime').reset_index(drop=True)

print(f"   ✓ Date range: {df_full['datetime'].min()} to {df_full['datetime'].max()}")

# Step 3: Focus on spot price data (our main target)
print(f"\n[4/6] Preparing spot price dataset...")

# For NIFTY index prediction, we'll use the spot price
# Aggregate minute data to daily data for easier prediction
df_daily = df_full.groupby(df_full['datetime'].dt.date).agg({
    'spot': ['first', 'max', 'min', 'last'],  # OHLC for spot
    'volume': 'sum',
    'oi': 'last',
    'iv': 'mean'
}).reset_index()

# Flatten column names
df_daily.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'oi', 'iv']
df_daily['date'] = pd.to_datetime(df_daily['date'])

print(f"   ✓ Daily data points: {len(df_daily)}")
print(f"   ✓ Columns: {df_daily.columns.tolist()}")

# Step 4: Remove any rows with missing values
print(f"\n[5/6] Checking data quality...")
print(f"   Missing values:\n{df_daily.isnull().sum()}")

df_daily = df_daily.dropna()
print(f"   ✓ Clean rows: {len(df_daily)}")

# Step 5: Save processed data
print(f"\n[6/6] Saving processed data...")
df_daily.to_csv('nifty_daily_clean.csv', index=False)
print(f"   ✓ Saved: nifty_daily_clean.csv")

# Display summary
print("\n" + "=" * 70)
print("📊 DATA PREPARATION COMPLETE")
print("=" * 70)
print(f"\nDaily Data Summary:")
print(df_daily.describe())

print(f"\n✅ First 5 days:")
print(df_daily.head())

print(f"\n✅ Last 5 days:")
print(df_daily.tail())

print("\n" + "=" * 70)
print("✅ Ready for Feature Engineering!")
print("=" * 70)
