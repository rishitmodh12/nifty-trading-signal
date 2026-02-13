'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Loader2 } from 'lucide-react'

export default function Home() {
  const [date, setDate] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const handlePredict = async () => {
    if (!date) {
      setError('Please select a date')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch(`http://localhost:8000/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date })
      })
      
      if (!response.ok) {
        throw new Error('Date not found in dataset. Please try another date.')
      }

      const data = await response.json()
      
      // Validate data
      if (!data.signal || !data.confidence) {
        throw new Error('Invalid response from server')
      }
      
      setResult(data)
    } catch (err: any) {
      setError(err.message || 'Error connecting to backend. Make sure it is running at localhost:8000')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            NIFTY Trading Signal
          </h1>
          <p className="text-xl text-slate-300">
            AI-Powered Stock Prediction for NIFTY Index
          </p>
          <p className="text-sm text-slate-500 mt-2">
            Powered by Machine Learning • Random Forest Algorithm
          </p>
        </div>

        {/* Main Card */}
        <Card className="p-8 bg-white/10 backdrop-blur border-slate-700 shadow-2xl">
          <div className="space-y-6">
            {/* Date Input */}
            <div>
              <label className="block text-white text-sm font-medium mb-2">
                Select Date (Available: Jul 23, 2024 - Jan 14, 2026)
              </label>
              <input
                type="date"
                value={date}
                onChange={(e) => {
                  setDate(e.target.value)
                  setError('')
                  setResult(null)
                }}
                min="2024-07-23"
                max="2026-01-14"
                className="w-full px-4 py-3 rounded-lg bg-slate-800 text-white border border-slate-600 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-500/20 border border-red-500 rounded-lg">
                <p className="text-red-300 text-sm">⚠️ {error}</p>
              </div>
            )}

            {/* Submit Button */}
            <Button 
              onClick={handlePredict}
              disabled={loading}
              className="w-full py-6 text-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Analyzing Market Data...
                </>
              ) : (
                '🎯 Get Trading Signal'
              )}
            </Button>

            {/* Results */}
            {result && (
              <div className="mt-8 p-6 bg-slate-800/50 rounded-lg border border-slate-700 animate-fade-in">
                {/* Signal Badge */}
                <div className={`text-center p-8 rounded-lg mb-6 transition-all duration-300 ${
                  result.signal === 'BUY' ? 'bg-green-500/20 border-2 border-green-500 shadow-green-500/50' :
                  result.signal === 'SELL' ? 'bg-red-500/20 border-2 border-red-500 shadow-red-500/50' :
                  'bg-yellow-500/20 border-2 border-yellow-500 shadow-yellow-500/50'
                } shadow-lg`}>
                  <div className="text-6xl mb-3">
                    {result.signal === 'BUY' ? '📈' : result.signal === 'SELL' ? '📉' : '➡️'}
                  </div>
                  <h2 className="text-5xl font-bold text-white mb-2">
                    {result.signal}
                  </h2>
                  <div className="flex items-center justify-center gap-2">
                    <div className="w-full max-w-xs bg-slate-700 rounded-full h-3 overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${
                          result.signal === 'BUY' ? 'bg-green-500' :
                          result.signal === 'SELL' ? 'bg-red-500' : 'bg-yellow-500'
                        }`}
                        style={{ width: `${result.confidence}%` }}
                      />
                    </div>
                  </div>
                  <p className="text-2xl text-slate-300 mt-2">
                    Confidence: <span className="font-bold">{result.confidence}%</span>
                  </p>
                </div>
                
                {/* Details Grid */}
                <div className="space-y-4 text-white">
                  <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
                    <h3 className="font-semibold text-lg mb-2 text-blue-400">💡 Recommendation:</h3>
                    <p className="text-slate-300">{result.recommendation}</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
                      <h3 className="font-semibold mb-1 text-purple-400">📊 Predicted Movement:</h3>
                      <p className="text-slate-300">{result.predicted_movement}</p>
                    </div>
                    
                    <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
                      <h3 className="font-semibold mb-1 text-orange-400">⚠️ Risk Level:</h3>
                      <p className={`font-bold text-lg ${
                        result.risk_level === 'High' ? 'text-red-400' :
                        result.risk_level === 'Medium' ? 'text-yellow-400' :
                        'text-green-400'
                      }`}>
                        {result.risk_level}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Disclaimer */}
                <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded text-xs text-yellow-200">
                  ⚠️ This is for educational purposes only. Not financial advice. Always do your own research before trading.
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* How it Works Section */}
        <Card className="mt-8 p-6 bg-white/5 backdrop-blur border-slate-700">
          <h2 className="text-2xl font-bold text-white mb-4">🧠 How It Works</h2>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="p-4 bg-slate-800/50 rounded-lg">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-semibold text-white mb-2">Data Analysis</h3>
              <p className="text-slate-400">Analyzes 360 days of NIFTY historical data with 39 technical indicators</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-lg">
              <div className="text-3xl mb-2">🤖</div>
              <h3 className="font-semibold text-white mb-2">ML Prediction</h3>
              <p className="text-slate-400">Random Forest algorithm predicts next-day price movement with confidence scores</p>
            </div>
            <div className="p-4 bg-slate-800/50 rounded-lg">
              <div className="text-3xl mb-2">🎯</div>
              <h3 className="font-semibold text-white mb-2">Trading Signals</h3>
              <p className="text-slate-400">Generates actionable BUY/HOLD/SELL recommendations with risk assessment</p>
            </div>
          </div>
        </Card>

        {/* Footer */}
        <footer className="mt-8 text-center">
          <div className="p-6 bg-white/5 backdrop-blur border border-slate-700 rounded-lg">
            <p className="text-slate-300 font-semibold mb-2">Built by RISHIT</p>
            <p className="text-slate-400 text-sm mb-4">Full-Stack AI Trading Signal System</p>
            <div className="flex justify-center gap-4 text-base items-center">
  <a href="https://github.com/rishitmodh12" target="_blank" className="text-blue-400 hover:text-blue-300 transition-colors">
    🔗 GitHub
  </a>
  <a href="https://linkedin.com/in/rishit-modh-1b0a26374" target="_blank" className="text-blue-400 hover:text-blue-300 transition-colors">
    🔗 LinkedIn
  </a>
  <span className="text-slate-300">
    📧 rishitmodh@gmail.com
  </span>
</div>
            <p className="text-slate-500 text-xs mt-4">
              Tech Stack: Python • FastAPI • Next.js • TypeScript • Tailwind CSS • scikit-learn
            </p>
          </div>
        </footer>
      </div>

      <style jsx global>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
      `}</style>
    </main>
  )
}