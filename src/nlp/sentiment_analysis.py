import json
import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_news_sentiment(input_path):
    with open(input_path, "r") as f:
        articles = json.load(f)

    analyzer = SentimentIntensityAnalyzer()

    data = []
    for article in articles:
        text = article.get("title", "") + " " + article.get("description", "")
        score = analyzer.polarity_scores(text)["compound"]
        data.append({
            "date": article["publishedAt"][:10],
            "title": article.get("title"),
            "description": article.get("description"),
            "sentiment": score
        })

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df

def save_sentiment(df, company, output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"sentiment_{company.lower()}.csv"
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"[✓] Sentimentos guardados em {path}")

if __name__ == "__main__":
    input_path = "data/raw/news_apple_20240416.json"
    df = analyze_news_sentiment(input_path)
    save_sentiment(df, "apple")
