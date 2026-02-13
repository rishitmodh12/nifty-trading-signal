"""
NIFTY Trading Signal - Feature Engineering
Creates technical indicators and prepares features for ML
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🔧 FEATURE ENGINEERING")
print("=" * 70)

# Load cleaned data
df = pd.read_csv('nifty_daily_clean.csv')
df['date'] = pd.to_datetime(df['date'])
print(f"\n✓ Loaded {len(df)} days of data")

# Create a copy for features
data = df.copy()

print("\n[1/5] Creating Technical Indicators...")

# 1. Simple Moving Averages
data['SMA_5'] = data['close'].rolling(window=5).mean()
data['SMA_10'] = data['close'].rolling(window=10).mean()
data['SMA_20'] = data['close'].rolling(window=20).mean()
data['SMA_50'] = data['close'].rolling(window=50).mean()

# 2. Exponential Moving Averages
data['EMA_12'] = data['close'].ewm(span=12, adjust=False).mean()
data['EMA_26'] = data['close'].ewm(span=26, adjust=False).mean()

# 3. MACD (Moving Average Convergence Divergence)
data['MACD'] = data['EMA_12'] - data['EMA_26']
data['MACD_signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
data['MACD_diff'] = data['MACD'] - data['MACD_signal']

# 4. RSI (Relative Strength Index)
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data['close'])

# 5. Bollinger Bands
data['BB_middle'] = data['close'].rolling(window=20).mean()
data['BB_std'] = data['close'].rolling(window=20).std()
data['BB_upper'] = data['BB_middle'] + (data['BB_std'] * 2)
data['BB_lower'] = data['BB_middle'] - (data['BB_std'] * 2)
data['BB_width'] = data['BB_upper'] - data['BB_lower']

# 6. Price Rate of Change
data['ROC'] = ((data['close'] - data['close'].shift(10)) / data['close'].shift(10)) * 100

# 7. Volume indicators
data['volume_sma'] = data['volume'].rolling(window=20).mean()
data['volume_ratio'] = data['volume'] / data['volume_sma']

print("   ✓ Created 20+ technical indicators")

print("\n[2/5] Creating Price-based Features...")

# Price change features
data['price_change'] = data['close'] - data['open']
data['price_change_pct'] = ((data['close'] - data['open']) / data['open']) * 100
data['high_low_diff'] = data['high'] - data['low']
data['daily_return'] = data['close'].pct_change() * 100

# Lag features (previous days)
for i in [1, 2, 3, 5, 7]:
    data[f'close_lag_{i}'] = data['close'].shift(i)
    data[f'volume_lag_{i}'] = data['volume'].shift(i)

print("   ✓ Created price-based features")

print("\n[3/5] Creating Target Variable (BUY/HOLD/SELL)...")

# Calculate next day's return
data['next_day_return'] = data['close'].shift(-1) - data['close']
data['next_day_return_pct'] = ((data['close'].shift(-1) - data['close']) / data['close']) * 100

# Create target based on thresholds
def create_signal(return_pct):
    if pd.isna(return_pct):
        return np.nan
    elif return_pct > 0.5:  # If price rises more than 0.5%
        return 'BUY'
    elif return_pct < -0.5:  # If price falls more than 0.5%
        return 'SELL'
    else:
        return 'HOLD'

data['signal'] = data['next_day_return_pct'].apply(create_signal)

# Convert to numeric for ML
signal_map = {'BUY': 2, 'HOLD': 1, 'SELL': 0}
data['target'] = data['signal'].map(signal_map)

print("   ✓ Created target variable")
print(f"\n   Signal Distribution:")
print(data['signal'].value_counts())

print("\n[4/5] Cleaning and preparing final dataset...")

# Remove rows with NaN (due to rolling windows)
data_clean = data.dropna()

print(f"   ✓ Rows after cleaning: {len(data_clean)}")

print("\n[5/5] Saving feature-engineered dataset...")

# Save full dataset with features
data_clean.to_csv('nifty_features.csv', index=False)
print("   ✓ Saved: nifty_features.csv")

# Display feature summary
print("\n" + "=" * 70)
print("✅ FEATURE ENGINEERING COMPLETE")
print("=" * 70)
print(f"\nTotal Features Created: {len(data_clean.columns)}")
print(f"Training Samples: {len(data_clean)}")
print(f"\nFeature List:")
feature_cols = [col for col in data_clean.columns if col not in ['date', 'signal', 'target', 'next_day_return', 'next_day_return_pct']]
for i, col in enumerate(feature_cols, 1):
    print(f"  {i}. {col}")

print("\n" + "=" * 70)
print("✅ Ready for Model Training!")
print("=" * 70)
