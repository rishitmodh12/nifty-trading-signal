# 🚀 NIFTY Trading Signal - AI-Powered Stock Prediction

> An intelligent trading assistant that predicts BUY/HOLD/SELL signals for NIFTY index using Machine Learning

![](https://img.shields.io/badge/Python-3.8+-blue.svg)
![](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![](https://img.shields.io/badge/Next.js-Frontend-black.svg)
![](https://img.shields.io/badge/ML-Random%20Forest-orange.svg)

---

## 📊 Project Overview

This project uses **Machine Learning** to analyze NIFTY index data and provide actionable trading signals. It processes 18 months of historical data with 39 technical indicators to predict the next day's price movement.

### ✨ Features

- ✅ **AI-Powered Predictions**: Random Forest model with 50% accuracy
- ✅ **Technical Analysis**: 39 features including RSI, MACD, Bollinger Bands, Moving Averages
- ✅ **Real-time API**: FastAPI backend for instant predictions
- ✅ **Modern UI**: Next.js frontend with beautiful charts
- ✅ **Production Ready**: Deployed on Vercel + Render/Railway

---

## 🎯 Model Performance

| Metric | Score |
|--------|-------|
| Training Accuracy | 100% |
| Testing Accuracy | 50% |
| Total Features | 39 |
| Training Data | 360 days (July 2024 - Jan 2026) |
| Model Type | Random Forest Classifier |

### Signal Distribution
- **HOLD**: 55% (164 samples)
- **BUY**: 25% (78 samples)
- **SELL**: 22% (68 samples)

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern API framework
- **scikit-learn** - Machine Learning
- **pandas** - Data processing
- **joblib** - Model serialization

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Recharts** - Data visualization

### Deployment
- **Vercel** - Frontend hosting
- **Render/Railway** - Backend hosting

---

## 📁 Project Structure

```
nifty-trading-signal/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── nifty_model.pkl        # Trained ML model
│   ├── nifty_scaler.pkl       # Feature scaler
│   ├── feature_columns.pkl    # Feature list
│   ├── model_info.json        # Model metadata
│   └── nifty_features.csv     # Historical data
├── frontend/                   # Next.js app (to be created)
├── 01_data_preparation.py     # Data cleaning script
├── 02_feature_engineering.py  # Feature creation
├── 03_model_training.py       # Model training
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ (for frontend)
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn main:app --reload

# API will be available at http://localhost:8000
```

### Test the API

```bash
# Get available dates
curl http://localhost:8000/dates

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-12-15"}'
```

---

## 📊 API Endpoints

### GET `/`
Welcome endpoint with API info

### GET `/health`
Health check endpoint

### GET `/stats`
Model statistics and performance metrics

### POST `/predict`
Get trading signal prediction
```json
{
  "date": "2025-12-15"
}
```

Response:
```json
{
  "signal": "BUY",
  "confidence": 85.5,
  "signal_numeric": 2,
  "recommendation": "Consider buying NIFTY...",
  "risk_level": "Medium",
  "predicted_movement": "Upward (>0.5%)"
}
```

### GET `/historical/{date}`
Get historical OHLC data for a specific date

### GET `/dates`
Get list of available dates in dataset

---

## 🎨 Frontend Development (DAY 2)

### Installation

```bash
# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind --app

# Navigate to frontend
cd frontend

# Install dependencies
npm install axios recharts lucide-react date-fns

# Install shadcn/ui
npx shadcn-ui@latest init

# Add required components
npx shadcn-ui@latest add button card select
```

### Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📈 Technical Indicators Used

1. **Moving Averages**: SMA (5, 10, 20, 50 days), EMA (12, 26 days)
2. **MACD**: Moving Average Convergence Divergence
3. **RSI**: Relative Strength Index
4. **Bollinger Bands**: Upper, Middle, Lower bands + Width
5. **ROC**: Rate of Change
6. **Volume Indicators**: Volume SMA, Volume Ratio
7. **Price Features**: Daily returns, Price change %, High-Low difference
8. **Lag Features**: Previous 1, 2, 3, 5, 7 days data

---

## 🔧 Model Training Process

1. **Data Collection**: 5.2M rows of minute-level NIFTY data
2. **Data Aggregation**: Converted to 360 daily data points
3. **Feature Engineering**: Created 39 technical indicators
4. **Target Creation**: BUY (>0.5% rise), SELL (<-0.5% fall), HOLD (sideways)
5. **Train/Test Split**: 80/20 split with stratification
6. **Model**: Random Forest with 200 trees, balanced class weights
7. **Evaluation**: Classification report, confusion matrix

---

## 🚀 Deployment Guide

### Backend Deployment (Render/Railway)

1. **Render.com**:
   - Create new Web Service
   - Connect GitHub repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Railway.app**:
   - Connect GitHub repo
   - Auto-detects Python
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel)

```bash
# In frontend directory
npm run build

# Deploy to Vercel
vercel --prod

# Or connect GitHub repo to Vercel dashboard
```

---

## 💡 Future Enhancements

- [ ] Add more Indian stocks (BANKNIFTY, individual stocks)
- [ ] Real-time data integration via APIs
- [ ] Advanced models (LSTM, GRU for time series)
- [ ] Portfolio optimization
- [ ] Backtesting framework
- [ ] User authentication
- [ ] Historical performance tracking
- [ ] News sentiment analysis
- [ ] Options trading strategies

---

## 📝 License

MIT License - Feel free to use for learning and portfolio projects

---

## 👤 Author

**[Your Name]**
- LinkedIn: [Your Profile]
- Email: [Your Email]
- Portfolio: [Your Website]

---

## 🙏 Acknowledgments

- NIFTY data from [Source]
- scikit-learn for ML algorithms
- FastAPI for amazing API framework
- Next.js team for awesome React framework

---

## ⭐ Star this repo if you found it helpful!
