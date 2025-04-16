import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def train():
    df_stock = pd.read_csv("data/raw/aapl_20250416.csv", skiprows=2, header=None)
    df_stock.columns = ["Close", "High", "Low", "Open", "Volume"] 

    df_stock["Date"] = pd.date_range(start="2025-03-01", periods=len(df_stock), freq="B")  

    if "Date" not in df_stock.columns:
        print("[!] The 'Date' column was not found in the stock DataFrame.")
        print("Available columns:", df_stock.columns)
        return

    df_sentiment = pd.read_csv("data/processed/sentiment_apple.csv")

    df_stock["Date"] = pd.to_datetime(df_stock["Date"])
    df_sentiment["date"] = pd.to_datetime(df_sentiment["date"])

    print("Stock DataFrame columns:", df_stock.columns)
    print("Sentiment DataFrame columns:", df_sentiment.columns)

    df_merged = pd.merge(df_stock, df_sentiment, left_on="Date", right_on="date", how="inner")

    print("Merged DataFrame columns:", df_merged.columns)

    X = df_merged[["sentiment"]]
    y = df_merged["Close"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/price_predictor.pkl")
    print("[✓] Model trained and saved in models/price_predictor.pkl")

if __name__ == "__main__":
    train()