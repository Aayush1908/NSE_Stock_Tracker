📈 NSE Stock Prediction & Analysis

A Python-based application to analyze, visualize, and predict stock price trends from the NSE (National Stock Exchange of India) using real-time financial data.
It leverages time-series analysis, technical indicators, and basic predictive models to generate insights such as expected returns, confidence intervals, and buy/sell signals.

🚀 Features

🔗 Real-Time Data: Fetches live stock price data from NSE via APIs.

📊 Technical Indicators: EMA, RSI, MACD, Bollinger Bands, Stochastic Oscillator.

🔮 Prediction Engine: Forecasts short-term price movement with confidence scoring.

🏆 Top Stock Filtering: Ranks stocks by highest expected return or lowest error (MAE).

📉 Visualization: Interactive charts for price and indicators.

📝 Export: Saves results to Excel (Sheet2 with predictions & confidence).

🛠️ Tech Stack

Programming Language: Python 🐍

Libraries:

pandas, numpy → Data preprocessing & analysis

matplotlib → Visualization

ta → Technical indicators

yfinance / nsetools → Data fetching

scikit-learn → Predictive modeling

⚙️ Installation & Setup
# Clone the repository
git clone https://github.com/your-username/NSE_Stock_Tracker.git
cd NSE_Stock_Tracker

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows

# Install dependencies
pip install -r requirements.txt

▶️ Usage
Run Stock Prediction
python main.py

Example Output
🧠 Signal: CALL (UP)
✅ Confidence: 2/2
📈 Expected Return (5 days): +3.7%  (95% CI: 2.1% – 5.4%)

Results

Predictions saved in Excel (Sheet2)

Interactive charts for analysis

📂 Project Structure
├── main.py               # Main script
├── indicators.py         # Technical indicators calculation
├── predictor.py          # Prediction & signal generation
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
└── outputs/              # Excel reports & charts

🧠 How It Works

Fetches the last 75 one-minute candles (configurable).

Computes EMA crossover, RSI, MACD, Bollinger Bands, Stochastic Oscillator.

Generates a buy/sell/hold signal with confidence score.

Uses historical data to predict expected return over the next 5 days with a confidence interval.

Exports results and ranks top 5 opportunities.

📸 Screenshots

(Add sample chart images, Excel output screenshots here)

🔒 Security Note

Your API keys / credentials.json are ignored via .gitignore.

Never push credentials to GitHub (GitHub Push Protection is enabled).

📌 Future Improvements

✅ Improve ML model accuracy with LSTM / Prophet

✅ Add portfolio simulation

✅ Deploy via Streamlit for interactive web dashboard

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork this repo and submit a PR.

👨‍💻 Author:

Aayush Singh

💼 www.linkedin.com/in/aayush1908

📧 code.aayush.19@gmail.com

⭐ If you like this project, give it a star on GitHub! ⭐