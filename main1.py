import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
import warnings

warnings.filterwarnings("ignore")


def fetch_forex_data(pair="EURUSD=X", lookback=75):
    print(f"📈 Fetching 1-minute data for {pair}...")
    data = yf.download(tickers=pair, period="2d", interval="1m")
    df = data.tail(lookback).copy()
    df = df.rename(columns={"Close": "close", "High": "high", "Low": "low"})
    return df


def compute_indicators(df):
    df = df.copy()

    # Force Series instead of DataFrame
    close = pd.Series(df["close"].values, index=df.index)
    high = pd.Series(df["high"].values, index=df.index)
    low = pd.Series(df["low"].values, index=df.index)

    df["EMA_10"] = EMAIndicator(close=close, window=10).ema_indicator()
    df["EMA_20"] = EMAIndicator(close=close, window=20).ema_indicator()
    df["RSI"] = RSIIndicator(close=close, window=14).rsi()
    df["MACD"] = MACD(close=close).macd_diff()

    bb = BollingerBands(close=close)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()

    stoch = StochasticOscillator(
        high=high,
        low=low,
        close=close
    )
    df["Stoch"] = stoch.stoch()

    df.dropna(inplace=True)
    return df


def make_signal(df):
    last = df.iloc[-1]

    signal = "HOLD"
    confidence = 0

    # EMA crossover + RSI + MACD
    if last["EMA_10"] > last["EMA_20"] and last["RSI"] > 55 and last["MACD"] > 0:
        signal = "CALL (UP)"
        confidence += 1
    elif last["EMA_10"] < last["EMA_20"] and last["RSI"] < 45 and last["MACD"] < 0:
        signal = "PUT (DOWN)"
        confidence += 1

    # Confirm with Stochastic
    if signal == "CALL (UP)" and last["Stoch"] > 60:
        confidence += 1
    elif signal == "PUT (DOWN)" and last["Stoch"] < 40:
        confidence += 1

    return signal, confidence


# MAIN FLOW
pair = "EURUSD=X"  # Change to "USD/JPY=X", etc., as needed
df = fetch_forex_data(pair)
df = compute_indicators(df)
signal, confidence = make_signal(df)

print("\n🧠 Signal:", signal)
print("✅ Confidence (0–2):", confidence)
