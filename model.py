import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator as VolumeSMA
import warnings

warnings.filterwarnings("ignore")


def compute_indicators(df):
    df = df.copy()
    df["EMA_5"] = EMAIndicator(close=df["Close"], window=5).ema_indicator()
    df["EMA_10"] = EMAIndicator(close=df["Close"], window=10).ema_indicator()
    df["RSI"] = RSIIndicator(close=df["Close"], window=14).rsi()

    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()

    boll = BollingerBands(close=df["Close"])
    df["Bollinger_h"] = boll.bollinger_hband()
    df["Bollinger_l"] = boll.bollinger_lband()

    stoch = StochasticOscillator(high=df["Close"], low=df["Close"], close=df["Close"])
    df["Stoch_K"] = stoch.stoch()
    df["Stoch_D"] = stoch.stoch_signal()

    adx = ADXIndicator(high=df["Close"], low=df["Close"], close=df["Close"])
    df["ADX"] = adx.adx()

    df["Volume_SMA_10"] = VolumeSMA(volume=df["Close"], window=10).sma_indicator()

    return df


def build_features_targets(df):
    df = compute_indicators(df)
    df["Target"] = df["Close"].shift(-5) / df["Close"] - 1  # 5-day forward return
    df = df.dropna()

    features = [
        "EMA_5", "EMA_10", "RSI", "MACD", "MACD_signal",
        "Bollinger_h", "Bollinger_l", "Stoch_K", "Stoch_D",
        "ADX", "Volume_SMA_10"
    ]
    return df[features], df["Target"]


def run_analysis(tickers, full_df):
    top_results = []

    for ticker in tickers:
        print(f"🔍 Analyzing {ticker}...")
        try:
            df = full_df[["Date", ticker]].dropna()
            df = df.rename(columns={ticker: "Close"})
            df.set_index("Date", inplace=True)
            df = df.sort_index()

            if len(df) < 25:
                print(f"⚠️ Not enough data for {ticker}")
                continue

            X, y = build_features_targets(df)

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            scores = cross_val_score(model, X, y, scoring="neg_mean_absolute_error", cv=5)
            mae = -scores.mean()

            model.fit(X, y)
            latest_features = X.iloc[[-1]]
            predicted_return = model.predict(latest_features)[0]

            top_results.append({
                "Ticker": ticker,
                "Expected Return (%)": round(predicted_return * 100, 2),
                "MAE": round(mae * 100, 4),
            })

        except Exception as e:
            print(f"❌ Error for {ticker}: {e}")
            continue

    results_df = pd.DataFrame(top_results)

    # Add confidence and sort
    if not results_df.empty:
        min_mae = results_df["MAE"].min()
        max_mae = results_df["MAE"].max()
        results_df["Confidence (%)"] = results_df["MAE"].apply(
            lambda x: round(100 * (1 - (x - min_mae) / (max_mae - min_mae + 1e-6)), 2)
        )
        results_df["Score"] = (
            results_df["Expected Return (%)"] * results_df["Confidence (%)"] / 100
        )
        results_df = results_df.sort_values(by="Score", ascending=False).head(5)

    return results_df
