"""
NIFTY Trading Signal - Model Training
Trains Random Forest classifier for BUY/HOLD/SELL predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🤖 MODEL TRAINING")
print("=" * 70)

# Load feature-engineered data
print("\n[1/7] Loading data...")
df = pd.read_csv('nifty_features.csv')
print(f"   ✓ Loaded {len(df)} samples")

# Select features for training
feature_cols = [
    'open', 'high', 'low', 'close', 'volume', 'oi', 'iv',
    'SMA_5', 'SMA_10', 'SMA_20', 'SMA_50',
    'EMA_12', 'EMA_26', 'MACD', 'MACD_signal', 'MACD_diff',
    'RSI', 'BB_middle', 'BB_upper', 'BB_lower', 'BB_width',
    'ROC', 'volume_ratio', 'price_change_pct', 'high_low_diff', 'daily_return',
    'close_lag_1', 'volume_lag_1', 'close_lag_2', 'volume_lag_2',
    'close_lag_3', 'volume_lag_3', 'close_lag_5', 'volume_lag_5',
    'close_lag_7', 'volume_lag_7'
]

X = df[feature_cols]
y = df['target']

print(f"   ✓ Features: {len(feature_cols)}")
print(f"   ✓ Target distribution:\n{y.value_counts()}")

# Split data
print("\n[2/7] Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"   ✓ Train samples: {len(X_train)}")
print(f"   ✓ Test samples: {len(X_test)}")

# Scale features
print("\n[3/7] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("   ✓ Features scaled")

# Train Random Forest model
print("\n[4/7] Training Random Forest model...")
print("   This may take 30-60 seconds...")

model = RandomForestClassifier(
    n_estimators=200,        # Number of trees
    max_depth=15,            # Maximum depth
    min_samples_split=5,     # Minimum samples to split
    min_samples_leaf=2,      # Minimum samples in leaf
    random_state=42,
    n_jobs=-1,               # Use all CPU cores
    class_weight='balanced'  # Handle imbalanced classes
)

model.fit(X_train_scaled, y_train)
print("   ✓ Model trained!")

# Make predictions
print("\n[5/7] Evaluating model...")
y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"   ✓ Training Accuracy: {train_accuracy*100:.2f}%")
print(f"   ✓ Testing Accuracy: {test_accuracy*100:.2f}%")

# Detailed metrics
print("\n[6/7] Classification Report:")
print("=" * 70)
target_names = ['SELL', 'HOLD', 'BUY']
print(classification_report(y_test, y_pred_test, target_names=target_names, zero_division=0))

print("\nConfusion Matrix:")
print("=" * 70)
cm = confusion_matrix(y_test, y_pred_test)
print(f"             Predicted")
print(f"             SELL  HOLD  BUY")
print(f"Actual SELL   {cm[0][0]:3d}   {cm[0][1]:3d}  {cm[0][2]:3d}")
print(f"       HOLD   {cm[1][0]:3d}   {cm[1][1]:3d}  {cm[1][2]:3d}")
print(f"       BUY    {cm[2][0]:3d}   {cm[2][1]:3d}  {cm[2][2]:3d}")

# Feature importance
print("\n" + "=" * 70)
print("Top 15 Most Important Features:")
print("=" * 70)
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(15).iterrows():
    print(f"  {row['feature']:20s}: {row['importance']:.4f}")

# Save model and scaler
print("\n[7/7] Saving model and scaler...")
joblib.dump(model, 'nifty_model.pkl')
joblib.dump(scaler, 'nifty_scaler.pkl')
joblib.dump(feature_cols, 'feature_columns.pkl')
print("   ✓ Saved: nifty_model.pkl")
print("   ✓ Saved: nifty_scaler.pkl")
print("   ✓ Saved: feature_columns.pkl")

# Create model info file
model_info = {
    'model_type': 'Random Forest Classifier',
    'n_estimators': 200,
    'train_accuracy': f"{train_accuracy*100:.2f}%",
    'test_accuracy': f"{test_accuracy*100:.2f}%",
    'n_features': len(feature_cols),
    'n_samples': len(df),
    'classes': ['SELL (0)', 'HOLD (1)', 'BUY (2)'],
    'date_trained': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
}

import json
with open('model_info.json', 'w') as f:
    json.dump(model_info, f, indent=2)
print("   ✓ Saved: model_info.json")

print("\n" + "=" * 70)
print("✅ MODEL TRAINING COMPLETE!")
print("=" * 70)
print(f"\n🎯 Final Model Performance:")
print(f"   Training Accuracy: {train_accuracy*100:.2f}%")
print(f"   Testing Accuracy: {test_accuracy*100:.2f}%")
print(f"\n✅ Model ready for deployment!")
print("=" * 70)
