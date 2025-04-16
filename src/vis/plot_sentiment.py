import pandas as pd
import matplotlib.pyplot as plt

def plot_sentiment(path="data/processed/sentiment_apple.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby("date").mean(numeric_only=True)

    df["sentiment"].plot(kind="line", title="Sentimento médio diário")
    plt.ylabel("Sentimento")
    plt.xlabel("Data")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_sentiment()
