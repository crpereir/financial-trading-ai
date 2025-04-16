import os
from src.data.get_stock_data import fetch_stock_data, save_to_csv
from src.data.get_news import fetch_news, save_news
from src.nlp.sentiment_analysis import analyze_news_sentiment, save_sentiment
from src.ml.train_model import train
from src.vis.plot_sentiment import plot_sentiment
from dotenv import load_dotenv

load_dotenv()

def main_pipeline():
    # 1. Download Stock Data
    print("Step 1: Downloading stock data...")
    stock_data = fetch_stock_data("AAPL", "2022-01-01", "2022-12-31")
    if stock_data.empty:
        print("[!] No stock data found for the given range.")
        return
    stock_data_path = save_to_csv(stock_data, "AAPL")
    print("Stock data downloaded and saved successfully.")

    # 2. Fetch News Data
    print("Step 2: Fetching news data...")
    from_date = "2025-03-16"
    to_date = "2025-04-16"
    articles = fetch_news("Apple", from_date, to_date)
    if not articles:
        print("[!] No news data fetched from the API.")
        return
    news_path = save_news(articles, "apple")
    print("News data fetched and saved successfully.")

    # 3. Perform Sentiment Analysis
    print("Step 3: Performing sentiment analysis...")
    sentiment_df = analyze_news_sentiment(news_path)
    save_sentiment(sentiment_df, "apple")
    print("Sentiment analysis completed and saved.")

    # 4. Train Machine Learning Model
    print("Step 4: Training machine learning model...")
    train()
    print("Model training completed and saved.")

    # 5. Visualize Sentiment Data
    print("Step 5: Visualizing sentiment data...")
    plot_sentiment()
    print("Visualization completed.")

    print("Pipeline executed successfully!")

if __name__ == "__main__":
    main_pipeline()