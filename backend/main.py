"""
NIFTY Trading Signal API
FastAPI backend for stock prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="NIFTY Trading Signal API",
    description="AI-powered trading signals for NIFTY index",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model, scaler, and feature columns
try:
    model = joblib.load('nifty_model.pkl')
    scaler = joblib.load('nifty_scaler.pkl')
    feature_cols = joblib.load('feature_columns.pkl')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    scaler = None
    feature_cols = None

# Load historical data for reference
df_historical = pd.read_csv('nifty_features.csv')
df_historical['date'] = pd.to_datetime(df_historical['date'])

# Request/Response models
class StockInput(BaseModel):
    date: Optional[str] = None  # If provided, use historical data
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None

class PredictionResponse(BaseModel):
    signal: str
    confidence: float
    signal_numeric: int
    recommendation: str
    risk_level: str
    predicted_movement: str

@app.get("/")
def read_root():
    return {
        "message": "NIFTY Trading Signal API",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Get trading signal prediction",
            "/health": "GET - Health check",
            "/stats": "GET - Model statistics"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
def get_stats():
    """Get model statistics"""
    import json
    with open('model_info.json', 'r') as f:
        model_info = json.load(f)
    
    return {
        "model_info": model_info,
        "data_range": {
            "start": df_historical['date'].min().strftime('%Y-%m-%d'),
            "end": df_historical['date'].max().strftime('%Y-%m-%d'),
            "total_days": len(df_historical)
        },
        "signal_distribution": df_historical['signal'].value_counts().to_dict()
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_signal(input_data: StockInput):
    """
    Predict trading signal for NIFTY
    Accepts either a date (to use historical data) or manual OHLC input
    """
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # If date is provided, use historical data
        if input_data.date:
            date_obj = pd.to_datetime(input_data.date)
            historical_row = df_historical[df_historical['date'] == date_obj]
            
            if len(historical_row) == 0:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No data found for date {input_data.date}"
                )
            
            # Get features from historical data
            features = historical_row[feature_cols].values[0]
            actual_signal = historical_row['signal'].values[0] if 'signal' in historical_row.columns else None
            
        else:
            # Manual input (would need to calculate all technical indicators)
            # For simplicity, this requires recent data to calculate moving averages
            raise HTTPException(
                status_code=400,
                detail="Manual input not supported yet. Please provide a date."
            )
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Get prediction and probabilities
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Map prediction to signal
        signal_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
        predicted_signal = signal_map[int(prediction)]
        confidence = float(probabilities[int(prediction)]) * 100
        
        # Generate recommendation
        if predicted_signal == 'BUY':
            recommendation = "Consider buying NIFTY. The model predicts upward movement."
            risk_level = "Medium"
            movement = "Upward (>0.5%)"
        elif predicted_signal == 'SELL':
            recommendation = "Consider selling or avoiding NIFTY. The model predicts downward movement."
            risk_level = "High"
            movement = "Downward (<-0.5%)"
        else:
            recommendation = "Hold current position. The model predicts sideways movement."
            risk_level = "Low"
            movement = "Sideways (-0.5% to +0.5%)"
        
        return PredictionResponse(
            signal=predicted_signal,
            confidence=round(confidence, 2),
            signal_numeric=int(prediction),
            recommendation=recommendation,
            risk_level=risk_level,
            predicted_movement=movement
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historical/{date}")
def get_historical_data(date: str):
    """Get historical data for a specific date"""
    try:
        date_obj = pd.to_datetime(date)
        row = df_historical[df_historical['date'] == date_obj]
        
        if len(row) == 0:
            raise HTTPException(status_code=404, detail=f"No data for {date}")
        
        return {
            "date": date,
            "open": float(row['open'].values[0]),
            "high": float(row['high'].values[0]),
            "low": float(row['low'].values[0]),
            "close": float(row['close'].values[0]),
            "volume": int(row['volume'].values[0]),
            "signal": row['signal'].values[0] if 'signal' in row.columns else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dates")
def get_available_dates():
    """Get list of available dates in the dataset"""
    dates = df_historical['date'].dt.strftime('%Y-%m-%d').tolist()
    return {
        "total_dates": len(dates),
        "date_range": {
            "start": dates[0],
            "end": dates[-1]
        },
        "sample_dates": dates[-30:]  # Last 30 dates
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
