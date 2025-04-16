import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def train():
    df_stock = pd.read_csv("data/raw/apple_20240401.csv")
    df_sentiment = pd.read_csv("data/processed/sentiment_apple.csv")

    # Preparar os dados
    df_stock["Date"] = pd.to_datetime(df_stock["Date"])
    df_sentiment["date"] = pd.to_datetime(df_sentiment["date"])

    df_merged = pd.merge(df_stock, df_sentiment, left_on="Date", right_on="date", how="inner")

    X = df_merged[["sentiment"]]
    y = df_merged["Close"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/price_predictor.pkl")
    print("[✓] Modelo treinado e guardado em models/price_predictor.pkl")

if __name__ == "__main__":
    train()
